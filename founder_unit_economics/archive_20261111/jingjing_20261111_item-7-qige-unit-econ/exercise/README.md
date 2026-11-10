# 教学用单位经济 / 漏斗模型

离线、零依赖（Python 标准库）的练习代码。用于理解「先卖再开发 / 测试单 / 定制单 / 课程」路径上的单位经济，而不是复现或证实原帖的营收与融资。

## 运行

```bash
cd exercise
python3 unit_econ.py assumptions
python3 unit_econ.py base
python3 unit_econ.py sensitivity
python3 unit_econ.py breakeven
python3 unit_econ.py narrative
python3 unit_econ.py stress
python3 -m unittest test_unit_econ.py -v
```

## 输入纪律

`assumptions.json` 里每一项都带 `source`：

- `author_claim`：原帖或引用长文的作者自述，未经独立核实
- `author_claim_derived`：由自述粗略推算，结论仍未核实
- `teaching_assumption`：为让模型能跑而设的教学假设，不是作者数据

模型拒绝把无标签数字直接入账。融资额不是 `unit_economics()` 的参数。

## 版权与范围

本练习代码为学习批次原创，仅用于离线数值实验。原帖版权归作者。不要用本模型去投放广告、改计费或对外承诺收益。
