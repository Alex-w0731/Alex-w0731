# 来源、核验范围与许可证记录

[中文研究指南](README.zh-CN.md) · [97项目录](CATALOGUE.zh-CN.md) · [结构化快照](catalogue.json)

## 本次核验做了什么

检索日期：**2026-09-26**。这是一份为癌症机制、功能基因组、单细胞/空间和DNA纳米递送研究制作的有范围的资源调查，不是GitHub全集、系统综述或最新性能排行榜。

1. 使用8组网页/GitHub定向发现检索和8组GitHub仓库搜索，扩展候选并纠正上游地址。发现清单中的“awesome”列表只作为线索，正式条目回到上游仓库。
2. 对104个候选仓库路径发起GitHub核查，其中包括纠错前的地址。98个返回有效仓库及README；97个纳入主目录，1个旧R实现保留迁移备注。另6个初始路径404；这不表示对应方法不存在。
3. 读取仓库元数据和README，重点核对功能、输入、方法边界、文档、硬件提示、模型权重与许可。未宣称全部issue、测试代码和论文全文均经审查。
4. 用研究索引定位部分论文，再用作者仓库核对。线性基线论文的全文工具未返回正文，Nature/PMC网页读取也受访问限制；关于它的表述限定为作者题名、元数据和仓库支持的benchmark结论，没有扩展为对所有模型的否定。
5. 为每个主目录条目保存README内容SHA和修改该文件的commit，下面链接指向对应版本。`last_push`只是GitHub仓库推送时间，不能等同于版本发布、维护质量或本地验证。

**没有执行的步骤：** 未安装97个工具、下载大型权重/数据、重现其论文结果、运行其测试套件、生成新实验或调用付费推理。因此“核验通过”只指来源和文档记录，不是结果正确性或运行兼容性认证。A/B/C、P1/P2/P3与资源类别是本目录的规划判断。

### 发现检索的主要主题

- `site:github.com single cell perturbation State Tahoe 2026`
- `site:github.com spatial transcriptomics niche foundation model 2026`
- `site:github.com BoltzGen RFdiffusion3 protein design`
- `site:github.com autonomous research agent PaperQA Biomni Kosmos`
- `site:github.com boltzgen boltz-community`
- `site:github.com RFdiffusion3 RosettaCommons foundry`
- `site:github.com DNA origami oxDNA scadnano active learning`
- `site:github.com perturbation prediction benchmark simple baseline Nature Methods 2025`

GitHub纠错/扩展词：MAGeCK、GSFA、SCENICplus、Geneformer、CellProfiler、botorch、decoupler-py、DNAforge。未找到可确认的Geneformer官方GitHub入口，因此没有将搜索返回的第三方镜像当作官方代码收录。

### 地址与迁移细节

- Novae：旧MICS-Lab地址解析至[prism-oncology/novae](https://github.com/prism-oncology/novae)。
- LIANA+、CellRank、PyDESeq2分别使用[scverse/liana](https://github.com/scverse/liana)、[scverse/cellrank](https://github.com/scverse/cellrank)、[scverse/PyDESeq2](https://github.com/scverse/PyDESeq2)。
- SCEPTRE解析至[Katsevich-Lab/sceptre](https://github.com/Katsevich-Lab/sceptre)，BoTorch使用[meta-pytorch/botorch](https://github.com/meta-pytorch/botorch)。
- [MAGeCK官方GitHub导航](https://github.com/liulab-dfci/MAGeCK)明确把源码与安装指向Bitbucket和SourceForge；[MAGeCK2](https://github.com/davidliwei/mageck2)是另一个需独立评估的分支，不能因名称近似替换已验证结果。
- [Python decoupler](https://github.com/scverse/decoupler)的README把[旧R decoupleR](https://github.com/saezlab/decoupleR)标为deprecated。主目录优先Python实现；已有依赖旧R实现的分析应锁定版本并评估迁移，而非直接删除依赖。
- DVC、GROBID和COSMOS的入口分别解析至[treeverse/dvc](https://github.com/treeverse/dvc)、[grobidOrg/grobid](https://github.com/grobidOrg/grobid)、[saezlab/cosmosR](https://github.com/saezlab/cosmosR)。

## 需要分开看代码、权重和依赖的项目

下表概括本次读取到的上游声明；采用时以所下载版本的完整条款为准。GitHub API的SPDX识别覆盖代码，不能代表模型、数据或附属软件。

| 项目 | 文档中明确的区别 | 来源 |
|---|---|---|
| State | 代码CC BY-NC-SA 4.0；权重及输出另有Arc非商用模型许可和使用政策 | [README](https://github.com/ArcInstitute/state#licenses) · [模型条款](https://github.com/ArcInstitute/state/blob/main/MODEL_LICENSE.md) |
| TERRA | 代码BSD-3-Clause；公开权重CC-BY-NC-4.0，非商用 | [README License](https://github.com/Lotfollahi-lab/terra#license) |
| SCENIC+ | 学术非商用软件协议，README也说明所覆盖的相关组件/数据库 | [LICENCE.txt](https://github.com/aertslab/scenicplus/blob/main/LICENCE.txt) |
| UNI / CONCH | README说明学术非商用及CC-BY-NC-ND 4.0等条款；权重申请/个人同意，另有再分发限制 | [UNI](https://github.com/mahmoodlab/UNI) · [CONCH](https://github.com/mahmoodlab/CONCH) |
| AlphaFold 3 | 代码Apache-2.0；模型参数使用单独条款，获取需遵循申请流程 | [README](https://github.com/google-deepmind/alphafold3) · [权重条款](https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md) |
| Boltz / Chai-1 | README分别说明代码及权重MIT / Apache-2.0；数据和外部服务仍按其条款 | [Boltz](https://github.com/jwohlwend/boltz) · [Chai-1](https://github.com/chaidiscovery/chai-lab) |
| BindCraft | 仓库许可不能覆盖全部依赖；流程使用PyRosetta等组件 | [README与安装说明](https://github.com/martinpacesa/BindCraft) |
| OpenMM | README说明不同部分采用MIT/LGPL等多个许可 | [README](https://github.com/openmm/openmm) |
| Biomni | 本体Apache-2.0；集成工具和数据库可能有更严格限制，且默认会下载数据湖 | [README](https://github.com/snap-stanford/Biomni) |
| PaperQA | 文献获取、模型服务成本和文献使用权独立于程序许可证 | [README](https://github.com/Future-House/paper-qa) |

## 部分关键论文的追溯入口

| 方法/问题 | 原始论文入口 | 对本目录的作用 |
|---|---|---|
| 扰动预测的简单基线 | [Ahlmann-Eltze等，Nature Methods 2025](https://doi.org/10.1038/s41592-025-02772-6) · [作者代码](https://github.com/const-ae/linear_perturbation_prediction-Paper) | 设计复杂模型与简单基线的对照；不作为2026所有模型的结论 |
| LIANA+ | [Nature Cell Biology 2024](https://doi.org/10.1038/s41556-024-01469-w) · [代码](https://github.com/scverse/liana) | 跨条件、单细胞/空间通讯推断框架的出处 |
| Nicheformer | [Nature Methods](https://doi.org/10.1038/s41592-025-02814-z) · [代码](https://github.com/theislab/nicheformer) | 单细胞与空间基础模型的原始来源 |
| Novae | [Nature Methods 2025](https://doi.org/10.1038/s41592-025-02899-6) · [代码](https://github.com/prism-oncology/novae) | 图模型空间域分析的出处 |
| SCENIC+ | [Nature Methods 2023](https://doi.org/10.1038/s41592-023-01938-4) · [代码](https://github.com/aertslab/scenicplus) | 增强子与调控网络推断的出处 |
| GSFA | [Nature Methods 2023](https://doi.org/10.1038/s41592-023-02017-4) · [代码](https://github.com/xinhe-lab/GSFA) | Perturb-seq潜在模块与基因响应方法 |
| moscot | [Nature](https://doi.org/10.1038/s41586-024-08453-2) · [代码](https://github.com/theislab/moscot) | 多模态最优传输研究路线的出处 |
| CellOracle | [Nature](https://doi.org/10.1038/s41586-022-05688-9) · [代码](https://github.com/morris-lab/CellOracle) | 网络与计算扰动的出处 |

这些引文用于定位方法，不表示本次重新评估了全部论文数据。预印本、正式论文与具体软件版本应在实际引用时分别记录。

## 97个条目的README版本与代码许可信号

下面“代码许可信号”是GitHub API检测结果；“未自动识别”不是没有许可证。前述重要补充优先于单个SPDX标签。完整README内容SHA、当次访问时间、原始请求地址、标准地址及推送时间保存在[catalogue.json](catalogue.json)。

### 基础分析

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [Scanpy](https://github.com/scverse/scanpy) | [读取版本](https://github.com/scverse/scanpy/blob/40d3860adfdea287db6a143b9c5851b181f5b7da/README.md) | 2026-09-25 | BSD-3-Clause |
| [Seurat](https://github.com/satijalab/seurat) | [读取版本](https://github.com/satijalab/seurat/blob/b4e5b105caff41ea3dbcb551c570bb303ce1ca88/README.md) | 2026-09-21 | 未自动识别；查上游 |
| [scvi-tools](https://github.com/scverse/scvi-tools) | [读取版本](https://github.com/scverse/scvi-tools/blob/3507d7997bb25db9b3310abd30edc53f048cc88b/README.md) | 2026-09-26 | BSD-3-Clause |
| [Scirpy](https://github.com/scverse/scirpy) | [读取版本](https://github.com/scverse/scirpy/blob/ba0a9fb4f5b06769fa8d53885fe9d80796dd7584/README.md) | 2026-09-23 | BSD-3-Clause |
| [PyDESeq2](https://github.com/scverse/PyDESeq2) | [读取版本](https://github.com/scverse/PyDESeq2/blob/78be6d0558adfca754bfb7217e8416c0276bd612/README.md) | 2026-09-21 | MIT |
| [dreamlet](https://github.com/GabrielHoffman/dreamlet) | [读取版本](https://github.com/GabrielHoffman/dreamlet/blob/6ddcb83fb060eae989e541b6b82b46b3eaebd7bb/README.md) | 2026-09-23 | 未自动识别；查上游 |
| [muscat](https://github.com/HelenaLC/muscat) | [读取版本](https://github.com/HelenaLC/muscat/blob/f4345b5dc1188daaf09d778cda1c4456a6299566/README.md) | 2026-07-06 | 未自动识别；查上游 |

### 空间组学

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [SpatialData](https://github.com/scverse/spatialdata) | [读取版本](https://github.com/scverse/spatialdata/blob/65dc73ea84b1d524e7a0228b5a86d8469de727d8/README.md) | 2026-09-24 | BSD-3-Clause |
| [Squidpy](https://github.com/scverse/squidpy) | [读取版本](https://github.com/scverse/squidpy/blob/821a370f93f7d9b2bb961e8939857c84adda0482/README.md) | 2026-09-26 | BSD-3-Clause |
| [cell2location](https://github.com/BayraktarLab/cell2location) | [读取版本](https://github.com/BayraktarLab/cell2location/blob/8480e66ef2fd8a7112b18432424e033f540d3171/README.md) | 2026-08-31 | Apache-2.0 |
| [RCTD / C-SIDE](https://github.com/dmcable/spacexr) | [读取版本](https://github.com/dmcable/spacexr/blob/081e425005d7dafc857e4c359bd6e48ae3bca9d0/README.md) | 2026-01-22 | GPL-3.0 |
| [Tangram](https://github.com/broadinstitute/Tangram) | [读取版本](https://github.com/broadinstitute/Tangram/blob/4c68995a418f41dc8caef567598c4d9b47781a13/README.md) | 2025-07-01 | BSD-3-Clause |
| [BANKSY](https://github.com/prabhakarlab/Banksy) | [读取版本](https://github.com/prabhakarlab/Banksy/blob/08d2d91fbdf8d13c2346f8daf90a2f6b57597b36/README.md) | 2026-05-30 | 未自动识别；查上游 |
| [Sopa](https://github.com/prism-oncology/sopa) | [读取版本](https://github.com/prism-oncology/sopa/blob/ae9b729e53bf5874f692a515e5fc5d2a3af24912/README.md) | 2026-09-15 | BSD-3-Clause |
| [Nicheformer](https://github.com/theislab/nicheformer) | [读取版本](https://github.com/theislab/nicheformer/blob/311f4e1569b792508e0b02d6cbaf350d84587c51/README.md) | 2025-11-23 | BSD-3-Clause |
| [Novae](https://github.com/prism-oncology/novae) | [读取版本](https://github.com/prism-oncology/novae/blob/2f20df90bdf55ea9b90ca9a0c4dce735256d103c/README.md) | 2026-09-18 | BSD-3-Clause |
| [TERRA](https://github.com/Lotfollahi-lab/terra) | [读取版本](https://github.com/Lotfollahi-lab/terra/blob/6d431af57fb0ba2055b1a7d47b9fe1659ef024d4/README.md) | 2026-08-10 | BSD-3-Clause |
| [stFormer](https://github.com/csh3/stFormer) | [读取版本](https://github.com/csh3/stFormer/blob/d69fcfd06fccadaef686ee7c223a8a8079350010/README.md) | 2026-08-21 | MIT |
| [scGPT-spatial](https://github.com/bowang-lab/scGPT-spatial) | [读取版本](https://github.com/bowang-lab/scGPT-spatial/blob/f9442d777ba47cd3dcac8253833a233ff5bf7262/README.md) | 2025-02-13 | MIT |

### 机制与谱系

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [LIANA+](https://github.com/scverse/liana) | [读取版本](https://github.com/scverse/liana/blob/c59472ccc9de8360dbbf5016db75f8abde08dd3e/README.md) | 2026-09-24 | BSD-3-Clause |
| [NicheNet](https://github.com/saeyslab/nichenetr) | [读取版本](https://github.com/saeyslab/nichenetr/blob/66f90d5eeafef280b2b2f339b3fd70ffec1781dd/README.md) | 2026-09-25 | 未自动识别；查上游 |
| [MultiNicheNet](https://github.com/saeyslab/multinichenetr) | [读取版本](https://github.com/saeyslab/multinichenetr/blob/2d2e9b0531126291d4dd66f64358b8561436ff86/README.md) | 2025-08-12 | GPL-3.0 |
| [decoupler (Python)](https://github.com/scverse/decoupler) | [读取版本](https://github.com/scverse/decoupler/blob/e1ff035553f7ca1073852cdf06dc38132ca22bed/README.md) | 2026-09-25 | BSD-3-Clause |
| [SCENIC+](https://github.com/aertslab/scenicplus) | [读取版本](https://github.com/aertslab/scenicplus/blob/840dab85de3044846234c157e327b6ea0290abfb/README.md) | 2026-01-16 | 未自动识别；查上游 |
| [CellRank 2](https://github.com/scverse/cellrank) | [读取版本](https://github.com/scverse/cellrank/blob/bd555e15cb88348fc041c413d13a1a6039071c15/README.md) | 2026-09-16 | BSD-3-Clause |
| [moscot](https://github.com/theislab/moscot) | [读取版本](https://github.com/theislab/moscot/blob/bb4e9c44c1d5f78ac683d079ea93420eb2336af2/README.rst) | 2026-09-21 | BSD-3-Clause |
| [CellOracle](https://github.com/morris-lab/CellOracle) | [读取版本](https://github.com/morris-lab/CellOracle/blob/9f821ea5878a97d6f0076a08e886331d57a88b57/README.md) | 2026-04-30 | 未自动识别；查上游 |
| [scBasset](https://github.com/calico/scBasset) | [读取版本](https://github.com/calico/scBasset/blob/aed3a6f713091fd988196b297e9c06e092ff1d22/README.md) | 2025-09-09 | Apache-2.0 |
| [tangermeme](https://github.com/jmschrei/tangermeme) | [读取版本](https://github.com/jmschrei/tangermeme/blob/ff18f9239cb7d8cbcef1955b3fcdd03478ff205d/README.md) | 2026-09-25 | MIT |
| [ChromBPNet](https://github.com/kundajelab/chrombpnet) | [读取版本](https://github.com/kundajelab/chrombpnet/blob/09938fdb4397ec0006510e5251e48920a505d4de/README.md) | 2026-06-09 | MIT |
| [COSMOS](https://github.com/saezlab/cosmosR) | [读取版本](https://github.com/saezlab/cosmosR/blob/f260369477b4a7910692406cf2e82234d4160a14/README.md) | 2026-09-03 | GPL-3.0 |
| [CARNIVAL](https://github.com/saezlab/CARNIVAL) | [读取版本](https://github.com/saezlab/CARNIVAL/blob/2b8887a0ae473a65deb934b121c8407b26e7a17d/README.md) | 2023-12-06 | 未自动识别；查上游 |
| [Cassiopeia](https://github.com/YosefLab/Cassiopeia) | [读取版本](https://github.com/YosefLab/Cassiopeia/blob/156fe1e8f24ce19d7245772ac5a46319214319dc/README.md) | 2026-07-23 | MIT |

### CRISPR实测

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [MAGeCK官方导航](https://github.com/liulab-dfci/MAGeCK) | [读取版本](https://github.com/liulab-dfci/MAGeCK/blob/1c54f6c2d3afe69939c501e6c420b9226184f447/README.md) | 2020-12-16 | 未自动识别；查上游 |
| [MAGeCK2](https://github.com/davidliwei/mageck2) | [读取版本](https://github.com/davidliwei/mageck2/blob/65dabeb893746b1f42aa07d637cf3fe44043ded9/README.md) | 2026-09-22 | BSD-3-Clause |
| [MAGeCKFlute](https://github.com/WubingZhang/MAGeCKFlute) | [读取版本](https://github.com/WubingZhang/MAGeCKFlute/blob/25b659e41eefbc3e107e70e1c4872724d4e68e1a/README.md) | 2026-06-08 | 未自动识别；查上游 |
| [Chronos](https://github.com/broadinstitute/chronos) | [读取版本](https://github.com/broadinstitute/chronos/blob/0f18c90c7b5a48edfd4d3494009aa631feb258ee/README.md) | 2026-09-11 | BSD-3-Clause |
| [DrugZ](https://github.com/hart-lab/drugz) | [读取版本](https://github.com/hart-lab/drugz/blob/29304c61163f8c98d7031786452c0c7e1b19a202/README.md) | 2021-08-09 | MIT |
| [BAGEL2](https://github.com/hart-lab/bagel) | [读取版本](https://github.com/hart-lab/bagel/blob/5aea1eb84a8eea66f5feeb6286442fd535b98bff/README.md) | 2024-01-30 | MIT |
| [Pertpy](https://github.com/scverse/pertpy) | [读取版本](https://github.com/scverse/pertpy/blob/199ba30b274d625d7d1f88cbcfadcfc91f1c66eb/README.md) | 2026-09-25 | MIT |
| [SCEPTRE](https://github.com/Katsevich-Lab/sceptre) | [读取版本](https://github.com/Katsevich-Lab/sceptre/blob/34aaaa4dd9a233cbef3734c0ada91c273a0fe184/README.md) | 2026-08-31 | GPL-3.0 |
| [GSFA](https://github.com/xinhe-lab/GSFA) | [读取版本](https://github.com/xinhe-lab/GSFA/blob/4797b72c0c1edcedac445f284bfb1cbd70ba3b93/README.md) | 2023-10-03 | MIT |

### 虚拟扰动与评测

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [GEARS](https://github.com/snap-stanford/GEARS) | [读取版本](https://github.com/snap-stanford/GEARS/blob/719328bd56745ab5f38c80dfca55cfd466ee356f/README.md) | 2025-02-01 | MIT |
| [CPA](https://github.com/theislab/cpa) | [读取版本](https://github.com/theislab/cpa/blob/5049da959faed61f95b1a14d381524bfa018f84a/README.md) | 2024-08-14 | BSD-3-Clause |
| [State](https://github.com/ArcInstitute/state) | [读取版本](https://github.com/ArcInstitute/state/blob/dbf71a30ea4109a3e874b56a3377d51d97c63aec/README.md) | 2026-07-24 | 未自动识别；查上游 |
| [Tahoe-x1](https://github.com/tahoebio/tahoe-x1) | [读取版本](https://github.com/tahoebio/tahoe-x1/blob/6b66818f2d8923f686813ea01c278236ffdfc704/README.md) | 2026-08-25 | Apache-2.0 |
| [scGPT](https://github.com/bowang-lab/scGPT) | [读取版本](https://github.com/bowang-lab/scGPT/blob/3793f9de637d54a2175ae3fc2ee5f415af2186a5/README.md) | 2026-04-29 | MIT |
| [scFoundation](https://github.com/biomap-research/scFoundation) | [读取版本](https://github.com/biomap-research/scFoundation/blob/6f14f83f6cf3db16cde8d6a0e722fbd95240379d/README.md) | 2025-11-23 | Apache-2.0 |
| [scPRINT](https://github.com/cantinilab/scPRINT) | [读取版本](https://github.com/cantinilab/scPRINT/blob/c4cb108ea485bceb2bd11c6b50bc089e8b1ac621/README.md) | 2026-08-11 | GPL-3.0 |
| [scPerturBench](https://github.com/bm2-lab/scPerturBench) | [读取版本](https://github.com/bm2-lab/scPerturBench/blob/6e24e7a9827e55d4567d2139427be9af0d1e7a6c/README.md) | 2026-09-14 | GPL-3.0 |
| [Linear baselines](https://github.com/const-ae/linear_perturbation_prediction-Paper) | [读取版本](https://github.com/const-ae/linear_perturbation_prediction-Paper/blob/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/README.md) | 2025-07-18 | MIT |
| [cell-eval](https://github.com/ArcInstitute/cell-eval) | [读取版本](https://github.com/ArcInstitute/cell-eval/blob/459b52a82633a51598598605f41060a0654e80b4/README.md) | 2026-07-27 | MIT |

### 影像与表型

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [Cellpose / Cellpose-SAM](https://github.com/MouseLand/cellpose) | [读取版本](https://github.com/MouseLand/cellpose/blob/746f0d296d0cdf1c8318e7b312e2581ac25d5fcb/README.md) | 2026-06-14 | BSD-3-Clause |
| [QuPath](https://github.com/qupath/qupath) | [读取版本](https://github.com/qupath/qupath/blob/7fc4749dda19a3bb66fc30175bdcdc27afd33a1e/README.md) | 2026-09-23 | GPL-3.0 |
| [napari](https://github.com/napari/napari) | [读取版本](https://github.com/napari/napari/blob/bb3fdfda8567fc84284b1b721553cf1e6bf1da3c/README.md) | 2026-09-25 | BSD-3-Clause |
| [DeepCell](https://github.com/vanvalenlab/deepcell-tf) | [读取版本](https://github.com/vanvalenlab/deepcell-tf/blob/1634b5fbe939e93f463e0385511f91170655839d/README.md) | 2026-06-04 | Apache-2.0 |
| [UNI](https://github.com/mahmoodlab/UNI) | [读取版本](https://github.com/mahmoodlab/UNI/blob/42715efc11722a496e0a67f3369505a8f277206c/README.md) | 2025-03-26 | 未自动识别；查上游 |
| [CONCH](https://github.com/mahmoodlab/CONCH) | [读取版本](https://github.com/mahmoodlab/CONCH/blob/141cc09c7d4ff33d8eda562bd75169b457f71a62/README.md) | 2025-03-26 | 未自动识别；查上游 |
| [CellProfiler](https://github.com/CellProfiler/CellProfiler) | [读取版本](https://github.com/CellProfiler/CellProfiler/blob/e3f62221be97f8135c91a0d6cf23decd9e1622b7/README.md) | 2026-09-25 | 未自动识别；查上游 |
| [Pycytominer](https://github.com/cytomining/pycytominer) | [读取版本](https://github.com/cytomining/pycytominer/blob/edbe8d6203732f13813c90abe086d5d74471b3d3/README.md) | 2026-09-21 | BSD-3-Clause |

### 结构与分子设计

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [Boltz / Boltz-2](https://github.com/jwohlwend/boltz) | [读取版本](https://github.com/jwohlwend/boltz/blob/fd69c81bf104eb5ed0841a0c1d164a17c56878bf/README.md) | 2026-05-29 | MIT |
| [Chai-1](https://github.com/chaidiscovery/chai-lab) | [读取版本](https://github.com/chaidiscovery/chai-lab/blob/2f7b713d6addd8cd7688ddfd5cb49e138f3e5b78/README.md) | 2026-06-30 | Apache-2.0 |
| [AlphaFold 3](https://github.com/google-deepmind/alphafold3) | [读取版本](https://github.com/google-deepmind/alphafold3/blob/9b30e9aa4b232c32a40fe2f3f22ee311f2be455c/README.md) | 2026-09-21 | Apache-2.0 |
| [Foundry / RFdiffusion3](https://github.com/RosettaCommons/foundry) | [读取版本](https://github.com/RosettaCommons/foundry/blob/2e3f2edde2b7bab5a048b550fb690518911686c5/README.md) | 2026-09-08 | BSD-3-Clause |
| [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion) | [读取版本](https://github.com/RosettaCommons/RFdiffusion/blob/25b908256a4949afe8391fc9827e700cb4fe5e41/README.md) | 2026-07-15 | 未自动识别；查上游 |
| [BoltzGen](https://github.com/HannesStark/boltzgen) | [读取版本](https://github.com/HannesStark/boltzgen/blob/2c71c0bcacddfa8196c6a1eab1a427efd9061e52/README.md) | 2026-05-28 | MIT |
| [BindCraft](https://github.com/martinpacesa/BindCraft) | [读取版本](https://github.com/martinpacesa/BindCraft/blob/424709bf6bc08966f9fce78cc31957de160cc2cf/README.md) | 2026-09-21 | MIT |
| [ProteinMPNN](https://github.com/dauparas/ProteinMPNN) | [读取版本](https://github.com/dauparas/ProteinMPNN/blob/6a3c134e3b7c6ad0c608f85247e78a2e6110570d/README.md) | 2024-08-14 | MIT |
| [LigandMPNN](https://github.com/dauparas/LigandMPNN) | [读取版本](https://github.com/dauparas/LigandMPNN/blob/84614f993220a5a1243c7c6b2360d886c62781f8/README.md) | 2025-02-06 | MIT |
| [OpenMM](https://github.com/openmm/openmm) | [读取版本](https://github.com/openmm/openmm/blob/3bbd3bb9906b725da6a2b4910e258e0cc5c7d767/README.md) | 2026-09-25 | 未自动识别；查上游 |
| [RDKit](https://github.com/rdkit/rdkit) | [读取版本](https://github.com/rdkit/rdkit/blob/f1606cb940d2041c007b32ac73f41827a6f72d9b/README.md) | 2026-09-26 | BSD-3-Clause |

### 纳米设计与实验优化

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [Ax](https://github.com/facebook/Ax) | [读取版本](https://github.com/facebook/Ax/blob/93b6c7d3a9ce5cb24c8b47d2f5aac75b1312a23a/README.md) | 2026-09-21 | MIT |
| [BoTorch](https://github.com/meta-pytorch/botorch) | [读取版本](https://github.com/meta-pytorch/botorch/blob/054a0417fc2a2790f60bb6262195ee3f5f5814e9/README.md) | 2026-09-23 | MIT |
| [oxDNA](https://github.com/lorenzo-rovigatti/oxDNA) | [读取版本](https://github.com/lorenzo-rovigatti/oxDNA/blob/78818e7bc6853c42a9973a65772df3a9de2063c9/README.md) | 2026-09-21 | GPL-3.0 |
| [scadnano](https://github.com/UC-Davis-molecular-computing/scadnano) | [读取版本](https://github.com/UC-Davis-molecular-computing/scadnano/blob/d7c0d8e42f1b72349b35924ec7eba05fca7a73f9/README.md) | 2026-09-24 | MIT |
| [cadnano 2.5](https://github.com/cadnano/cadnano2.5) | [读取版本](https://github.com/cadnano/cadnano2.5/blob/24726d36b5892d4832bea7ee9a806370b33d6483/README.md) | 2023-11-15 | 未自动识别；查上游 |
| [oxView](https://github.com/sulcgroup/oxdna-viewer) | [读取版本](https://github.com/sulcgroup/oxdna-viewer/blob/85dccf1156778d7e04414e4b1a10139f3a3b734f/README.md) | 2026-07-10 | GPL-3.0 |
| [DNAforge](https://github.com/dnaforge/dnaforge) | [读取版本](https://github.com/dnaforge/dnaforge/blob/729005c3bc22995945c8594d89414ef52cb3bdb9/README.md) | 2026-08-18 | MIT |

### 可复现与论文工作流

| 项目 | 当次README版本 | 最近推送（UTC日期） | 代码许可信号 |
|---|---|---|---|
| [nf-core/rnaseq](https://github.com/nf-core/rnaseq) | [读取版本](https://github.com/nf-core/rnaseq/blob/ab4d7a724b57c5d6d02831921ddf4bdfaf1b82e5/README.md) | 2026-09-26 | MIT |
| [nf-core/chipseq](https://github.com/nf-core/chipseq) | [读取版本](https://github.com/nf-core/chipseq/blob/bfcd696b51d111b69328806d7b2c0e13c3cae428/README.md) | 2026-09-22 | MIT |
| [nf-core/atacseq](https://github.com/nf-core/atacseq) | [读取版本](https://github.com/nf-core/atacseq/blob/375eedba8ac52bd0afa0397a267104c947eb85fc/README.md) | 2026-09-26 | MIT |
| [nf-core/sarek](https://github.com/nf-core/sarek) | [读取版本](https://github.com/nf-core/sarek/blob/c3cbfab868258f8c8ad686a1453ca1703286915c/README.md) | 2026-09-23 | MIT |
| [nf-core/crisprseq](https://github.com/nf-core/crisprseq) | [读取版本](https://github.com/nf-core/crisprseq/blob/5316dc94d36084e260a6c6215983189b954f16ac/README.md) | 2026-09-11 | MIT |
| [Snakemake](https://github.com/snakemake/snakemake) | [读取版本](https://github.com/snakemake/snakemake/blob/9ab925e9b453f168e7f46e26c86d292c4d42fe0b/README.md) | 2026-09-26 | MIT |
| [Nextflow](https://github.com/nextflow-io/nextflow) | [读取版本](https://github.com/nextflow-io/nextflow/blob/93b244449012f2da034c5d1b34d00054f45245fe/README.md) | 2026-09-26 | Apache-2.0 |
| [DataLad](https://github.com/datalad/datalad) | [读取版本](https://github.com/datalad/datalad/blob/59e1c0b2d985421f6ebbb04db4064f0b3178162e/README.md) | 2026-09-26 | 未自动识别；查上游 |
| [DVC](https://github.com/treeverse/dvc) | [读取版本](https://github.com/treeverse/dvc/blob/cb96cf14872e842f461e84510ca73d337f5ace8e/README.rst) | 2026-09-21 | Apache-2.0 |
| [Quarto](https://github.com/quarto-dev/quarto-cli) | [读取版本](https://github.com/quarto-dev/quarto-cli/blob/45f556781e7bbe7fc80471d995d2d647dc941e50/README.md) | 2026-09-25 | 未自动识别；查上游 |
| [Jupyter Book](https://github.com/jupyter-book/jupyter-book) | [读取版本](https://github.com/jupyter-book/jupyter-book/blob/5eb284e4bfbc3ceae70f3f44dcb38bce21c301c6/README.md) | 2026-09-23 | BSD-3-Clause |
| [JASP](https://github.com/jasp-stats/jasp-desktop) | [读取版本](https://github.com/jasp-stats/jasp-desktop/blob/befa6ce9c641fbc4dd7863b9b1470d65156f73df/README.md) | 2026-09-26 | AGPL-3.0 |
| [Zotero](https://github.com/zotero/zotero) | [读取版本](https://github.com/zotero/zotero/blob/f5fcc9ee7be9f95be7bce0c8dd6c6efa87956f25/README.md) | 2026-09-25 | 未自动识别；查上游 |
| [GROBID](https://github.com/grobidOrg/grobid) | [读取版本](https://github.com/grobidOrg/grobid/blob/3227e9a6a990ec1687173045f119c24e17d10103/Readme.md) | 2026-09-22 | Apache-2.0 |
| [PaperQA2 / paper-qa](https://github.com/Future-House/paper-qa) | [读取版本](https://github.com/Future-House/paper-qa/blob/24878cb7c0428d226212652e35f669e4f10141fa/README.md) | 2026-09-25 | Apache-2.0 |
| [Biomni](https://github.com/snap-stanford/Biomni) | [读取版本](https://github.com/snap-stanford/Biomni/blob/c73eb050597f566c14f6313b1920c65d668db3aa/README.md) | 2026-09-21 | Apache-2.0 |
| [AI-Researcher](https://github.com/HKUDS/AI-Researcher) | [读取版本](https://github.com/HKUDS/AI-Researcher/blob/15d629504b91336616e124631f32a02cd952a68a/README.md) | 2025-10-16 | 未自动识别；查上游 |
| [DoWhy](https://github.com/py-why/dowhy) | [读取版本](https://github.com/py-why/dowhy/blob/487013f3896d35ce88a2230abaaf291bca83a20f/README.rst) | 2026-09-26 | MIT |
| [EconML](https://github.com/py-why/EconML) | [读取版本](https://github.com/py-why/EconML/blob/f0fc2e7d39d20e1a9d9201233fb7945e88cab0cc/README.md) | 2026-09-25 | 未自动识别；查上游 |
