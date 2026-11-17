---
tags: [项目, 防御性学习, Web安全]
类别: 开源项目类（防御性学习重构）
上游仓库: https://github.com/ultrasecurity/Storm-Breaker
学习日期: 2026-10-30
状态: 产物待 ready / 独立审核
---

# storm_breaker_defense

**这是什么**：对 ultrasecurity/Storm-Breaker 的防御性源码学习，不复现部署或采集，而是把钓鱼页的敏感权限请求、社会工程话术和授权后回传链转化为浏览器权限知识、检测清单、撤权流程与事件响应。

**它给我什么能力**：
- 区分“页面加载”“请求权限”“用户决定”“数据回传”，纠正“点链接即无提示开启全部设备”的夸大。
- 从安全上下文、Permissions Policy、站点权限、操作系统四层审查摄像头、麦克风与定位。
- 识别设备指纹、第三方公网 IP 查询、周期上传和权限不相称等风险信号。
- 在站点与系统两层撤销权限，按停止、撤权、证据、影响、报告、复盘响应事件。
- 用本地合成实验验证机制，避免真实传感器、第三方目标和不知情人员数据。

**引入的概念**（概念正文由协调者按项目目录提案合并）：
- [[浏览器敏感权限分层模型]]
- [[安全上下文信任边界]]
- [[权限社工与授权后回传]]

**已有知识关联**：
- [[WebRTC机器人应用]]：正当实时音视频与滥用采集共享浏览器能力，边界在明确同意、最小授权、可见指示和可撤销性。
- [[本地MCP端点安全四道门]]：回环被浏览器视为可信来源，不代表本地服务可以省略 Host/Origin/令牌检查。
- [[证据优先质检ProofOverClaims]]：真实浏览器查询、合成 mock、静态源码和外推限制分开记录。

**实验记录**：
- 上游固定到 `4d7235104870ec0224f445fd905c98f22a105426`，只读扫描 38 个文件，七类防御指示器全部命中，没有运行上游代码。
- 本地 Edge 回环实验实测 `isSecureContext=true`；camera/microphone/geolocation 权限查询均为 `prompt`，未弹窗或授权。
- 合成媒体拒绝为 `NotAllowedError`；合成轨道停止后为 `ended`；定位仅使用合成 0,0。
- CSP 阻止回传金丝雀，本地服务器只收到页面与 favicon 的 GET；最终 11/11 检查通过，服务器与临时浏览器目录均清理。
- 指南含 Q1-Q10 与十张内联 SVG；PDF 15 页、876385 字节，HTML 首屏已渲染查看。因缺少 `pdftoppm`，本 worker 未宣称 PDF 逐页视觉审核。

**产物**：
- [彩色 HTML 指南](../../storm_breaker_defense/storm-breaker-defense-guide.html)
- [中文 PDF 指南](../../storm_breaker_defense/storm_breaker_defense-小白指南.pdf)
- [实验日志](../../storm_breaker_defense/exercise/experiment-log.md)
- [静态审计](../../storm_breaker_defense/exercise/static-audit.json)
- [浏览器结果](../../storm_breaker_defense/exercise/browser-results.json)
- [确定性复核](../../storm_breaker_defense/exercise/verification.json)
- [知识入库提案](../../storm_breaker_defense/storm_breaker_defense-knowledge-proposal.md)

**来源**：
- https://github.com/ultrasecurity/Storm-Breaker
- https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
- https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts
- https://developer.mozilla.org/en-US/docs/Web/API/Permissions_API
- https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API
- https://support.google.com/chrome/answer/114662?hl=en
- https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks

**坑与限制**：媒体与定位成功/拒绝分支是显式 mock，不是硬件验证；单台 Windows 11 + Edge 结果不能外推其他平台。Windows 官方支持页直接抓取返回 404，指南已标注。未执行上游服务、隧道、诱导、秘密采集或任何第三方目标。法律内容只是风险提示，不构成法律意见。

**后续可深入的方向**：由授权团队在自有浏览器矩阵中验证权限策略、企业站点允许列表审计和隐私友好的遥测检测；不得把本项目转成第三方部署或监控教程。
