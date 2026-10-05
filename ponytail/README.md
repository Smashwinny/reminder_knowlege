# Ponytail：保留边界的简洁编程

[10 页指南](Ponytail-小白指南.pdf)、[HTML](guide.html)、[练习](exercise/README.md)、[云端实测日志](experiment_log.txt)及[知识笔记](../vault/项目笔记/ponytail.md)。固定上游 e15862bb04d04285233a164460ced063941d9ef5；没有安装插件或执行全局 hooks。

在 exercise 目录运行以下 Windows 命令；2026-10-05 已用 Python 3.12.14、UTF-8 实际验证全部六步：

```powershell
python -X utf8 inspect_source.py
python -X utf8 demo.py minimal alice
python -X utf8 demo.py layered alice
python -X utf8 demo.py minimal "x' OR '1'='1"
python -X utf8 test_lookup.py
python -X utf8 audit_sources.py
```

两版各 21 项检查通过，共 42 项；故意不安全的负对照被识别。全部使用一次性内存数据库和假数据，不读真实聊天或生产数据库。原始来源任务片段仅静态检查，未导入执行。许可见 exercise/LICENSE-upstream.txt。

Windows 又核对固定 Git 中的 19 份选取来源指纹、完整任务片段与 MIT 许可，查看全部 10 页 PDF。云端另一执行者有额外 28 项边界检查的独立记录；这些不是本机复跑数量。原件保存在网站及本机私有备份。

这是两份自写实现的工程实验，未复现 Haiku 4.5 基准、付费 API、模型节省或全面安全。PDF 用 ReportLab 直接生成；HTML 浏览器视觉未验收，字体在不同阅读器中可能替换，不声称两格式逐像素一致。
