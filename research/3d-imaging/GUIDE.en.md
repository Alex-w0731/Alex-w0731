# Guide to the 3D scientific imaging workflow

[中文](GUIDE.zh-CN.md) · [Sources and licensing](SOURCES.en.md)

Verification date: **2026-10-02**. This guide covers confocal, light-sheet, and other research microscopy data with genuine z-stacks. See [SOURCES.en.md](SOURCES.en.md) for the projects and their terms.

**The browser currently provides workflow planning and a synthetic demonstration, with no real AI inference backend.** Changes to parameters, synthetic cells, 3D models, and status feedback on the page help explain the workflow. They do not mean that your microscopy files have been read, Cellpose has run, stitching has completed, or valid measurements have been produced. Real analysis must run in the external tools described below, with its results and records saved.

## Define the data and the question first

Example research questions: Within an experimentally confirmed tumor region, how does the 3D spatial distribution of a particular immune cell population relate to tumor cells, vessels, or tissue boundaries? Are there reproducible differences in cell density, morphology, and distance distributions between treatment and control groups?

Inputs should include volumetric data, acquisition metadata, and the experimental design. If only 2D sections are available, perform 2D analysis. Repeating slices along z, interpolating them, or using a model to fill in missing structure for a 3D display does not add genuine evidence about depth. CT/MRI coordinates, organ segmentation, and validation require a separate specialist approach; this guide does not treat Cellpose as a general medical model.

## Step 1: Verify axes, scale, and channels

Inspect a small portion of the data in Fiji or napari first. Record and confirm the following information before batch processing:

| Field | What to record | Common errors |
|---|---|---|
| `axes` and `shape` | Identify the t, c, z, y, and x axes and their lengths. OME-Zarr can use `t,c,z,y,x`; explicitly identify any absent dimensions. Different tools expect different axis orders. | Treating channels as z or time as depth; guessing axes from dimension lengths alone. |
| `spacing` / voxel size | `dz, dy, dx` and their units, from acquisition records or verifiable calibration. | Assuming 1 µm in every direction; confusing pixel size with optical resolution. |
| `channel` | Each channel's name, stain/marker, purpose, exposure, and related information. Specify which channels support segmentation and which support phenotype assignment. | Equating RGB display colors with raw channels; treating marker positivity as proof of cell identity. |
| `PSF` | Whether a measured or theoretical point spread function is available, its corresponding channel/view, acquisition conditions, and file version. | Deconvolving with an incompatible PSF; calling arbitrary sharpening a genuine recovery of information. |
| `anisotropy` | When dx≈dy, the z/xy sampling ratio for Cellpose can be recorded as `dz/dy`. | Entering a value before confirming axes and spacing; retaining the original spacing after interpolation. |
| Coordinates and bit depth | Origin, orientation, transformations, pixel type, intensity range, time interval, and missing slices. | Changing intensity bit depth without recording it; losing coordinates after stitching; silently filling missing slices. |

For example: `axes = z,c,y,x`, `shape = 80,4,512,512`, with spatial spacing `dz = 1.0 µm` and `dy = dx = 0.25 µm`. The corresponding anisotropy ratio is 4. This describes a sampling difference; it does not establish that axial resolution matches lateral resolution. If dx and dy differ, first determine how each tool handles that case and verify the coordinate conversion.

Current official Cellpose documentation allows explicit `z_axis`, `channel_axis`, and `anisotropy` settings. Avoid relying on automatic guesses. [3D inputs and parameters](https://github.com/MouseLand/cellpose/blob/main/docs/do3d.rst).

## Step 2: Build a multiscale data layer

Keep the original acquisition files as a read-only version and save derived data separately. Use the [official OME-Zarr documentation](https://ome-zarr.readthedocs.io/en/stable/) and [writer documentation](https://github.com/ome/ome-zarr-py/blob/master/ome_zarr/writer.py) to organize chunked data and multiscale pyramids, explicitly storing axes, scale, units, and coordinate transformations.

Choose image downsampling to suit the research task. Instance labels must preserve discrete IDs; do not apply linear interpolation to labels. Record the actual spacing at every scale. After conversion, spot-check the shape, bit depth, channels, values, and physical positions in the original and reread files to confirm that units have been preserved.

Test chunk size and memory use on a small ROI before expanding to more data. Use a low-resolution overview for global 3D viewing, read the original resolution for detailed ROI review, and retain the full measurement layer as the quantitative basis. The current stable napari documentation states that multiscale 3D display shows only the lowest-resolution level; this should not be interpreted as native streaming 3D at full detail. [napari Image](https://napari.org/stable/howtos/layers/image.html).

## Step 3: Stitch, register, and preprocess as needed

Skip stitching for a single volume. For multiple tiles or views, choose one of these routes:

1. **Fiji / BigStitcher**: Follow the [official installation and workflow](https://imagej.net/plugins/bigstitcher/) to enable the update site, define a dataset, verify its channels, views, time points, and initial positions, and save the XML. Calculate pairwise shifts, preview and filter them, run global optimization, inspect seams and corresponding points, then export the fused volume. For larger computation, refer to [BigStitcher-Spark](https://github.com/JaneliaSciComp/BigStitcher-Spark) and return to the GUI to verify each stage.
2. **Python / multiview-stitcher**: Load a small test dataset from the [official quickstart](https://github.com/multiview-stitcher/multiview-stitcher). Keep the transformation key for stage metadata and save the registration under a separate transformation key. Inspect the registration summary, compare before and after, then perform chunked fusion. Use official examples that match your pinned version; do not describe currently unsupported non-rigid transformations as available.

Check for spatial misalignment between channels, brightness differences at edges, duplicated structures, and missing tiles. Record registration residuals and the reasons for exclusions. If overlap or reliable correspondences are insufficient, reacquire data or intervene manually; an attractive fused image must not conceal unreliable alignment.

Treat flat-field/background correction, denoising, and deconvolution as explicit derivation steps. Deconvolution requires a compatible PSF. BigStitcher's [PSF management workflow](https://imagej.net/plugins/bigstitcher/psf) can estimate or assign PSFs from suitable fluorescent beads. If no trustworthy PSF is available, deconvolution can be skipped with the reason recorded. Compare signal and segmentation performance before and after processing, retaining all parameters and raw data.

## Step 4: Generate candidate segmentation, from ROIs to the full volume

Create a separate environment using the [official Cellpose installation instructions](https://github.com/MouseLand/cellpose). Record the software version, model name, weight source, and hash. The following GUI installation and launch commands have been verified in the official documentation:

```text
python -m pip install "cellpose[gui]"
python -m cellpose --Zstack
```

Start with representative ROIs covering dense, sparse, and low-contrast regions, tissue boundaries, deep regions, and stitching seams. Verify axes, segmentation channels, and anisotropy. Inspect labels in XY/XZ/YZ views before deciding whether to expand inference. Cellpose's default 3D approach computes predictions on orthogonal 2D slices and runs dynamics in 3D. A 3D label output alone does not establish that anisotropy was handled correctly. [Official 3D documentation](https://github.com/MouseLand/cellpose/blob/main/docs/do3d.rst).

For larger data, refer to [Distributed Cellpose](https://github.com/MouseLand/cellpose/blob/main/docs/distributed.rst): it uses Zarr input, inference on overlapping blocks, and label merging through the Python API. Check block edges for duplicated cell counts or fragmented cells across blocks. Use the official examples for the pinned version to determine the API and parameters; do not infer an unverified execution command from browser configuration.

Nuclear segmentation cannot directly substitute for complete cell boundaries, and cell instance segmentation does not automatically determine tumor, immune, or other phenotypes. Assign phenotypes in the object table using experimental markers, negative/positive controls, and predefined rules.

## Step 5: Review ROIs manually and apply QC gates

In [napari](https://github.com/napari/napari), inspect the original image, preprocessed image, automatic labels, and final labels together. In ROIs at the original resolution, manually check for missed objects, merged objects, fragmentation, incorrect segmentation, channel misalignment, and block boundaries. Save edits as a new label version and record the changed objects and reviewer. Edit labels in 2D slice views; where needed, set the brush to extend across neighboring slices. Labels cannot be edited directly in 3D display mode or when represented as multiscale data. [Labels documentation](https://napari.org/stable/howtos/layers/labels.html).

| Gate | What to check | Action if it fails |
|---|---|---|
| Metadata | Axis order, spacing, units, channels, and missing slices agree with the original records. | Complete or correct the records; stop measurements that depend on physical units. |
| Registration | Inspect seams, known structures, correspondence residuals, and cross-channel positions. | Register again, restrict the analysis region, or reacquire data. |
| Image quality | Saturation, low contrast, attenuation with depth, occlusion, and processing artifacts. | Record exclusion/stratification rules; reconsider acquisition or preprocessing conditions. |
| Segmentation | Compare with manual annotations in representative ROIs; inspect object-level misses/duplicates, boundaries, fragmentation, and merging. | Adjust parameters, fine-tune, or correct labels; reassess independent validation ROIs. |
| 3D and scale | Verify completeness in orthogonal slices; inspect downsampling/interpolation and anisotropy. | Correct scale settings or limit which metrics can be interpreted. |
| Output | Labels, object tables, coordinates, and exported files correspond, and can be recovered by rereading. | Repair export and ID mappings before publishing results. |

When manual reference labels are available, record Dice/IoU and object-level detection errors, explaining the object-matching rules, sample count, and ROI selection. Without reference annotations, report only manual spot-checks and known failure modes; do not present model scores as calibrated probabilities of correctness. Set QC thresholds in advance using real validation samples, not the synthetic demonstration.

## Step 6: Quantify labels and visualize meshes

**Labels** assign a discrete class or instance ID to each voxel. They support counting, voxel-based volume measurement, association with raw intensities, and instance review. A **mesh** is surface geometry derived from labels or an intensity isosurface. It supports sectioning, rotation, and presentation, and is affected by thresholds, spacing, smoothing, and simplification.

Start by calculating object volume from the final labels: voxel count × dx × dy × dz, in µm³. Use the actual physical volume of analyzable tissue as the denominator for density, recording excluded regions. Calculate coordinates, distances, and adjacency in the same physical coordinate system. Specify whether a metric uses centroid distance, shortest surface distance, or neighbor count within a predefined radius.

Use the [official vedo examples and documentation](https://github.com/marcomusy/vedo) to generate isosurfaces, sections, and research figures, saving the camera, color scale, opacity, cropping limits, and scale. Preserve original labels and geometry without presentation processing in the measurement layer. Simplification or smoothing is allowed only on display copies; a hole-filled appearance cannot substitute for genuinely missing data. If measuring mesh volume, check that the mesh is closed and geometrically valid.

## Example: tumor cells and the microenvironment

Assume the input is multichannel 3D tissue data with a nuclear stain, experimentally validated tumor-associated markers, immune phenotype markers, and annotations of vessels or tissue boundaries, together with sample IDs, experimental groups, and biological replicates. This is an analysis plan; it does not mean that the page has identified a real sample.

1. Use nuclear or cell instances as the objects of analysis. Keep segmentation separate from phenotype assignment, and retain a category for objects that cannot be classified reliably.
2. Record tumor regions, immune objects, vessels, and boundaries in one coordinate system. Review crowded regions, weak-signal regions, and tissue edges.
3. Calculate cell density, morphology, distance to vessels/boundaries, and proximity distributions between phenotypes. Specify parameters, adjacency definitions, and handling of truncated boundaries.
4. Compare groups using samples/donors or genuine experimental replicates. Do not treat every cell within one sample as an independent biological replicate. Consider attenuation with depth, tissue density, region selection, and detection bias.
5. Treat spatial results as candidate hypotheses for follow-up experiments. **Proximity, co-occurrence, or correlation does not establish direct interaction, and still less mechanistic causality.** Conclusions about mechanisms or drug responses require independent validation and an appropriate experimental design.

## Step 7: Save a reproducible evidence package

Assign a `run_id` to every run and record the relationship between original and derived versions. Suggested minimum records:

| Category | Fields to record |
|---|---|
| Data | Sample ID, experimental group, raw file list and checksums, format, axes, shape, dtype, spacing, units, channel names, and missing slices/excluded regions. |
| Processing | Input and output versions, tool versions or Git commits, model/weight sources and hashes, parameters, random seeds, registration transformations, PSF files and conditions, and resampling methods. |
| Manual review | Physical ROI bounds, reference label version, reviewer, time, object ID edit history, QC metrics, failure modes, and passed/pending-review status. |
| Quantification and visualization | Label version, object ID mapping, measurement formulas and units, adjacency definition, boundary rules, display mesh processing parameters, camera, and color scale. |
| Deliverables | Raw and derived data indexes, labels, object tables, parameter files, environment records, QC reports, slice evidence, research figures, and source/license records. |

Create a new run version when upgrading a model or changing parameters; do not overwrite old labels. Compare before and after in key ROIs. The existence of a file does not establish a successful run: reread the outputs and verify the records. Browser-exported configuration can only serve as planning input for these external execution steps. Until actual execution and validation are complete, retain a status of “not executed / demonstration / pending validation.”
