# storm_breaker_defense 实验日志

- task_id：d605f8e5-94e8-455d-a5d8-00d423a64f2c
- owner：main-k3-w1
- 日期：2026-10-30
- 上游：https://github.com/ultrasecurity/Storm-Breaker
- 固定提交：4d7235104870ec0224f445fd905c98f22a105426
- 范围：防御性静态源码审计、本地回环浏览器机制验证、权限/检测/响应学习。

## 安全边界

1. 只克隆和读取上游源码；没有执行上游 `st.py`、PHP 服务、安装脚本、隧道、收集器或诱导页面。
2. 没有对任何第三方目标使用工具，没有发送诱导链接，没有采集任何不知情人员的数据。
3. 浏览器实验只绑定 `127.0.0.1` 随机端口；真实摄像头、麦克风、定位均未访问。
4. 媒体成功/拒绝与定位分支使用页面内显式 mock；定位仅使用固定合成标记 0,0，不代表设备位置。
5. Permissions API 查询是真实 Edge 浏览器调用，只读取状态，没有打开提示或授予权限。
6. CSP `connect-src 'none'` 用于证明意外回传会被拦截；金丝雀 POST 未到达本地服务器。

## 环境与初始化

- 上游克隆命令实际执行成功，`git -C repo log --oneline -1` 返回：`4d72351 Merge pull request #363 from jalalsaberi/main`。
- Python：3.14.7；当前进程 `PYTHONUTF8=1`，实测 `sys.flags.utf8_mode=1`。
- 初次用相对路径运行静态审计时，因为工具调用工作目录重置到仓库根，出现：`can't open file F:\reminder\exercise\audit_upstream.py`。未绕过错误；改用绝对路径后成功，后续命令全部使用绝对路径。

## 实验 1：只读静态审计

实际命令：

```powershell
$env:PYTHONUTF8='1'; python -I "F:\reminder\storm_breaker_defense\exercise\audit_upstream.py" "F:\reminder\storm_breaker_defense\repo" --output "F:\reminder\storm_breaker_defense\exercise\static-audit.json"
```

真实输出：

```text
STATIC_AUDIT commit=4d7235104870ec0224f445fd905c98f22a105426 files=38
camera_capture=5
microphone_capture=14
geolocation=4
device_fingerprint=10
third_party_ip_lookup=1
periodic_upload=17
weak_default_credential=1
missing_expected_categories=0
```

产物：`static-audit.json`。退出码 0。审计器只读取文本并调用 `git rev-parse`，网络请求为 0，未导入或执行上游代码。

关键源码定位：

- `storm-web/assets/js/loc.js:1-55`：设备/浏览器指纹与第三方公网 IP 查询。
- `storm-web/templates/camera_temp/index.html:43-80`：摄像头请求、canvas 帧编码和周期 POST。
- `storm-web/templates/microphone/js/_app.js:26-40,48-75,99-133`：麦克风录制、导出和上传。
- `storm-web/assets/js/location.js:1-55`：高精度定位与成功/失败状态回传。
- `storm-web/receiver.php:8-17`：读取并清空结果文件。

## 实验 2：本地 Edge 权限与防护机制

实际命令：

```powershell
$env:PYTHONUTF8='1'; python -I "F:\reminder\storm_breaker_defense\exercise\run_browser_lab.py"
```

真实输出摘要：

```text
BROWSER_LAB status=DONE edge_exit=0
secure_context={'isSecureContext': True, 'protocol': 'http:', 'hostname': '127.0.0.1', 'loopback': True, 'mediaDevicesExposed': True, 'geolocationExposed': True}
permission_queries={'camera': {'supported': True, 'state': 'prompt', 'prompt_shown': False}, 'microphone': {'supported': True, 'state': 'prompt', 'prompt_shown': False}, 'geolocation': {'supported': True, 'state': 'prompt', 'prompt_shown': False}}
edge_exit_zero=PASS
script_done=PASS
loopback_secure_context=PASS
synthetic_denial=PASS
track_stopped=PASS
synthetic_geolocation_only=PASS
csp_blocked_canary=PASS
canary_never_reached_server=PASS
loopback_clients_only=PASS
loopback_requests=[{'method': 'GET', 'path': '/lab_page.html', 'client': '127.0.0.1'}, {'method': 'GET', 'path': '/favicon.ico', 'client': '127.0.0.1'}]
```

产物：`browser-results.json`、`browser-dom.html`、`browser-stdout.txt`、`browser-stderr.txt`。临时浏览器配置目录由 `TemporaryDirectory` 自动清理。

## 实验 3：确定性复核与清理验证

实际命令：

```powershell
$env:PYTHONUTF8='1'; python -I "F:\reminder\storm_breaker_defense\exercise\verify_defense.py"
```

最终真实输出：

```text
static_commit_pinned=PASS
static_all_indicator_classes_present=PASS
upstream_never_executed=PASS
no_real_sensor_or_location=PASS
loopback_secure_context=PASS
denial_branch_understood=PASS
cleanup_stops_track=PASS
network_canary_blocked=PASS
only_loopback_clients=PASS
local_server_stopped=PASS
temporary_browser_profiles_removed=PASS
RESULT=11/11 PASS
```

`verify_defense.py` 在浏览器实验结束后对原随机端口做连接探测，确认本地服务器已停止；同时确认没有遗留 `edge-defense-*` 临时目录。

## 证据哈希

实际执行 `Get-FileHash -Algorithm SHA256` 得到：

```text
995BD41B557A9103A7D2AB08A7F04D2C74DC6AACDAF1C92CBA081821652A9100  static-audit.json
BD205E55655A22C3C19DB644ECA4E6F153447F547D5F2E2C23E6738107DBC293  browser-results.json
7CEB6C3D325FD5BEA1A7C7791ADB4BDB1D13977EE60238322ED040C436217678  verification.json
```

这些哈希绑定当前文件版本；后续修改必须重算。

## 指南与 PDF 验证

- HTML：`storm-breaker-defense-guide.html`，含 Q1-Q10 十个疑问卡片和十张内联 SVG。
- Edge 无头打印后，首次立即重命名遇到异步落盘竞态，报错目标 PDF 尚不存在；随后确认文件已生成并完成改名，没有重复伪造输出。
- 最终 PDF：`storm_breaker_defense-小白指南.pdf`，876385 字节。
- 结构检查：`%PDF-1.4`、15 个页面对象、以 `%%EOF` 结束。
- PDF SHA-256：`A97A46A2D14DE1479D8D52C3440D29BC2029305CF68601D81FE2AE5A587ED2EC`。
- Edge 额外渲染 HTML 首屏到 `exercise/guide-preview.png`，已实际查看，中文、鲜艳配色和目录布局正常。
- 当前环境缺少 `pdftoppm`，Read 工具无法把 PDF 逐页转图；因此本 worker 不宣称已完成 PDF 逐页视觉审核，留待独立 reviewer。

## 限制与未完成项

- 这是单台 Windows 11、单 Edge 环境的本地机制实验，不是跨浏览器、移动平台、企业网络或检测覆盖率认证。
- 没有验证真实硬件授权提示、硬件指示灯、真实定位或实际恶意流量；这些都被有意排除在安全边界之外。
- Windows 官方支持页通过搜索获得，但直接 WebFetch 返回 404；指南已明确标注，不伪称抓取成功。
- 仅运行到 ready；review、release、Git、网站状态、publish/confirm-analysis 均由协调者按权限处理。
