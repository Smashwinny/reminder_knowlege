# Route Studio 合成路线历史实验日志

公开副本说明：本次整理未重跑实验，也未生成样例、执行源码获取或连接任何设备。以下完整命令、stdout、stderr、退出码、时间与耗时均来自 2026-10-05 的历史实测；71 项断言的结果与边界不变。

日期：2026-10-05 UTC。范围：TEST_ONLY 纯模块软件测试，不是活动记录或设备观测。

## 环境和固定版本

- Bash、Python 3.12.14；未安装依赖
- 上游：https://github.com/yinsuecci/mockrunning
- 固定提交：137297d7ca980f92a6a832708c9c61964bde7591
- 只执行上游包入口、gpx.py、motion.py；源码哈希在结果中
- 接受的路线全为自建原点附近3点，GPX无时间戳；非法范围值只用作拒绝哨兵
- 速度波动和横向波动均为0
- 原始实验于11:12:33 UTC通过71项断言；下面记录最终ZIP全新解包后的实际六步
- 第2步读取公开Git需要网络；实验过程没有网络、设备、服务或浏览器

## 历史最终 ZIP 的逐步实际执行

前置条件：下载 ZIP，在其所在目录打开 Bash；route-studio-lab 目标不存在。从第2步起，继续在上一步进入的解包目录。不是 PowerShell 复验结果。

### 第1步 解包并核对工具

目的：建立全新目录；只需 Bash、Python 3.11+、Git 与一次源码获取网络

```bash
python3 -I -B -m zipfile -e route-studio-exercise.zip route-studio-lab
cd route-studio-lab
python3 --version
git --version
```

开始：2026-10-05T11:16:08+00:00；耗时：0.034 秒；退出码：0

实现结果：解包成功；Python 3.12.14 与 Git 可用；不需要 pip 安装。

验证与失败条件：Python 至少 3.11；出现 exercise/run_offline.py 和 TEST_ONLY_fixture.gpx

标准输出：

```text
Python 3.12.14
git version 2.52.0

```

标准错误：

```text
(empty)
```

### 第2步 获取固定版源码

目的：单独获取并固定上游版本，避免默认分支日后变化

```bash
git init --quiet source
git -C source remote add origin https://github.com/yinsuecci/mockrunning.git
git -C source fetch --depth 1 origin \
  137297d7ca980f92a6a832708c9c61964bde7591
git -C source checkout --quiet --detach FETCH_HEAD
git -C source rev-parse HEAD
```

开始：2026-10-05T11:16:08+00:00；耗时：7.026 秒；退出码：0

实现结果：公开 Git 获取成功；HEAD 为指定的完整 40 位提交哈希。

验证与失败条件：HEAD 必须完整等于固定哈希；获取失败就停止，不改为其他版本

标准输出：

```text
137297d7ca980f92a6a832708c9c61964bde7591

```

标准错误：

```text
From https://github.com/yinsuecci/mockrunning
 * branch            137297d7ca980f92a6a832708c9c61964bde7591 -> FETCH_HEAD

```

### 第3步 运行纯模块实验

目的：只运行 gpx 和 motion；所有错误必须触发非零退出码

```bash
python3 -I -B exercise/run_offline.py \
  --repo source --output first.json
```

开始：2026-10-05T11:16:15+00:00；耗时：0.068 秒；退出码：0

实现结果：status=passed，内部步骤6，断言71，failure=null；两个波动参数为0。

验证与失败条件：status=passed，steps=6，断言数匹配本包记录；否则读 failure 后停止

标准输出：

```text
{"status": "passed", "steps": 6, "assertions": 71, "failure": null}

```

标准错误：

```text
(empty)
```

### 第4步 查看几何与状态结果

目的：把通过状态展开成米数、插值、反例和推进状态

```bash
python3 -I -B inspect_result.py metrics first.json
```

开始：2026-10-05T11:16:15+00:00；耗时：0.042 秒；退出码：0

实现结果：段长111.194927米，总长222.389853米；10秒时速度翻倍，距离由10米变20米。

验证与失败条件：段长约111.194927m，总长约222.389853m；零波动速度翻倍后距离翻倍

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

### 第5步 用同一输入重新计算

目的：验证确定性；同版本同输入应产生逐字段一致的 JSON

```bash
python3 -I -B exercise/run_offline.py \
  --repo source --output second.json
python3 -I -B inspect_result.py compare first.json second.json
```

开始：2026-10-05T11:16:15+00:00；耗时：0.103 秒；退出码：0

实现结果：第二次仍为71项断言通过；REPLAY_IDENTICAL: true，两个 JSON 逐字段一致。

验证与失败条件：显示 REPLAY_IDENTICAL: true；任何不同都需要查版本与输入

标准输出：

```text
{"status": "passed", "steps": 6, "assertions": 71, "failure": null}
REPLAY_IDENTICAL: true

```

标准错误：

```text
(empty)
```

### 第6步 检查边界与源码清洁度

目的：确认模块范围、无设备观察、无活动导出、无源码改动

```bash
python3 -I -B inspect_result.py boundary first.json
git -C source status --porcelain --untracked-files=all
```

开始：2026-10-05T11:16:15+00:00；耗时：0.039 秒；退出码：0

实现结果：仅加载允许的三项项目模块；禁止I/O尝试为0；源码未变；Git状态输出为空。

验证与失败条件：仅三项允许的项目模块、禁用 I/O 尝试数为0；Git 状态应为空

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

## 最终原始结果 JSON

结果保留断言总数、每步摘要及数值，并不逐项输出全部断言名称。

```json
{
  "label": "TEST_ONLY_OFFLINE_SOFTWARE_TEST_NOT_ACTIVITY_EVIDENCE",
  "upstream": "https://github.com/yinsuecci/mockrunning",
  "pinned_commit": "137297d7ca980f92a6a832708c9c61964bde7591",
  "python_version": "3.12.14",
  "scope": "Only genuine gpx.py and motion.py, synthetic input near 0,0",
  "activity_timestamps": false,
  "activity_export": false,
  "device_observation": false,
  "steps": [
    {
      "step": 1,
      "name": "Pin source and parse synthetic GPX",
      "status": "passed",
      "parsed_points": 3
    },
    {
      "step": 2,
      "name": "Compare parser and route-validation contracts",
      "status": "passed",
      "gpx_rejection_cases": 6,
      "route_rejection_cases": 8,
      "singleton_parser_accepts_route_validator_rejects": true,
      "standalone_parser_rejects_rtept": true
    },
    {
      "step": 3,
      "name": "Verify distance and interpolation",
      "status": "passed",
      "synthetic_segment_m": 111.19492664455875,
      "synthetic_total_m": 222.3898532891175,
      "interpolation_cases": 5
    },
    {
      "step": 4,
      "name": "Replay seven upstream-derived validation cases",
      "status": "passed",
      "upstream_cases_adapted": 7,
      "upstream_test_modules_executed": 0,
      "variations_zero": true
    },
    {
      "step": 5,
      "name": "Verify explicit motion state transitions",
      "status": "passed",
      "nonloop_endpoint_clamped": true,
      "loop_counter": 2,
      "controller_pause_resume_tested": false,
      "state_trace": {
        "midpoint_distance_m": 111.19492664455875,
        "midpoint_synthetic_point": {
          "lat": 0.0,
          "lng": 0.001
        },
        "endpoint_distance_m": 222.3898532891175,
        "endpoint_synthetic_point": {
          "lat": 0.0,
          "lng": 0.002
        },
        "loop_residual_m": 55.597463322279395
      },
      "controlled_speed_comparison": [
        {
          "test_speed_kmh": 3.6,
          "logical_dt_s": 10,
          "synthetic_distance_m": 10.0,
          "synthetic_point": {
            "lat": 0.0,
            "lng": 8.993216059187304e-05
          }
        },
        {
          "test_speed_kmh": 7.2,
          "logical_dt_s": 10,
          "synthetic_distance_m": 20.0,
          "synthetic_point": {
            "lat": 0.0,
            "lng": 0.0001798643211837461
          }
        }
      ]
    },
    {
      "step": 6,
      "name": "Replay deterministically and verify offline boundary",
      "status": "passed",
      "deterministic_replay_steps": 6,
      "loaded_project_modules": [
        "ios_location_controller",
        "ios_location_controller.gpx",
        "ios_location_controller.motion"
      ],
      "source_unchanged": true,
      "guard_scope": "Process-local audit/import guards, not an OS-level network sandbox",
      "forbidden_io_attempts": 0
    }
  ],
  "assertions": 71,
  "forbidden_io_attempts": [],
  "source_hashes": {
    "src/ios_location_controller/__init__.py": "17b0bb01dc54f5c4d0ec16a7191aa50aeaf3c0123b76495d708f243c8e776630",
    "src/ios_location_controller/gpx.py": "5eeb6740526cceb54fc51b27e61efff5921044d57e8795558190d8004259f98a",
    "src/ios_location_controller/motion.py": "69a5f59b42616bb65b6ef4f57937bcedaa70ad09256f8a757fa8fc7223828297"
  },
  "status": "passed",
  "fixture_sha256": "d713135faf1a47ac6e04de76d28f68d6bfaa05602a5dc2b8e375ec41f6250e5b"
}
```

## 结论与未测范围

本次6个内部步骤通过71项断言。6组GPX反例、8组路线反例、7组改写的上游设置无效输入是71项断言的组成部分；不要把它们重复相加。上游测试模块执行数为0，没有执行全量pytest。

数学结果：段长111.19492664455875米，总长222.3898532891175米；10逻辑秒下3.6km/h为10米，7.2km/h为20米；循环2.25圈得到2圈及55.597463322279395米余量。纯函数/状态通过不能说明现实中经过了这些位置。

静态核对而非运行：gpx纬度±90与route_points纬度±85的契约差异；后者接受10000节点的上限；Web trkpt/rtept、长度限制及XML实体处理；控制器暂停、恢复、清理、持久化、发现；任何设备、平台、浏览器或真实集成效果。10001节点拒绝、单点解析接受而路线拒绝、零长度路线拒绝已运行。

Motion.__init__ 与 advance 不是通用安全入口；本实验先验证路线和设置，dt仅用有限非负值。代码防护是Python进程内audit/import guard，不是操作系统沙箱。没有尝试启动控制器：源码表明即使用FakeDevice也会启动设备发现线程。

## 发行与停止条件

固定提交未发现LICENSE/COPYING。本ZIP只含自建运行器、检查器、TEST_ONLY输入、README与来源哈希清单；没有上游实现。读取者正常获取公开固定源码后才能执行。禁止把其他提交自动当作等价版本。

任何源码哈希不符、Python低于3.11、文件缺失、断言失败、禁止导入/I/O、摘要不可写、结果不一致或Git状态非空，都应停止并保留失败，不得删掉失败记录后声称成功。

没有修改设备设置、写入真实位置或导出活动数据，也没有访问真实活动服务。所有输入均保留 TEST_ONLY 测试身份，软件计算不构成现实活动证明。


## 当前公开副本检查

公开 PDF 由 ReportLab 直接重新生成，并逐页渲染查看。HTML 仅做结构检查；浏览器视觉及 HTML 转 PDF 原路线受环境限制，本次未重试。当前独立审核另见第六份审查日志。ZIP 仅新增 README 公开副本说明；原 TEST_ONLY GPX、运行器、检查器与来源清单均保持原字节。当前处理没有导入或运行项目模块，没有源码获取、网络实验、服务、控制器构造、设备发现或真实活动输出。

当前公开 ZIP：9487 字节；SHA-256 936d9fa4de6478d85435abfc8efbe594cf84e734c29aef14da54785d763c49e1
