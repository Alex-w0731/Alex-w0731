<a name="top"></a>

<p align="center">
  <img src="assets/hud/hero.svg" width="100%" alt="Alex Wang. Experimental × computational cancer research: tumor immunology, functional genomics, single-cell and spatial omics. An animated mission-control view scanning a schematic tumor microenvironment." />
</p>

<p align="center">
  <a href="mailto:Alexw0731@icloud.com"><img src="assets/hud/btn-email.svg" height="36" alt="Email Alex: exchange ideas" /></a>
  &nbsp;
  <a href="https://orcid.org/0009-0005-8480-5387"><img src="assets/hud/btn-orcid.svg" height="36" alt="ORCID 0009-0005-8480-5387" /></a>
  &nbsp;
  <a href="https://github.com/Alex-w0731/tmelens"><img src="assets/hud/btn-tmelens.svg" height="36" alt="tmelens toolkit" /></a>
</p>

<p align="center">
  <a href="#research-focus">Research focus</a> &nbsp;·&nbsp;
  <a href="#open-tools">Open tools</a> &nbsp;·&nbsp;
  <a href="#selected-work">Selected work</a> &nbsp;·&nbsp;
  <a href="#tools-and-methods">Tools &amp; methods</a> &nbsp;·&nbsp;
  <a href="#research-radar">Research radar</a> &nbsp;·&nbsp;
  <a href="#selected-publications">Publications</a>
</p>

<a name="research-focus"></a>

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/sec-focus.svg" /><img src="assets/hud/sec-focus.svg" width="100%" alt="01 / Research focus" /></picture></p>

Hi, I'm **Alex Wang**. I connect experiments and computation to **identify and validate therapeutic targets in cancer**.

My work spans tumor omics, single-cell and spatial analysis, functional genomics, and in vivo models. I also have experience in **DNA nanomedicine and targeted drug delivery**. My recent open-source work looks at the **tumor immune microenvironment**: a transparent profiling toolkit for bulk transcriptomes.

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/loop.svg" /><img src="assets/hud/loop.svg" width="100%" alt="Research loop: observe tumor and clinical data → model single-cell and spatial patterns → perturb with functional genomics → validate mechanisms and targets → return with new questions." /></picture></p>

<details>
<summary><b>The questions behind the work</b></summary>

- **Tumor-scale patterns** — large-scale tumor transcriptomics and clinical-data integration.
- **Cell-scale context** — tumor heterogeneity and the microenvironment.
- **Causal mechanisms** — CRISPR screening, molecular biology and tumor models.
- **Therapeutic delivery** — nanomedicine-based therapeutic delivery.

I enjoy the space where an unexpected pattern becomes a testable question—and a question becomes an experiment.

</details>

<a name="open-tools"></a>

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/sec-build.svg" /><img src="assets/hud/sec-build.svg" width="100%" alt="02 / Open tools" /></picture></p>

<p><a href="https://github.com/Alex-w0731/tmelens"><picture><source media="(max-width: 640px)" srcset="assets/hud/m/feat-tmelens.svg" /><img src="assets/hud/feat-tmelens.svg" width="100%" alt="tmelens: look inside the tumour immune microenvironment from a bulk expression matrix. Signature scoring, hot / excluded / cold phenotypes, deconvolution, survival, ICB response." /></picture></a></p>

**[tmelens ↗](https://github.com/Alex-w0731/tmelens)** — a transparent Python toolkit to profile the tumour immune microenvironment from bulk transcriptomes: signature scoring, immune phenotypes, deconvolution, survival statistics checked against R, and immunotherapy-response analysis, with a single-file HTML report.

```bash
pip install git+https://github.com/Alex-w0731/tmelens.git
```

<a name="selected-work"></a>

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/sec-work.svg" /><img src="assets/hud/sec-work.svg" width="100%" alt="03 / Selected work" /></picture></p>

**From a biological question to an inspectable analysis.** Six starting points from the lab.

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/Alex-w0731/breast-cancer-multiomics"><img src="assets/hud/card-multiomics.svg" width="100%" alt="01 / Multiomics — connected layers" /></a>
      <h3><a href="https://github.com/Alex-w0731/breast-cancer-multiomics">Breast cancer multiomics ↗</a></h3>
      <p>Integrate single-cell, spatial and bulk RNA-seq with patient-aware analysis and synthetic checks.</p>
      <p><code>Python</code> <code>Multiomics</code></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/Alex-w0731/multiscale-tumor-transcriptomics"><img src="assets/hud/card-multiscale.svg" width="100%" alt="02 / Multiscale — from cells to tissue to cohort" /></a>
      <h3><a href="https://github.com/Alex-w0731/multiscale-tumor-transcriptomics">Multiscale tumor transcriptomics ↗</a></h3>
      <p>Connect cell states to tissue context through deconvolution, spatial analysis and joint NMF.</p>
      <p><code>R</code> <code>Transcriptomics</code></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/Alex-w0731/tcga-luad-survival-analysis"><img src="assets/hud/card-survival.svg" width="100%" alt="03 / Clinical signals — expression and outcome" /></a>
      <h3><a href="https://github.com/Alex-w0731/tcga-luad-survival-analysis">TCGA-LUAD survival analysis ↗</a></h3>
      <p>Retrieve cBioPortal cohorts, model survival and report Cox estimates with FDR correction.</p>
      <p><code>R</code> <code>Survival analysis</code></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/Alex-w0731/single-cell-melanoma-analysis"><img src="assets/hud/card-singlecell.svg" width="100%" alt="04 / Single cell — cellular heterogeneity" /></a>
      <h3><a href="https://github.com/Alex-w0731/single-cell-melanoma-analysis">Single-cell melanoma analysis ↗</a></h3>
      <p>Explore GSE72056 with Scanpy, from memory-conscious preprocessing to clustering and markers.</p>
      <p><code>Python</code> <code>Scanpy</code></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/Alex-w0731/breast-cancer-multiomics/tree/main/modules/crispr-screen"><img src="assets/hud/card-crispr.svg" width="100%" alt="05 / CRISPR screen — perturbation to evidence" /></a>
      <h3><a href="https://github.com/Alex-w0731/breast-cancer-multiomics/tree/main/modules/crispr-screen">CRISPR Screen Workbench ↗</a></h3>
      <p>Guide QC and MAGeCK RRA, plus separate SCLC/TNBC gene-summary audits and synthetic checks.</p>
      <p><code>Python</code> <code>MAGeCK</code></p>
    </td>
    <td width="50%" valign="top">
      <a href="research/3d-imaging/README.en.md"><img src="assets/hud/card-volume.svg" width="100%" alt="06 / AX / VOLUME — 3D microscopy, voxels to evidence" /></a>
      <h3><a href="research/3d-imaging/README.en.md">AX / VOLUME · 3D microscopy ↗</a></h3>
      <p>Plan calibrated 3D analysis, review orthogonal slices and export a reproducible run plan.</p>
      <p><code>Microscopy</code> <code>Research planner</code></p>
    </td>
  </tr>
</table>

<sub>Project illustrations are schematics, not experimental results. AX / VOLUME provides a synthetic demonstration and run planning; it has no browser AI inference backend.</sub>

<details>
<summary><b>Explore the CRISPR screen case studies</b></summary>

[KDM6B / SCLC case](https://github.com/Alex-w0731/breast-cancer-multiomics/blob/main/modules/crispr-screen/docs/cases/sclc/README.md) · [TNBC metastasis case](https://github.com/Alex-w0731/breast-cancer-multiomics/blob/main/modules/crispr-screen/docs/cases/nc/README.md) · [Synthetic demo](https://github.com/Alex-w0731/breast-cancer-multiomics/blob/main/modules/crispr-screen/docs/demo/README.md)

Guide-level quality control, MAGeCK RRA and separate contrasts across cell lines. Published gene-summary case studies and synthetic count validation have different evidence limits; the case pages document them.

</details>

<a name="3d-microscopy"></a>

<details>
<summary><b>AX / VOLUME: the 3D microscopy workflow, review gates and getting started</b></summary>

**AX / VOLUME** connects physical calibration, candidate segmentation and human review with measurement in the original label space.

[**Explore the workflow →**](research/3d-imaging/README.en.md) &nbsp;·&nbsp; [English workbench ↓](research/3d-imaging/workbench.en.html) &nbsp;·&nbsp; [中文工作台 ↓](research/3d-imaging/workbench.html)

[English guide](research/3d-imaging/GUIDE.en.md) · [中文指南](research/3d-imaging/GUIDE.zh-CN.md) · [中文流程](research/3d-imaging/README.md) · [Sources & licenses](research/3d-imaging/SOURCES.en.md)

[![Seven stages from calibrated microscopy voxels to reproducible evidence](assets/workflow-3d-imaging.svg)](research/3d-imaging/README.en.md)

Physical calibration → multiscale data → optional reconstruction → candidate segmentation → human review → native-label quantification → reproducible evidence.

- **Inspect before interpreting** — preserve axes, physical units, channel identity and raw-data checksums.
- **Review across scales** — use a low-resolution overview, then check original-resolution ROIs, raw slices, labels and revisions.
- **Keep measurement traceable** — quantify native labels; save display meshes, transforms and software versions separately. Spatial association does not establish causality.

Download <code>workbench.en.html</code> for English or <code>workbench.html</code> for Chinese and open it in a browser. Rotate the synthetic volume, inspect orthogonal slices, compare threshold sensitivity and export a run plan. Each file works independently; save both in the same folder to use the language links.

For real TIFFs, the [QC tool](research/3d-imaging/scripts/inspect_tiff.py) checks axes, spacing, intensity limits and optional instance-label volumes. [Nine synthetic tests](research/3d-imaging/scripts/tests/test_inspect_tiff.py) verify the QC tool; they are not biological or model-validation results. The [execution guide](research/3d-imaging/GUIDE.en.md) connects OME-Zarr, BigStitcher or multiview-stitcher, Cellpose, napari and scientific rendering.

<sub>Research planner + synthetic 3D demonstration. The browser does not read real samples or run model inference; real data, models and measurements require external tools and sample-specific validation. Sources checked 2 October 2026.</sub>

</details>

<a name="tools-and-methods"></a>

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/sec-stack.svg" /><img src="assets/hud/sec-stack.svg" width="100%" alt="04 / Tools &amp; methods" /></picture></p>

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/stack.svg" /><img src="assets/hud/stack.svg" width="100%" alt="Compute: R, Python, Seurat, Scanpy, CellChat, CytoTRACE2, Palantir, pySCENIC, bulk RNA-seq, scRNA-seq, ChIP-seq, survival analysis, pathway enrichment. Validate: CRISPR-Cas9 screens, qRT-PCR, Western blot, Co-IP, flow cytometry, cell culture, xenograft models, H&amp;E, IHC, IF, confocal microscopy, pathology-image analysis." /></picture></p>

<details>
<summary><b>Computational toolkit</b></summary>

R · Python · bulk RNA-seq · scRNA-seq · ChIP-seq · Seurat · Scanpy · CellChat · CytoTRACE2 · Palantir · pySCENIC · pathway enrichment · survival analysis · reproducible visualization

</details>

<details>
<summary><b>Experimental toolkit</b></summary>

Genome-wide CRISPR-Cas9 screening · qRT-PCR · Western blotting · Co-IP · flow cytometry · mammalian cell culture · xenograft models · H&E · IHC · immunofluorescence · confocal microscopy · quantitative pathology-image analysis

</details>

<a name="research-radar"></a>

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/sec-radar.svg" /><img src="assets/hud/sec-radar.svg" width="100%" alt="05 / Research radar" /></picture></p>

<p><a href="research/README.md"><picture><source media="(max-width: 640px)" srcset="assets/hud/m/radar.svg" /><img src="assets/hud/radar.svg" width="100%" alt="Research radar: five directions from questions to methods across spatial context, cell states, perturbation, delivery and morphology, drawn from a catalogue of 97 public resources." /></picture></a></p>

A curated map of **97 public GitHub resources** for experimental and computational cancer research.

[**Explore the roadmap →**](research/README.md) · [中文研究路线与90天计划](research/README.zh-CN.md) · [Full catalogue](research/CATALOGUE.zh-CN.md)

<details>
<summary><b>Five directions to explore</b></summary>

| Research question | Methods to evaluate |
|---|---|
| Spatial context and treatment vulnerability | SpatialData · BANKSY · LIANA+ · MultiNicheNet |
| Resistant states and lineage dynamics | CellRank · moscot · Cassiopeia · SCENIC+ |
| Perturbation models and experimental choices | SCEPTRE · State · linear baselines · cell-eval |
| Geometry and effective delivery | scadnano · oxDNA · Ax |
| Morphology, transcription and function | CellProfiler · Pycytominer · QuPath · COSMOS |

</details>

<sub>A learning and evaluation roadmap with data requirements, validation steps and stopping conditions. Inclusion does not imply that I have used or validated every tool. [Sources & license notes](research/SOURCES.md) · Checked 26 September 2026.</sub>

<a name="selected-publications"></a>

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/sec-pubs.svg" /><img src="assets/hud/sec-pubs.svg" width="100%" alt="06 / Selected publications" /></picture></p>

**2025 · Cell & Bioscience**<br />
[**KDM6B inhibition enhances chemotherapeutic response in small cell lung cancer via epigenetic regulation of apoptosis and ferroptosis. ↗**](https://doi.org/10.1186/s13578-025-01496-6)<br />
<sub>Wang Z&#42;, Liu Z&#42;, Yang Y&#42;, et al.</sub>

**2024 · JACS Au**<br />
[**A reconfigurable DNA framework nanotube-assisted antiangiogenic therapy. ↗**](https://doi.org/10.1021/jacsau.3c00661)<br />
<sub>Li W&#42;, Wang Z&#42;, Su Q&#42;, et al.</sub>

**2025 · Biology Direct**<br />
[**Large-scale bulk and single-cell RNA sequencing combined with machine learning reveals glioblastoma-associated neutrophil heterogeneity and establishes a VEGFA+ neutrophil prognostic model. ↗**](https://doi.org/10.1186/s13062-025-00640-z)<br />
<sub>Yang Y&#42;, Liu Z&#42;, Wang Z&#42;, et al.</sub>

<sub>* Co-first authors.</sub>

<p><picture><source media="(max-width: 640px)" srcset="assets/hud/m/footer.svg" /><img src="assets/hud/footer.svg" width="100%" alt="" /></picture></p>

<p align="center">
  <b>Rigorous science. Reproducible code. Room for playful ideas.</b><br />
  <sub>认真探索，也保持好玩。 ⚡</sub><br /><br />
  <a href="mailto:Alexw0731@icloud.com">Let's exchange ideas</a> &nbsp;·&nbsp; <a href="https://orcid.org/0009-0005-8480-5387">ORCID</a> &nbsp;·&nbsp; <a href="#top">Back to top ↑</a>
</p>

<details>
<summary><sub>⚡ Lab partner: Killua (open the Curiosity Lab)</sub></summary>
<br />
<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="assets/curiosity-lab-poster.png" />
    <img src="assets/curiosity-lab.gif" width="100%" alt="The Curiosity Lab. Curiosity, with a spark. Animated Killua scientist fan art with a glowing flask, orbiting electrons and electric sparks." />
  </picture>
</p>
<p align="center"><sub><a href="assets/CREDITS.md">Artwork &amp; credits</a> · <a href="motion/index.html">How the animation is made</a> · Profile graphics are generated by <a href="tools/profile_assets/build.py">tools/profile_assets</a></sub></p>
</details>
