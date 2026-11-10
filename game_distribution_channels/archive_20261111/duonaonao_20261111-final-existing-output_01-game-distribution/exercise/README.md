# 发行初筛离线实验
Python 3标准库，无网络或密钥。画像为合成；事实来自同级sources.json。

在ZIP解压根运行：
```bash
python3 exercise/run_all.py
```
六步骤也可分别运行lab.py init / validate / shortlist / costs / test / audit。
输出在exercise/results，真实命令日志exercise/run-log.json。运行会覆盖生成数据与结果，不动外部系统。

字段约束：None表示未知；modes是本次有限研究模型的能力范围，不是平台全部业务能力。候选仍须完成真实主体、地区、合规、合同、隐私、支付和审核核验。测试为自编局部断言，不是独立审核。
