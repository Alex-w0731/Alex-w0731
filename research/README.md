# Research methods radar

**A curated map of 97 public GitHub resources for experimental and computational cancer research.** Checked 26 September 2026.

[中文研究路线与90天计划](README.zh-CN.md) · [Full catalogue / 完整目录](CATALOGUE.zh-CN.md) · [Sources and verification](SOURCES.md) · [Machine-readable catalogue](catalogue.json) · [Profile](../README.md)

This collection connects my interests in cancer mechanisms, functional genomics, single-cell and spatial omics, and DNA nanomedicine. It is a learning and evaluation roadmap. Inclusion does not imply that I developed, installed, benchmarked, or validated a tool, or that a proposed research direction has produced a finding.

## Start with a question

I prioritize patient-aware inference, reproducible analysis, and experimental tests of competing mechanisms. New models are useful when they improve a defined decision or reveal a testable explanation.

| Research direction | Selected starting points |
|---|---|
| Spatial context and treatment vulnerability | [SpatialData](https://github.com/scverse/spatialdata), [BANKSY](https://github.com/prabhakarlab/Banksy), [LIANA+](https://github.com/scverse/liana), [MultiNicheNet](https://github.com/saeyslab/multinichenetr) |
| Resistant states and lineage dynamics | [CellRank](https://github.com/scverse/cellrank), [moscot](https://github.com/theislab/moscot), [Cassiopeia](https://github.com/YosefLab/Cassiopeia), [SCENIC+](https://github.com/aertslab/scenicplus) |
| Perturbation models that earn their experimental cost | [SCEPTRE](https://github.com/Katsevich-Lab/sceptre), [State](https://github.com/ArcInstitute/state), [cell-eval](https://github.com/ArcInstitute/cell-eval), [linear baselines](https://github.com/const-ae/linear_perturbation_prediction-Paper) |
| Geometry-aware delivery and adaptive experiments | [scadnano](https://github.com/UC-Davis-molecular-computing/scadnano), [oxDNA](https://github.com/lorenzo-rovigatti/oxDNA), [Ax](https://github.com/facebook/Ax) |
| Morphology, transcription and functional evidence | [CellProfiler](https://github.com/CellProfiler/CellProfiler), [Pycytominer](https://github.com/cytomining/pycytominer), [QuPath](https://github.com/qupath/qupath), [COSMOS](https://github.com/saezlab/cosmosR) |

The [Chinese guide](README.zh-CN.md) develops these five directions with required data, validation steps, stopping conditions, twelve priority tool combinations, and a 90-day starting plan. The [catalogue](CATALOGUE.zh-CN.md) separates established infrastructure, specialized research methods and exploratory projects, including spatial foundation models, perturbation models, protein design, evidence retrieval and executable publishing.

## How this collection was checked

Repository identity, README availability, descriptions, update metadata and license signals were checked against GitHub. Selected papers were located through research metadata and author repositories. This was a source review, not an installation test or independent performance benchmark. Code, weights, data and third-party components can carry different terms; the [source register](SOURCES.md) records important distinctions and immutable README links.

Research priorities and stopping conditions are editorial judgments. No tool or workflow guarantees acceptance by a particular journal.
