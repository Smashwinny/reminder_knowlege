# AI Native 第三章教学实验日志

历史实验日期：2026-10-05 UTC

本公开副本保留原六条命令、执行时间、标准输出与结果；公开整理未重跑实验。练习包仅清理历史记录中的绝对工作路径，并同步包内清单，三个脚本、合成输入和实验结果未改。

## 结论

17 个用例符合预期，其中 16 个检验设计行为、1 个检验故意漏洞；正确路径拒绝后读取为 0，错误缓存路径撤销后读取为 1。29 条审计事件能关联用例；两套测试及新目录解压重放得到相同规范化结果，3 份夹具文件未改。

边界：没有实现真实认证、OAuth/MCP、凭证代理、Challenge 审批流或运行环境关闭检查；不证明操作系统隔离、同进程抗绕过、并发竞态、分布式缓存撤销、长连接终止或日志防篡改。后续新请求被拒绝，也不表示已返回内容能够被收回。

本程序独立编写，非官方阿里实现；不存在真实模型调用、真实用户批准、真实凭证或生产环境动作。17/17 是预设用例的断言满足，不是安全认证或性能证明。

## 原学习版本的练习包与精确重放

历史练习 ZIP：ai_native_handbook-exercise.zip。下面的大小与 SHA-256 仅属于原学习版本，不是当前公开副本的指纹。

字节：22515

SHA-256：85473907acbc09fb11f993880999d2f169efe814e6d1ac6fb5198f86f56a268f

作者将这个 ZIP 解压至此前不存在的新目录；解压根目录内没有 replay-results。逐条执行下述原样命令，六条退出码均为 0。输出目录是新建的，原证据未覆盖。

环境：Python 3.12.14；Linux。纯标准库。程序内部注入逻辑时钟；运行墙钟只用于留痕，不能当性能基准。

## 步骤 1 生成夹具并执行完整实验

完整命令：

```sh
python3 -B run_experiment.py --output replay-results
```

目的：建立 3 份虚构资料，以逻辑时钟演练读委托、收窄、过期、撤销和错误缓存，并自动运行两套新初始化的测试。

实际结果：17/17 符合预期：16 个预期设计用例，加 1 个故意不安全的缓存反例；两套规范化结果一致，3 份合成文件不变。

验证：输出须出现 CASES: 17/17、DETERMINISTIC_TWO_SUITES: True、SYNTHETIC_FILES_UNCHANGED: True；退出码 0。

开始：2026-10-05T07:39:27.257867+00:00

结束：2026-10-05T07:39:27.309159+00:00

退出码：0

标准输出：
```text
PASS 01_allowed_root_read reads=1 audit=1
PASS 02_narrow_child_only_reads_subset reads=1 audit=3
PASS 03_deny_other_task_context reads=0 audit=1
PASS 04_deny_other_runtime reads=0 audit=1
PASS 05_deny_other_task_resource reads=0 audit=1
PASS 06_deny_write reads=0 audit=1
PASS 07_deny_unknown_grant reads=0 audit=1
PASS 08_deny_at_exact_expiry reads=1 audit=2
PASS 09_deny_child_resource_expansion reads=0 audit=1
PASS 10_deny_child_action_expansion reads=0 audit=1
PASS 11_deny_child_expiry_extension reads=0 audit=1
PASS 12_revoke_parent_denies_new_root_read reads=1 audit=3
PASS 13_revoke_parent_denies_existing_child reads=1 audit=4
PASS 14_revoke_parent_denies_new_delegation reads=0 audit=2
PASS 15_untrusted_approval_text_does_not_authorize reads=0 audit=1
PASS 16_audit_correlates_actual_read_and_denial reads=1 audit=2
PASS 17_INTENTIONALLY_UNSAFE_stale_cache_negative_control reads=2 audit=3
CASES: 17/17
DETERMINISTIC_TWO_SUITES: True
SYNTHETIC_FILES_UNCHANGED: True
NORMALIZED_SUITE_SHA256: 3b06607940423ac1ef5b51f66efa5dd0040725734b183616189e68a786afbaef
NEGATIVE CONTROL: expected unsafe cached allow caused one post-revocation SYNTHETIC read.
LIMIT: application-level teaching model only; not an OS sandbox or enterprise security proof.
OVERALL_EXPECTATIONS_MET: True
```

标准错误：空

## 步骤 2 核对权限范围与有效期

完整命令：

```sh
python3 -B inspect_results.py --input replay-results --section scope
```

目的：从保存证据复核父读取、子集读取，以及任务、运行实例、资源、动作、委托、有效期与伪造批准文本的限制。

实际结果：范围检查覆盖 12 个用例；被拒绝的请求路径实际读取次数为 0。到期用例包含到期前一次允许读取，不能把整例总读取数误当拒绝后读取数。

验证：输出 PASS scope 与 PASS denied requests；同时可查看 cases.json 和 audit.jsonl 对照各项理由。

开始：2026-10-05T07:39:27.309174+00:00

结束：2026-10-05T07:39:27.345116+00:00

退出码：0

标准输出：
```text
PASS scope: 12 cases cover valid root/subset reads, task/runtime/resource/action/grant/expiry limits and untrusted approval text
PASS denied requests: zero actual file reads on denial paths
```

标准错误：空

## 步骤 3 核对父委托撤销

完整命令：

```sh
python3 -B inspect_results.py --input replay-results --section revocation
```

目的：确认已撤销根委托不能继续读、旧子委托不能继续读，也不能从已撤销父委托签发新子委托。

实际结果：三种撤销检查均满足预期；正确设计路径的撤销后读取次数为 0。

验证：输出 PASS revocation 和 intended-design post-revocation actual reads: 0；审计中撤销事件后的资源请求均拒绝。

开始：2026-10-05T07:39:27.345137+00:00

结束：2026-10-05T07:39:27.374920+00:00

退出码：0

标准输出：
```text
PASS revocation: new root read denied; existing child read denied; new child delegation denied
PASS intended-design post-revocation actual reads: 0
```

标准错误：空

## 步骤 4 观察故意错误的缓存反例

完整命令：

```sh
python3 -B inspect_results.py --input replay-results --section negative-control
```

目的：把只相信旧 allow 的错误路径与每次重新判定的路径对比，让撤销失效成为可见现象。

实际结果：出现预期漏洞：陈旧缓存导致撤销后仍读取 1 次合成文件。这一反例测试通过，表示成功暴露漏洞，不表示路径安全。

验证：输出 EXPECTED VULNERABILITY OBSERVED；case 17 标明 negative_control，post_revoke_reads 为 1。

开始：2026-10-05T07:39:27.374935+00:00

结束：2026-10-05T07:39:27.402784+00:00

退出码：0

标准输出：
```text
EXPECTED VULNERABILITY OBSERVED: stale cached allow caused 1 synthetic file read after revocation
This intentionally unsafe control must not be used as a security implementation
```

标准错误：空

## 步骤 5 对照决定与实际读取证据

完整命令：

```sh
python3 -B inspect_results.py --input replay-results --section audit
```

目的：检查任务、实例、委托、资源、策略、决定和原因能关联回每个请求，且审计读取数量与用例记录一致。

实际结果：每套有 29 条审计事件；拒绝、允许、委托、撤销均可检查。日志是普通 JSONL，不具备防篡改保证。

验证：输出 PASS audit: 29 events；保存的事件字段、序号和实际读取标记必须通过断言。

开始：2026-10-05T07:39:27.402800+00:00

结束：2026-10-05T07:39:27.429974+00:00

退出码：0

标准输出：
```text
PASS audit: 29 events correlate case/request/task/runtime/grant/resource/decision with actual IO
LIMIT: plain reviewable JSONL, not authenticated or tamper-proof audit storage
```

标准错误：空

## 步骤 6 核对可复现性与夹具指纹

完整命令：

```sh
python3 -B inspect_results.py --input replay-results --section reproducibility
```

目的：检查两次新初始化测试、规范化证据与当前三个合成文件，避免只看一串 PASS。

实际结果：两套结果相同，文件前后指纹和当前文件指纹一致；解压重放的规范化 SHA-256 与包内基线一致。

验证：输出 PASS reproducibility；规范化哈希应为 3b06607940423ac1ef5b51f66efa5dd0040725734b183616189e68a786afbaef。

开始：2026-10-05T07:39:27.429988+00:00

结束：2026-10-05T07:39:27.458152+00:00

退出码：0

标准输出：
```text
PASS reproducibility: two fresh suites matched; normalized evidence agrees; all 3 current fixture hashes match
NORMALIZED_SUITE_SHA256: 3b06607940423ac1ef5b51f66efa5dd0040725734b183616189e68a786afbaef
```

标准错误：空

## 两类计数不要混淆

到期或撤销用例常先读一次再拒绝一次，整例 file_reads=1 不能解释为拒绝后读了1次。应看 post_revoke_reads、各事件 decision 和 read_performed。负对照 case17 整例读取2次，其中撤销前1次、撤销后1次。

正确设计的拒绝路径不进入读取；负对照故意先命中旧缓存而漏查撤销，必须保留为错误示范。

## 规范化证据

SHA-256：3b06607940423ac1ef5b51f66efa5dd0040725734b183616189e68a786afbaef

两套新初始化测试结果一致；作者解压重放与包内 verified-results 的规范化证据一致。逻辑时钟使测试稳定，真实墙钟时间没有放进规范化比较。

夹具前后 SHA-256：
```json
{
  "before": {
    "task-a-notes.txt": "baccc157ebcf13e3a3c0bfa82f9caf51a55c014aa9ac7375f0ae2b5736ced7f0",
    "task-a-appendix.txt": "7409437067f33554e4f862cc455a4219bef7df9f8b3a7cad385b9ca5af5f69df",
    "task-b-notes.txt": "cf2393438d9b0063f38e054a29563db2809cda204d1a4a36828bf99dd55e4cff"
  },
  "after": {
    "task-a-notes.txt": "baccc157ebcf13e3a3c0bfa82f9caf51a55c014aa9ac7375f0ae2b5736ced7f0",
    "task-a-appendix.txt": "7409437067f33554e4f862cc455a4219bef7df9f8b3a7cad385b9ca5af5f69df",
    "task-b-notes.txt": "cf2393438d9b0063f38e054a29563db2809cda204d1a4a36828bf99dd55e4cff"
  }
}
```

## 当前公开练习包

当前公开 ZIP：22691 字节；SHA-256：b819bbff400c4342141a2393a83fec096ba67f5f8baa53fb348c1942939c4bb3。

执行记录中的 cwd 已改为解压根目录的相对表示 `.`；历史命令和输出未改。代码、合成资源与 verified-results 全部保留原字节。公开副本的完整文件映射与检查结论见配套独立发布审核日志。

## 包内原始证据

verified-results/ 包含 cases.json、audit.jsonl、normalized-suite.json、summary.json、stdout.txt 和三个虚构资源。execution-record.json 与 execution-transcript.txt 记录来源研究者首次六条命令的真实执行；该轮输出目录叫 verified-results，作者按本指南命令使用新目录 replay-results。

## 未实现和未外推的事项

- 没有运行环境关闭、父委托更新后旧子委托复活、静态路径逃逸、真实 Challenge 批准流用例
- 没有阻止恶意同进程代码绕过包装器或修改注册表/日志
- 没有验证并发 TOCTOU、符号链接竞态、跨服务撤销传播、真实会话终止、崩溃恢复
- 未执行官方 OpenSandbox/OpenCode 示例；未测试产品功能、价格、性能或企业级安全
- 普通 JSONL 与文件哈希提供可核对线索，不构成真实性或不可篡改证明

## 资料与版面检验范围

官方 PDF 第三章全部29页逐页视觉阅读。指南 PDF 由 ReportLab 直接生成，使用 STSong-Light CJK CID 字体引用，不在文件中嵌入字体文件；本次 Poppler 渲染需逐页视觉检查。其他阅读器可能进行字体替换。HTML 只做结构校验。原 HTML 浏览器视觉预览与 HTML 到 PDF 路线因环境限制未完成，本次未重试；不得把直接生成 PDF 的渲染通过当成 HTML 浏览器验收通过。

原学习独立复验还记录了 19 次资源请求、8 次真实合成文件读取、所有拒绝路径读取为 0、故意错误缓存路径撤销后读取为 1；这些是历史复验记录，不是本次新增实验。当前公开副本的独立审核结果见第六份 ai_native_handbook-review-log.md；作者重放不替代独立审核。