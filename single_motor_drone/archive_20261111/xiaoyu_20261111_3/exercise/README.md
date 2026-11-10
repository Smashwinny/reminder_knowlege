# 单电机铰链桨：数值实验

只依赖 Python 3 标准库。在本目录运行：

```bash
python3 ex_cyclic_hinge_sim.py --outdir ./out
python3 -m unittest test_mcout_crc.py
```

- `ex_cyclic_hinge_sim.py`：六步主实验（几何与时序、45° 运动学、周期调速侧向力、160 Hz 与刚度缩放、MCOUT CRC 组包、与 PULSAR/Paulos 面积对照）。
- 侧向力、推力、挥舞频率使用的惯性、弦长、集体桨距和刚度都是**假设参数**，用来展示机理，不是 Joshua Bird 的台架或试飞测量。
- 作者报告的 6 英寸、约 20,000 RPM、每秒约 300 次加减速、45° 铰链、160 Hz 振动、PULSAR「小六倍多桨盘面积」等，在脚本里单独标注为 author-reported。

固件协议对照来源：

- `jyjblrd/moteus` `704a0dd9f30a3704e8915a82c1631301fdbff9bd` 的 `fw/mcout_protocol.h` 与 `docs/guides/ardupilot-mcout.md`
- `jyjblrd/ardupilot` `455b266cc2a73505eb98c56a8049fa6a4d50f9bf` 的 `libraries/AP_MotorControlOutput/README.md`
