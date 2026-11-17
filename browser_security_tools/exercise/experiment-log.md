# 浏览器安全工具清单 · 实验日志（task f9051c75-4321-4ba6-b914-9bac6dad9a20）

实验日期：2026-10-27
性质：**防御性学习**。只做源码级事实核对与浏览器权限机制实测；
不部署、不运行任何针对他人的采集/钓鱼流程，不提供诱导访问或采集密码的操作。

## 实验设计

原帖列出 5 个"开源安全工具"（Storm-Breaker / Seeker / Zphisher / HackingTool / SayCheese）。
实验回答三个防御者真正关心的问题：
①这些工具的"能力宣称"哪些被浏览器权限机制真实约束？
②不设防的访问会泄露什么？（被动指纹 vs 需授权的敏感权限）
③如何识别和防御？（权限请求审查 + 仿冒页识别）

## 步骤与真实输出

### 步骤 1：Seeker 源码级核对（git clone @ 7bf501a）

读 `js/location.js` + `template/nearyou/`，确认采集分两类：

**A. 被动指纹（无任何授权弹窗即可收集）**——location.js 第 47-72 行：
```
POST info_handler.php: Ptf(平台) Brw(浏览器) Cc(CPU核数) Ram(内存)
Ven/Gpu(显卡厂商/型号) Ht/Wd(屏幕) Os(UA解析)
```
→ 这类数据每次网页访问都可能被读走，防御靠反指纹插件/浏览器加固。

**B. 精确定位（必须用户点"允许"）**——第 90-92 行：
```
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(showPosition, showError, {enableHighAccuracy:true...});
```
且 showError 明确处理 PERMISSION_DENIED（"User denied the request"）。
→ 宣传中"点击链接即被精确定位"是**夸大**：必须受害者手动授予定位权限。

### 步骤 2：浏览器权限机制实测（自建测试页）

`exercise/permission-test.html`：检测安全上下文 + 查询权限状态机 + 发起定位请求 + 摄像头请求。
Headless Edge 真实运行（--dump-dom 捕获页面日志）：

```
① isSecureContext = true           （Edge 视 file:// 为安全上下文——口径注意点）
② geolocation 权限状态（请求前）: prompt    ← 浏览器先问，绝不默认放行
③ 定位被拒/失败(正常防御行为): code=1 User denied Geolocation
                                    ← PERMISSION_DENIED，页面拿不到坐标
④ （摄像头行未捕获完整输出——virtual-time 截断，如实记录未复测）
```

### 步骤 3：与 MDN 约束对照

- Geolocation API：仅安全上下文 + 用户显式授权；
- getUserMedia：同上加硬件指示灯；HTTP 页面直接被拒；
- 与步骤 1/2 实测完全吻合。

## 结论

- 工具宣称要分两类看：**被动指纹真实存在**（无需授权），**精确定位/摄像头必须用户授权**；
- 浏览器权限状态机（prompt/granted/denied）是防御的第一道闸：默认 prompt，拒绝即拿不到；
- 防御清单：① 不随便点"允许" ② 检查地址栏权限图标 ③ 敏感操作看域名是否官方（防 Zphisher 仿冒页）④ 反指纹插件挡被动采集；
- 夸大宣称本身也是防御信号——"点链接即定位你"的说法常用于恐吓式传播。

## 产物

- `exercise/permission-test.html` — 权限机制实测页
- `exercise/experiment-log.md`（本文件）
- `repo/` Seeker 源码克隆（仅静态阅读，未运行）
