# 离线练习与复现

依赖：Python3标准库；无第三方依赖。

从ZIP解压后的、含exercise/的父目录运行，按次序：

```bash
python3 exercise/lab.py snapshot
python3 exercise/lab.py binding
python3 exercise/lab.py deploy
python3 exercise/lab.py assets
```

lab.py为本次自编教学夹具，不是作者项目实现；合成输入在代码内明确标注。没有账号、用户密钥、真实硬件或外部发布。局部数据库/图片/视频写入exercise/，回环HTTP监听127.0.0.1随机端口并关闭。运行第一个步骤会重建本项合成练习数据库（如有），不用于用户业务数据。

完整原始命令输出与边界随ZIP附experiment-log.md；来源随ZIP附sources.md。
