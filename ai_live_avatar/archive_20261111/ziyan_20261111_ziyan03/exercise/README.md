> 公开归档版说明：下文是原完整实验包的历史README。本轮已移除第三方源码，请先阅读项目根目录[ARCHIVE_DEPENDENCIES.md](../ARCHIVE_DEPENDENCIES.md)。本轮未恢复依赖或重跑，不代表当前目录直接可运行。

# 离线数字人场控实验（标准库、无密钥、无联网运行）
Python 3.11+；本次真实运行 Python 3.13.5。

```
python3 -m unittest discover -s vendor/tests -v
python3 run_experiment.py
python3 cost_calculator.py
python3 verify.py
```

vendor 的五个 live 文件、moderation.json、test_logic.py 和 LICENSE 来自上游 dc87db8ad53fb81cfe07dcac08215497dfa1a50d，未修改。session.py 只通过 AST 取出原始 pick_idle_topic 函数运行；不导入整个会话模块、不启动服务、不接触网络。run_experiment.py 和 cost_calculator.py、verify.py 是本次教学新增；视觉降级是教学适配层，不冒充完整 LiveRoom 集成测试。gift 仅在上游单测和容量反例中作为合成数据，不接真实礼物、不用于公开排队。

全部真实 stdout/stderr 在交付包 experiment-output.txt，断言失败会非零退出。201 次抽样只验证编号话题池的去重机制，不是 100 条真人感文案质量测评。模拟时钟只验证规则逻辑，不是网络延迟或直播性能。
