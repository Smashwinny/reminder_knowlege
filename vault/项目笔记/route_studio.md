---
tags: [项目笔记, 坐标契约, 离线组件测试]
学习审核日期: 2026-10-05
上游仓库: https://github.com/yinsuecci/mockrunning
固定版本: 137297d7ca980f92a6a832708c9c61964bde7591
验证范围: TEST_ONLY合成输入；真实gpx与motion模块
分发范围: 自写练习与来源链接；不再分发上游源码
---

# Route Studio：合成坐标、输入契约与显式状态推进

## 是什么，能学到什么

本页整理 Route Studio 固定版的路线数据工程学习：读取 GPX、核对坐标和设置、计算球面距离、按显式时间增量推进内存状态。实际学习对象是上游真实 gpx.py / motion.py 的有限离线行为，界面、服务与设备能力没有在本实验验收。

可以借此学会：沿字段核对经纬度顺序；区分解析、范围和路线业务校验；给角度、米、秒、瓦片与像素标明单位；对照预期拒绝与实际错误；把逻辑状态和外部观测分别取证。所有可接受路线都是原点附近三个自写 TEST_ONLY 点，GPX 没有活动时间戳；这里只形成软件测试摘要，不是实际活动或设备位置记录。

## 与已有知识的合并

- [[Web墨卡托与瓦片金字塔]]：追加历史单位勘误，以及投影、球面距离、经纬度分量插值的区别，不抹掉旧文本和来源
- [[GPS朝向融合]]：追加旧阈值属于 Deadrun 实现、罗盘可用性不能无条件保证的边界说明；没有重新测传感器或 Deadrun
- [[Agent输出协议契约]]：追加 GPX 解析、路线点集和 Settings.parse 的不同校验入口；坐标顺序与有限值留作具体案例，不另建同义“输入有效性”概念
- [[接缝与桩实现StubSeam]]：追加真实纯模块与未启动控制器的边界；避免把惰性设备工厂误当成整个构造过程无副作用的证明
- [[纯函数游戏引擎与种子复放]]、[[确定性脚本]]、[[双时钟模型]]：复用显式输入和逻辑时间的测试思路；Motion 是会更新自身状态的对象，不能称为纯函数，也不能把逻辑 dt 当真实等待时间
- [[事实与判断分离]]、[[产物留痕与状态外置]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]]、[[确定性快进与真渲染取证]]：字节、脚本结果、界面和真实观测分别验收
- [[共享状态与Reducer]]、[[可逆派生状态]]、[[工具调用生命周期]]：提供状态和调用分层背景，本模块不因此具备 LangGraph Reducer、任务终态判断或 MCP 工具循环
- [[开源验货三查]]：公开源码与再分发依据分开核对；固定快照未发现 LICENSE/COPYING 或项目许可字段，练习包只含自写材料和来源定位

[[项目笔记/deadrun]] 提供地图与无头状态测试背景；[[项目笔记/codex_advanced]]、[[项目笔记/patchright_enhanced]]、[[项目笔记/nce_reading]] 分别提供独立契约验证、惰性依赖和受控组件接线的范围对照。旧项目的数量、版本、权限、设备或平台成绩不迁移到 Route Studio。

## 已有六步实验与计数

历史环境为 Bash、Python 3.12.14、Git 2.52.0，没有安装依赖。教材六步是解包与工具核对、固定源码获取、运行纯模块实验、查看几何与状态结果、同输入重跑并比较、检查边界与源码清洁度。公开源码取得阶段需要网络；被测实验路径本身没有网络或设备操作。此次公开整理只复核已有文件和日志，没有重新运行实验或上游脚本。

历史结果为 71 条检查断言匹配，6 个程序步骤通过，禁止 I/O 尝试记录为 0。71 包含版本、输入标识、源码指纹、模块/边界检查及行为断言，不能写成 71 个上游官方测试或全功能覆盖；历史独立重放同一集合也不增加独立用例数。

- GPX 组包含 6 个预期拒绝输入；路线校验组包含 8 个预期拒绝输入，两组入口与前提不同
- 设置组借用了上游 tests/test_motion.py 的 7 个无效设置向量，通过自写 harness 调用；没有导入上游测试模块或运行全量 pytest
- 所有 Motion 执行的速度波动和横向波动均为 0；没有实验调节轨迹拟真程度
- 只加载包入口、gpx、motion 三个上游模块；指纹前后不变。进程内导入/audit 守卫不是操作系统级网络沙箱
- 历史独立审核从最终 ZIP 的全新目录按六步命令重放。命令输出和文件核对证明所列有限行为，不证明真实活动、GPS 精度或整套应用可用

## 核心观察与坑

1. **解析器和业务校验器不是同一道门。** 独立 load_points 读取 trkpt，单点能解析；route_points 要求路线点集满足进一步条件，所以同一单点被拒。独立 GPX 入口不支持 rtept；Web 的回退路径只作源码观察，不能用来改写独立解析器的实测结果
2. **名字和单位须沿接口核对。** GPX 属性为 lat/lon，路线对象使用 lat/lng，Point 字段为 latitude/longitude。数值在范围内不证明顺序正确。GeoJSON 的经度、纬度顺序只属于其格式，不能自动套用其他 Python 对象
3. **非有限数和退化路线要分开。** NaN、无穷、超范围值作为拒绝哨兵；空/单点/重复或过短路线、10001 点等按已有用例被拒。纬度边界 ±85、恰好 10000 点及所有非法类型并未逐一实测，不能称为全边界覆盖
4. **距离与插值不是同一种算法。** 固定 gpx.py 使用半径 6371000 米的球面大圆近似；原点附近相邻千分之一经度的历史结果约 111.194926645 米，两段约 222.389853289 米。interpolate 对经纬度分量线性插值并将 fraction 钳在 0–1；不是椭球测地线插值或实测路程精度
5. **状态推进只覆盖显式输入。** 历史检查观察到非循环到端点钳制、中间零长度段跳过、循环计数与剩余距离，以及相同 dt 序列下的重复结果一致。读取状态不推进，不等于控制器暂停/恢复已验证；dt 只传有限非负值，不能宣称 advance 自行拦截所有坏输入
6. **PASS 不抹掉层次差异。** Motion 构造及 advance 不承担全部前置校验；练习先用 route_points 与 Settings.parse 检查输入。七个借用的设置反例、六步程序、断言数和来源指纹是不同统计口径，不累加成更大的成绩

## 仅静态观察：控制器、发送状态与清理

已有源码审核指出，PlaybackController 构造会安排后台线程和设备发现；传入 FakeDevice 工厂并不能证明这些路径停止。因此实验没有导入 CLI/Web/PlaybackController，没有创建该控制器。纯模块检查不支持控制器暂停、取消、清理、持久化、发现、竞态或异常恢复的运行结论。

固定控制器里的 current 是最近成功发送的模拟坐标，不是设备读回或现实运动的证据；本实验连发送环节也没有执行。生成数值、调用接口、接收方收到和外部真实呈现要分层证明，关联 [[证据状态机]]、[[证据优先质检ProofOverClaims]]。这里记录的是既有源码观察，没有增加设备调用或操作步骤。

## 既有知识勘误：瓦片与像素

旧 [[Web墨卡托与瓦片金字塔]] 将 zoom 17 的 131072 误写为每轴像素数。应区分：每轴 2^17=131072 张瓦片；在每瓦片边长 256 像素的前提下，每轴为 256×2^17=33554432 像素。原公式乘 2^z 输出瓦片坐标；像素坐标还需乘实际瓦片边长。256 是本算例条件，不是所有服务永远固定的值。

投影平面坐标、地表距离和经纬度线性插值分别命名；球面近似结果不能升级为真实路线精度。该勘误已在原学习材料中提出，此次追加到最新笔记，保留全部历史正文；没有重新进行地图服务器或真机测量。

## 未验证范围与分发边界

没有真实手机、ADB/iOS/模拟器、设备发现、定位发送、传感器数据、真实活动导出、校园服务或规则规避测试。没有 Web/CLI 启动、浏览器地图、交互、HTML 视觉、完整构建、上游完整测试、GPS 精度、全输入安全或跨平台验证。未连接环节保持未测，禁止 I/O 尝试为 0 也不等于全面安全证明。

固定快照没有 LICENSE/COPYING，pyproject.toml 没有项目许可字段；不据此推导再分发或商业许可，也不作独立法律结论。练习 ZIP 五个成员为自写 README、TEST_ONLY_fixture.gpx、run_offline.py、inspect_result.py、source-manifest.json；不含上游源码或测试模块，来源保留固定链接。

原彩色 PDF 由 ReportLab 直接生成，共 13 页，历史审核逐页查看渲染图片；HTML 仅结构核查，没有浏览器或 HTML→PDF 验收。本次公开副本检查另见审核日志。图示不是设备截图，学习材料完成也不表示读者已经掌握全部内容。

## 最新公开知识读取范围

此次合并基于 GitHub main 快照 808f3bff6d1879948598b632ee0c43ce118cebe1。通过连接器读取并核对完整 UTF-8 字节、Git blob SHA 与 SHA-256：MOC、学习方法、仓库说明、两份模板、上方列出的 16 篇概念及 4 篇项目，共 25 份正文。与刚完成公开整理的内容相同者，按精确字节一致复用已完成正文阅读，不把元数据当正文。

快照共有 306 篇概念、108 篇项目笔记；其余 290 篇概念、104 篇项目只做路径/标题筛查，没有全文阅读。命名筛查覆盖 RouteStudio、Route Studio、route_studio、route-studio、mockrunning、路线/路線、坐标/座標、经纬度、CRS、GPX、投影、插值和状态等。结论限于该公开快照及实际已读范围，不声称全库正文无重复、其他设备副本已核对或“从未学过”。

本次新增项目笔记、向四篇已有概念追加案例/勘误、在 MOC 增加入口，不新建概念，不重写历史累计计数或既有正文。原学习的 394 条公开元数据、17 篇正文和 377 篇未读正文范围，仍作为历史阶段单独说明。

## 六份配套材料

- [彩色 PDF 指南](../../route_studio/delivery/route-studio-guide.pdf)
- [HTML 指南](../../route_studio/delivery/route-studio-guide.html)
- [TEST_ONLY 练习包](../../route_studio/delivery/route-studio-exercise.zip)
- [历史实验日志](../../route_studio/delivery/route-studio-experiment-log.md)
- [学习笔记](../../route_studio/delivery/route-studio-learning-notes.md)
- [发布审核及历史证据复核](../../route_studio/delivery/route-studio-review-log.md)

## 固定来源与已有参考

- [GPX、距离与插值](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/gpx.py)、[路线、设置与状态](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/motion.py)
- [控制器，仅静态观察](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/playback.py)、[Web 解析，仅静态观察](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/web.py)
- [七个设置反例来源，未运行测试模块](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/tests/test_motion.py)、[包元数据](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/pyproject.toml)
- [MapTiler 坐标、瓦片与像素说明](https://docs.maptiler.com/google-maps-coordinates-tile-bounds-projection/)
- [PROJ Web Mercator](https://proj.org/en/stable/operations/projections/webmerc.html)、[PROJ 测地计算](https://proj.org/en/stable/geodesic.html)
- [RFC 7946 GeoJSON 坐标顺序](https://www.rfc-editor.org/rfc/rfc7946)

返回 [[00-总览|知识库总览]]。
