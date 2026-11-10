# Item03 实验日志

实际执行：2026-11-11 01:07:31起（Asia/Shanghai UTC+8），Linux云机，Python 3.13.5。完整stdout/stderr见experiment-output.txt；9个上游单测0.003s是该次日志记录，不作基准性能结论。

## 执行与证据
1. 公开API重新查询 vault main=a8674777e18302b8804b137212b1396cbfe5a747、source HEAD=dc87db8ad53fb81cfe07dcac08215497dfa1a50d；读取已有快照及固定版本源码。
2. `python3 -m unittest discover -s vendor/tests -v`：9/9通过；未改上游断言。
3. `python3 run_experiment.py`：真实调用上游Moderator/classify/CommandQueue。10条模拟消息5通过5拦；容量3最终D、E、F按FIFO出队。expire与preparing测试通过。脚本视觉降级是教学适配层，不是整个服务集成。
4. 同脚本通过AST抽取session.py原始pick_idle_topic函数，不导入含网络依赖的LiveRoom。随机种子20261111，100个编号话题抽201次，两轮各100唯一，轮间不相同；空池异常预期捕获。编号话题不是完整角色文案，未测LLM复读。
5. 全礼物合成队列反例：max_size=2却容纳3条；观察而未改上游代码。主实验不设礼物优先。
6. `python3 cost_calculator.py`：Decimal历史算术168.75元/小时，67min=188.4375元，对作者声称191.47差3.0325元；等价额外64.6933秒只是数学换算。未读取实际账单、未确认现价。
7. `python3 verify.py`：5份源文件hash和关键结果核对通过。

## 运行边界
未安装或调用Vidu、OBS、RTC SDK、Evolink、火山引擎；没有声音克隆、摄像头、真实弹幕、真实直播、付费API、用户密钥或安全设置变动。没有把“代码空跑”包装成端到端数字人。真实模型延迟、服装一致性、RTC恢复、音频路由、画面合规、平台政策与人工接管均待验证。原作者播放量、在线人数、账单、延迟、换装耗时均未独立验证。

PDF实际打印和逐页PNG检查追加在pdf-inspection.md；这只是本worker自检，无独立审核背书。
