---
tags: [项目笔记, OSINT, HTTP, 公开信息]
领域: OSINT / HTTP 状态推断
来源项目: "https://github.com/sherlock-project/sherlock"
实测版本: "0.16.2 / e40a45e"
---

# sherlock_osint

## 这是什么

Sherlock 是一个 Python CLI：把用户名代入站点清单中的公开资料页或探测端点，并发请求后用站点特定的 `status_code`、`message`、`response_url` 规则给出 `Claimed`、`Available`、`Unknown`、`ILLEGAL`、`WAF` 等结果，并可导出 TXT、CSV、XLSX。

**命中只表示某个公开 URL 符合规则，不证明同名账户属于同一人；未命中也不证明用户名可注册。** 关联 [[AI味模式库与信号非证据]]、[[可逆派生状态]]、[[事实与判断分离]]。

## 来源边界

原始记录是 `https://x.com/Caijingtianxia/status/2101193075976802508`。直接页面、oEmbed 与公开 syndication 均未取得可核验正文和出链，因此不能证明原帖目标就是 Sherlock。经用户明确授权，本次把候选 `sherlock-project/sherlock` 作为独立学习对象；指南和实验不冒充原帖已证实。

## 学到的核心机制

- 清单字段：`url`、`urlMain`、可选 `urlProbe`、`regexCheck`、`errorType`、`errorMsg` / `errorCode`、请求方法与 payload。
- 默认请求：`status_code` 多用 HEAD；需要正文的其他判定用 GET；`response_url` 禁止跟随重定向。
- 请求池上限为 20 个 worker；`--timeout` 是等待上限，不是站点级限速或 `Retry-After` 退避。
- 输出：CSV 可保留用户名、站点、URL、判定、HTTP 状态和耗时；配合 `--print-all` 才能保留非命中行，便于审计。
- 429、WAF、软 404、超时和规则陈旧都会造成误报或漏报，不能将结果压成“找到/没找到”两态。

## 真实实验

全部账户探测使用 `127.0.0.1:8765` 本地桩，未枚举第三方账户。最终通过：

- 26 条主 CSV 判定与本地真值一致；
- 同一慢响应在 0.4 秒 timeout 下为 `Unknown`，2 秒下为 `Claimed`；
- 27 次账户探测均按本地夹具定义发出，非法用户名 `bad name` 零请求；
- 429 下 `status_code=Available`、`message=Claimed`，直接展示规则导致的相反结论；
- WAF、404、302、200 错误文案、HEAD/GET 与超时分支均有原始日志。

证据：`sherlock_osint/exercise/experiment-log.md`、`verification.txt`、`request-log.jsonl`、`results/`、`results-timeout-04/`、`results-timeout-2/`。

## 坑与结论

1. `Available` 可能只是“非 2xx”，429 也会落入此分支；它不是可用性证明。
2. `message` 规则只要没看到指定错误文案就可能报 `Claimed`，限流页或软 404 会变成误报。
3. timeout 不是越大越好也不是越小越好；它改变可观察证据窗口，A/B 中直接改变结果。
4. 输出文件用于保存线索，不是身份结论；自查时应保留原始状态并人工复核自己的公开页面。
5. 本次只验证本地受控行为，没有验证真实站点当前覆盖率、准确率、站点条款或账户归属。

## 知识关联与待合并

与 [[健康探测三态]] 的“执行探测而不是猜”相通，与 [[证据优先质检ProofOverClaims]] 的“保留可定位证据”相通。候选新概念“用户名公开页探测”及既有概念补强见 `sherlock_osint/sherlock_osint-knowledge-proposal.md`，由协调者查重合并；worker 未修改概念笔记或总览。
