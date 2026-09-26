# 科研工具目录：97 个核验条目

[研究路线与优先级](README.zh-CN.md) · [English overview](README.md) · [核验方法与来源快照](SOURCES.md) · [机器可读目录](catalogue.json)

分类跳转：[基础分析](#基础分析) · [空间组学](#空间组学) · [机制与谱系](#机制与谱系) · [CRISPR实测](#CRISPR实测) · [虚拟扰动与评测](#虚拟扰动与评测) · [影像与表型](#影像与表型) · [结构与分子设计](#结构与分子设计) · [纳米设计与实验优化](#纳米设计与实验优化) · [可复现与论文工作流](#可复现与论文工作流)

核验日期：2026-09-26。每个名称链接到当日确认的上游仓库；功能说明依据仓库README/官方文档，建议与局限是本目录的研究判断。未安装或运行这些工具，不能将“核验”理解为本机兼容性测试、结果复现或独立性能认证。

- **A**：优先作为已有文档的工程/分析底座；**B**：针对特定问题的研究方法，需数据适配与对照；**C**：前沿/探索性项目，先小规模验证。此为使用策略，非官方评级或期刊等级。
- **P1**：最先考虑；**P2**：有相应数据/资源后再启用；**P3**：观察或探索。不是建议同时安装97项。
- 资源为粗略规划类别：**L** 普通电脑小规模任务；**M** 随样本/图像量需要更多内存；**G** GPU路线优先或官方要求GPU；**H** 原始测序往往适合服务器/HPC；**API** 通常涉及模型服务或额外部署。不是测得的硬件下限，L也不意味着任意规模都能本地完成。
- 仓库代码许可证、模型权重、训练数据及第三方组件分别核查。详见[SOURCES.md](SOURCES.md)，特别是State、TERRA、SCENIC+、UNI/CONCH和AlphaFold 3。

## 基础分析

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [Scanpy](https://github.com/scverse/scanpy) | A/P1/M | 单细胞计数与元数据；QC、注释、降维与探索 | 按患者/批次诊断；漂亮UMAP不是生物学重复 |
| [Seurat](https://github.com/satijalab/seurat) | A/P2/M | R单细胞及多模态分析；已有Seurat对象时优先 | 选择一个主生态，避免反复转换丢失counts与元数据 |
| [scvi-tools](https://github.com/scverse/scvi-tools) | A/P1/G | 单细胞计数、多模态输入；概率建模与整合 | 逐模型核对输入；不能把疾病效应作为批次消掉 |
| [Scirpy](https://github.com/scverse/scirpy) | A/P2/M | 配套TCR/BCR及单细胞数据；克隆型与细胞状态 | 需要真实受体测序；克隆扩增不等于肿瘤抗原特异性 |
| [PyDESeq2](https://github.com/scverse/PyDESeq2) | A/P1/M | bulk或患者×细胞类型聚合计数；差异表达 | 沿用当前Python工作流；设计矩阵要满秩，避免细胞伪重复 |
| [dreamlet](https://github.com/GabrielHoffman/dreamlet) | B/P1/M | 多样本单细胞；加权伪bulk与复杂混合模型 | 有重复测量/多中心时优先评估；病人数决定推断能力 |
| [muscat](https://github.com/HelenaLC/muscat) | B/P2/M | 多样本、多条件、多亚群差异状态分析 | 作为患者层级DE的独立方法对照，不挑最显著的方法 |

## 空间组学

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [SpatialData](https://github.com/scverse/spatialdata) | A/P1/M | 图像、坐标、分割与表达的共同数据结构 | 固定坐标变换和格式版本；这是数据底座 |
| [Squidpy](https://github.com/scverse/squidpy) | A/P1/M | 空间邻接图、共现与空间统计 | 逐切片建图，患者级汇总；跨切片连接会制造邻居 |
| [cell2location](https://github.com/BayraktarLab/cell2location) | B/P1/G | 有注释scRNA参考＋空间原始计数；细胞丰度估计 | 检查参考覆盖、后验和超参数敏感性；丰度不是直接计数 |
| [RCTD / C-SIDE](https://github.com/dmcable/spacexr) | B/P2/M | spacexr中解卷积与细胞类型特异空间DE | 可作为解卷积对照；README说明Bioconductor实现暂仅RCTD，C-SIDE仍看该仓库 |
| [Tangram](https://github.com/broadinstitute/Tangram) | B/P2/G | scRNA与空间表达对齐、映射 | 推断的未测基因不是独立观测，不能当验证真值 |
| [BANKSY](https://github.com/prabhakarlab/Banksy) | B/P1/M | 表达＋邻域特征；空间分区与状态识别 | 与纯表达聚类对照，检查邻域尺度和组织边界 |
| [Sopa](https://github.com/prism-oncology/sopa) | A/P2/M | 空间单细胞/多重成像的大图处理与分割流程 | 已有Xenium/Visium HD等时采用；分割质量决定后续可信度 |
| [Nicheformer](https://github.com/theislab/nicheformer) | B/P2/G | 单细胞及空间预训练表征 | 独立患者/平台外部测试；不能从解离表达恢复已证实的空间位置 |
| [Novae](https://github.com/prism-oncology/novae) | B/P2/G | 图模型表征与跨切片空间域分析 | 和BANKSY及病理分区比较；检查预训练重叠 |
| [TERRA](https://github.com/Lotfollahi-lab/terra) | C/P3/G | 空间细胞及邻居；JEPA基础模型表征 | 官方要求NVIDIA GPU；权重非商用；先评估是否增加可解释信息 |
| [stFormer](https://github.com/csh3/stFormer) | C/P3/G | 考虑配体邻域的空间基因表征与模拟扰动 | 注意spot与单细胞分辨率差异；模拟配体扰动待实验证实 |
| [scGPT-spatial](https://github.com/bowang-lab/scGPT-spatial) | C/P3/G | 空间数据上继续预训练的scGPT | 核查面板覆盖、预训练来源及平台泛化 |

## 机制与谱系

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [LIANA+](https://github.com/scverse/liana) | B/P1/M | 单细胞/空间多条件通讯推断 | 用空间邻接与接收细胞靶基因限制候选；通讯分数不是因果证据 |
| [NicheNet](https://github.com/saeyslab/nichenetr) | B/P2/M | 配体与接收细胞响应基因的关联排序 | 先验数据库会影响结果；受体表达、蛋白与扰动另核验 |
| [MultiNicheNet](https://github.com/saeyslab/multinichenetr) | B/P1/M | 多患者、多条件差异通讯与配体靶基因 | 优于简单合并患者后画通讯圈图的设计；保留样本层级 |
| [decoupler (Python)](https://github.com/scverse/decoupler) | A/P1/M | 表达/组学与基因集/调控先验；通路与TF活性 | 优先活性及一致性证据；活性评分不直接测量酶活 |
| [SCENIC+](https://github.com/aertslab/scenicplus) | B/P2/M | scRNA＋scATAC；增强子—TF—靶基因网络 | 需匹配数据/参考；学术非商用许可；预测连边要用扰动检验 |
| [CellRank 2](https://github.com/scverse/cellrank) | B/P2/M | 多视角单细胞；状态转移与命运概率 | 伪时间不等于真实时间，更不是实测谱系 |
| [moscot](https://github.com/theislab/moscot) | B/P2/G | 最优传输连接时间、空间及多模态细胞状态 | 不同传输假设作敏感性比较；运输耦合不能证明祖先关系 |
| [CellOracle](https://github.com/morris-lab/CellOracle) | B/P2/M | 单细胞及调控网络；计算扰动候选TF | 模型方向是待验证假设；用真实扰动效应作留出评价 |
| [scBasset](https://github.com/calico/scBasset) | B/P2/G | scATAC峰及DNA序列；序列模型、TF推断 | 按染色体/样本隔离评估；序列归因需要正交证据 |
| [tangermeme](https://github.com/jmschrei/tangermeme) | C/P3/G | 序列模型解释与计算序列扰动 | 解释的是模型；先检查模型预测质量，再解释motif |
| [ChromBPNet](https://github.com/kundajelab/chrombpnet) | B/P2/G | ATAC/DNase等可及性与序列；偏差分解的碱基分辨率建模 | 需要原始信号、偏差模型与留出染色体；不能从表达矩阵凭空生成 |
| [COSMOS](https://github.com/saezlab/cosmosR) | B/P2/M | 转录/磷酸化蛋白/代谢及先验；整合机制子网络 | 适合从转录走向信号/代谢；先验与求解器影响解，不证明唯一机制 |
| [CARNIVAL](https://github.com/saezlab/CARNIVAL) | B/P2/M | TF活性与有向网络；寻找上游信号解释 | 因果推理依赖先验、假设和输入；求解器许可单独检查 |
| [Cassiopeia](https://github.com/YosefLab/Cassiopeia) | B/P2/M | 真实谱系条码测序；重建与分析细胞谱系树 | 需要先规划谱系实验；ILP等可选求解器有额外依赖 |

## CRISPR实测

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [MAGeCK官方导航](https://github.com/liulab-dfci/MAGeCK) | A/P1/L | pooled CRISPR计数；当前筛选基线的官方入口 | 该GitHub仓库指向Bitbucket/SourceForge，不能当成完整源码发行包 |
| [MAGeCK2](https://github.com/davidliwei/mageck2) | C/P3/L | 配对样本、UMI与paired-guide支持的新分支 | README有2026版发布记录；先和已验证MAGeCK结果逐项对照 |
| [MAGeCKFlute](https://github.com/WubingZhang/MAGeCKFlute) | B/P2/M | MAGeCK结果；QC、偏差处理与功能解释 | 核查所用R包上游/发行渠道；不替代原始guide QC |
| [Chronos](https://github.com/broadinstitute/chronos) | B/P2/M | pDNA＋后期guide计数和时间；基因适应度模型 | 缺pDNA或大多数细胞死亡的筛选不宜套用；差异显著性需生物学重复 |
| [DrugZ](https://github.com/hart-lab/drugz) | B/P1/L | 药物处理与对照筛选计数；药物—基因交互 | 药物增敏/抑制方向要明确；处理匹配、重复与后续救援验证 |
| [BAGEL2](https://github.com/hart-lab/bagel) | B/P2/L | pooled CRISPR；必需性分类 | 依赖参考必需/非必需基因集，不能替代情境特异交互分析 |
| [Pertpy](https://github.com/scverse/pertpy) | A/P2/M | 单细胞扰动；整理数据、距离、细胞组成及分析接口 | 按子方法选择依赖与统计单位；框架不是统一的因果估计器 |
| [SCEPTRE](https://github.com/Katsevich-Lab/sceptre) | B/P1/M | 基因计数＋gRNA/细胞映射；Perturb-seq检验 | 先做校准与功效检查；技术协变量及guide分配非常关键 |
| [GSFA](https://github.com/xinhe-lab/GSFA) | B/P2/M | 标准化表达＋扰动矩阵；扰动控制的潜在基因模块 | 贝叶斯因子模型需检查收敛、模块稳定性与符号错误率 |

## 虚拟扰动与评测

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [GEARS](https://github.com/snap-stanford/GEARS) | B/P2/G | 训练Perturb-seq；预测未见多基因扰动 | 官方不支持跨细胞类型迁移；可靠组合预测需部分组合训练数据；按适用任务评测 |
| [CPA](https://github.com/theislab/cpa) | B/P2/G | 药物/剂量/协变量标记的单细胞；组合效应预测 | 外推范围受训练覆盖限制；剂量、时间和细胞系都要核对 |
| [State](https://github.com/ArcInstitute/state) | C/P2/G | 细胞嵌入与状态转移模型；跨情境扰动响应 | 代码、权重、输出均有许可边界；必须对比简单基线 |
| [Tahoe-x1](https://github.com/tahoebio/tahoe-x1) | C/P3/G | 扰动训练的单细胞基础模型；癌症任务候选表征 | 官方训练栈要求较新NVIDIA GPU；首选小模型评估，不从头预训练 |
| [scGPT](https://github.com/bowang-lab/scGPT) | B/P2/G | 单细胞预训练、迁移及多类下游任务 | 核查预训练数据重叠；cell embedding用途与扰动预测分开评价 |
| [scFoundation](https://github.com/biomap-research/scFoundation) | B/P3/G | 大规模单细胞预训练表征与下游迁移 | 预训练规模不是你数据上的性能证据 |
| [scPRINT](https://github.com/cantinilab/scPRINT) | B/P2/G | 细胞表征、标签及基因网络推断 | README提示cellxgene数据可能已被训练使用；CPU可跑但慢 |
| [scPerturBench](https://github.com/bm2-lab/scPerturBench) | B/P1/M | 多扰动方法与数据集的比较代码 | 用于设计评测；该历史基准不能直接给2026新模型排总榜 |
| [Linear baselines](https://github.com/const-ae/linear_perturbation_prediction-Paper) | B/P1/M | 作者论文代码；简单线性扰动预测对照 | 复用其对照思想；研究结论仅适用于所测模型、数据及任务 |
| [cell-eval](https://github.com/ArcInstitute/cell-eval) | A/P1/M | 预测/真实AnnData；统一扰动效果评价 | 同时看差异响应与分布；随机分细胞的噪声上限不能代替独立重复 |

## 影像与表型

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [Cellpose / Cellpose-SAM](https://github.com/MouseLand/cellpose) | A/P1/G | 显微图像；细胞/细胞核分割与人工修正 | 在你的染色/组织上盲法抽查并保存分割误差 |
| [QuPath](https://github.com/qupath/qupath) | A/P1/M | 全切片、IHC/IF；组织与细胞量化 | 冻结阈值、区域规则与扫描条件；患者而非patch作为独立单位 |
| [napari](https://github.com/napari/napari) | A/P2/M | 多维图像与标注层；交互检查 | 可视化入口，分析正确性仍需脚本和元数据 |
| [DeepCell](https://github.com/vanvalenlab/deepcell-tf) | B/P2/G | 深度学习单细胞图像分析/分割 | 代码许可与具体预训练模型/数据条款分别核验 |
| [UNI](https://github.com/mahmoodlab/UNI) | B/P2/G | 病理图像patch表征；下游分类与关联 | 权重需申请，学术非商用条款；患者/中心隔离并控制染色偏差 |
| [CONCH](https://github.com/mahmoodlab/CONCH) | B/P2/G | 病理图文表征；图像/文本联合检索与分析 | 受控权重及非商用条款；语言相似度不是分子表达实测值 |
| [CellProfiler](https://github.com/CellProfiler/CellProfiler) | A/P1/M | 显微图像；可追踪的形态学特征提取 | 在机制研究中提供转录以外的表型读出 |
| [Pycytominer](https://github.com/cytomining/pycytominer) | A/P1/M | 高内涵成像特征；归一化、聚合、特征筛选 | 保留板/孔/批次信息；用独立实验检查形态指纹 |

## 结构与分子设计

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [Boltz / Boltz-2](https://github.com/jwohlwend/boltz) | B/P2/G | 分子序列/结构输入；复合物结构与亲和力预测 | 结构置信度与亲和力字段意义不同；不能当实验Kd或疗效 |
| [Chai-1](https://github.com/chaidiscovery/chai-lab) | B/P2/G | 蛋白、DNA/RNA、小分子及约束；复合物结构 | 官方Linux/CUDA要求；用作不同模型假设下的复核 |
| [AlphaFold 3](https://github.com/google-deepmind/alphafold3) | B/P2/G | 多类型生物分子；结构推断 | 代码Apache-2.0不代表权重同许可；权重另需申请并接受条款 |
| [Foundry / RFdiffusion3](https://github.com/RosettaCommons/foundry) | C/P3/G | 生物分子设计/结构/逆折叠共用框架 | 前沿合作路线；核对模型版本、权重、输出结构与真实功能 |
| [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion) | B/P2/G | 约束下的蛋白骨架生成 | 已有稳定工作流时可保留；生成结构必须做表达与结合验证 |
| [BoltzGen](https://github.com/HannesStark/boltzgen) | C/P3/G | 面向靶标的蛋白/肽binder生成和筛选 | 官方提示GPU与约6GB首次模型下载；不从预测成功率推算实验成功率 |
| [BindCraft](https://github.com/martinpacesa/BindCraft) | B/P2/G | binder设计、过滤的整合流程 | 需蛋白制备/结合验证合作；PyRosetta等依赖另有许可；检查特异性 |
| [ProteinMPNN](https://github.com/dauparas/ProteinMPNN) | B/P2/G | 给定蛋白骨架；序列设计 | 拟合骨架的序列不保证可溶、稳定或有功能 |
| [LigandMPNN](https://github.com/dauparas/LigandMPNN) | B/P2/G | 含配体/原子环境的骨架；条件序列设计 | 验证配体状态、结构质量与选择性 |
| [OpenMM](https://github.com/openmm/openmm) | A/P2/G | 结构、力场与模拟体系；分子动力学 | 采样长度/力场/重复影响结论；轨迹稳定不证明结合或药效 |
| [RDKit](https://github.com/rdkit/rdkit) | A/P2/L | 分子结构；规范化、描述符与相似性 | 适合药物数据清理和骨架划分；不直接预测临床有效性 |

## 纳米设计与实验优化

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [Ax](https://github.com/facebook/Ax) | A/P1/L | 实验参数＋带噪声测量；约束、多目标自适应实验 | 先定义成功指标、重复与安全可行范围，再让模型建议下一批 |
| [BoTorch](https://github.com/meta-pytorch/botorch) | A/P2/L | 贝叶斯优化建模与采集函数；Ax的定制底层 | 官方仍称beta；常规实验先用Ax，复杂算法才直接使用 |
| [oxDNA](https://github.com/lorenzo-rovigatti/oxDNA) | B/P2/G | DNA/RNA拓扑与构象；粗粒化模拟 | 适合几何/力学筛选；不能单独推断血清稳定性或体内分布 |
| [scadnano](https://github.com/UC-Davis-molecular-computing/scadnano) | A/P2/L | DNA纳米结构；浏览器与脚本化设计 | 可与你DNA框架经验结合；输出仍需结构及功能表征 |
| [cadnano 2.5](https://github.com/cadnano/cadnano2.5) | A/P2/L | DNA折纸交互/脚本设计 | 旧GUI依赖先做兼容性试跑；与scadnano选适合现有格式的一种 |
| [oxView](https://github.com/sulcgroup/oxdna-viewer) | A/P2/L | oxDNA拓扑/构象/轨迹；查看和编辑 | 浏览与诊断，不代替定量模拟结果 |
| [DNAforge](https://github.com/dnaforge/dnaforge) | B/P3/L | 3D网格→DNA/RNA线框结构 | 几何设计新方向；制造与生物环境性能仍需验证 |

## 可复现与论文工作流

| 工具 | 层级/优先/资源 | 能解决什么、需要什么 | 关键判断与使用边界 |
|---|---|---|---|
| [nf-core/rnaseq](https://github.com/nf-core/rnaseq) | A/P1/H | FASTQ/BAM→基因计数与QC | 固定参考、流程版本与容器；全量测序需估计存储/内存 |
| [nf-core/chipseq](https://github.com/nf-core/chipseq) | A/P2/H | ChIP-seq原始读段；QC/峰等标准流程 | IP/input与峰类型匹配，公开重分析明确标注来源 |
| [nf-core/atacseq](https://github.com/nf-core/atacseq) | A/P2/H | ATAC-seq原始读段；QC与峰 | 质量指标和批次在解释调控机制前检查 |
| [nf-core/sarek](https://github.com/nf-core/sarek) | A/P2/H | WGS/靶向测序；胚系/体细胞变异 | 仅在有对应数据时纳入，肿瘤/正常样本配对明确 |
| [nf-core/crisprseq](https://github.com/nf-core/crisprseq) | A/P2/H | 编辑测序或pooled screen原始输入 | targeted和screening是不同路径，不能互换结果 |
| [Snakemake](https://github.com/snakemake/snakemake) | A/P1/L | 步骤、依赖与配置；现有分析模块编排 | 优先扩展已有Snakemake流程；锁定环境并保留日志 |
| [Nextflow](https://github.com/nextflow-io/nextflow) | A/P2/L | 容器/HPC/云工作流编排 | 跑nf-core时需要；执行引擎不决定统计有效性 |
| [DataLad](https://github.com/datalad/datalad) | A/P2/L | Git/git-annex数据与来源追踪 | 适合大数据引用；存储访问权限与数据发布许可独立 |
| [DVC](https://github.com/treeverse/dvc) | A/P2/L | 数据、模型与实验版本追踪 | 与DataLad按团队习惯二选一；不把大文件直接塞进Git |
| [Quarto](https://github.com/quarto-dev/quarto-cli) | A/P1/L | 文字、代码、结果和引文；可执行报告 | 让图表和数字来自同一冻结分析；文档生成不能校正错误统计 |
| [Jupyter Book](https://github.com/jupyter-book/jupyter-book) | A/P2/L | notebook与Markdown；可执行研究档案 | 当前版本与旧v1体系有差别，模板和依赖一起锁定 |
| [JASP](https://github.com/jasp-stats/jasp-desktop) | A/P2/L | 表格化实验结果；图形界面统计核查 | 适合小实验复核；须保存分析设置，不能靠反复试检验挑显著 |
| [Zotero](https://github.com/zotero/zotero) | A/P1/L | 论文元数据、PDF与引文库 | 维护正式发表版/勘误，逐条核对用于主张的引文 |
| [GROBID](https://github.com/grobidOrg/grobid) | A/P2/M | 论文PDF→结构化TEI与参考文献 | 适合批量知识库入口；OCR/表格/公式仍要人工核对 |
| [PaperQA2 / paper-qa](https://github.com/Future-House/paper-qa) | B/P2/API | 论文库检索、证据片段与带引文问答 | 模型/API成本和文献访问权限另计；回到原文核验每个关键结论 |
| [Biomni](https://github.com/snap-stanford/Biomni) | C/P2/API | 生物医学工具与数据编排的研究代理 | 默认数据湖约11GB；集成组件许可各异；只先用于可审计小任务 |
| [AI-Researcher](https://github.com/HKUDS/AI-Researcher) | C/P3/API | 从检索到代码/报告的科研自动化原型 | 保持人审科学问题、分析与引文；GitHub版本和托管产品分开看 |
| [DoWhy](https://github.com/py-why/dowhy) | B/P2/M | 因果图、假设、估计与反驳检验 | 帮助显式陈述假设；隐藏混杂不会因为调用库而消失 |
| [EconML](https://github.com/py-why/EconML) | B/P2/M | 观测数据与协变量；异质处理效应估计 | 先满足可识别性和数据设计；不把TCGA相关性包装为治疗因果效应 |
