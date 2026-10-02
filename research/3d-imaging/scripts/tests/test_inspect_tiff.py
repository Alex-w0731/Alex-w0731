"""Synthetic TIFF checks; no real microscopy data or model inference required."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import tifffile


SCRIPT = Path(__file__).resolve().parents[1] / "inspect_tiff.py"
SPEC = importlib.util.spec_from_file_location("inspect_tiff", SCRIPT)
qc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qc)


class InspectTiffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def save(self, name, data, **kwargs):
        path = self.root / name
        tifffile.imwrite(path, data, photometric="minisblack", **kwargs)
        return path

    def test_anisotropic_volume_centroid_and_edge_retention(self):
        image = self.save("image.tif", np.zeros((4, 4, 4), dtype=np.uint16), metadata={"axes": "ZYX"})
        labels = np.zeros((4, 4, 4), dtype=np.uint16)
        labels[1, 1, 1] = labels[2, 2, 2] = 1
        labels[0, 0, 0] = 3
        label_path = self.save("labels.tif", labels, metadata={"axes": "ZYX"})
        result = qc.inspect(image, labels_path=label_path, spacing_zyx=[2.0, 0.5, 0.25], checksum=True)
        objects = result["label_metrics"]["objects"]
        self.assertEqual([o["label"] for o in objects], [1, 3])
        self.assertAlmostEqual(objects[0]["volume_um3"], 0.5)
        self.assertEqual(objects[0]["centroid_zyx_um"], [3.0, 0.75, 0.375])
        self.assertFalse(objects[0]["touches_volume_edge"])
        self.assertTrue(objects[1]["touches_volume_edge"])
        self.assertEqual(result["spacing"]["source"], "user_override")
        self.assertEqual(len(result["input"]["sha256"]), 64)

    def test_unknown_metadata_axes_are_refused_until_explicit_override(self):
        path = self.save("unlabelled.tif", np.zeros((4, 5, 6), dtype=np.uint16), metadata=None)
        with self.assertRaisesRegex(qc.InspectionError, "Untrusted"):
            qc.inspect(path)
        result = qc.inspect(path, axes="ZYX")
        self.assertEqual(result["input"]["axes"]["source"], "user_override")

    def test_dtype_and_detector_ceiling_use_actual_values(self):
        path = self.save("ceiling.tif", np.array([0, 4095, 65535], dtype=np.uint16).reshape(1, 1, 3), metadata={"axes": "ZYX"})
        result = qc.inspect(path, detector_max=4095)["intensity"]
        self.assertEqual(result["dtype_ceiling_value"], 65535)
        self.assertEqual(result["dtype_ceiling_count"], 1)
        self.assertAlmostEqual(result["dtype_ceiling_fraction"], 1 / 3)
        self.assertEqual(result["detector_ceiling_count"], 1)
        self.assertEqual(result["above_detector_ceiling_count"], 1)
        self.assertEqual(result["fraction_denominator"], "finite_count")

    def test_ome_units_convert_to_micrometers(self):
        path = self.save("ome.ome.tif", np.zeros((2, 3, 4), dtype=np.uint16), ome=True, metadata={
            "axes": "ZYX", "PhysicalSizeZ": 2, "PhysicalSizeZUnit": "µm",
            "PhysicalSizeY": 0.0005, "PhysicalSizeYUnit": "mm",
            "PhysicalSizeX": 250, "PhysicalSizeXUnit": "nm",
        })
        result = qc.inspect(path)
        self.assertEqual(result["spacing"]["source"], "ome_first_pixels")
        self.assertEqual(result["spacing"]["zyx_um"], [2.0, 0.5, 0.25])

    def test_no_spacing_omits_physical_metrics(self):
        data = np.ones((2, 3, 4), dtype=np.uint16)
        image = self.save("image.tif", data, metadata={"axes": "ZYX"})
        labels = self.save("labels.tif", data, metadata={"axes": "ZYX"})
        result = qc.inspect(image, labels_path=labels)
        self.assertIsNone(result["spacing"])
        self.assertFalse(result["label_metrics"]["physical_metrics_available"])
        self.assertNotIn("volume_um3", result["label_metrics"]["objects"][0])
        self.assertNotIn("centroid_zyx_um", result["label_metrics"]["objects"][0])

    def test_float_nonfinite_values_are_excluded_from_denominator_and_range(self):
        path = self.save("float.tif", np.array([np.nan, np.inf, -np.inf, 0, 10], dtype=np.float32).reshape(1, 1, 5), metadata={"axes": "ZYX"})
        result = qc.inspect(path, detector_max=10)["intensity"]
        self.assertEqual(result["finite_count"], 2)
        self.assertEqual(result["nonfinite_count"], 3)
        self.assertEqual((result["finite_min"], result["finite_max"]), (0, 10))
        self.assertEqual(result["detector_ceiling_fraction"], 0.5)
        self.assertNotIn("dtype_ceiling_fraction", result)

    def test_metadata_budget_rejects_before_decoding(self):
        path = self.save("image.tif", np.zeros((2, 3, 4), dtype=np.uint16), metadata={"axes": "ZYX"})
        with patch.object(tifffile.TiffPageSeries, "asarray", side_effect=AssertionError("decoder must not run")):
            with self.assertRaisesRegex(qc.InspectionError, "exceeding"):
                qc.inspect(path, max_bytes=1)

    def test_label_shape_and_integer_requirements(self):
        image = self.save("image.tif", np.zeros((2, 3, 4), dtype=np.uint16), metadata={"axes": "ZYX"})
        labels = self.save("labels.tif", np.ones((2, 3, 4), dtype=np.float32), metadata={"axes": "ZYX"})
        with self.assertRaisesRegex(qc.InspectionError, "integer"):
            qc.inspect(image, labels_path=labels)

    def test_cli_writes_utf8_json_and_help_works_on_windows(self):
        path = self.save("显微.tif", np.zeros((2, 3, 4), dtype=np.uint16), metadata={"axes": "ZYX"})
        output = self.root / "结果.json"
        run = subprocess.run([sys.executable, "-B", str(SCRIPT), "--input", str(path),
                              "--spacing", "2", "0.5", "0.25", "--output", str(output)],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["spacing"]["unit"], "µm")
        help_run = subprocess.run([sys.executable, "-B", str(SCRIPT), "--help"],
                                  capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(help_run.returncode, 0, help_run.stderr)


if __name__ == "__main__":
    unittest.main()
