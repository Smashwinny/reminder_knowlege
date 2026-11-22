# Antigravity 登录排查知识入库提案（2026-11-22 审核修订）

> 原 worker 提案保留在 pending 文件；本文件记录协调者实际合并决定。

- 新建 [[登录排查四层拆解]]：资格/授权网络/额度/服务限制。
- 新建 [[第三方工具数据流审计]]：端点/凭据路径/许可/当前官方授权，静态与运行分开。
- 向 [[健康探测三态]]、[[OAuth资源发现]] 追加边界，不把标准认证当产品授权。
- 新建项目笔记 `vault/项目笔记/antigravity_login.md`，MOC 添加概念与项目索引。

当前官方 FAQ/Terms 复核；Manager 固定源码 6 项测试通过。Bridge 不碰凭据仅为 README 自述，社区封禁/全账号影响/通用申诉不冒充官方事实。

审核版 PDF：`antigravity_login/Antigravity登录排查-小白指南-v2.pdf`；原 PDF 保留。
