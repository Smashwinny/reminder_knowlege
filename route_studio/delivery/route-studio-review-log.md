# Route Studio 独立审核与公开副本检查

历史实验与独立复跑日期：2026-10-05 UTC。公开副本审核日期：2026-10-06 UTC。

结论：通过本次限定范围的内容、历史证据、公开副本和知识合并检查。没有重跑实验、生成新样例、执行获取源码的 Git 命令、导入上游模块或连接设备。原历史结果仍是 71 条检查断言匹配，不是 71 个上游测试、整套产品通过或真实活动证明。

## 1. 独立性和本次实际检查

本次审查者没有编写或改动作者的前五份公开交付物，也没有编写知识库候选正文；只编写本审核日志。检查绑定最终文件字节，覆盖历史命令、日志、结果、固定源码、归档成员、来源归属、文字与链接，并实际查看最终 PDF 全部 13 页。

本次读取并比较原实验结果、原作者两次解包结果和历史独立审核两次结果，共五份已保存的 JSON。它们逐字节相同，均为 3400 字节，SHA-256 9d1e65b924fdd25ab9e435d1e5c96969ccbdaa78df5c7cbe4ef96934525249ca，记录 status=passed、6 个内部步骤、71 条断言。这个比对不增加新的运行次数或独立用例。

以下六步为 2026-10-05 历史独立审核的实际记录。每步当时使用 Bash 的 -euo pipefail，退出码均为 0；第 2 步有正常公开 Git 获取输出，其余步骤 stderr 为空。时间与耗时保留历史主机记录，不是本次审核的新执行时间。

## 2. 当前公开文件与历史来源指纹

以下五份为本次实际检查的公开副本。本审核日志是第六份，其最终指纹由配套发布清单记录，不在正文中制造自指哈希。
- route-studio-guide.pdf：54241 字节；SHA-256 eca2fb2c0d6fa49b78c69ba6452dcb66822802ad17ea2ea7f3d2403cbb820d9e
- route-studio-guide.html：42589 字节；SHA-256 cd065ade82c26d92acae0b16af36628f0019608f57f3bb5197e9d37f70dbe691
- route-studio-exercise.zip：9487 字节；SHA-256 936d9fa4de6478d85435abfc8efbe594cf84e734c29aef14da54785d763c49e1
- route-studio-experiment-log.md：12875 字节；SHA-256 724c9d55924ac29bcf0f5fa7d19d53b3b865cfcdddbaf5d7b720d3aadeddce6c
- route-studio-learning-notes.md：17152 字节；SHA-256 7428794019b879cd5e6b34988b999f0a856a04c801c69e2d49adb90d5d42051b

六份公开交付物的原始字节合计低于 1,000,000 字节；不采用额外压缩后的大小替代。历史六份原始文件总计 151280 字节，以下原始指纹用于来源对照，不冒充当前公开文件的指纹。
- route-studio-guide.pdf：历史原始 54260 字节；SHA-256 1b9778e2b01ea0620f36cedd8e95c115b0c8411f91b0d98672144ca785e38b06
- route-studio-guide.html：历史原始 42546 字节；SHA-256 06c7244701efb458e064d953ecd49ee1e438c1362801b3f7c6d37d67d7d10a13
- route-studio-exercise.zip：历史原始 9236 字节；SHA-256 a74313e2c273d27dbcc9a2598920703111b56042c8bff9a059e0e1e5e8cae1e3
- route-studio-experiment-log.md：历史原始 12024 字节；SHA-256 3a8a33479a46a748ef27dff92e354c64cf9d22f8c3d95923332b1242eda5a399
- route-studio-learning-notes.md：历史原始 17386 字节；SHA-256 ad888797dfa25020c3e23f9460bf5cfc8823d21cbdbaaf35267d014012f1c154
- route-studio-review-log.md：历史原始 15828 字节；SHA-256 5264364d4e6aff6729745eab297eafad5e771643b44e10cb25744c2e012111fa

## 3. 2026-10-05 六步独立复跑记录

### 第 1 步

开始：2026-10-05T11:23:01.118713+00:00；耗时：0.038 秒；退出码：0

```bash
python3 -I -B -m zipfile -e route-studio-exercise.zip route-studio-lab
cd route-studio-lab
python3 --version
git --version
```

标准输出：

```text
Python 3.12.14
git version 2.52.0
```

标准错误：

```text
(empty)
```

### 第 2 步

开始：2026-10-05T11:23:01.156701+00:00；耗时：4.621 秒；退出码：0

```bash
git init --quiet source
git -C source remote add origin https://github.com/yinsuecci/mockrunning.git
git -C source fetch --depth 1 origin \
  137297d7ca980f92a6a832708c9c61964bde7591
git -C source checkout --quiet --detach FETCH_HEAD
git -C source rev-parse HEAD
```

标准输出：

```text
137297d7ca980f92a6a832708c9c61964bde7591
```

标准错误：

```text
From https://github.com/yinsuecci/mockrunning
 * branch            137297d7ca980f92a6a832708c9c61964bde7591 -> FETCH_HEAD
```

### 第 3 步

开始：2026-10-05T11:23:05.778139+00:00；耗时：0.056 秒；退出码：0

```bash
python3 -I -B exercise/run_offline.py \
  --repo source --output first.json
```

标准输出：

```text
{"status": "passed", "steps": 6, "assertions": 71, "failure": null}
```

标准错误：

```text
(empty)
```

### 第 4 步

开始：2026-10-05T11:23:05.834783+00:00；耗时：0.030 秒；退出码：0

```bash
python3 -I -B inspect_result.py metrics first.json
```

标准输出：

```text
STATUS: passed
ASSERTIONS: 71
{"gpx_rejection_cases": 6, "name": "Compare parser and route-validation contracts", "route_rejection_cases": 8, "singleton_parser_accepts_route_validator_rejects": true, "standalone_parser_rejects_rtept": true, "status": "passed", "step": 2}
{"interpolation_cases": 5, "name": "Verify distance and interpolation", "status": "passed", "step": 3, "synthetic_segment_m": 111.19492664455875, "synthetic_total_m": 222.3898532891175}
{"name": "Replay seven upstream-derived validation cases", "status": "passed", "step": 4, "upstream_cases_adapted": 7, "upstream_test_modules_executed": 0, "variations_zero": true}
{"controlled_speed_comparison": [{"logical_dt_s": 10, "synthetic_distance_m": 10.0, "synthetic_point": {"lat": 0.0, "lng": 8.993216059187304e-05}, "test_speed_kmh": 3.6}, {"logical_dt_s": 10, "synthetic_distance_m": 20.0, "synthetic_point": {"lat": 0.0, "lng": 0.0001798643211837461}, "test_speed_kmh": 7.2}], "controller_pause_resume_tested": false, "loop_counter": 2, "name": "Verify explicit motion state transitions", "nonloop_endpoint_clamped": true, "state_trace": {"endpoint_distance_m": 222.3898532891175, "endpoint_synthetic_point": {"lat": 0.0, "lng": 0.002}, "loop_residual_m": 55.597463322279395, "midpoint_distance_m": 111.19492664455875, "midpoint_synthetic_point": {"lat": 0.0, "lng": 0.001}}, "status": "passed", "step": 5}
```

标准错误：

```text
(empty)
```

### 第 5 步

开始：2026-10-05T11:23:05.865247+00:00；耗时：0.099 秒；退出码：0

```bash
python3 -I -B exercise/run_offline.py \
  --repo source --output second.json
python3 -I -B inspect_result.py compare first.json second.json
```

标准输出：

```text
{"status": "passed", "steps": 6, "assertions": 71, "failure": null}
REPLAY_IDENTICAL: true
```

标准错误：

```text
(empty)
```

### 第 6 步

开始：2026-10-05T11:23:05.964819+00:00；耗时：0.042 秒；退出码：0

```bash
python3 -I -B inspect_result.py boundary first.json
git -C source status --porcelain --untracked-files=all
```

标准输出：

```text
PROJECT_MODULES: ios_location_controller, ios_location_controller.gpx, ios_location_controller.motion
FORBIDDEN_IO_ATTEMPTS: 0
SOURCE_UNCHANGED: true
DEVICE_OBSERVATION: false
GUARD: process-local audit/import guard, not OS sandbox
```

标准错误：

```text
(empty)
```

## 4. 历史结果与反例口径

2026-10-05 历史最终两次运行均为 status=passed、6 个内部步骤、71 项断言，JSON 字段与字节均相同，并且与实验作者的最终结果一致。结果 SHA-256：9d1e65b924fdd25ab9e435d1e5c96969ccbdaa78df5c7cbe4ef96934525249ca。

71 是断言总数，不是 71 个测试函数；以下反例是其中的组成部分，不能再次累加：

- GPX 拒绝 6 组：空文档、只有 rtept、NaN 纬度、无穷经度、纬度 91、经度 181
- route_points 拒绝 8 组：非列表、空列表、单点、整条重复点、总长不足 0.1 米、NaN 纬度、无穷经度、10001 个节点
- Settings.parse 拒绝 7 组：速度 0、NaN 间隔、负横向值、速度波动 81、字符串 loop、非整数种子、未知字段。这些只是从上游测试改写的参数覆盖，上游测试模块执行数为 0
- 插值核对 5 个 fraction：-1、0、0.5、1、2；覆盖端点、截断与数值中点
- 距离检查包含同点、对称与两段相加。段长 111.19492664455875 米，总长 222.3898532891175 米
- 状态检查覆盖初始值、零推进、路段中点、非循环终点限制、重复节点形成的零长段跳过、循环圈数与余量、6 次相同逻辑步进的确定性对照
- 两种零波动速度各推进 10 逻辑秒：3.6 km/h 得 10 米，7.2 km/h 得 20 米；推进 2.25 圈得到 2 个整圈及 55.597463322279395 米余量

所有接受的路线节点均由原点附近的 TEST_ONLY 样本构造；越界数字只是拒绝哨兵，没有成为路线。GPX 无活动时间戳，运行输出只是测试摘要，没有活动 GPX 导出。仅加载 ios_location_controller、ios_location_controller.gpx、ios_location_controller.motion；禁用 I/O 尝试记录为 0；正常获取的上游工作区前后均清洁。

没有运行的检查：route_points 纬度正负 85 度边界、恰好 10000 节点接受、Web GPX 文本大小/实体过滤/rtept 回退、完整 CLI、控制器暂停恢复/持久化/清理/取消竞态、任何设备及浏览器效果。load_points 的正负 90 度与 route_points 正负 85 度的差异已核对源码，未把所有边界写成运行通过。没有宣称上述缺口被修复。

## 5. 固定源码、许可发现与归档边界

上游固定为 [yinsuecci/mockrunning@137297d7ca980f92a6a832708c9c61964bde7591](https://github.com/yinsuecci/mockrunning/tree/137297d7ca980f92a6a832708c9c61964bde7591)。本次通过只读 Git 对象核对已存在的固定源码，并将八份固定来源的完整公开读取字节与该历史源码逐项比较，全部一致。没有运行这些模块、上游测试或启动器。历史实际加载的三个模块及设置反例来源指纹如下；最后一项只读过，未作为测试模块执行。

- [src/ios_location_controller/__init__.py](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/__init__.py)：66 字节；SHA-256 17b0bb01dc54f5c4d0ec16a7191aa50aeaf3c0123b76495d708f243c8e776630
- [src/ios_location_controller/gpx.py](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/gpx.py)：2498 字节；SHA-256 5eeb6740526cceb54fc51b27e61efff5921044d57e8795558190d8004259f98a
- [src/ios_location_controller/motion.py](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/src/ios_location_controller/motion.py)：3800 字节；SHA-256 69a5f59b42616bb65b6ef4f57937bcedaa70ad09256f8a757fa8fc7223828297
- [tests/test_motion.py](https://github.com/yinsuecci/mockrunning/blob/137297d7ca980f92a6a832708c9c61964bde7591/tests/test_motion.py)：1739 字节；SHA-256 0fa820697095aad245629d56a24a8852578a6be1123bb330b3c5ab143f69588e

固定树内没有 LICENSE、COPYING 或 NOTICE 文件，pyproject.toml 没有项目许可字段。这里只报告固定材料的发现，不推导再分发或商业许可，也不作独立法律结论。公开 ZIP 不含上游源代码、上游测试模块或设备启动器；需要的源码仍由读者按原固定 Git 命令另行取得。

公开 ZIP 有且只有五个唯一成员：README.md、exercise/TEST_ONLY_fixture.gpx、exercise/run_offline.py、inspect_result.py、source-manifest.json。CRC 检查无错误，无绝对路径、父目录逃逸或符号链接。与历史 ZIP 相比只有 README 增加公开副本说明；其余四个成员逐字节不变。来源清单中的自建运行器、fixture 与检查器指纹全部匹配。

fixture 仍为原点附近三个合成节点：纬度均为 0，经度依次为 0、0.001、0.002；XML 没有 time 元素，明确标记 TEST_ONLY。高幅值或非有限数字仅作为拒绝哨兵，未变成接受的路线。运行器只写测试摘要，既不输出活动轨迹，也不构造个人位置或运动证据。

六步命令在 PDF、HTML、ZIP README 与实验日志中完全一致。实验日志的所有历史代码块保持原样，保留命令、stdout、stderr、退出码、时间与耗时。公开 ZIP 的当前大小和哈希另列，未把历史结果说成当前重新执行。

静态源码也支持范围划分：PlaybackController 构造会启动线程，线程安排设备发现；替换设备工厂不足以证明没有外部副作用。current 是最近成功发送的模拟坐标，本实验没有执行发送。Motion 更新自身状态，不能称为无状态纯函数；自建检查先验证路线和设置，只传有限非负 dt。进程内导入/audit 防护不是操作系统沙箱或对任意未知代码的安全保证。

## 6. 最终 PDF 逐页与 HTML 结构检查

当前 PDF 由 ReportLab 直接生成，为 13 页 A4。审查者独立将该精确文件用 pdftoppm 渲染为 110 DPI PNG，实际逐页查看第 1 至 13 页，没有仅凭页数或提取文本判断版面。

- 第 1 页：范围、历史日期、未复跑声明、十二问目录和许可边界清楚
- 第 2 至 4 页：分层、GPX 入口、坐标单位、验证门槛、距离与插值图文完整
- 第 5 至 7 页：逻辑 dt、终点与循环、控制器副作用、发送与观测、状态清理边界可读
- 第 8 页：五项能力与五个用途完整，静态观察和运行结果分开
- 第 9 至 11 页：六步命令、历史结果与时间完整，没有命令截断
- 第 12 页：71 条断言口径、未测项、公开知识范围与瓦片勘误一致
- 第 13 页：固定来源、标准适用范围与交付限制完整，长链接没有越界

全部页未见遮挡、裁切、缺字方框、损坏图示或页码错误。PDF 无 JavaScript、表单或附加文件；元数据和提取文本未发现环境专属路径。Poppler 的字体缓存不可写警告不影响成功渲染与实际图像检查，未为此改变系统设置。

HTML 静态检查通过：12 个递进问题、12 个可解析且带标题的内联 SVG、6 个步骤、6 组命令、12 个目录锚点，无重复 id 或无效内部锚点。没有脚本、表单或外部加载资源，中文 lang、UTF-8 和 viewport 保留。HTML 浏览器视觉与 HTML 转 PDF 原路线受环境限制，本次未重试；直接 PDF 检查不替代这两项验收。

## 7. 最新公开知识合并与历史保留

本次候选基于 main 的 808f3bff6d1879948598b632ee0c43ce118cebe1，树为 b71381b82b0d0765cd5e020f1c33a17c28272101。完整读取并核对 MOC、学习方法、仓库说明、两份模板、16 篇概念及 4 篇项目，共 25 份正文；字节数、SHA-256 与基线 Git blob 一致。相同历史内容的语义阅读按精确字节一致复用，不把元数据当全文。

基线有 306 篇概念、108 篇项目；其余 290 篇概念、104 篇项目只筛查路径和标题，未宣称全库全文查重。原学习的 394 条公开元数据、17 篇实际公开正文及 377 篇未读正文属于较早阶段，保留为独立历史口径。

候选只涉及六份知识文件：新增 route_studio 项目；向 Agent输出协议契约、GPS朝向融合、Web墨卡托与瓦片金字塔、接缝与桩实现StubSeam 四篇已有概念追加案例或勘误；在 MOC 增加领域入口和项目行。没有新建同义概念。审查发现项目六步摘要的第 4 至 6 步描述不够准确，作者已改成与原始命令一致的顺序，重新固定该文件后复核。

四篇概念的全部旧字节仍为新文件前缀；MOC 恰有两块插入，没有替换或删除。去掉追加/插入可精确恢复每份旧文件的字节、长度与 SHA-256。既有历史标签、累计计数、项目索引与无关工具文件保持原样。新加双链唯一解析到实际基线或候选条目，配套材料相对链接指向这组六份文件。

瓦片勘误保留旧文并追加解释：zoom 17 的每轴瓦片数为 131072；若每瓦片边长 256 像素，每轴像素数为 33554432。该算例是原材料已有勘误，[MapTiler 文档](https://docs.maptiler.com/google-maps-coordinates-tile-bounds-projection/) 的坐标与瓦片说明支持单位区分。纬经度、投影米、像素与瓦片不可互换，256 是条件而非所有服务的固定值。

对 [RFC 7946](https://www.rfc-editor.org/rfc/rfc7946) 与 [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) 的既有引用作了限定核对：GeoJSON 顺序不替代 Route Studio 具名字段的契约；JSON 数字语法与运行时有限值检查也分别说明。GPS 旧阈值留在原 Deadrun 实现范围，罗盘可用性与显示回退不冒充测量事实。没有把本次阅读标准写成设备或地图实验。

## 8. 公开内容边界与最终结论

检查覆盖六份公开交付文本、PDF 提取文本和元数据、ZIP 全部成员及知识文件新增内容。未发现非公开账号或对象标识、环境专属路径、私人知识原文、凭证、私人位置或真实活动记录。已经公开的旧知识正文按原字节保留；新增内容没有带入其历史背景标识。

全部材料保留 TEST_ONLY 和历史日期，明确软件数值、发送调用、设备读回与现实运动需要不同证据。没有新增源码执行、controller 构造、设备发现、Web/CLI、网络实验、手机定位、运动或传感器输出，没有生成真实活动证明或提供规避验证的流程。

本审核只确认上述精确候选的内容、证据、归档、视觉、结构与知识合并通过，不表示全功能、GPS 精度、真机、浏览器或所有输入安全已验收。Git 发布成功与否须以随后实际发布和回读另行确认，不能由本日志推断。
