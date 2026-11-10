# Pi 零付费组件实验

本练习是教学测试夹具，不是 Pi 官方测试套件，也不是独立第三方安全审计。源代码许可见 snapshots/LICENSE-pi；每份上游快照的 SHA/文件哈希见 snapshots/provenance.json。自写 graph.py/run.py/final-check.py 及从旧审计复用的三个 .mjs 都有明确范围。

## 前提与执行
Node >=22.19.0、npm、Python 3、tar。先解压此 ZIP 到新目录，不要置于用户 Pi 配置目录。

```bash
cd exercise
python3 run.py
```

六步全部执行；步骤 1 仅公共 npm 下载，--ignore-scripts，不安装依赖。不启动 Pi CLI、不调用模型、不读账户配置或密钥。日志写到 exercise 的父目录 experiment-log.md；每步失败即停，不会自升级。

## 已含归档的离线复跑
ZIP 自带精确 npm tgz。第 1 步不必再次联网下载：
```bash
cd exercise/lab
tar -xzf earendil-works-pi-coding-agent-0.84.2.tgz
node manifest.mjs
cd ..
python3 graph.py
cd lab
node switch.mjs
node ping-mock.mjs
cd ..
python3 final-check.py
```

manifest 检查 No MCP、导出与依赖；switch 导入真实发布物纯函数十用例；ping 从发布物抽出 reportInstallTelemetry 单方法，向 VM 注入 mock fetch/timeout。VM 不作为安全沙箱承诺，只让此已审查单方法不接真实 fetch。五分支不等于全进程联网测试。

snapshots 含四个固定提交的主包清单及选定源码，供离线图分析；main 只代表本次读取时刻，不会自动追踪。results.json/graph-results.json 是本次真实运行留痕。上游客户端/Changelog 与完整包归档均保留公开原始来源；没有任何私密记录。
