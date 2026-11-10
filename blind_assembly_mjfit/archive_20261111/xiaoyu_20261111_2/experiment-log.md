# experiment-log：真实执行记录

日期2026-11-11（Asia/Shanghai）；所有命令运行在云端隔离目录，未连接用户本机或机器人。

## 依赖与上游示例
安装原始输出：qa/install-log.txt；Python3.13.5、mjfit0.1.0、MuJoCo4.0.0、NumPy2.5.4。包由固定GitHub公开SHA的ZIP安装，未修改上游。

```text
2026-11-11T01:03:08+08:00
usb_c: fell 11.5 mm in 49 ms and never touched the plate.
rj45: fell 13.0 mm in 52 ms and never touched the plate.
```
上面49/52ms是模拟时间，不是CPU性能数字。

## 首次失败与真实诊断
初次clearance执行发生AssertionError：`assert all(x['passed_depth_threshold'] for x in rows if x['offset_mm']==[0.,0.])`。
原因：起始销底在板顶上1mm，板厚10mm且下面有地板，居中落距最多约11mm；初稿要求12mm不可能达到。
诊断实际测得20/100/500µm三种居中落距均11.0000668mm；偏2mm为5.1873/5.5954/6.1421mm。
据此将阈值明确改为落距>9mm，保留其“中心深度代理、非整面入孔”含义并重跑。首次标准输出保存在exercise/first-attempt-output.txt；其异常栈未重定向到该文件，本段依据实际工具异常记录补记，不假称原日志已含stderr。

## 最终主实验完整标准输出
```text

=== 2026-11-11T01:03:59+08:00 | .sim-env/bin/python exercise/lab.py env ===
{
  "python": "3.13.5",
  "platform": "Linux-6.12.113+-x86_64-with-glibc2.41",
  "mujoco": "4.0.0",
  "mjfit": "0.1.0",
  "numpy": "2.5.4",
  "mjfit_sha": "5833f465896e1e06bc4be4f003be847f5183a4db",
  "scope": "CPU MuJoCo passive geometry/contact; no RL actor"
}

=== 2026-11-11T01:03:59+08:00 | .sim-env/bin/python exercise/lab.py clearance ===
[
  {
    "clearance_mm": 0.02,
    "offset_mm": [
      0.0,
      0.0
    ],
    "width_mm": 16.0,
    "height_mm": 16.0,
    "friction": 1.0,
    "tau_ms": 2.0,
    "dt_ms": 1.0,
    "drop_mm": 11.000066818011089,
    "peg_plate_contact_count": 0,
    "max_simultaneous_contacts": 0,
    "minimum_contact_distance_um": 0.0,
    "passed_depth_threshold": true,
    "simulation_s": 0.25000000000000017,
    "cpu_wall_s": 0.018238237000332447
  },
  {
    "clearance_mm": 0.02,
    "offset_mm": [
      2.0,
      0.0
    ],
    "width_mm": 16.0,
    "height_mm": 16.0,
    "friction": 1.0,
    "tau_ms": 2.0,
    "dt_ms": 1.0,
    "drop_mm": 5.187312685825868,
    "peg_plate_contact_count": 790,
    "max_simultaneous_contacts": 4,
    "minimum_contact_distance_um": -70.3082724237842,
    "passed_depth_threshold": false,
    "simulation_s": 0.25000000000000017,
    "cpu_wall_s": 0.0187091040006635
  },
  {
    "clearance_mm": 0.1,
    "offset_mm": [
      0.0,
      0.0
    ],
    "width_mm": 16.0,
    "height_mm": 16.0,
    "friction": 1.0,
    "tau_ms": 2.0,
    "dt_ms": 1.0,
    "drop_mm": 11.000066818011103,
    "peg_plate_contact_count": 0,
    "max_simultaneous_contacts": 0,
    "minimum_contact_distance_um": 0.0,
    "passed_depth_threshold": true,
    "simulation_s": 0.25000000000000017,
    "cpu_wall_s": 0.018081756001265603
  },
  {
    "clearance_mm": 0.1,
    "offset_mm": [
      2.0,
      0.0
    ],
    "width_mm": 16.0,
    "height_mm": 16.0,
    "friction": 1.0,
    "tau_ms": 2.0,
    "dt_ms": 1.0,
    "drop_mm": 5.5953788665330775,
    "peg_plate_contact_count": 780,
    "max_simultaneous_contacts": 4,
    "minimum_contact_distance_um": -140.48503137358875,
    "passed_depth_threshold": false,
    "simulation_s": 0.25000000000000017,
    "cpu_wall_s": 0.020263730999431573
  },
  {
    "clearance_mm": 0.5,
    "offset_mm": [
      0.0,
      0.0
    ],
    "width_mm": 16.0,
    "height_mm": 16.0,
    "friction": 1.0,
    "tau_ms": 2.0,
    "dt_ms": 1.0,
    "drop_mm": 11.000066818011089,
    "peg_plate_contact_count": 0,
    "max_simultaneous_contacts": 0,
    "minimum_contact_distance_um": 0.0,
    "passed_depth_threshold": true,
    "simulation_s": 0.25000000000000017,
    "cpu_wall_s": 0.018152269998608972
  },
  {
    "clearance_mm": 0.5,
    "offset_mm": [
      2.0,
      0.0
    ],
    "width_mm": 16.0,
    "height_mm": 16.0,
    "friction": 1.0,
    "tau_ms": 2.0,
    "dt_ms": 1.0,
    "drop_mm": 6.142126247759863,
    "peg_plate_contact_count": 780,
    "max_simultaneous_contacts": 4,
    "minimum_contact_distance_um": -188.74715244455606,
    "passed_depth_threshold": false,
    "simulation_s": 0.25000000000000017,
    "cpu_wall_s": 0.0194455389992072
  }
]

=== 2026-11-11T01:04:00+08:00 | .sim-env/bin/python exercise/lab.py randomize ===
{
  "seed": 2026,
  "pairs": 32,
  "nominal_centered_pass": true,
  "randomized_passes": 2,
  "oracle_centered_passes": 32,
  "scope": "paired passive drop distribution test; oracle uses exact hole center, NOT blind policy or randomized training"
}

=== 2026-11-11T01:04:01+08:00 | .sim-env/bin/python exercise/lab.py sampling ===
{
  "generated_compiled_stepped": 8,
  "steps_each": 20,
  "seed_prefix_reproducible": true,
  "geom_counts": [
    24,
    56,
    33,
    31,
    25,
    46,
    29,
    29
  ],
  "scope": "real mjfit.sample_pegs/build/compile/step, not learned insertion"
}

=== 2026-11-11T01:04:02+08:00 | .sim-env/bin/python exercise/lab.py evidence ===
{
  "paper_success_count": 173,
  "paper_trial_count": 237,
  "paper_fraction_recomputed": 0.729957805907173,
  "wilson95": [
    0.6700979640567583,
    0.782481922038145
  ],
  "scope": "counts are authors reported; only interval calculation ours",
  "blocked_drop_dt05mm": 5.341172780788058,
  "blocked_drop_dt1mm": 5.5953788665330775,
  "dt_sensitivity_scope": "one passive scene, not convergence proof"
}

=== 2026-11-11T01:04:38+08:00 | evidence naming correction (ms, not mm) ===
{
  "paper_success_count": 173,
  "paper_trial_count": 237,
  "paper_fraction_recomputed": 0.729957805907173,
  "wilson95": [
    0.6700979640567583,
    0.782481922038145
  ],
  "scope": "counts are authors reported; only interval calculation ours",
  "blocked_drop_dt05ms": 5.341172780788058,
  "blocked_drop_dt1ms": 5.5953788665330775,
  "dt_sensitivity_scope": "one passive scene, not convergence proof"
}
```

字段名曾把dt05ms误拼为dt05mm，代码已改名并再执行evidence；旧输出保留以追踪修正，数值不变。

## 输出解释与验证范围
1. clearance：真实生成6个方孔场景，各步进250次；3居中通过落距阈值，3偏置受阻。穿透量为软接触动态dist，不是几何精度误差。
2. randomize：32对真实MuJoCo被动落销，随机组2/32，oracle32/32；参数原始值及每个结果在randomized-results.json。没有PPO训练，不能当“训练随机化提高成功率”。
3. sampling：8件上游primitive生成/编译/20步，全部有限；同seed采样前缀一致。
4. evidence：作者173/237重新计算Wilson区间[0.67010,0.78248]；单个受阻场景步长敏感性只演示，未作收敛证明。
5. 上游完整测试套件、CoACD/V-HACD/SDF/Warp基准、视觉/本体策略训练比较、真实机械臂均未执行。

## PDF过程
实际命令：`/workspace/learn-batch/01-lingbot-map/.print-env/bin/python print_guide.py`，复用本bot第一项的打印环境（共享box，但未更改第一项成果）。
首次打印11页，发现E3孤页后调整卡片排版，最终10页A4；再修第四页SVG长标签。最终逐页渲染并查看，详见qa/page-check.md。pdftotext对原论文打印字体嵌入warning，但文本与原PDF均保存；指南PDF正常提取12问。

本批没有独立审核；所有自写断言与视觉检查均出自同一worker。没有修改安全设置、购买、密钥使用、共享vault合入、Git发布、任务勾选或日程。
