---
tags: [项目笔记, 防御性安全, 浏览器权限, 反钓鱼]
created: 2026-10-27
---
# 浏览器安全工具清单（防御视角）

对 X 帖中的 Storm-Breaker、Seeker、Zphisher、HackingTool、SayCheese 做防御性来源审核与权限机制验证，不运行任何采集或钓鱼流程。

## 核心概念
- [[采集分级防御法]]：被动指纹、敏感权限、主动输入分级防御。
- [[浏览器权限状态机]]：敏感 API 默认 prompt，拒绝即拿不到数据。

## 实测
Seeker `js/location.js` 先 POST 平台/浏览器/硬件/屏幕等被动指纹，再请求 geolocation；后者必须用户授权。自建权限页在 headless Edge 实测 `isSecureContext=true`、定位权限为 prompt，拒绝时 `code=1 User denied Geolocation`。因此“点链接即被精确定位”是夸大，但被动指纹无需弹窗即可采集。

SayCheese 无确切仓库地址，身份未核实；摄像头行输出被 virtual-time 截断，未复测。Zphisher 的防御重点是域名核对、官方入口和 2FA。
