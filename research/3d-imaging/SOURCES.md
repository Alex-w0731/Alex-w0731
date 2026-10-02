# 三维成像 workflow：来源与借鉴记录

**中文** · [English](SOURCES.en.md)

核查日期：**2026-10-02**。本页依据项目作者的 GitHub 仓库、官方文档和许可文件；核查的是公开能力与使用边界，未对这些工具进行本机安装、独立性能测试或临床验证。

这里的 workflow 面向科研显微体数据。浏览器页面是**流程规划器与合成数据演示**，没有真实 AI 推理后台；模型名称、处理节点和示例图不代表已运行外部工具。使用指南见 [GUIDE.zh-CN.md](GUIDE.zh-CN.md)。

## 六个主要参考项目

| 项目与官方来源 | 已核实能力 | 在本 workflow 中借鉴的方式 | 许可与实用限制 |
|---|---|---|---|
| **napari** · [GitHub](https://github.com/napari/napari) · [Image layer](https://napari.org/stable/howtos/layers/image.html) · [Labels layer](https://napari.org/stable/howtos/layers/labels.html) | 多维图像、标签、点、轨迹与表面图层；二维切片与三维查看；支持 Dask/Zarr 等数组。 | 图像、自动标签、人工修正标签并列；全局低分辨率三维定位后，进入原始分辨率 ROI 与正交切片复核。 | [BSD-3-Clause](https://github.com/napari/napari/blob/main/LICENSE)。官方 stable 文档明确，多尺度渲染主要支持二维，三维仅显示最低分辨率级别；三维显示与多尺度标签不可直接编辑。切片编辑时可用三维笔刷范围，不等于在三维渲染视图绘制。 |
| **OME-Zarr / ome-zarr-py** · [GitHub](https://github.com/ome/ome-zarr-py) · [官方文档](https://ome-zarr.readthedocs.io/en/stable/) · [writer 源码与参数说明](https://github.com/ome/ome-zarr-py/blob/master/ome_zarr/writer.py) | 按 OME NGFF 组织多分辨率生物图像；writer 支持 NumPy/Dask 金字塔、轴、物理尺寸、单位和坐标变换。 | 数据与标签分层保存；通过分块和金字塔降低全量读取压力；显式保留轴顺序、体素间距与单位。 | [BSD-2-Clause](https://github.com/ome/ome-zarr-py/blob/master/LICENSE)。格式不自动产生完整分析 provenance；需自行保存参数、版本、校验和与人工修改记录。NGFF 版本和读取器兼容性需锁定并验证；不能只因目录以 `.zarr` 结尾就认为符合 OME-Zarr。 |
| **BigStitcher** · [GitHub](https://github.com/JaneliaSciComp/BigStitcher) · [官方 ImageJ 文档](https://imagej.net/plugins/bigstitcher/) · [PSF 管理](https://imagej.net/plugins/bigstitcher/psf) | 多块、多角度显微数据配准与融合，交互检查中间步骤；支持多视图重建与 PSF 驱动的反卷积。 | 把拼接拆成预对齐、局部匹配、全局优化、接缝复核、融合；保留项目 XML 与变换，避免只保存最终合成图。 | [GPL-2.0](https://github.com/JaneliaSciComp/BigStitcher/blob/master/LICENSE.txt)。需要真实重叠和可靠信号，不能自动修复缺失采集；反卷积需要匹配光学条件的 PSF。官方 ImageJ 旧迁移文档提示部分页面未重新审核，操作应以锁定版本界面为准。旧 PreibischLab 仓库地址现跳转到 JaneliaSciComp。 |
| **multiview-stitcher** · [GitHub](https://github.com/multiview-stitcher/multiview-stitcher) · [官方文档](https://multiview-stitcher.github.io/multiview-stitcher/) | Python 原生二维/三维配准与分块融合；接入 Dask/Zarr/xarray、napari 等；允许替换配准与融合函数。 | Python 批处理支路；对照 stage metadata 与配准结果的坐标系；将大体数据拼接嵌入可记录参数的脚本。 | [BSD-3-Clause](https://github.com/multiview-stitcher/multiview-stitcher/blob/main/LICENSE)。官方明确当前不支持非刚性变换；数百块以上的全局配准可能变慢；API 正在发展，应锁定版本。它是可组合的拼接组件，不能直接视作 BigStitcher 的所有功能替代。 |
| **Cellpose / Cellpose-SAM** · [GitHub](https://github.com/MouseLand/cellpose) · [3D segmentation](https://github.com/MouseLand/cellpose/blob/main/docs/do3d.rst) · [Distributed Cellpose](https://github.com/MouseLand/cellpose/blob/main/docs/distributed.rst) · [模型说明](https://github.com/MouseLand/cellpose/blob/main/docs/models.rst) | 细胞/细胞核分割、人工反馈训练与三维分割；大体数据可分成重叠块，合并为 Zarr 标签；官方 2026 年 6 月更新提供 `cpsam_v2`、`cpdino`、`cpdino-vitb`。 | 候选标签进入人工复核队列；按真实 z/xy 采样比设置各向异性；大样本先在代表性 ROI 验证，再扩大分块推理。 | [代码 BSD-3-Clause](https://github.com/MouseLand/cellpose/blob/main/LICENSE)。README 注明全部模型在 CC-BY-NC 数据上训练，标注数据也为 CC-BY-NC；训练数据、各权重与第三方骨干条款要分别核对，代码许可不等于所有权重无限商用。默认三维方案在正交二维切片预测后运行三维 dynamics，官方称为 2.5D；不是任意器官或临床通用模型。 |
| **vedo** · [GitHub](https://github.com/marcomusy/vedo) · [官方文档](https://vedo.embl.es/) | 基于 VTK/NumPy 的科学三维呈现；体数据切片、裁剪、体绘制、等值面与网格操作；计算面积、体积，导出网格或场景。 | 用相同物理坐标连接体素、表面和对象表；保存相机、透明度、色标等展示参数，形成可复现的科研图。 | [MIT](https://github.com/marcomusy/vedo/blob/master/LICENSE)。平滑、补洞和简化会改变几何；测量使用经校准的标签或未做展示加工的几何。网格体积解释还需检查封闭性、方向、重复顶点等条件。 |

## 其他执行组件

| 组件 | 实际用途与边界 | 官方来源 |
|---|---|---|
| BioIO | 插件读取显微格式，访问通道与物理尺寸，规范数据轴；普通 TIFF 的缺失尺度仍需采集记录。主包 BSD-3-Clause，插件另行核查。 | [仓库](https://github.com/bioio-devs/bioio) · [官方 API](https://bioio-devs.github.io/bioio/bioio.html) |
| tifffile / NumPy | 首版检查脚本的 TIFF 第一 series 读取、OME XML 解析、数组统计与体素计量基础。当前脚本全量加载，不声称支持任意显微格式或无限大数据。 | [tifffile](https://github.com/cgohlke/tifffile) · [NumPy](https://github.com/numpy/numpy) |
| scikit-image | `regionprops`、连通域、带 spacing 的 `marching_cubes` 与表面积估计。几何指标依赖分割与采样；平滑展示表面不替代计量标签。 | [仓库](https://github.com/scikit-image/scikit-image) · [measure API](https://scikit-image.org/docs/stable/api/skimage.measure.html) |
| pycudadecon | 可选 GPU Richardson–Lucy 去卷积、PSF / OTF、deskew 与仿射变换。需要 NVIDIA CUDA；wrapper 为 MIT，底层组件许可单独适用；本工作台未集成执行。 | [官方仓库](https://github.com/tlambert03/pycudadecon) |
| Snakemake | 可选批处理依赖、环境与运行报告。科研核心先以普通 Python CLI 开始；Windows 批处理路线参考官方 WSL 安装方式。MIT。 | [仓库](https://github.com/snakemake/snakemake) · [安装](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) · [报告](https://snakemake.readthedocs.io/en/stable/snakefiles/reporting.html) |

## 大数据扩展与资源规划

[BigStitcher-Spark](https://github.com/JaneliaSciComp/BigStitcher-Spark) 是 BigStitcher 的扩展：把重采样、兴趣点检测、匹配、求解和融合等步骤分布到工作站或集群；每一步结果可以重新打开 XML 进行交互检查。GUI 与 Spark 的功能不完全相同。其仓库同时包含 [BSD 两条许可](https://github.com/JaneliaSciComp/BigStitcher-Spark/blob/main/LICENSE) 与 [GPL-2.0 文件](https://github.com/JaneliaSciComp/BigStitcher-Spark/blob/main/LICENSE.txt)，组合使用或再分发时要按对应组件核对。

没有一个固定显存数字能覆盖本工作流。块大小、重叠、通道数、位深、并发与三维范围都会改变内存需求。Cellpose README 给出的系统 RAM 起点为 8 GB，大图及三维体数据可能需要 16–32 GB；这不是所有数据的容量保证。GPU 可提高分割速度。其分布式模块目前要求 Zarr 输入与 Python API，不能把 GUI 或浏览器演示当成已经提供该能力。

## 我们的组合设计与能力边界

以下是本项目提出的组合设计，并非上游仓库已经统一实现的产品承诺：

1. **全局三维 + ROI 原始分辨率检查**：全局定位与局部校验采用不同读取预算，保留从表面返回原始切片的路径。
2. **QC 决定后续节点**：元数据缺失、配准异常、低对比区域及块边界冲突进入复核；阈值需要用实际样本校准。
3. **标签负责测量，网格负责表达**：展示简化不覆盖测量依据，避免好看的表面改变定量结论。
4. **证据包与版本卡**：记录数据校验和、软件与模型版本、物理单位、参数、变换、人工编辑及复核状态。

本路线关注真实采集体数据。单张普通照片生成三维资产、生成式补全和合成演示，不作为实验测量证据。肿瘤细胞及微环境示例属于研究计划，空间邻近或标记共现不能直接推出相互作用、机制或治疗因果。没有真实样本与验证时，不宣称已获得科研发现或临床结论。
