# 知识增量提案：一个域名背后的 Cloudflare 分层

仅候选，未合入vault、未Git推送、未勾选任务。

基线 `a8674777e18302b8804b137212b1396cbfe5a747`；2026-11-11 01:25:26 北京时间（UTC+8）

## 查重
已读vault/00-总览.md、项目笔记/cloudflare_email_routing.md及动作投递语义与安全重试.md。只补跨服务依赖图与离线验收，不重造邮件路由匹配知识。

## 建议追加而非重写
追加“域名入口分层验收”：DNS可解析、TLS可校验、HTTP可响应、业务可读回分别取证；在既有邮件路由笔记注明本次没有重测邮件；将Flexible重定向循环作为模型示例。

## 实测及边界
真实DNS切换、证书签发、Workers部署、邮件收发、R2 API、Workers AI推理及cf命令均未执行；本地HTTP是Python夹具，不是workerd或Wrangler。

总体状态：待验证。真实离线输出见experiment-log.md，教学夹具不能替代端到端验收。没有独立审核。
