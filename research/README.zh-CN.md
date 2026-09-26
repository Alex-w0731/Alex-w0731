# 从肿瘤组学线索到可验证机制：科研工具与研究路线

**2026-09-26 · 面向实验与计算结合的癌症研究。**

[97项分类目录](CATALOGUE.zh-CN.md) · [来源与核验记录](SOURCES.md) · [English overview](README.md) · [返回主页](../README.md)

这份导航围绕我已有的癌症机制、CRISPR功能筛选、单细胞/空间组学与DNA纳米递送背景，整理值得学习、评测和组合的公开工具。它是未来研究的工具地图与候选路线，条目不代表我已经掌握、运行或验证了所有方法；下面的研究方向也不是已经获得的发现。

我的优先选择是：**把现有组学与筛选工作推进到患者层级的可靠结果，再围绕一个可证伪机制做正交验证。** 大型模型最有价值的角色，是在这个过程中提高候选选择或实验效率。面向Nature、Cell、Science的长期目标，需要重要问题、解释深度和能经受独立检验的证据；任何工具组合都不构成录用保证。方法发表于Nature Methods等期刊，也不等于使用该方法就达到Nature主刊的研究标准。

```mermaid
flowchart LR
    Q[明确可证伪问题] --> D[患者与实验设计]
    D --> O[组学与空间证据]
    O --> H[少量机制候选]
    H --> P[真实扰动与正交验证]
    P --> V[独立背景复核]
    V --> R[可重现分析与论文]
    P --> A[更新假设与实验选择]
    A --> H
```

## 最先考虑的12个组合

优先级针对当前研究基础；可以复用现有代码的部分先复用。通常一次启用其中两到三个组合就足够。

| 顺序 | 组合与上游 | 对当前研究的实际增量 | 第一份应拿到的证据 |
|---|---|---|---|
| 1 | [Scanpy](https://github.com/scverse/scanpy)＋[PyDESeq2](https://github.com/scverse/PyDESeq2)，复杂设计再用[dreamlet](https://github.com/GabrielHoffman/dreamlet) | 把当前分析推进到患者/样本层级 | 样本纳入表、设计矩阵、效应量与置信区间，而非细胞数量堆叠 |
| 2 | [scvi-tools](https://github.com/scverse/scvi-tools) | 合理整合单细胞/多模态数据 | 批次减少且已知生物差异得到保留的对照诊断 |
| 3 | [SpatialData](https://github.com/scverse/spatialdata)＋[Squidpy](https://github.com/scverse/squidpy) | 保留表达、位置、切片和图像的一致性 | 逐切片可复核的邻域图与患者级空间统计 |
| 4 | [cell2location](https://github.com/BayraktarLab/cell2location)＋[RCTD](https://github.com/dmcable/spacexr) | 完成当前空间解卷积计划，并加入替代方法 | 丰度后验、参考偏差分析和病理核对 |
| 5 | [BANKSY](https://github.com/prabhakarlab/Banksy)，再对照[Novae](https://github.com/prism-oncology/novae) | 将空间位置转化为可比较的组织生态位 | 独立患者中稳定的空间分区，不只是更漂亮的嵌入 |
| 6 | [LIANA+](https://github.com/scverse/liana)＋[MultiNicheNet](https://github.com/saeyslab/multinichenetr) | 把通讯候选连接到接收细胞响应 | 配体、受体、靶基因、空间邻接相互支持的少量候选 |
| 7 | [decoupler](https://github.com/scverse/decoupler)，有ATAC再用[SCENIC+](https://github.com/aertslab/scenicplus) | 从差异基因走向TF/通路和增强子机制 | 候选调控程序及其可检验预测 |
| 8 | [DrugZ](https://github.com/hart-lab/drugz)＋已有[MAGeCK工作台](https://github.com/Alex-w0731/breast-cancer-multiomics/tree/main/modules/crispr-screen) | 在现有筛选基础上评估治疗情境下的基因效应 | guide一致性、重复、处理匹配和独立验证 |
| 9 | [SCEPTRE](https://github.com/Katsevich-Lab/sceptre)＋[Pertpy](https://github.com/scverse/pertpy) | 有Perturb-seq时连接干预与细胞状态 | 校准、功效、guide分配和扰动响应审计 |
| 10 | [QuPath](https://github.com/qupath/qupath)＋[Cellpose](https://github.com/MouseLand/cellpose)＋[CellProfiler](https://github.com/CellProfiler/CellProfiler) | 建立转录组以外的组织/形态证据 | 盲法标注子集、分割误差和独立实验表型 |
| 11 | [Ax](https://github.com/facebook/Ax)＋按需[BoTorch](https://github.com/meta-pytorch/botorch) | 让下一轮实验选择具有明确目标和约束 | 同预算下与随机/均匀选择比较的实验效率 |
| 12 | [Snakemake](https://github.com/snakemake/snakemake)＋[Quarto](https://github.com/quarto-dev/quarto-cli)＋[Zotero](https://github.com/zotero/zotero) | 把来源、分析、图和论文数字连起来 | 能重跑的结果、版本与每个主张对应的原始来源 |

如果目前只有公开表达矩阵，先做1、3、6、12；如果已有处理/对照CRISPR计数，先做8；如果已有可重复的递送实验读数，11可能比引入新基础模型更快产生价值。

## 五条值得发展的研究路线

以下是基于公开研究背景提出的方向性假设。具体靶点和实验方案应在数据评估、合作资源与文献查新后决定。

### 1. 空间生态位是否决定治疗脆弱性？

**问题。** 同一肿瘤细胞状态的治疗反应，是否受邻近基质/免疫细胞构成和信号影响？从目前公开的乳腺癌多组学项目切入最顺手。

**流程。** 患者级差异状态 → BANKSY/Novae定位生态位 → LIANA+/MultiNicheNet缩小信号候选 → decoupler/SCENIC+连接接收细胞程序 → 在可操纵的模型中改变信号或候选基因，并测定治疗反应。先跑基础空间模型，再判断基础模型有没有额外信息。[BANKSY](https://github.com/prabhakarlab/Banksy)、[LIANA+](https://github.com/scverse/liana)、[SCENIC+](https://github.com/aertslab/scenicplus)

**需要。** 多患者空间/单细胞数据，病理核对，以及能够区分肿瘤细胞自身效应与微环境效应的实验体系。独立细胞背景、不同扰动手段、救援/反向干预和空间蛋白证据可逐步加强解释。

**值得争取的贡献。** 证明可改变的组织环境如何决定治疗反应，并明确在哪些患者/细胞背景成立。

**停止或转向条件。** 空间信号完全由细胞比例、坏死、切片质量或批次解释；独立患者方向不一致；扰动虽改变表达却不改变预设功能终点。此时不继续围绕通讯分数堆图。

### 2. 耐药状态来自既有克隆选择，还是可逆状态转换？

**问题。** 治疗后出现的细胞状态，是原有少数克隆扩张，还是同一谱系发生状态改变？这能把SCLC治疗反应与表观遗传研究推进到时间和因果层面。

**流程。** 多时间点scRNA/必要时multiome → CellRank/moscot提出状态转换假说 → 有真实谱系条码时用Cassiopeia检验来源 → SCENIC+/CellOracle提出调控候选 → 在独立背景中做功能和恢复性验证。[CellRank](https://github.com/scverse/cellrank)、[moscot](https://github.com/theislab/moscot)、[Cassiopeia](https://github.com/YosefLab/Cassiopeia)、[CellOracle](https://github.com/morris-lab/CellOracle)

**需要。** 时间与重复设计是先决条件。没有谱系数据时，可以讨论模型推断的状态关系，不能宣称已经区分克隆选择与转分化。转录组与ATAC之外，可按问题加入蛋白/代谢读出。

**值得争取的贡献。** 区分“谁活下来”和“活下来的细胞如何改变”，再确定可干预的状态控制机制。

**停止或转向条件。** 结论依赖一种伪时间根节点、缺乏真实时间支持，或谱系结果与推断方向冲突；只改变增殖速度却被误解释为特异状态转换。

### 3. 虚拟细胞能否提高下一批实验的命中率？

**问题。** 对当前癌症背景，State/GEARS/CPA等模型能否在相同实验预算下，比简单规则更有效地选择值得验证的扰动？

**流程。** 冻结训练/验证/测试集合 → 先建立无变化、平均响应、线性等与任务相符的基线 → 分别测试未见扰动、未见细胞背景、未见组合 → 用cell-eval/scPerturBench的评价思路核对响应方向、差异基因/程序和分布 → Ax选择下一批实验，和基线选择策略同预算比较。[State](https://github.com/ArcInstitute/state)、[GEARS](https://github.com/snap-stanford/GEARS)、[CPA](https://github.com/theislab/cpa)、[cell-eval](https://github.com/ArcInstitute/cell-eval)

**模型分工。** GEARS官方明确不以跨细胞类型迁移为设计目标，可靠组合预测也需要部分组合训练数据；只在适用范围内评价它。跨背景任务应另选支持该任务的模型。

**需要。** 真实扰动数据、可保留的独立验证批次、预训练重叠审计和明确定义的成功终点。按患者/细胞系及扰动拆分；同一生物学重复的细胞不能散落在训练和测试两侧。

**值得争取的贡献。** 明确模型在何种背景具有前瞻性实验价值，以及失败时缺失了什么生物学信息。2025年的线性基线研究提示，应测试复杂度是否带来增益；该结果针对所测方法与任务，不能推出所有新模型无效。[作者代码与论文入口](https://github.com/const-ae/linear_perturbation_prediction-Paper)、[scPerturBench](https://github.com/bm2-lab/scPerturBench)

**停止或转向条件。** 独立背景上不优于基线，优势只来自数据泄漏或某一个指标，或者预测误差下降却没有提高真实实验效率。优先保留有用的简单模型。

### 4. DNA递送能否通过几何设计实现可解释的选择性？

**问题。** 在固定货物/识别模块条件下，纳米结构的形状、柔性与多价呈现方式，是否改变有效递送，而不只是增加摄取？

**流程。** scadnano/DNAforge提出结构家族 → oxDNA/oxView检查可行几何与构象 → Ax在测量噪声和资源约束下优化多个终点。只有当缺少合适识别模块、且具备蛋白验证合作时，再评估BoltzGen/BindCraft与Boltz/Chai-1；结构设计路线不必成为起步条件。[scadnano](https://github.com/UC-Davis-molecular-computing/scadnano)、[DNAforge](https://github.com/dnaforge/dnaforge)、[oxDNA](https://github.com/lorenzo-rovigatti/oxDNA)、[Ax](https://github.com/facebook/Ax)

**需要。** 可重复的结构表征与功能读数。区分结合、内吞、有效货物作用、正常细胞影响及稳定性；计算模拟只为筛选设计服务。多目标之间的取舍应提前定义，避免只优化最好看的一个终点。

**值得争取的贡献。** 一个可解释、跨批次成立的“几何—递送—功能”关系，再说明其适用边界。

**停止或转向条件。** 优势来自货物量不等、游离成分或批次；摄取增加但有效作用没有改善；模拟排序和真实结构/性能系统性不一致。结合预测分数不能代替实测结合或体内证据。

### 5. 形态、转录和功能能否共同揭示治疗机制？

**问题。** 某些治疗响应是否首先体现为形态/组织变化，而仅靠转录差异容易遗漏？

**流程。** CellProfiler/Cellpose提取单细胞表型 → Pycytominer处理板/孔和形态特征 → 与独立实验的转录程序及CRISPR响应对照 → 如有磷酸化蛋白/代谢数据，再用COSMOS/CARNIVAL生成可检验的机制网络。[CellProfiler](https://github.com/CellProfiler/CellProfiler)、[Pycytominer](https://github.com/cytomining/pycytominer)、[COSMOS](https://github.com/saezlab/cosmosR)、[CARNIVAL](https://github.com/saezlab/CARNIVAL)

**需要。** 匹配处理、剂量/时间、实验批次与对照；独立实验验证。不同技术产生相似图案本身不算独立证据，要排除共同受到细胞数、死亡比例或成像批次影响。

**值得争取的贡献。** 一个能被扰动改变、在多个正交终点得到支持的机制，以及可用于后续筛选的表型读数。

**停止或转向条件。** 形态关联在校正细胞密度/死亡后消失；结果主要由显微镜或染色批次区分；整合模型没有优于单模态基线。

## 前沿项目：哪些值得现在看，哪些先等数据？

| 方向 | 候选 | 当前建议 |
|---|---|---|
| 空间基础模型 | [Novae](https://github.com/prism-oncology/novae)、[Nicheformer](https://github.com/theislab/nicheformer) | 有独立空间队列后，挑一个与BANKSY和病理分区对照 |
| 较新的空间模型 | [TERRA](https://github.com/Lotfollahi-lab/terra)、[stFormer](https://github.com/csh3/stFormer)、[scGPT-spatial](https://github.com/bowang-lab/scGPT-spatial) | 先核查权重、预训练队列和数据平台匹配；不同时铺开 |
| 扰动基础模型 | [State](https://github.com/ArcInstitute/state)、[Tahoe-x1](https://github.com/tahoebio/tahoe-x1)、[scPRINT](https://github.com/cantinilab/scPRINT) | 用已有权重、小规模任务和严格留出评价；不从头训练大模型 |
| 多基因/UMI筛选 | [MAGeCK2](https://github.com/davidliwei/mageck2) | README记录2026年包装更新及paired-guide/UMI功能；作为待验证升级路线 |
| 分子生成 | [Foundry/RFdiffusion3](https://github.com/RosettaCommons/foundry)、[BoltzGen](https://github.com/HannesStark/boltzgen) | 在明确靶点和实验验证能力后，与结构生物学/蛋白工程伙伴合作 |
| 文献与分析代理 | [PaperQA2](https://github.com/Future-House/paper-qa)、[Biomni](https://github.com/snap-stanford/Biomni) | 先完成一个能人工核验的小任务，如带来源的证据表和分析脚本草稿 |

这里的“前沿”表示值得评测，不是跨任务领先的已证实排名。论文存在、仓库活跃、模型规模和GitHub星数分别代表不同事情。

## 90天执行建议

这是研究启动计划，时间根据样本、实验周期与合作资源调整；不把90天当作完成整篇顶刊研究的承诺。

| 时间 | 工作 | 可审查交付物 | 继续条件 |
|---|---|---|---|
| 第1–7天 | 从五条路线中选一条主线；盘点数据/实验/算力，完成针对问题的查新 | 一页问题书、竞争解释、资源表、预设主要终点 | 数据与验证体系能回答同一个问题 |
| 第8–21天 | 整理真实数据及样本层级，复用现有流程 | 纳入排除记录、患者表、QC、版本/来源清单 | 无法解决的批次混杂先处理，不进入大规模候选筛选 |
| 第22–35天 | 跑简单基线，再增加一个有明确目的的方法 | 效应量、置信区间、失败案例、方法对照 | 新方法带来可解释且稳定的增量 |
| 第36–50天 | 冻结候选和验证设计 | 少量候选、每项竞争解释、功效/精度规划与停止标准 | 有独立于发现数据的验证路径 |
| 第51–70天 | 做可完成的独立复核/试验；记录阴性结果 | 原始数据、盲法/随机化记录、正交终点、批次一致性 | 主要方向可复现且混杂解释减弱 |
| 第71–90天 | 综合证据、补关键缺口，决定继续/转向 | 机制证据图、缺口表、可执行报告、后续实验计划 | 结论强度与证据相称，能说清尚未回答的问题 |

**当前最短起步路径。** 从[已有乳腺癌工作流](https://github.com/Alex-w0731/breast-cancer-multiomics)选一个真实数据切入点，或从[已有CRISPR模块](https://github.com/Alex-w0731/breast-cancer-multiomics/tree/main/modules/crispr-screen)完成一组真实计数的严格分析；先生成可核查的结果，再决定是否加入空间基础模型或Perturb-seq。已有项目中的合成演示和公开汇总表复核，不能直接充当这一阶段的真实整队列分析。

## 一套可以贯穿论文的证据记录

每个主张保留：问题与预期方向 → 数据来源/纳入标准 → 患者或实验单位 → 冻结输入与版本 → 主分析与基线 → 效应量/不确定性 → 替代解释 → 独立验证 → 失败/阴性结果 → 对应图表与原文来源。

图表从真实数据与脚本产生，机制示意与实验观测分开；数据、代码、参考基因组、模型权重版本和主要参数能互相追溯。样本量按生物学重复和目标效应/精度规划，不按细胞或图像patch数推算。预训练数据、发现集和验证集的重叠记录也是结果的一部分。

公开主页展示方法学习与可复现资源；未公开数据、私有靶点和未发表机制细节留在研究项目的受控记录中。
