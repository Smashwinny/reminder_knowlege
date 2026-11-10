# DSH 57插件增量研究

index.html / dsh-plugins-57.pdf为彩色学习报告；plugin-candidates.md/csv/json为57项候选核查；experiment-log.md为真实输出；sources.md固定版本；knowledge-proposal.md仅为合入建议。

在exercise.zip解压根目录重放（Node24、Python3，无npm install、模型key或DSH）：
```bash
node --version
python3 exercise/verify.py
python3 exercise/run.py catalog
python3 exercise/run.py overlap
python3 exercise/run.py guard
python3 exercise/run.py cost
```
共25条自写检查。真正执行上游的只有纯mountOnce模块，fake ctx模拟effect/dispose；未执行完整插件、SSH、看板、cron或付费模型。catalog重放已存公共核查结果，不声称重新查询当前状态。cost只测热JSON.parse，不是DSH启动。Node模块类型警告保留，不改上游package。

旧archify成果只复用，不重做；与item-4共用引用长文，但本项聚焦重复/冲突/成本。未修改用户任务、vault、Git发布、账户或安全设置。PDF实际打印/逐页查看记录随后追加到experiment-log.md。
