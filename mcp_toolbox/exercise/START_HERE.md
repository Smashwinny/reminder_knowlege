# 练习包入口

1. 打开 exercise/README.md，先按其官方链接下载约315 MB的 Linux x86_64 Toolbox 到 exercise/vendor/toolbox
2. 进入 exercise，按PDF中的六条命令执行。学习命令的 evidence/learner-run 在本包中刻意留空，避免首跑目录冲突
3. 既有执行证据在 exercise/evidence/recorded-learner-run；日志路径保留当时执行现场
4. knowledge_reference/verify_knowledge.py 可离线复核公开笔记和已清理元数据的旧网站笔记
5. reviewer_evidence 是独立复跑证据；根源文件/许可分别见 sources、exercise/reference、source_evidence
6. author 是图文源与PDF生成脚本。重建需Python及ReportLab（作者实测4.4.9）；在包根执行 python3 author/build_lesson.py。不需运行整个上游源码

不含大型官方二进制、账号凭据、私密路由ID、全局配置或本机vault写入操作。勿将故意错误只读提示标签的对照配置用于生产。

archive_manifest.json 给出包内原始字节指纹；官方二进制来源和单独下载指纹见 exercise/evidence/binary_provenance.json。
