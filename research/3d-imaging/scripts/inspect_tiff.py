#!/usr/bin/env python3
"""Inspect the first series of a microscopy TIFF; optionally measure a 3D label map.

Dependencies: numpy, tifffile. This is metadata/QC and voxel metrology, not
segmentation, deconvolution, model inference, or a reader for arbitrary formats.
All input arrays are loaded into memory. --max-bytes bounds their combined
decoded payload, not process RSS or TIFF decoder temporary allocations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import tifffile


DEFAULT_MAX_BYTES = 1_073_741_824
CHUNK_VOXELS = 262_144
UNIT_TO_UM = {
    "µm": 1.0, "μm": 1.0, "um": 1.0,
    "micrometer": 1.0, "micrometre": 1.0,
    "nm": 0.001, "nanometer": 0.001, "nanometre": 0.001,
    "mm": 1000.0, "millimeter": 1000.0, "millimetre": 1000.0,
}


class InspectionError(ValueError):
    """A requested inspection cannot be performed without guessing."""


def resolve_axes(metadata_axes: str, shape: tuple, override: str | None) -> dict:
    axes = override.upper() if override else metadata_axes.upper()
    if (len(axes) != len(shape) or len(set(axes)) != len(axes)
            or set(axes) - set("TCZYX") or "X" not in axes or "Y" not in axes):
        raise InspectionError(
            f"Untrusted or unsupported axis order {metadata_axes!r} for shape {shape}. "
            "Provide --axes with the verified order using T, C, Z, Y, X; "
            "generic Q/I axes and RGB sample axes are not interpreted."
        )
    return {
        "value": axes,
        "source": "user_override" if override else "tiff_series_axes",
        "metadata_value": metadata_axes,
    }


def read_ome_spacing(ome_xml: str | None) -> tuple[dict | None, list[str]]:
    """Read first OME Pixels spacing; OME's omitted length unit defaults to µm."""
    if not ome_xml:
        return None, []
    warnings = []
    try:
        root = ET.fromstring(ome_xml)
        pixels = next((n for n in root.iter() if n.tag.rsplit("}", 1)[-1] == "Pixels"), None)
        if pixels is None:
            return None, ["OME XML has no Pixels element; physical spacing unavailable."]
        values = {}
        original = {}
        for axis in "ZYX":
            raw = pixels.get(f"PhysicalSize{axis}")
            if raw is None:
                continue
            unit = pixels.get(f"PhysicalSize{axis}Unit", "µm")
            original[axis] = {"value": raw, "unit": unit}
            factor = UNIT_TO_UM.get(unit.strip().lower())
            if factor is None:
                warnings.append(f"Unsupported OME PhysicalSize{axis} unit {unit!r}.")
                continue
            value = float(raw) * factor
            if not math.isfinite(value) or value <= 0:
                warnings.append(f"Invalid OME PhysicalSize{axis} {raw!r}; must be positive and finite.")
                continue
            values[axis] = value
        if set(values) != set("ZYX"):
            if original:
                warnings.append("Complete positive OME Z/Y/X spacing is unavailable; physical object metrics are omitted.")
            return None, warnings
        return {
            "zyx_um": [values[a] for a in "ZYX"],
            "source": "ome_first_pixels",
            "original": original,
            "unit": "µm",
        }, warnings
    except (ET.ParseError, ValueError, OverflowError) as exc:
        return None, [f"Cannot parse OME physical spacing: {exc}"]


def _metadata(tiff: tifffile.TiffFile, path: Path, override: str | None) -> dict:
    if not tiff.series:
        raise InspectionError(f"TIFF has no readable series: {path}")
    series = tiff.series[0]
    shape = tuple(int(n) for n in series.shape)
    dtype = np.dtype(series.dtype)
    if dtype.kind not in "uifb":
        raise InspectionError(f"Unsupported non-real numeric dtype {dtype} in {path}")
    return {
        "path": str(path.resolve()),
        "series_index": 0,
        "series_count": len(tiff.series),
        "shape": list(shape),
        "axes": resolve_axes(series.axes, shape, override),
        "dtype": str(dtype),
        "decoded_bytes": math.prod(shape) * dtype.itemsize,
        "ome": bool(tiff.is_ome),
        "imagej": bool(tiff.is_imagej),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1_048_576), b""):
            digest.update(block)
    return digest.hexdigest()


def intensity_stats(array: np.ndarray, detector_max: int | float | None = None) -> dict:
    flat = array.reshape(-1)
    finite_count = 0
    low = high = None
    dtype_ceiling = int(np.iinfo(array.dtype).max) if array.dtype.kind in "ui" else None
    dtype_ceiling_count = detector_ceiling_count = detector_above_count = 0
    for start in range(0, flat.size, CHUNK_VOXELS):
        block = flat[start:start + CHUNK_VOXELS]
        valid = block[np.isfinite(block)]
        finite_count += int(valid.size)
        if valid.size:
            block_low, block_high = valid.min().item(), valid.max().item()
            low = block_low if low is None else min(low, block_low)
            high = block_high if high is None else max(high, block_high)
            if dtype_ceiling is not None:
                dtype_ceiling_count += int(np.count_nonzero(valid == dtype_ceiling))
            if detector_max is not None:
                detector_ceiling_count += int(np.count_nonzero(valid == detector_max))
                detector_above_count += int(np.count_nonzero(valid > detector_max))
    result = {
        "voxel_count": int(flat.size),
        "finite_count": finite_count,
        "nonfinite_count": int(flat.size) - finite_count,
        "finite_min": low,
        "finite_max": high,
        "fraction_denominator": "finite_count",
    }
    if dtype_ceiling is not None:
        result.update({
            "dtype_ceiling_value": dtype_ceiling,
            "dtype_ceiling_count": dtype_ceiling_count,
            "dtype_ceiling_fraction": dtype_ceiling_count / finite_count if finite_count else None,
            "dtype_ceiling_interpretation": "Storage dtype maximum; not proof of detector saturation.",
        })
    if detector_max is not None:
        result.update({
            "detector_ceiling_value": detector_max,
            "detector_ceiling_source": "user_assertion",
            "detector_ceiling_count": detector_ceiling_count,
            "detector_ceiling_fraction": detector_ceiling_count / finite_count if finite_count else None,
            "above_detector_ceiling_count": detector_above_count,
        })
    return result


def label_metrics(labels: np.ndarray, spacing: dict | None) -> dict:
    if labels.ndim != 3 or labels.dtype.kind not in "ui":
        raise InspectionError("Labels must be a strict 3D integer ZYX array; Boolean/float labels are unsupported.")
    flat = labels.reshape(-1)
    zsize, ysize, xsize = labels.shape
    totals: dict[int, list] = {}
    background_count = 0
    for start in range(0, flat.size, CHUNK_VOXELS):
        block = flat[start:start + CHUNK_VOXELS]
        if block.size and block.min() < 0:
            raise InspectionError("Labels must be nonnegative; label 0 is background.")
        positions = np.flatnonzero(block)
        background_count += int(block.size - positions.size)
        if positions.size == 0:
            continue
        ids, inverse = np.unique(block[positions], return_inverse=True)
        indices = positions + start
        zz = indices // (ysize * xsize)
        yy = (indices // xsize) % ysize
        xx = indices % xsize
        counts = np.bincount(inverse)
        sums = [np.bincount(inverse, weights=c) for c in (zz, yy, xx)]
        edge = ((zz == 0) | (zz == zsize - 1) | (yy == 0) | (yy == ysize - 1)
                | (xx == 0) | (xx == xsize - 1))
        edge_counts = np.bincount(inverse, weights=edge, minlength=len(ids))
        for i, label in enumerate(ids):
            label = int(label)
            row = totals.setdefault(label, [0, 0.0, 0.0, 0.0, False])
            row[0] += int(counts[i])
            for dim in range(3):
                row[dim + 1] += float(sums[dim][i])
            row[4] = row[4] or bool(edge_counts[i])
    objects = []
    for label, (count, sum_z, sum_y, sum_x, edge) in sorted(totals.items()):
        centroid = [s / count for s in (sum_z, sum_y, sum_x)]
        row = {
            "label": label, "voxel_count": count,
            "centroid_zyx_voxels": centroid, "touches_volume_edge": edge,
        }
        if spacing:
            sizes = spacing["zyx_um"]
            row["volume_um3"] = count * math.prod(sizes)
            row["centroid_zyx_um"] = [c * s for c, s in zip(centroid, sizes)]
        objects.append(row)
    return {
        "background_label": 0,
        "background_voxel_count": background_count,
        "object_count": len(objects),
        "physical_metrics_available": bool(spacing),
        "coordinate_convention": "ZYX voxel indices; first voxel center at coordinate 0; no stage/world origin applied.",
        "object_definition": "One object per positive integer ID; disconnected regions sharing an ID are combined.",
        "edge_policy": "Reported and retained; no objects are automatically deleted.",
        "objects": objects,
    }


def inspect(input_path: Path, *, axes: str | None = None, spacing_zyx=None,
            labels_path: Path | None = None, detector_max=None,
            max_bytes: int = DEFAULT_MAX_BYTES, checksum: bool = False) -> dict:
    input_path = Path(input_path)
    labels_path = Path(labels_path) if labels_path else None
    if max_bytes <= 0:
        raise InspectionError("--max-bytes must be positive.")
    if spacing_zyx is not None:
        if len(spacing_zyx) != 3 or any(not math.isfinite(s) or s <= 0 for s in spacing_zyx):
            raise InspectionError("--spacing requires three positive finite values in Z Y X order, in µm.")
    if detector_max is not None and (not math.isfinite(detector_max) or detector_max < 0):
        raise InspectionError("--detector-max must be a nonnegative finite value.")
    warnings = []
    with tifffile.TiffFile(input_path) as source:
        source_meta = _metadata(source, input_path, axes)
        if spacing_zyx is not None:
            spacing = {
                "zyx_um": [float(s) for s in spacing_zyx], "unit": "µm",
                "source": "user_override",
            }
        else:
            spacing, ome_warnings = read_ome_spacing(source.ome_metadata)
            warnings.extend(ome_warnings)
        if source_meta["series_count"] > 1:
            warnings.append("Only the first TIFF series is inspected; other series are not loaded.")
        if spacing is None:
            warnings.append("No verified complete Z/Y/X spacing; all physical object metrics are omitted.")
        label_meta = None
        # Check all metadata budgets before decoding either array.
        if labels_path:
            with tifffile.TiffFile(labels_path) as label_source:
                label_meta = _metadata(label_source, labels_path, axes)
                if (source_meta["axes"]["value"] != "ZYX"
                        or label_meta["axes"]["value"] != "ZYX"
                        or len(source_meta["shape"]) != 3
                        or label_meta["shape"] != source_meta["shape"]):
                    raise InspectionError("--labels requires both input and labels to have identical strict 3D ZYX shape/order.")
                if np.dtype(label_meta["dtype"]).kind not in "ui":
                    raise InspectionError("Labels must use an integer dtype; Boolean/float labels are unsupported.")
                required_bytes = source_meta["decoded_bytes"] + label_meta["decoded_bytes"]
                if required_bytes > max_bytes:
                    raise InspectionError(f"Decoded input + labels require {required_bytes:,} bytes, exceeding --max-bytes {max_bytes:,}. No arrays were loaded.")
                label_array = label_source.series[0].asarray()
        else:
            required_bytes = source_meta["decoded_bytes"]
            if required_bytes > max_bytes:
                raise InspectionError(f"Decoded input requires {required_bytes:,} bytes, exceeding --max-bytes {max_bytes:,}. No array was loaded.")
        array = source.series[0].asarray()
    stats = intensity_stats(array, detector_max)
    if stats.get("above_detector_ceiling_count", 0):
        warnings.append("Values exceed the asserted detector maximum; verify the detector setting and data encoding.")
    if checksum:
        source_meta["sha256"] = _sha256(input_path)
        if label_meta:
            label_meta["sha256"] = _sha256(labels_path)
    result = {
        "schema_version": "1.0",
        "software": {"python": platform.python_version(), "numpy": np.__version__, "tifffile": tifffile.__version__},
        "input": source_meta,
        "spacing": spacing,
        "intensity": stats,
        "memory": {
            "mode": "full_load",
            "decoded_payload_bytes": required_bytes,
            "max_decoded_payload_bytes": max_bytes,
            "budget_scope": "Combined decoded arrays only; decoder, QC chunks and per-object aggregates add memory. Not a peak RSS guarantee.",
        },
        "warnings": warnings,
        "limitations": [
            "First TIFF series only; axes override is the user's assertion and is not independently validated.",
            "No segmentation or inference; supplied label IDs define objects.",
            "Voxel-based volumes assume rectangular voxels and verified spacing; no PSF, distortion or registration correction.",
            "Source OME spacing does not independently verify label registration, segmentation quality or acquisition calibration.",
            "Research QC only; no clinical or diagnostic validation.",
        ],
    }
    if label_meta:
        result["labels"] = label_meta
        result["label_metrics"] = label_metrics(label_array, spacing)
    return result


def detector_value(value: str) -> int | float:
    try:
        return int(value)
    except ValueError:
        return float(value)


def main(argv=None) -> int:
    # Windows redirected streams can otherwise use GBK and reject µm or paths.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, type=Path, help="Microscopy TIFF; inspect its first series.")
    parser.add_argument("--axes", help="Verified axis order (T/C/Z/Y/X). Applied to input and optional labels; never auto-guessed.")
    parser.add_argument("--spacing", nargs=3, type=float, metavar=("Z", "Y", "X"), help="Verified voxel sizes in µm, Z Y X order; override OME spacing.")
    parser.add_argument("--labels", type=Path, help="Same-shaped nonnegative integer ZYX TIFF label volume, 0 = background.")
    parser.add_argument("--detector-max", type=detector_value, help="User-verified detector ceiling; e.g. 4095 for 12-bit values stored in uint16.")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="Maximum combined decoded payload bytes (default 1 GiB). Arrays are fully loaded; not peak RSS.")
    parser.add_argument("--sha256", action="store_true", help="Hash complete input and label files; may add substantial I/O.")
    parser.add_argument("--output", required=True, type=Path, help="UTF-8 JSON report path.")
    args = parser.parse_args(argv)
    try:
        if args.output.resolve() in {args.input.resolve(), args.labels.resolve() if args.labels else None}:
            raise InspectionError("--output cannot overwrite an input TIFF.")
        print("Reading TIFF arrays with full-load mode; --max-bytes limits decoded payload, not peak RAM.", file=sys.stderr)
        result = inspect(args.input, axes=args.axes, spacing_zyx=args.spacing,
                         labels_path=args.labels, detector_max=args.detector_max,
                         max_bytes=args.max_bytes, checksum=args.sha256)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        print(f"Saved JSON report: {args.output.resolve()}")
        return 0
    except (InspectionError, OSError, ValueError, tifffile.TiffFileError) as exc:
        print(f"Inspection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
