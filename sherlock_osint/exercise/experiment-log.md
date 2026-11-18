# Sherlock 本地桩实验记录

- task_id：`1414100f-ce46-4b2d-9c34-e87a98dd7b05`
- owner：`main-k3-w6`
- 上游：`https://github.com/sherlock-project/sherlock`
- 实测提交：`e40a45e`（`Merge pull request #3143 from Londopy/fix-logo-link`）
- 包版本：`Sherlock v0.16.2`
- 环境：Windows 11，Python 3.14.7，`exercise/.venv`
- 最终请求日志时段：2026-10-31T05:02:33Z 至 05:02:49Z
- 边界：全部账户探测 URL 指向 `127.0.0.1:8765`；用户名均为虚构本地夹具，没有查询或枚举第三方账户。

## 1. 环境实测

执行：

```bash
python --version
python -m venv /f/reminder/sherlock_osint/exercise/.venv
PYTHONUTF8=1 /f/reminder/sherlock_osint/exercise/.venv/Scripts/python.exe -m pip install --disable-pip-version-check -e /f/reminder/sherlock_osint/repo
PYTHONUTF8=1 NO_PROXY=127.0.0.1,localhost /f/reminder/sherlock_osint/exercise/.venv/Scripts/sherlock.exe --version
```

实际结果：Python `3.14.7`；依赖安装退出码 0；版本输出 `Sherlock v0.16.2`。

## 2. 环回桩与输入

`local_stub.py` 只绑定 `127.0.0.1`，实现 200、404、302、429、403 WAF 指纹和约 1.2 秒慢响应。`local_sites.json` 定义六种本地目标，覆盖 `status_code`、`message`、`response_url`、正则、超时与 WAF。

服务启动后执行：

```bash
curl --noproxy '*' --fail --silent http://127.0.0.1:8765/health
```

实际输出：`OK`。

## 3. 主测试命令

```bash
PYTHONUTF8=1 NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost /f/reminder/sherlock_osint/exercise/.venv/Scripts/sherlock.exe --json /f/reminder/sherlock_osint/exercise/local_sites.json --timeout 0.4 --print-all --no-color --csv --txt --folderoutput /f/reminder/sherlock_osint/exercise/results learner_demo missing_demo limited_demo slow_demo
```

完整终端输出保存在 `cli-main.txt`。关键实际结果：

| 本地用户名 | 站点规则 | HTTP | Sherlock 判定 | 说明 |
|---|---|---:|---|---|
| learner_demo | LocalStatus / Message / Redirect | 200 | Claimed | 三种基本命中路径 |
| missing_demo | LocalStatus | 404 | Available | 状态码未命中 |
| missing_demo | LocalMessage | 200 + PROFILE_NOT_FOUND | Available | 200 不等于账户存在 |
| missing_demo | LocalRedirect | 302 | Available | 禁止跟随重定向后判定 |
| missing_demo | LocalWaf | 404 + NOT_FOUND | Claimed | 本地真值为不存在，正文未含指定 errorMsg，形成误报 |
| limited_demo | LocalStatus | 429 | Available | 本地真值为存在但被限流，形成漏报 |
| limited_demo | LocalMessage | 429 + RATE_LIMIT | Claimed | 结果碰巧符合真值，但“未见 errorMsg”不是可靠依据 |
| limited_demo | LocalRedirect | 429 | Available | 非 2xx 被判 Available |
| slow_demo | 六个本地站点 | 客户端超时 | Unknown | 终端显示 Timeout Error |

`limited_demo.csv` 的原始终端外证据还显示：同一 429 下 `LocalStatus=Available`、`LocalMessage=Claimed`、`LocalRedirect=Available`。

## 4. WAF 与非法用户名

执行：

```bash
PYTHONUTF8=1 NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost /f/reminder/sherlock_osint/exercise/.venv/Scripts/sherlock.exe --json /f/reminder/sherlock_osint/exercise/local_sites.json --site LocalWaf --timeout 2 --print-all --no-color --csv --txt --folderoutput /f/reminder/sherlock_osint/exercise/results waf_demo
PYTHONUTF8=1 NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost /f/reminder/sherlock_osint/exercise/.venv/Scripts/sherlock.exe --json /f/reminder/sherlock_osint/exercise/local_sites.json --site LocalRegex --timeout 2 --print-all --no-color --csv --txt --folderoutput /f/reminder/sherlock_osint/exercise/results "bad name"
```

实际输出：WAF 行为 `Blocked by bot detection`；非法用户名行为 `Illegal Username Format For This Site!`。请求日志没有任何用户名为 `bad name` 的 HTTP 请求，证明正则分支在发请求前终止。

## 5. timeout A/B

对同一个 `slow_demo`、同一个 `LocalSlow`、同一个约 1.2 秒响应，只改变 `--timeout`：

```bash
PYTHONUTF8=1 NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost /f/reminder/sherlock_osint/exercise/.venv/Scripts/sherlock.exe --json /f/reminder/sherlock_osint/exercise/local_sites.json --site LocalSlow --timeout 0.4 --print-all --no-color --csv --folderoutput /f/reminder/sherlock_osint/exercise/results-timeout-04 slow_demo
PYTHONUTF8=1 NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost /f/reminder/sherlock_osint/exercise/.venv/Scripts/sherlock.exe --json /f/reminder/sherlock_osint/exercise/local_sites.json --site LocalSlow --timeout 2 --print-all --no-color --csv --folderoutput /f/reminder/sherlock_osint/exercise/results-timeout-2 slow_demo
```

实际输出保存于 `cli-timeout-ab.txt`：0.4 秒为 `Timeout Error`，2 秒为命中。CSV 进一步确认：0.4 秒为 `Unknown,?`；2 秒为 `Claimed,200`，响应时间约 `1.2040351` 秒。

## 6. 自动验收

执行：

```bash
PYTHONUTF8=1 /f/reminder/sherlock_osint/exercise/.venv/Scripts/python.exe -I /f/reminder/sherlock_osint/exercise/verify_results.py
```

`verification.txt` 最终原文：

```text
PASS: 26 CSV verdicts match local ground truth
PASS: timeout A/B changed slow_demo from Unknown (0.4s) to Claimed (2s)
PASS: 27 probes were emitted only by the loopback fixture
PASS: 429, HEAD/GET, timeout, WAF and zero-request ILLEGAL cases verified
```

计数口径：26 条主 CSV 判定，另有 2 条 timeout A/B CSV 判定；27 次账户探测请求，另有 1 次健康检查。`request-log.jsonl` 共 28 条有效事件。实验结束后本地服务已停止，健康检查超时确认端口不再响应。

## 限制

本地桩证明的是此提交在受控输入下的判定行为，不证明任何真实站点当前规则、覆盖率或准确率，也不证明同名账户属于同一人。CLI 的更新检查和排除列表元数据请求不计入上述账户探测数。本实验没有测试 Tor/代理绕过、真实第三方站点、批量用户名、NSFW 目标或任何攻击行为。
