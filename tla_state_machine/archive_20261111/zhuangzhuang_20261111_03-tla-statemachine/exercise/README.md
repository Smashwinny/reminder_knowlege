# TLA+状态机练习

来源与访问：2026-11-11 Asia/Shanghai。pstack一手方法固定SHA `de8ee15dd1194627d21eb5fcd41cb1873208dabb`；TLC官方release v1.7.4（工具显示TLC2 2.19 rev5a47802）；Java21.0.13+9。全部业务数据为合成，无付费API或真实支付操作。

## 复现
解压后从包根运行：
```bash
python3 exercise/setup_tools.py
cd exercise
python3 run_labs.py all
```
setup_tools.py只在相邻tools目录下载/解压固定Linux x86-64 JRE与tla2tools.jar，约50MiB下载；SHA256锁在脚本中，TLC另核对官方发布正文SHA1，不改系统安装/环境/安全设置。已经有兼容Java时，可手动准备JAR并通过JAVA和TLA2TOOLS_JAR环境变量指定路径，跳过下载脚本。非Linux x86-64机器应自备兼容Java，未实测其他平台。

主实验可分别运行bug、fixed、scaling、mutation、replay；run_labs.py真实spawn Java，保留全部命令、原始输出与退出码。重复运行会覆盖results中的同名合成证据，不要放入用户业务数据。

## 文件与原始来源对应
- models/OrderCore.tla、OrderBug/Fixed/Many.tla及cfg：按pstack元技能的“选一条规则、保留边界、能失败”原则自编，不是从任何真实订单产品抽取。
- order_reference.py：自编纯Python状态转移，作为模型对应的可执行合成实现；非数据库或并发服务。
- run_labs.py：自编TLC调用/断言/反例解析与重放；不是TLC的替代实现。
- verification-contract.md：按pstack方法手写的候选合同，未注册或声称执行正式插件。
- upstream-reference/：来自cursor/plugins的三份原样技能、plugin.json及MIT LICENSE，固定SHA为 `de8ee15dd1194627d21eb5fcd41cb1873208dabb`，仅参考，不执行其发布/日程/安装建议。
- coverage-manifest.json：合成代码/模型文件内容哈希；无Git提交，不借用上游SHA冒充代码同步点。

## 实测结果
bug：8生成/6不同/队列1，TLC退出12，5状态/4转移反例；固定版8/5/0退出0；多订单1/2/3分别5/25/125不同状态，均退出0；模型变异再次退出12。Python逐步重放反例，并验证固定版DOT全部状态集合与Python5状态相同。

这不是任意规模证明、真实支付产品验证、活性证明、完整供应链审核或独立审计。详见verification-contract.md与experiment-log.md。
