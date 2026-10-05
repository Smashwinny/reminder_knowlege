# MCP Toolbox：数据库执行权限与工具提示

[13 页指南](MCP-Toolbox-小白指南.pdf)、[HTML](guide.html)、[练习包入口](exercise/START_HERE.md)、[实验日志](experiment_log.txt)、[知识入库笔记](../vault/项目笔记/mcp_toolbox.md)。

本次在 Dot 云端实际运行官方 Toolbox v1.13.1 Linux x86_64 发布程序，经 MCP stdio 验证 26 项；另一审核者复跑同一 26 项并通过独立 CLI 再验证 5 项。26 的复跑不能算作新增 26 个不同检查。

完整练习在 exercise/exercise/README.md，约 315 MB 的官方 Linux 程序按其中固定链接单独下载，不含在 ZIP/Git；运行会创建独立的新输出目录，不使用生产数据、凭据或付费模型。README 的旧 evidence/run-01 路径在本次交付应查看 exercise/exercise/evidence/recorded-learner-run/results.json；保留冻结原件，另在这里说明。

主分支观察固定 a24e5e68567fa014a42fc6cc711faa82b964d4c0，实测发布提交 e14cda6b4f483e6b5e5ec23e342f9f232a6ce60f；二者分开记账。完整 Apache-2.0 许可与 Google 版权头随摘录保留。

Windows 本机校验六原件，实际查看全部 13 页 PDF，离线复核包内 85 个文件及 23 份选定源码指纹，执行四组既有协议结果核查和知识来源校验。未在 Windows 运行固定 Linux 二进制，不把离线检查当作 Toolbox 重新运行。Poppler 使用 SimSun 替代 PDF 的中文 CID 字体，当前页图可读无裁切；原 PDF 字节未变。HTML 浏览器视觉仍未验收，PDF 为直接 ReportLab 生成。

真实证明的是通过 SQLite URI mode=ro 打开的这份主库拒写，以及故意错误的 readOnlyHint=true 不禁止独立可写库写入。没有验证云数据库 readOnly、OAuth、HTTP、租户隔离、ATTACH/temp/扩展或全进程安全。后续生产部署需要相应授权与专项验收。
