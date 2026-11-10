# 实验日志 · 03-single-motor-drone

- 运行位置：云端隔离目录 `/workspace/learn-batch/03-single-motor-drone/`
- 运行时间：2026-11-11 01:14 Asia/Shanghai（UTC+8）
- 解释器：Python 3.13.5
- 命令：

```bash
python3 exercise/ex_cyclic_hinge_sim.py --outdir logs/exp-out
cd exercise && python3 -m unittest test_mcout_crc.py
```

- 墙钟耗时（脚本自报）：0.055 s
- 单元测试：3 passed（CRC 向量、组包往返与安全门、45° 1:1 运动学）
- 原始输出：`logs/exp-out/results.md`、`logs/exp-out/results.json`、四张 SVG、`step3_timeseries.csv`

## 步骤与真实结果

### 1. 几何、桨尖马赫、延迟角度 — 真实完成

6 英寸 = 0.1524 m。按作者「几乎 20,000 RPM」：

- 1/rev = 333.3333 Hz，周期 = 3.0000 ms
- 桨尖速度 = 159.59 m/s = 357.0 mph = 574.5 km/h，马赫 0.465（a = 343 m/s，假设 20 °C 干空气）
- 「接近音速一半」与马赫 0.465 相符。二级报道写的 310 mph / 500 km/h 偏低，未采用
- 每秒 300 次加减速 = 0.900 次/转；正好每转一次应对应 18,000 RPM
- 0.2 ms → 24.00°；2 ms → 240.00°；正好 20° → 0.1667 ms
- moteus 15–30 kHz：每转 45.0–90.0 次更新；MCOUT 400 Hz：每转 1.20 包

验证：v = π D n；角度 = (20000×360/60)×Δt。手算一致。

### 2. 斜铰链运动学 — 真实完成

公式 θ = ζ tan(α)。45° 耦合 = 1。假设滞后 8° 时变距：30° → 4.62°，45° → 8.00°，60° → 13.86°。`test_forty_five_degree_is_one_to_one` 通过。

### 3. 周期调速侧向力（假设模型）— 真实完成（模型输出，非试飞）

假设：单桨 4 g、回转半径 4 cm、wn = 1.4 Ω、阻尼比 0.25、集体桨距 12°、弦长 18 mm、δΩ/Ω = 4%、cl_α = 2π。

- 滞后/变距振幅 1.929°，相对角加速度相位 143.9°
- 平均推力 16.978 N（假设集体桨距下的数量级，**不是**作者实测）
- 平均侧向力 1.3646 N，倾斜 4.595°
- 关闭周期调速后基线侧向力 5.24×10⁻¹⁷ N（数值零）
- 侧向力随调速幅值单调上升（见图 `step3_side_force.svg`）

验证：无周期输入时侧向力回到机器精度；45° 下两片桨变距等幅反相（见 `step3_timeseries.csv`）。

### 4. 160 Hz 与刚度缩放 — 真实完成（对照与缩放，非实测模态）

- Ω = 333.33 Hz，Ω/2 = 166.67 Hz，|160−Ω/2| = 6.67 Hz
- 若 160 Hz 为 1/rev，对应 9,600 RPM
- 若软桨一阶挥舞在 160 Hz，EI 加倍后频率 226.3 Hz（√2）

硬件频闪与试飞待验证。

### 5. MCOUT CRC 与安全门 — 真实完成

对照 `jyjblrd/moteus@704a0dd` 的 `fw/mcout_protocol.h`：

- XMODEM CRC-16 `"123456789"` → 0x31C3，与公开测试向量一致
- 84 字节武装包往返 CRC_ok=True，output_allowed=True
- 翻转 1 bit 后 CRC_ok=False
- 去掉 INTERLOCK 或置位 ESTOP 后 output_allowed=False
- 文档冲突已记录：moteus 指南 `SERIALx_PROTOCOL=50`，ArduPilot README `=51`（钉住 SHA 上的文档，不是硬件结论）

### 6. 面积对照 — 真实完成（PULSAR 直径待用论文 PDF 再核）

- Bird 6 英寸桨盘 0.01824 m²
- PULSAR 37.6 cm（HKU / Science Robotics 报道）0.11104 m²，比值 6.087，支持「小六倍多」
- Paulos 2013 的 38.6 cm 面积比 6.42，但飞行器是双电机共轴机

## 未运行（不是失败，是没有硬件）

- 3D 打印 PPA-CF 桨毂 / TPU 机身
- moteus r4 + ArduPilot 实机刷写与 20,000 RPM 台架
- 频闪摄影与 160 Hz 复现
- 卧室悬停 / 室外飞行
- YouTube 官方英文字幕整文件（timedtext 空响应，yt-dlp HTTP 429）
- Paulos JGCD 2018、AIAA 2018 PDF（modlabupenn.org HTTP 429）；IROS 2013 已全文读取

没有把作者口中的 20 FPS 式性能（这里是 RPM / 300 次）写成我测到的数，也没有自我审核。
