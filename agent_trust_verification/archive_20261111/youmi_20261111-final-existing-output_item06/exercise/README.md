# 自写类型/状态模型练习
Python3.13、Node24。包锁固定TypeScript5.9.3，不含node_modules，首次恢复依赖：
```bash
cd exercise
npm ci --ignore-scripts --no-audit --no-fund
cd ..
sh exercise/verify.sh
```
或按guide.html逐步跑六条python3命令。negative.ts编译错误为预期；mutant.ts为故意as any逃逸。所有receipt/send都只是纯内存合成状态，无邮件/Slack/API执行器。自写静态扫描只有一条语法规则，非ESLint；BFS有限枚举非TLA+/TLC。没有真实用户授权凭证或隐私数据。源码自写，允许复制修改用于学习。
