# Pi-Purge 学习候选成果

报告：index.html；pi-purge.pdf。证据：sources.md / experiment-log.md；建议：knowledge-proposal.md。

exercise.zip 内含自写夹具、指纹和安全源快照。解压到新目录后，在解压根目录依次运行：
```bash
node --version
python3 exercise/verify.py
python3 exercise/run.py modes
python3 exercise/run.py lifecycle
python3 exercise/run.py compat
python3 exercise/run.py upstream
python3 exercise/run.py env
```
无需安装 Pi/npm 依赖，不需要任何模型 key。只对已审代码提供全局 fetch 抛错保护，不是 OS 沙箱。被测当前扩展为原样源码；历史固定版只改内嵌 persona 为无害常量（原指纹见 evidence/pinned-redaction.json），不分发历史破甲提示词。Pi 构造器用路径与 skills 替身，当前分节拼接为夹具；没有 Pi CLI、TUI、模型或 RAE 端到端运行。

本项保存私有云端候选产物，没有合入 vault、发布 Git、勾任务、创建提醒或改变账户/安全设置。状态详见 STATUS.md。PDF渲染与逐页检查记录随后附于 experiment-log.md。
