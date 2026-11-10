# mjfit 真实接触与域随机化练习

## 范围
真实调用mjfit生成器与MuJoCo编译/动力学；不是盲装配学习actor、完整PPO或真机成功率复现。
`lab.py`为原创；`upstream/drop_peg.py`为上游 `5833f465896e1e06bc4be4f003be847f5183a4db` 未修改示例，MIT许可及来源一并保留。

## 六步重放（从exercise的上级运行）
```bash
python3 -m venv .sim-env
.sim-env/bin/pip install 'mjfit @ https://github.com/younghyopark/mjfit/archive/5833f465896e1e06bc4be4f003be847f5183a4db.zip' mujoco==4.0.0 numpy==2.5.4
.sim-env/bin/python exercise/lab.py env
.sim-env/bin/python exercise/upstream/drop_peg.py usb_c
.sim-env/bin/python exercise/upstream/drop_peg.py rj45 --clearance 2e-5
.sim-env/bin/python exercise/lab.py clearance
.sim-env/bin/python exercise/lab.py randomize
.sim-env/bin/python exercise/lab.py sampling
.sim-env/bin/python exercise/lab.py evidence
```
依赖锁定见requirements-lock.txt。无需GPU、窗口、摄像头、私密记录或付费API。

## 指标不能混淆
- `passed_depth_threshold`：0.25秒被动仿真内，销体中心落距>9mm；不是论文完整插销成功检查。销有自由关节，允许倾斜；不能把中心落距当整张底面入孔。
- `peg_plate_contact_count`：跨时间步累计销/板接触记录数，不是独立撞击次数；不含地板。
- `minimum_contact_distance_um`：动态接触dist最小值，可因软接触为负；不是轮廓建模误差。
- randomize的32对使用完全相同几何、摩擦和时间常数；一组随机偏置，一组把偏置归零。后者是知道孔中心的oracle，不是盲策略、视觉策略或任何训练结果。
- 参数：方孔宽/高14–24mm、c=0.1–0.5mm、μ按log-uniform从0.25–2抽样、τ=2.5–6ms、XY偏置各±1.5mm，seed2026。没有随机姿态、质量、机器人动力学或学习动作。
- simulation_s是模拟时间，cpu_wall_s仅该本机步进循环墙钟时间，非作者benchmark。
- evidence的173/237来自论文，仅Wilson区间由我们计算。

## 真实失败与纠正
首次clearance用落距>12mm，导致居中断言失败；地板使居中最多约11mm，因此依据场景几何改为>9mm，随后重跑。不是隐藏失败或把阈值改到所有样本通过，偏2mm仍全部受阻。完整记录见experiment-log.md。
