# RouteStudio 坐标契约与合成组件知识笔记

历史学习日期：2026-10-05 UTC。本文保留固定来源、公开知识关联、历史合成组件结果和未测边界。本次公开整理未重跑实验，未生成样例，未执行源码获取或设备链。

## 1. 查重范围与真正新增之处

固定公开索引含 394 条元数据，本轮实际全文读取并核验 17 篇相关公开概念/项目笔记，其余 377 篇仅元数据检索。公开索引固定于 Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352；相关公开正文固定于 1043e9d6080bff7af9724162e2c44559fab63e40。

历史公开索引与已读公开正文的名称查重覆盖 RouteStudio、Route Studio、route_studio、route-studio 及简繁体路线工作室/路线演播室，未找到同名项目。已有 [[deadrun]]，且包含 [[GPS朝向融合]]、[[Web墨卡托与瓦片金字塔]]、[[纯函数游戏引擎与种子复放]]。因此本轮重点应是路线数据的单位与边界契约、真实核心代码的合成回放和状态清理，不重复 GPS 游戏教学。

这个结论只针对历史快照的实际阅读范围，不覆盖其他版本和 377 篇未读正文；不能写成“全库无重复”或“从未学过”。笔记存在也不表示读者已经掌握。

## 2. 优先修正：瓦片数与像素数的单位错误

已有 [[Web墨卡托与瓦片金字塔]] 在固定版本中将 zoom 17 对应的 131072 误写成世界每轴像素数。应保留历史来源并增加如下勘误，不抹掉版本记录：

- 每轴瓦片数：2^17 = 131072
- 在每瓦片 256 像素的前提下，世界每轴像素数：256 × 2^17 = 33554432
- 原笔记 x=(lng+180)/360×2^z 与 y=(0.5−ln((1+sinφ)/(1−sinφ))/4π)×2^z 输出瓦片坐标；像素坐标需再乘瓦片边长。三角函数内的 φ 使用弧度；经纬度输入的单位转换须显式说明

领域：地图渲染、量纲检查。该算术已独立执行；不同瓦片边长应代入实际值，不能将 256 写成所有服务的固定事实。[MapTiler 官方说明](https://docs.maptiler.com/google-maps-coordinates-tile-bounds-projection/) 区分经纬度、投影米、缩放级别像素与瓦片坐标，栅格瓦片常见 256 或 512 像素。

旧笔记依据：[Web墨卡托与瓦片金字塔，固定正文](https://github.com/Smashwinny/reminder_knowlege/blob/1043e9d6080bff7af9724162e2c44559fab63e40/vault/概念/Web墨卡托与瓦片金字塔.md)。该正文 UTF-8 1342 字节，SHA-256 290923a4b61c519e793d6ededbbfdbee8c96b7f424d53ea5eec9f11e5619429d。哈希证明读到同一历史文本，不替其中所有断言背书。

## 3. 候选增量：路线坐标必须携带顺序与单位契约

一句话定义：一个坐标值只有同时明确坐标参考系统、分量顺序、单位、有效范围与时间意义，才足以被另一个组件正确解释。

领域：地理信息、接口设计、数据验证。关联 [[Agent输出协议契约]]、[[事实与判断分离]] 与 [[Web墨卡托与瓦片金字塔]]。先在目标知识库查找“坐标契约、经纬度顺序、角度单位、CRS”等同义项，再决定独立成篇或增补旧笔记。

纯合成例子：两个合法数值 10 与 20 交换后仍可能落在经纬度范围内，但代表另一点，所以范围检查不能证明顺序正确。经纬度差值以度计，地图投影坐标可能以米计，屏幕点可能以像素计；不能把它们都放进名为 distance 的字段后直接比较。

[RFC 7946 §3.1.1/§4](https://www.rfc-editor.org/rfc/rfc7946) 规定 GeoJSON 的前两分量为经度、纬度，单位为十进制度。这个规定仅支撑 GeoJSON 契约，不能据此推断 RouteStudio 内部数组、函数参数或其他 API 也用相同顺序。项目顺序仍需沿真实定义、调用点和测试逐一核对。

## 4. 优先增补：投影图形与地表距离分开

一句话定义：把地球位置映射到平面以便显示，与求地表两点之间的距离，是不同数学问题。

领域：地图投影、测地计算。[[Web墨卡托与瓦片金字塔]] 已有投影基础，本轮只补单位与距离边界。[PROJ Web Mercator 文档](https://proj.org/en/stable/operations/projections/webmerc.html) 明确其输入是地理坐标、输出是投影坐标；平面上的线不能自动当成地表测距证据。

[PROJ 测地计算说明](https://proj.org/en/stable/geodesic.html) 区分由起点/方向/距离求终点的正解，和由两点求距离/方向的逆解；球面大圆是扁率为零的特例。球面近似、椭球测地线和经纬度线性插值应分别命名。RFC 7946 也提醒经纬度分量的直线插值可能显著不同于椭球测地路径。

项目里的公式采用何种半径、输入单位、插值规则与退化处理，应以固定代码和日志为准；不能仅因为返回一个数字就说是“精确实际路程”。边界样本可包含同点、空路线、重复点、跨经度边界或接近极区的纯合成数据，实际覆盖多少就报告多少。

## 5. 优先增补：解析、有限值、范围与业务有效性

一句话定义：文本能被解析成数值，不代表它是有限数、落在约定范围内或满足路线处理的业务前提。

领域：数值可靠性、输入契约。优先给 [[Agent输出协议契约]] 增补 RouteStudio 案例，不重建近期 Qwen/Codex 已提出的“解析与有效性分层”同义概念。

[RFC 8259 §6](https://www.rfc-editor.org/rfc/rfc8259#section-6) 不允许 JSON 数字字面量 NaN 与 Infinity；但内存浮点对象、数值计算与实现的转换行为仍可能产生非有限值。严格 JSON 语法检查、运行时有限值检查、经纬度范围检查、非负时间间隔与路线点数要求应分开记录。

测试必须明确拒绝发生在哪层：上游函数自行拒绝、自建消费者策略拒绝，还是后续算术才暴露异常。自建严格校验器不能冒充上游已有能力；发现缺陷的预期行为检查通过，也不表示缺陷已经修好。

## 6. 复用并推进：回放时间、状态转换与清理

一句话定义：一次回放应由显式输入与时间推进决定状态，并在停止、结束或错误后清楚交代待处理工作及资源状态。

领域：可测试性、时序系统、资源生命周期。复用 [[纯函数游戏引擎与种子复放]] 的固定输入思路、[[双时钟模型]] 的时间口径区分、[[产物留痕与状态外置]] 的日志证据；与 [[可逆派生状态]]、[[工具调用生命周期]] 仅作相关互链，不能把这些旧项目的机制当成 RouteStudio 实现。

本轮可增补的具体检查是：同一 TEST_ONLY 输入重复运行是否一致；步进前后索引、状态与时间如何变化；停止或异常后是否继续产生计划输出；重复清理是否产生额外效果。源码阅读、真实函数执行、惰性替身的调用记录与外部资源实际释放应分别标注。

若函数依赖时钟、随机源或设备边界，应注明实际替换的接缝以及哪些代码仍为未改动上游；没有执行的初始化、取消竞态与异常分支保留未测，不保证“所有情况都会自动清理”。

## 7. 优先增补：已发送与已观察不能互相替代

一句话定义：代码生成了坐标、调用了输出接口、接收方确认收到、外部系统实际呈现了结果，是逐层增加证据的不同事实。

领域：集成测试、可观测性。已有 [[接缝与桩实现StubSeam]]、[[证据状态机]] 和 [[证据优先质检ProofOverClaims]] 足够承载这一增量，不另造同义原则。

若离线替身记录收到一组 TEST_ONLY 坐标，只能支持调用参数与顺序的结论；不能写成手机位置已改变、真实设备已运行或真实活动已发生。状态字段叫 running、sent 或 completed 也不能单独证实外部效果。应保留 source/version、输入身份、预期、实际输出和未连接环节。

本轮仅使用本人自写合成样本，不读取私人位置记录，不连接手机，不生成真实活动证明或规避验证的流程。示例中的路线、时间与状态均需保留测试身份。

## 8. GPS 旧概念的适用范围也需修订

[[GPS朝向融合]] 里的约 1.4 m/s 航向切换和 2° 罗盘节流来自 [[deadrun]] 历史实现，不能概括为通用 GPS 规则。航向描述移动方向，朝向描述面向方向，两者不应因同用角度单位而混淆。

旧文“罗盘永远可用”过度概括，应改为“具体平台和测量可用时可作朝向来源；无有效测量时保留缺失/未知状态”。向北的回退图标属于显示策略，不能标成测量值。这里没有重新运行 Deadrun，也没有设备测量证据；保留该项目原有版本和历史实验边界。

## 9. 历史项目证据与复用安排

本轮实际执行版本为 [yinsuecci/mockrunning@137297d7ca980f92a6a832708c9c61964bde7591](https://github.com/yinsuecci/mockrunning/tree/137297d7ca980f92a6a832708c9c61964bde7591)。Python 3.12.14，仅加载包入口与真实 gpx.py、motion.py；未安装依赖，未改动上游源码。原始与全新解包复跑均通过 6 个内部步骤、71 项断言。这里的 71 是断言总数，不代表 71 个独立测试函数；输出保留分步摘要、数值结果与总数。

自建 TEST_ONLY GPX 的 3 点是 (纬度0, 经度0)、(0,0.001)、(0,0.002)，均无时间戳。段长 111.19492664455875 米，总长 222.3898532891175 米。速度与横向波动均为0：3.6 km/h 推进10逻辑秒得到10米，7.2 km/h 得到20米。非循环推进到终点会限制距离；循环推进2.25圈得到2整圈与55.597463322279395米余量。同输入二次运行的 JSON 逐字段一致。

具体契约：gpx.load_points 只收 trkpt、允许单点且纬度范围为正负90度；route_points 要2至10000节点、有限数、正负85度纬度范围和至少0.1米总长。单点解析接受而路线校验拒绝已执行；10001节点拒绝已执行；正负85度边界与10000节点接受仅静态核对。Motion 构造器和 advance 不自行校验全部输入，尤其 dt 必须由调用方保证有限且非负。本实验先验证路线和设置，再给出有限非负 dt。

6组 GPX 反例、8组路线反例、7组改写的上游设置无效输入属于这71项断言的组成部分；不代表运行了上游测试模块或全量 pytest。源码中的 Web GPX 支持、文件限制、控制器暂停恢复、清理、会话保存和设备能力全部为静态阅读。PlaybackController 构造后会启动设备发现线程，因此没有用 FakeDevice 控制器冒充无设备实验。

程序内 audit/import 防护检查禁止的网络、子进程、非摘要写入与设备模块导入，但这不是操作系统沙箱。实验没有浏览器、服务或设备连接，不产生活动轨迹导出、手机观测或现实运动证明。固定提交未发现 LICENSE/COPYING，练习包仅含自建材料、固定版正常 Git 获取命令与哈希清单。所有 learner 命令及退出码、耗时、完整输出见独立实验日志。

复用时先核对目标知识库中的同义概念和已有编辑，保留历史版本与明确勘误，相关内容互链。只有确有独立价值且没有同义项的候选才另建条目。软件结果只支持已运行的纯模块范围，不能代替未运行的设备链验收。

## 10. 本次实际全文核验的公开知识来源

以下条目均固定于 1043e9d6080bff7af9724162e2c44559fab63e40，已核对 UTF-8 字节数与 SHA-256。它们作为已有知识依据，历史项目中的外部主张并未全部重验。

1. [Agent输出协议契约](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Agent%E8%BE%93%E5%87%BA%E5%8D%8F%E8%AE%AE%E5%A5%91%E7%BA%A6.md)
   UTF-8 1742 字节；SHA-256 85b2ef5207651ba4807bd3da205a45c72c1fe38a5cb8ce91a052f66dea5bba4e

2. [GPS朝向融合](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/GPS%E6%9C%9D%E5%90%91%E8%9E%8D%E5%90%88.md)
   UTF-8 1255 字节；SHA-256 dec7a4e24bdebcbf9d8d0d1b5abe097b2fd73dbeee7ac5eec525b85c1d200ba4

3. [Web墨卡托与瓦片金字塔](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Web%E5%A2%A8%E5%8D%A1%E6%89%98%E4%B8%8E%E7%93%A6%E7%89%87%E9%87%91%E5%AD%97%E5%A1%94.md)
   UTF-8 1342 字节；SHA-256 290923a4b61c519e793d6ededbbfdbee8c96b7f424d53ea5eec9f11e5619429d

4. [事实与判断分离](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%8B%E5%AE%9E%E4%B8%8E%E5%88%A4%E6%96%AD%E5%88%86%E7%A6%BB.md)
   UTF-8 1653 字节；SHA-256 53f5643580c0ab2e2860c6d2b25e3ea7eeb80cf806c1fdf4d989cab59319427b

5. [产物留痕与状态外置](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%A7%E7%89%A9%E7%95%99%E7%97%95%E4%B8%8E%E7%8A%B6%E6%80%81%E5%A4%96%E7%BD%AE.md)
   UTF-8 2389 字节；SHA-256 6aba36f09afc580c08a669663e1ddaef6fa2c99067fcfedb65f56ba81a5ecceb

6. [共享状态与Reducer](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%85%B1%E4%BA%AB%E7%8A%B6%E6%80%81%E4%B8%8EReducer.md)
   UTF-8 1438 字节；SHA-256 a09fb5e07eba8ee88fe6c917c45cf04ecda284fb73cf0326a9b9233a8af79da9

7. [双时钟模型](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%8F%8C%E6%97%B6%E9%92%9F%E6%A8%A1%E5%9E%8B.md)
   UTF-8 1677 字节；SHA-256 ab74a0126c149cad5251df1f8863882a0ff262b83472c37fc0c04b746e023b29

8. [可逆派生状态](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%8F%AF%E9%80%86%E6%B4%BE%E7%94%9F%E7%8A%B6%E6%80%81.md)
   UTF-8 2076 字节；SHA-256 f08c023413927f01deab7be39889ea0c8539f1f389b6f25506c9395f72430d37

9. [工具调用生命周期](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F.md)
   UTF-8 1411 字节；SHA-256 9f8e203fdc45687ecf8625edc7fe4fc3c766850385879f97623333710d2c5481

10. [开源验货三查](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%BC%80%E6%BA%90%E9%AA%8C%E8%B4%A7%E4%B8%89%E6%9F%A5.md)
   UTF-8 1815 字节；SHA-256 836585db83f85f393815551357aad9b894567c5e57bc7c4623e088040c50b0ce

11. [接缝与桩实现StubSeam](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A5%E7%BC%9D%E4%B8%8E%E6%A1%A9%E5%AE%9E%E7%8E%B0StubSeam.md)
   UTF-8 1752 字节；SHA-256 83decb2724ea3ac736e0f9c4c89e17e043504be4733162e6ee44d7988c976804

12. [确定性快进与真渲染取证](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%BF%AB%E8%BF%9B%E4%B8%8E%E7%9C%9F%E6%B8%B2%E6%9F%93%E5%8F%96%E8%AF%81.md)
   UTF-8 1902 字节；SHA-256 29854a02e9a9a472da6e921019fae7fbeccf6cb912cfbdb73392a742bb86fcf4

13. [确定性脚本](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%A1%AE%E5%AE%9A%E6%80%A7%E8%84%9A%E6%9C%AC.md)
   UTF-8 976 字节；SHA-256 9c4ad9b95b3ffd67200ea11cd302678eb46057249027ce622bac0f0573cdebae

14. [纯函数游戏引擎与种子复放](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%BA%AF%E5%87%BD%E6%95%B0%E6%B8%B8%E6%88%8F%E5%BC%95%E6%93%8E%E4%B8%8E%E7%A7%8D%E5%AD%90%E5%A4%8D%E6%94%BE.md)
   UTF-8 1308 字节；SHA-256 6416e8d792850128e55cb060625d5ce2103870a74a5197993f74224a417aa4e6

15. [证据优先质检ProofOverClaims](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md)
   UTF-8 3593 字节；SHA-256 c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac

16. [证据状态机](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md)
   UTF-8 2488 字节；SHA-256 4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328

17. [deadrun](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/deadrun.md)
   UTF-8 2253 字节；SHA-256 ba39104b2b6d502fee30f045525913cb4245686eea2c5542a749f8398e9c7c35
