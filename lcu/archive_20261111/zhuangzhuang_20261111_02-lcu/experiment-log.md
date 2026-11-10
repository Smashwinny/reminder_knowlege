# LCU真实学习实验日志

时间：Asia/Shanghai（UTC+8）。真实执行进程与MCP交互；桌面对象是自编内存模拟，不冒称OpenAI运行时。未访问账户、密钥、真实窗口或权限配置。

## 发现与取证记录
- git ls-remote知识库main：a8674777e18302b8804b137212b1396cbfe5a747，未变化；复用旧快照，只读。
- git clone --depth 1 --branch main https://github.com/amontlabs/lcu /workspace/learn-batch/02-lcu/upstream：退出0；HEAD a7e30c1862707214dfe748d410854771ab4f4494。
- 初次试读根package.json、VERSION、bundle.json与lib目录不存在；是路径探测错误，不据此判项目缺失。实际包元数据在adapters/package.json。
- urllib下载引用配图首试HTTP403，ffmpeg因视频尚未下载失败；普通公共curl取回相同素材成功。视频30.058667秒，仅抽样六帧阅读；未声称连续观看或听音轨。

## 2026-11-11T01:15:55.422333+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
python3 demo.py baseline
```

真实输出：
```text
系统 Linux-6.12.113+-x86_64-with-glibc2.41 Python 3.13.5 Node v24.22.1
PASS 上游原样副本 adapters/host-guard.mjs "5b8360ae81517ae15277d564fff32b4195e350becba0880b6e98c8d84ddc01bc"
PASS 上游原样副本 adapters/test/host-guard.test.mjs "e954ce902ac762d7a178e73eae3f42ad2f454e64ccd85d3fb23e2db7825fe9bc"
PASS 上游原样副本 tests/mcp_client.py "014d97a4a7b760f7aa7584f0e8aec861979904f84fc23be73855f524ff2360eb"
PASS 上游原样副本 LICENSE "7fff04d38b9a70f51822eb46ad6ee390ef505932f36429a5be54ec78c212581c"
PASS 当前README已明确不需要Python null
PASS 不触发原始LCU安装或运行 "实验只启动mock_mcp.mjs，不导入LCU启动器、不读取ChatGPT目录"
本组命名检查：6 PASS；不是完整MCP合规或真实桌面验收。

```
退出码：0

## 2026-11-11T01:15:55.515426+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
python3 demo.py protocol
```

真实输出：
```text
PASS 固定协议版本 "2025-11-25"
PASS 初始化说明传回 "只操作模拟记事本；同步JS变量跨调用保留。js_reset不撤销文档。不接入真实桌面。"
PASS 公开工具恰好两个 ["js", "js_reset"]
PASS 工具schema为对象 null
PASS ping返回空对象 null
PASS 模拟桌面明确非实机 null
本组命名检查：6 PASS；不是完整MCP合规或真实桌面验收。

```
退出码：0

## 2026-11-11T01:15:55.607719+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
python3 demo.py state
```

真实输出：
```text
PASS 首次JS返回值 42
PASS 跨调用保留变量 41
PASS 先发现模拟应用 "demo.notes"
PASS 单次调用组合读写保存 {"kind": "SIMULATED_APP", "appId": "demo.notes", "text": "学习MCP", "saved": true, "revision": 1, "cursor": {"x": 0, "y": 0}, "elements": [{"id": "editor", "role": "textbox"}, {"id": "save", "role": "button", "name": "保存"}]}
PASS 后续调用复用app句柄 null
PASS 截图仅模拟元数据 {"kind": "SYNTHETIC_DESCRIPTOR", "actualCapture": false, "width": 800, "height": 600, "note": "仅模拟元数据，无真实截图像素"}
本组命名检查：6 PASS；不是完整MCP合规或真实桌面验收。

```
退出码：0

- 初次生成脚本末尾漏import json，进度JSON写入NameError；此前模拟器与驱动文件已写出，修复生成器后恢复。基线范围声明不算命名检查，修正后重新跑基线为5项。

## 2026-11-11T01:16:15.523531+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
python3 demo.py baseline
```

真实输出：
```text
系统 Linux-6.12.113+-x86_64-with-glibc2.41 Python 3.13.5 Node v24.22.1
PASS 上游原样副本 adapters/host-guard.mjs "5b8360ae81517ae15277d564fff32b4195e350becba0880b6e98c8d84ddc01bc"
PASS 上游原样副本 adapters/test/host-guard.test.mjs "e954ce902ac762d7a178e73eae3f42ad2f454e64ccd85d3fb23e2db7825fe9bc"
PASS 上游原样副本 tests/mcp_client.py "014d97a4a7b760f7aa7584f0e8aec861979904f84fc23be73855f524ff2360eb"
PASS 上游原样副本 LICENSE "7fff04d38b9a70f51822eb46ad6ee390ef505932f36429a5be54ec78c212581c"
PASS 当前README已明确不需要Python null
范围声明：仅启动mock_mcp.mjs，不导入LCU启动器、不读取ChatGPT目录；这不是安全隔离证明。
本组命名检查：5 PASS；不是完整MCP合规或真实桌面验收。

```
退出码：0

## 2026-11-11T01:16:15.628384+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
python3 demo.py reset
```

真实输出：
```text
PASS 重置前变量存在 null
PASS reset返回成功 null
PASS reset清空JS变量 null
PASS reset不撤销外部模拟文档 "A"
PASS 半程失败带isError {"content": [{"type": "text", "text": "{\"error\":\"故障注入\",\"rollback\":false}"}], "isError": true}
PASS 错误不回滚文档 "AB"
PASS 盲重试产生重复副作用 "ABB"
本组命名检查：7 PASS；不是完整MCP合规或真实桌面验收。

```
退出码：0

## 2026-11-11T01:16:15.883068+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
python3 demo.py negative
```

真实输出：
```text
PASS 初始化前拒绝工具 null
PASS 协议版本不支持明确拒绝 null
PASS 畸形JSON产生解析错误 null
PASS 未知方法错误 null
PASS 未知工具拒绝 null
PASS 缺code参数拒绝 null
PASS 模拟白名单拒绝未知App null
PASS 模拟坐标越界拒绝 null
PASS 同步循环80ms超时为工具错误 {"content": [{"type": "text", "text": "{\"error\":\"Script execution timed out after 80ms\",\"rollback\":false}"}], "isError": true}
PASS 超时后仍可执行 4
PASS console日志不污染stdout 7
PASS 另一进程看不到JS变量 null
PASS 真实stderr捕获日志 "模拟日志：只进stderr\n模拟服务stdin已关闭，正常退出"
本组命名检查：13 PASS；不是完整MCP合规或真实桌面验收。

```
退出码：0

## 2026-11-11T01:16:15.988600+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
python3 demo.py upstream
```

真实输出：
```text
PASS 上游轻客户端握手互通 null
PASS 上游客户端发现两个工具 null
PASS 上游客户端跨调用状态 null
PASS 上游客户端接收isError null
本组命名检查：4 PASS；不是完整MCP合规或真实桌面验收。

```
退出码：0

## 2026-11-11T01:16:16.110474+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
node --test vendor/adapters/test/host-guard.test.mjs
```

真实输出：
```text
✔ appBundleOf returns the outermost app bundle (0.747189ms)
✔ findHostApps collects ancestor bundles and skips the runtime own bundle (1.742586ms)
✔ findHostApps uses the outer bundle of a nested helper process (0.175113ms)
✔ findHostApps returns nothing for missing processes, cycles, absent bundle ids and plain chains (0.241095ms)
✔ known agent hosts and the detected host are refused, other apps are not (0.595453ms)
✔ the escape hatch disables the guard only when set to 1 (0.177411ms)
✔ declineAgentHostApp answers decline only for native-app approvals of agent hosts (0.673994ms)
ℹ tests 7
ℹ suites 0
ℹ pass 7
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 62.024947

```
退出码：0

## 2026-11-11T01:17:17.570058+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu`

```sh
git ls-remote https://github.com/Smashwinny/reminder_knowlege refs/heads/main
```

真实输出：
```text
a8674777e18302b8804b137212b1396cbfe5a747	refs/heads/main

```
退出码：0

## 2026-11-11T01:17:17.931327+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu`

```sh
git ls-remote https://github.com/amontlabs/lcu refs/heads/main
```

真实输出：
```text
a7e30c1862707214dfe748d410854771ab4f4494	refs/heads/main

```
退出码：0

## 2026-11-11T01:17:17.962377+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/upstream`

```sh
git log -1 --format=%H%n%cI%n%s
```

真实输出：
```text
a7e30c1862707214dfe748d410854771ab4f4494
2026-11-10T12:24:21+01:00
docs(release): add 0.13.6 release notes with archive checksums

```
退出码：0

## 2026-11-11T01:20:12.481487+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu`

```sh
python3 _tools/render_pdf.py 'LCU-状态化MCP学习指南.html' 'LCU-状态化MCP学习指南.pdf'
```

真实输出：
```text
命令： ['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--timeout=15000', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/02-lcu/render-profile', '--print-to-pdf=/workspace/learn-batch/02-lcu/LCU-状态化MCP学习指南.pdf', 'file:///workspace/learn-batch/02-lcu/LCU-%E7%8A%B6%E6%80%81%E5%8C%96MCP%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.html']
[1111/011927.476769:WARNING:chrome/app/chrome_main_linux.cc:84] Read channel stable from /opt/google/chrome/CHROME_VERSION_EXTRA
[201096:201119:1111/011927.513044:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[201096:201119:1111/011927.535478:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[201096:201119:1111/011927.535538:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[201096:201119:1111/011927.535558:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[201096:201119:1111/011927.716955:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[201096:201119:1111/011927.716984:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[201096:201096:1111/011927.728191:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: unknown error type: 
Created TensorFlow Lite XNNPACK delegate for CPU.
Traceback (most recent call last):
  File "/workspace/learn-batch/02-lcu/_tools/render_pdf.py", line 7, in <module>
    print('命令：',cmd,flush=True);r=subprocess.run(cmd,timeout=45,env={**os.environ,'FONTCONFIG_FILE':'/etc/fonts/fonts.conf','FONTCONFIG_PATH':'/etc/fonts'});raise SystemExit(r.returncode)
                                     ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 556, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
                     ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1222, in communicate
    stdout, stderr = self._communicate(input, endtime, timeout)
                     ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 2154, in _communicate
    self.wait(timeout=self._remaining_time(endtime))
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1280, in wait
    return self._wait(timeout=timeout)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 2058, in _wait
    raise TimeoutExpired(self.args, timeout)
subprocess.TimeoutExpired: Command '['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--timeout=15000', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/02-lcu/render-profile', '--print-to-pdf=/workspace/learn-batch/02-lcu/LCU-状态化MCP学习指南.pdf', 'file:///workspace/learn-batch/02-lcu/LCU-%E7%8A%B6%E6%80%81%E5%8C%96MCP%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.html']' timed out after 45 seconds

```
退出码：1

## 2026-11-11T01:20:30.573912+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu`

```sh
python3 _tools/render_pdf.py 'LCU-状态化MCP学习指南.html' 'LCU-状态化MCP学习指南.pdf'
```

真实输出：
```text
命令： ['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--timeout=15000', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/02-lcu/render-profile', '--print-to-pdf=/workspace/learn-batch/02-lcu/LCU-状态化MCP学习指南.pdf', 'file:///workspace/learn-batch/02-lcu/LCU-%E7%8A%B6%E6%80%81%E5%8C%96MCP%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.html']
[1111/012029.728641:WARNING:chrome/app/chrome_main_linux.cc:84] Read channel stable from /opt/google/chrome/CHROME_VERSION_EXTRA
[204328:204349:1111/012029.770385:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[204328:204349:1111/012029.793329:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[204328:204349:1111/012029.793487:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[204328:204349:1111/012029.793646:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[204328:204349:1111/012029.940165:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[204328:204349:1111/012029.940210:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[204328:204328:1111/012029.948470:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: unknown error type: 
Created TensorFlow Lite XNNPACK delegate for CPU.
1048127 bytes written to file /workspace/learn-batch/02-lcu/LCU-状态化MCP学习指南.pdf

```
退出码：0

## 2026-11-11T01:21:07.902722+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu/exercise`

```sh
python3 verify_vendor.py
```

真实输出：
```text
PASS 上游原样文件SHA256 adapters/host-guard.mjs 5b8360ae81517ae15277d564fff32b4195e350becba0880b6e98c8d84ddc01bc
PASS 上游原样文件SHA256 adapters/test/host-guard.test.mjs e954ce902ac762d7a178e73eae3f42ad2f454e64ccd85d3fb23e2db7825fe9bc
PASS 上游原样文件SHA256 tests/mcp_client.py 014d97a4a7b760f7aa7584f0e8aec861979904f84fc23be73855f524ff2360eb
PASS 上游原样文件SHA256 LICENSE 7fff04d38b9a70f51822eb46ad6ee390ef505932f36429a5be54ec78c212581c
仅校验随包副本与已记录哈希；不是远程签名认证。

```
退出码：0

## 主实验结论与证据边界
六组最终命名检查：baseline5、protocol6、state6、reset7、negative13、upstream4，共41项通过；另上游host-guard7/7通过。补充便携校验4个文件哈希通过，不计入41。41中包含源文件/文档断言，不是41次桌面操作。

原始Git提交时间换算：2026-11-10 19:24:21 Asia/Shanghai（原始输出偏移+01:00）。所有本地日志时间是Asia/Shanghai。

PDF首次45秒超时后，用完全相同默认沙箱命令重试成功；12页A4，已pdftoppm逐页导图并Read检查12/12，见pdf-review.md。首次超时不是原始运行时失败。

未执行：官方应用安装/启动/登录、账户/密钥访问、真实AX/截图、鼠标键盘、宿主配置或安全设置；引用图片的自动放行/白名单建议未采纳。宿主生命周期和真实平台/GUI验收均待验证。

## 2026-11-11T01:23:22.133132+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/02-lcu`

```sh
python3 _tools/validate_artifacts.py
```

真实输出：
```text
{
  "访问日期": "2026-11-11 Asia/Shanghai",
  "问答数": 12,
  "内联SVG数": 13,
  "PDF页数": 12,
  "逐页Read检查": 12,
  "PDF文本字符数": 10768,
  "替换字符数": 0,
  "各组命名检查": {
    "baseline": 5,
    "protocol": 6,
    "state": 6,
    "reset": 7,
    "negative": 13,
    "upstream": 4
  },
  "命名检查总数": 41,
  "上游纯测试数": 7,
  "PDF中文字体": "NotoSansCJKsc已嵌入，Unicode映射存在",
  "证据边界": "无原始运行时/真实GUI，无完整MCP合规或安全审核"
}

```
退出码：0

## 交付包装
执行 `python3 _tools/package_deliverables.py`：LCU-exercise.zip含29个条目，Python zipfile.testzip()为None（CRC全通过）。仅打包本项目录的公开来源、合成实验与交付；排除render-profile、__pycache__及完整Git。
