# OpenMuse 历史核心实验日志

公开副本说明：保留 2026-10-05 历史实验，本次整理未安装依赖或重跑测试。原始绝对路径以 <EXERCISE_DIR>、<REVIEW_EXERCISE_DIR> 和 <NODE_RUNTIME> 表示位置角色；命令参数、输出、错误、时间、耗时、用例和结果保持不变。

日期：2026-10-05 UTC
固定提交：b06caad7005ac5b6d2b451752a3794a6ae1759c1
来源：https://github.com/CopilotKit/openmuse/tree/b06caad7005ac5b6d2b451752a3794a6ae1759c1

## 结论先读

原始选取测试21项通过（12审批+8引擎+1持久化），独立编写变式4项通过，失败0。四组测试退出0，NETWORK_GUARD attempts=0。独立审核者对最终ZIP执行六组文档命令并重跑同25项，全部通过；不把复跑数量累加为新的测试覆盖。

真实执行：上游SQL Store、PGlite、ActionService、TaskWorker。受控输入：提供方execute/prepare、连接判断、任务处理器、模拟时钟。仅同进程竞争，正常close/reopen；未测跨进程PostgreSQL、强杀/断电、真实Google/模型/浏览器/Docker/E2B。版本fixture验证旧版本转交，不是HTTP ETag冲突实测。

## 环境与来源

本环境为Linux，Node v24.19.0、npm 11.9.0、Python3、Bash。核心依赖为PGlite 0.3.16、pg 8.23.0、zod 4.6.5，含传递依赖共16项，版本及完整性与固定上游锁一致。TypeScript转换使用Node实验特性，警告保留。

历史原始练习ZIP为211031字节，SHA-256为714ca8560289c4ec076a6b0ecb87a6c40b921fadd12c62cec89142d878994157，37成员。独立审核者核对36项内嵌成员摘要及15项上游原件指纹，确认PGlite/pg/zod从新解压目录的本地依赖解析。ZIP不含node_modules、缓存或临时数据库；保留MIT原许可证。

## 2026-10-05 实际执行的六组文档命令

### 1. 先核对版本与材料

```bash
node --version; npm --version; python3 verify-exercise.py
```

目的：确认运行时版本、原始源码复制件和依赖锁一致，先把“跑的是谁”说清楚。

时间：独立审核者从最终ZIP新目录解压后的同命令复跑：2026-10-05 11:51:11 UTC；相关命令均退出0。

结果：源文件核验15项，锁文件依赖16项。Node v24.19.0，npm 11.9.0。

验证：两项检查均输出 OK 且最终退出码为0；verify脚本逐项比对SHA-256和上游锁的依赖完整性。

失败判据：任一文件摘要或依赖完整性不一致都停止；不要略过检查继续跑。

### 2. 只装核心所需依赖

```bash
bash install-deps.sh; python3 verify-exercise.py
```

目的：从官方npm仓库安装固定16项依赖，禁用生命周期脚本；不装整个应用。

时间：独立审核者从最终ZIP新目录解压后的同命令复跑：2026-10-05 11:51:26 至 11:51:33 UTC，安装约7秒；相关命令均退出0。

结果：安装脚本采用npm ci并读取随包lock；不加载用户npm配置，保留平台代理与证书变量，未关闭证书校验。

验证：安装退出码为0，随后源码与锁核验通过。安装阶段需可访问npm仓库；测试阶段无需网络或账号。

失败判据：网络、代理、证书或锁文件问题应保留报错并修复原因；不能用关闭TLS校验绕过。初次准备经历配置冲突、DNS与证书问题，完整记录在日志。

### 3. 验证审批的拒绝与一次领取

```bash
bash run-core.sh actions
```

目的：运行原样上游actions.test.ts，覆盖拒绝、错拥有者、旧hash、到期、断连、换账号、并发批准和未知结果等。

时间：独立审核者从最终ZIP新目录解压后的同命令复跑：2026-10-05 11:51:48 至 11:51:49 UTC；相关命令均退出0。

结果：12个原始审批测试通过。真实ActionService和PGlite执行；execute、prepare、connected等是受控fixture。

验证：检查rawlogs/03-original-actions.log中的12pass、0fail、退出码0；并发批准断言fixture调用1次，拒绝类断言不调用。

失败判据：任何断言失败或网络guard尝试非0都需要调查。版本测试只检查保存版本转交fixture，不代表真实HTTP If-Match或Google写入。

### 4. 看两个执行器如何争抢与取消

```bash
bash run-core.sh engine; cat rawlogs/04-original-engine.log
```

目的：运行原样任务引擎测试，观察领取竞争、取消前守卫、恢复保存状态、调度和审批公平性。

时间：独立审核者从最终ZIP新目录解压后的同命令复跑：2026-10-05 11:51:58 至 11:52:04 UTC；相关命令均退出0。

结果：8个原始引擎测试通过。双Worker共享同一个PGlite；取消测试在效果前调用guard，效果计数保持0。

验证：日志应为8pass；原始测试断言一次领取、保存state读回、run开始时间，以及写运行记录失败后worker.stop能完成且任务标为failed。

失败判据：这是同进程Worker对象竞争；不是多进程数据库或分布式故障验收。自定义处理器若不调用守卫，不能套用取消保护结论。

### 5. 关闭数据库再打开

```bash
bash run-core.sh persistence; cat rawlogs/05-original-persistence.log
```

目的：对真实嵌套目录PGlite检查持久记录和中断动作恢复，不依赖内存字典。

时间：独立审核者从最终ZIP新目录解压后的同命令复跑：2026-10-05 11:52:16 至 11:52:18 UTC；相关命令均退出0。

结果：只选择名称含fresh nested data directory的1项原始测试。22项源码测试定义中，本轮选21项；另一项PostgreSQL池错误测试未选择。

验证：run-core明确加入--test-name-pattern="fresh nested data directory"；测试close/reopen后调用recoverInterruptedActions，断言留存executing转为outcome_unknown。

失败判据：Node此次报告skipped=0，不能凭排除1项改写成skipped=1。该实验正常关闭再打开，不是进程强杀、断电或崩溃耐久性测试。

### 6. 改输入和时间 观察边界变化

```bash
bash run-core.sh characterization; cat rawlogs/06-changed-input-characterization.log; python3 verify-exercise.py
```

目的：运行独立编写的4个变式：新键改内容、同键改内容、未知结果重开、虚拟时钟触发接管。

时间：独立审核者从最终ZIP新目录解压后的同命令复跑：2026-10-05 11:52:28 至 11:52:32 UTC；相关命令均退出0。

结果：4个新增变式通过：新键改主题令hash变化；同键改主题返回原提案；未知结果重开后仍不重放；推进60001ms后新Worker接管，旧checkpoint和下一守卫效果被拒绝。

验证：查看完整OBSERVATION行；检查旧checkpoint被拒绝、新处理器1次、总领取2次、最终结果new_worker，最后再次验证源码与依赖未变。

失败判据：这些是刻意编写的边界刻画，不是上游新增官方测试。虚拟时钟与注入提供方属于受控输入；不能声称真实服务曾超时或真实等待60秒。

## 初始环境恢复过程

第一次npm配置将userconfig与globalconfig同时设为/dev/null，npm因重复加载配置而退出1。改用练习目录中两个独立空配置文件；没有加载用户npm凭据。

随后过度清理环境导致依赖下载出现DNS/连接失败；其短stdout日志为空，另保留npm debug日志。恢复平台代理变量后，又因缺少平台CA变量出现UNABLE_TO_VERIFY_LEAF_SIGNATURE。最终仅保留正常平台代理和证书环境，安装成功；未关闭TLS校验、未全局改配置。依赖安装使用官方npm仓库、关闭生命周期脚本。原始准备采用npm install生成随包lock；独立复跑采用npm ci。

原始核心入口实际是bash run-core.sh，它顺序执行四组底层命令。六组README选择器命令后来由独立审核者在最终ZIP新解压目录逐组实际执行，下面两类日志严格分开。所有旧报告中的154测试和浏览器/Docker演示均非本次成绩。

## 初始准备与原始核心执行的完整日志

以下保留原始UTF-8日志；只将绝对路径按位置角色规范化，空文件仍明确标记。实验内的owner和example.com地址均为合成fixture，不是任何真实账户。路径标记不是新的执行记录。

### 02-dependency-install.log

字节数：133；SHA-256：edff19e0e4e7757ab207e2767c66651f9f495bd3a068cf90dc0749e1a0468d24

```text
Exit prior to config file resolving
cause
double-loading config "/dev/null" as "global", previously loaded as "user"

install_exit=1

```

### 02b-debug-dns.log

字节数：1648；SHA-256：bac5190152c93e70719b27a082f23eb5136787ae0563de316d2a9f0b4caa072a

```text
0 verbose cli <NODE_RUNTIME>/bin/node <NODE_RUNTIME>/bin/npm
1 info using npm@11.9.0
2 info using node@v24.19.0
3 silly config load:file:<NODE_RUNTIME>/lib/node_modules/npm/npmrc
4 silly config load:file:<EXERCISE_DIR>/.npmrc
5 silly config load:file:<EXERCISE_DIR>/home/empty-user.npmrc
6 silly config load:file:<EXERCISE_DIR>/home/empty-global.npmrc
7 verbose title npm install
8 verbose argv "install" "--ignore-scripts" "--no-audit" "--no-fund" "--registry" "https://registry.npmjs.org" "--loglevel" "notice"
9 verbose logfile logs-max:10 dir:<EXERCISE_DIR>/cache/_logs/2026-10-05T11_41_18_026Z-
10 verbose logfile <EXERCISE_DIR>/cache/_logs/2026-10-05T11_41_18_026Z-debug-0.log
11 silly logfile done cleaning log files
12 http fetch GET https://registry.npmjs.org/npm attempt 1 failed with EAI_AGAIN
13 silly packumentCache heap:2348810240 maxSize:587202560 maxEntrySize:293601280
14 silly idealTree buildDeps
15 silly fetch manifest @electric-sql/pglite@0.3.16
16 silly packumentCache full:https://registry.npmjs.org/@electric-sql%2fpglite cache-miss
17 http fetch GET https://registry.npmjs.org/@electric-sql%2fpglite attempt 1 failed with EAI_AGAIN
18 http fetch GET https://registry.npmjs.org/npm attempt 2 failed with EAI_AGAIN
19 http fetch GET https://registry.npmjs.org/@electric-sql%2fpglite attempt 2 failed with EAI_AGAIN

```

### 02b-dependency-install.log

字节数：0；SHA-256：e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

```text
[此原始文件为0字节，无stdout/stderr文本]
```

### 02c-dependency-install.log

字节数：511；SHA-256：6e22537d3f2e2a4e2882722bc9b44d23dfb43e82fdf2b6f383413d6226f296b8

```text
2026-10-05T11:42:24Z
npm error code UNABLE_TO_VERIFY_LEAF_SIGNATURE
npm error errno UNABLE_TO_VERIFY_LEAF_SIGNATURE
npm error request to https://registry.npmjs.org/@electric-sql%2fpglite failed, reason: unable to verify the first certificate; if the root CA is installed locally, try running Node.js with --use-system-ca
npm error A complete log of this run can be found in: <EXERCISE_DIR>/cache/_logs/2026-10-05T11_42_24_603Z-debug-0.log

install_exit=1
2026-10-05T11:42:43Z

```

### 02d-dependency-install.log

字节数：84；SHA-256：e91fb82264be793f76b67ea1c53abdb2551052563274b86b9b3a4e2fbf9f6116

```text
2026-10-05T11:43:42Z

added 16 packages in 16s

install_exit=0
2026-10-05T11:43:58Z

```

### 03-original-actions.log

字节数：3096；SHA-256：f05226d5fe7c26b13db5a222d6b07b62ea652b9cf698b2cd48436faa48efba41

```text
2026-10-05T11:46:11Z
COMMAND: env -i PATH=<existing> HOME=<EXERCISE_DIR>/home TMPDIR=<EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap upstream/tests/actions.test.ts 
(node:15) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
# Subtest: denying a persisted proposal never calls its adapter
ok 1 - denying a persisted proposal never calls its adapter
  ---
  duration_ms: 1020.231226
  type: 'test'
  ...
# Subtest: concurrent approval consumes the proposal only once
ok 2 - concurrent approval consumes the proposal only once
  ---
  duration_ms: 9.938719
  type: 'test'
  ...
# Subtest: wrong owner and stale hash cannot approve
ok 3 - wrong owner and stale hash cannot approve
  ---
  duration_ms: 3.173861
  type: 'test'
  ...
# Subtest: expired and disconnected proposals never reach the provider
ok 4 - expired and disconnected proposals never reach the provider
  ---
  duration_ms: 6.063617
  type: 'test'
  ...
# Subtest: uncertain writes retain uncertainty and cannot be retried
ok 5 - uncertain writes retain uncertainty and cannot be retried
  ---
  duration_ms: 5.424839
  type: 'test'
  ...
# Subtest: another service instance sees persisted proposals
ok 6 - another service instance sees persisted proposals
  ---
  duration_ms: 5.650807
  type: 'test'
  ...
# Subtest: event validation preserves all-day semantics and rejects missing offsets
ok 7 - event validation preserves all-day semantics and rejects missing offsets
  ---
  duration_ms: 21.049037
  type: 'test'
  ...
# Subtest: account switching and reconnecting invalidate a prepared action
ok 8 - account switching and reconnecting invalidate a prepared action
  ---
  duration_ms: 4.235995
  type: 'test'
  ...
# Subtest: review stores authoritative calendar details and binds execution to their version
ok 9 - review stores authoritative calendar details and binds execution to their version
  ---
  duration_ms: 9.013602
  type: 'test'
  ...
# Subtest: idempotent proposal replay returns a completed action before another provider preparation
ok 10 - idempotent proposal replay returns a completed action before another provider preparation
  ---
  duration_ms: 8.580662
  type: 'test'
  ...
# Subtest: concurrent idempotent proposals retain a single persisted review and activity entry
ok 11 - concurrent idempotent proposals retain a single persisted review and activity entry
  ---
  duration_ms: 5.327072
  type: 'test'
  ...
# Subtest: an expired stale review cannot overwrite a concurrently executing action
ok 12 - an expired stale review cannot overwrite a concurrently executing action
  ---
  duration_ms: 10.882286
  type: 'test'
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 1344.111084
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:46:12Z

```

### 04-original-engine.log

字节数：2177；SHA-256：bfccf13a1e9ad86d11bb3b37d15bb8fce4ac16511bec85a2384ee2ba72e30688

```text
2026-10-05T11:46:12Z
COMMAND: env -i PATH=<existing> HOME=<EXERCISE_DIR>/home TMPDIR=<EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap upstream/tests/engine.test.ts 
(node:40) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
# Subtest: two workers claim one task only once
ok 1 - two workers claim one task only once
  ---
  duration_ms: 934.52918
  type: 'test'
  ...
# Subtest: cancellation invalidates a stale worker before its next effect
ok 2 - cancellation invalidates a stale worker before its next effect
  ---
  duration_ms: 651.600031
  type: 'test'
  ...
# Subtest: expired leases recover saved checkpoints after the database restarts
ok 3 - expired leases recover saved checkpoints after the database restarts
  ---
  duration_ms: 996.574299
  type: 'test'
  ...
# Subtest: scheduled tasks wait for due time and approvals wait for a recorded outcome
ok 4 - scheduled tasks wait for due time and approvals wait for a recorded outcome
  ---
  duration_ms: 580.369569
  type: 'test'
  ...
# Subtest: finance artifacts compute cents exactly and reject ambiguous CSV
ok 5 - finance artifacts compute cents exactly and reject ambiguous CSV
  ---
  duration_ms: 3.318373
  type: 'test'
  ...
# Subtest: pending reviews do not starve queued work
ok 6 - pending reviews do not starve queued work
  ---
  duration_ms: 587.946964
  type: 'test'
  ...
# Subtest: run history keeps the time the run started
ok 7 - run history keeps the time the run started
  ---
  duration_ms: 532.411946
  type: 'test'
  ...
# Subtest: a failed run record does not leave the task stuck in the worker
ok 8 - a failed run record does not leave the task stuck in the worker
  ---
  duration_ms: 530.991673
  type: 'test'
  ...
1..8
# tests 8
# suites 0
# pass 8
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 5487.974141
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:46:18Z

```

### 05-original-persistence.log

字节数：956；SHA-256：6dbe7c502747f897bac16b12d67364474dc0ddc5b902c70b3bb968ae42537055

```text
2026-10-05T11:46:18Z
COMMAND: env -i PATH=<existing> HOME=<EXERCISE_DIR>/home TMPDIR=<EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap --test-name-pattern=fresh\ nested\ data\ directory upstream/tests/persistence.test.ts 
(node:65) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
# Subtest: fresh nested data directory starts and survives a database restart
ok 1 - fresh nested data directory starts and survives a database restart
  ---
  duration_ms: 1307.523767
  type: 'test'
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 1424.478567
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:46:19Z

```

### 06-changed-input-characterization.log

字节数：2146；SHA-256：e7b2340d4d6180efb42f2450786358ff20355a9d02d4e40003f8a9d7bc70933b

```text
2026-10-05T11:46:19Z
COMMAND: env -i PATH=<existing> HOME=<EXERCISE_DIR>/home TMPDIR=<EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap characterization.test.ts 
(node:90) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
OBSERVATION changed_subject=true changed_hash=true stale_hash_rejected=true wrong_owner_rejected=true provider_calls=0
# Subtest: changed payload with a new operation key changes the review hash and rejects the old hash
ok 1 - changed payload with a new operation key changes the review hash and rejects the old hash
  ---
  duration_ms: 981.465057
  type: 'test'
  ...
OBSERVATION changed_subject=true reused_key=true original_payload_returned=true action_count=1
# Subtest: same operation key with changed payload returns the original persisted proposal
ok 2 - same operation key with changed payload returns the original persisted proposal
  ---
  duration_ms: 601.280933
  type: 'test'
  ...
OBSERVATION provider_calls=1 reopened_database=true final_status=outcome_unknown replay_calls=0
# Subtest: uncertain provider outcome survives real PGlite reopen and repeated approval does not replay
ok 3 - uncertain provider outcome survives real PGlite reopen and repeated approval does not replay
  ---
  duration_ms: 1020.384999
  type: 'test'
  ...
OBSERVATION same_process=true virtual_clock_advanced_ms=60001 claims=2 stale_checkpoint_rejected=true old_guarded_effects=0 new_handler_calls=1 final_result=new_worker
# Subtest: expired-lease takeover rejects an old worker checkpoint and its next guarded effect
ok 4 - expired-lease takeover rejects an old worker checkpoint and its next guarded effect
  ---
  duration_ms: 572.489412
  type: 'test'
  ...
1..4
# tests 4
# suites 0
# pass 4
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 3368.458687
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:46:23Z

```

### 07-final-integrity.log

字节数：142；SHA-256：b78bc7920ff8626127a29cb9a6218c6712dcc562295ae22f4f5d55f53bfc5543

```text
SOURCE_SHA256_OK files=15 commit=b06caad7005ac5b6d2b451752a3794a6ae1759c1
NPM_LOCK_INTEGRITY_OK packages=16 lifecycle_scripts_not_needed=true

```

## 最终ZIP新目录解压后的独立复跑完整日志

这些是原用例的独立复跑，不新增覆盖数量。命令中cat会重复展示刚生成的TAP，这是日志回显，不是又运行了一轮。

### 01-replay-environment.log

字节数：258；SHA-256：be510cf68ac3360c0a2c939bc137176ae5cdcb3180c716be4ea05d076fcf9308

```text
2026-10-05T11:51:11Z
COMMAND: node --version; npm --version; python3 verify-exercise.py
v24.19.0
11.9.0
SOURCE_SHA256_OK files=15 commit=b06caad7005ac5b6d2b451752a3794a6ae1759c1
NPM_LOCK_INTEGRITY_OK packages=16 lifecycle_scripts_not_needed=true
EXIT_CODE=0

```

### 02-replay-install.log

字节数：348；SHA-256：5d230f4449716fa92f8e2d4aa4d2d0f625ee406e3a1970b39d84f6c255bf9726

```text
2026-10-05T11:51:26Z
COMMAND: bash install-deps.sh; python3 verify-exercise.py
2026-10-05T11:51:26Z

added 16 packages in 7s
2026-10-05T11:51:33Z
INSTALL_EXIT_CODE=0
SOURCE_SHA256_OK files=15 commit=b06caad7005ac5b6d2b451752a3794a6ae1759c1
NPM_LOCK_INTEGRITY_OK packages=16 lifecycle_scripts_not_needed=true
VERIFY_EXIT_CODE=0
2026-10-05T11:51:33Z

```

### 03-replay-actions.log

字节数：3264；SHA-256：67f9bc503035c91cd2009fa90675c3a925b9a554aa6c97ecbb431fc905acf807

```text
2026-10-05T11:51:48Z
COMMAND: bash run-core.sh actions
2026-10-05T11:51:48Z
COMMAND: env -i PATH=<existing> HOME=<REVIEW_EXERCISE_DIR>/home TMPDIR=<REVIEW_EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap upstream/tests/actions.test.ts 
(node:19) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
# Subtest: denying a persisted proposal never calls its adapter
ok 1 - denying a persisted proposal never calls its adapter
  ---
  duration_ms: 882.500825
  type: 'test'
  ...
# Subtest: concurrent approval consumes the proposal only once
ok 2 - concurrent approval consumes the proposal only once
  ---
  duration_ms: 13.300977
  type: 'test'
  ...
# Subtest: wrong owner and stale hash cannot approve
ok 3 - wrong owner and stale hash cannot approve
  ---
  duration_ms: 4.759894
  type: 'test'
  ...
# Subtest: expired and disconnected proposals never reach the provider
ok 4 - expired and disconnected proposals never reach the provider
  ---
  duration_ms: 7.47184
  type: 'test'
  ...
# Subtest: uncertain writes retain uncertainty and cannot be retried
ok 5 - uncertain writes retain uncertainty and cannot be retried
  ---
  duration_ms: 8.368093
  type: 'test'
  ...
# Subtest: another service instance sees persisted proposals
ok 6 - another service instance sees persisted proposals
  ---
  duration_ms: 5.475276
  type: 'test'
  ...
# Subtest: event validation preserves all-day semantics and rejects missing offsets
ok 7 - event validation preserves all-day semantics and rejects missing offsets
  ---
  duration_ms: 21.026816
  type: 'test'
  ...
# Subtest: account switching and reconnecting invalidate a prepared action
ok 8 - account switching and reconnecting invalidate a prepared action
  ---
  duration_ms: 3.478684
  type: 'test'
  ...
# Subtest: review stores authoritative calendar details and binds execution to their version
ok 9 - review stores authoritative calendar details and binds execution to their version
  ---
  duration_ms: 8.618327
  type: 'test'
  ...
# Subtest: idempotent proposal replay returns a completed action before another provider preparation
ok 10 - idempotent proposal replay returns a completed action before another provider preparation
  ---
  duration_ms: 7.381525
  type: 'test'
  ...
# Subtest: concurrent idempotent proposals retain a single persisted review and activity entry
ok 11 - concurrent idempotent proposals retain a single persisted review and activity entry
  ---
  duration_ms: 5.094275
  type: 'test'
  ...
# Subtest: an expired stale review cannot overwrite a concurrently executing action
ok 12 - an expired stale review cannot overwrite a concurrently executing action
  ---
  duration_ms: 9.579759
  type: 'test'
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 1181.140366
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:51:49Z
GROUP_EXIT_CODE=0
2026-10-05T11:51:49Z

```

### 04-replay-engine.log

字节数：4651；SHA-256：6223fdd7bae40b4434d82a60a20db795066d8c5ef50eee46b85a3ad2d605d827

```text
2026-10-05T11:51:58Z
COMMAND: bash run-core.sh engine; cat rawlogs/04-original-engine.log
2026-10-05T11:51:58Z
COMMAND: env -i PATH=<existing> HOME=<REVIEW_EXERCISE_DIR>/home TMPDIR=<REVIEW_EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap upstream/tests/engine.test.ts 
(node:19) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
# Subtest: two workers claim one task only once
ok 1 - two workers claim one task only once
  ---
  duration_ms: 1098.104715
  type: 'test'
  ...
# Subtest: cancellation invalidates a stale worker before its next effect
ok 2 - cancellation invalidates a stale worker before its next effect
  ---
  duration_ms: 615.371896
  type: 'test'
  ...
# Subtest: expired leases recover saved checkpoints after the database restarts
ok 3 - expired leases recover saved checkpoints after the database restarts
  ---
  duration_ms: 960.913244
  type: 'test'
  ...
# Subtest: scheduled tasks wait for due time and approvals wait for a recorded outcome
ok 4 - scheduled tasks wait for due time and approvals wait for a recorded outcome
  ---
  duration_ms: 594.723978
  type: 'test'
  ...
# Subtest: finance artifacts compute cents exactly and reject ambiguous CSV
ok 5 - finance artifacts compute cents exactly and reject ambiguous CSV
  ---
  duration_ms: 2.847327
  type: 'test'
  ...
# Subtest: pending reviews do not starve queued work
ok 6 - pending reviews do not starve queued work
  ---
  duration_ms: 587.091978
  type: 'test'
  ...
# Subtest: run history keeps the time the run started
ok 7 - run history keeps the time the run started
  ---
  duration_ms: 600.175228
  type: 'test'
  ...
# Subtest: a failed run record does not leave the task stuck in the worker
ok 8 - a failed run record does not leave the task stuck in the worker
  ---
  duration_ms: 531.749929
  type: 'test'
  ...
1..8
# tests 8
# suites 0
# pass 8
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 5692.46191
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:52:04Z
2026-10-05T11:51:58Z
COMMAND: env -i PATH=<existing> HOME=<REVIEW_EXERCISE_DIR>/home TMPDIR=<REVIEW_EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap upstream/tests/engine.test.ts 
(node:19) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
# Subtest: two workers claim one task only once
ok 1 - two workers claim one task only once
  ---
  duration_ms: 1098.104715
  type: 'test'
  ...
# Subtest: cancellation invalidates a stale worker before its next effect
ok 2 - cancellation invalidates a stale worker before its next effect
  ---
  duration_ms: 615.371896
  type: 'test'
  ...
# Subtest: expired leases recover saved checkpoints after the database restarts
ok 3 - expired leases recover saved checkpoints after the database restarts
  ---
  duration_ms: 960.913244
  type: 'test'
  ...
# Subtest: scheduled tasks wait for due time and approvals wait for a recorded outcome
ok 4 - scheduled tasks wait for due time and approvals wait for a recorded outcome
  ---
  duration_ms: 594.723978
  type: 'test'
  ...
# Subtest: finance artifacts compute cents exactly and reject ambiguous CSV
ok 5 - finance artifacts compute cents exactly and reject ambiguous CSV
  ---
  duration_ms: 2.847327
  type: 'test'
  ...
# Subtest: pending reviews do not starve queued work
ok 6 - pending reviews do not starve queued work
  ---
  duration_ms: 587.091978
  type: 'test'
  ...
# Subtest: run history keeps the time the run started
ok 7 - run history keeps the time the run started
  ---
  duration_ms: 600.175228
  type: 'test'
  ...
# Subtest: a failed run record does not leave the task stuck in the worker
ok 8 - a failed run record does not leave the task stuck in the worker
  ---
  duration_ms: 531.749929
  type: 'test'
  ...
1..8
# tests 8
# suites 0
# pass 8
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 5692.46191
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:52:04Z
RUN_EXIT_CODE=0 CAT_EXIT_CODE=0
2026-10-05T11:52:04Z

```

### 05-replay-persistence.log

字节数：2217；SHA-256：54aed094ea44c93970bcf239bc02cb5f01c7582072a2bafac1df2ed97ee4fcc0

```text
2026-10-05T11:52:16Z
COMMAND: bash run-core.sh persistence; cat rawlogs/05-original-persistence.log
2026-10-05T11:52:16Z
COMMAND: env -i PATH=<existing> HOME=<REVIEW_EXERCISE_DIR>/home TMPDIR=<REVIEW_EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap --test-name-pattern=fresh\ nested\ data\ directory upstream/tests/persistence.test.ts 
(node:19) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
# Subtest: fresh nested data directory starts and survives a database restart
ok 1 - fresh nested data directory starts and survives a database restart
  ---
  duration_ms: 1258.255114
  type: 'test'
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 1375.793662
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:52:18Z
2026-10-05T11:52:16Z
COMMAND: env -i PATH=<existing> HOME=<REVIEW_EXERCISE_DIR>/home TMPDIR=<REVIEW_EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap --test-name-pattern=fresh\ nested\ data\ directory upstream/tests/persistence.test.ts 
(node:19) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
# Subtest: fresh nested data directory starts and survives a database restart
ok 1 - fresh nested data directory starts and survives a database restart
  ---
  duration_ms: 1258.255114
  type: 'test'
  ...
1..1
# tests 1
# suites 0
# pass 1
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 1375.793662
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:52:18Z
RUN_EXIT_CODE=0 CAT_EXIT_CODE=0
2026-10-05T11:52:18Z

```

### 06-replay-characterization.log

字节数：4799；SHA-256：119a2688e9124addb8217bc4e21fe3f5f008c1c301c001d5722a605bac656ba1

```text
2026-10-05T11:52:28Z
COMMAND: bash run-core.sh characterization; cat rawlogs/06-changed-input-characterization.log; python3 verify-exercise.py
2026-10-05T11:52:28Z
COMMAND: env -i PATH=<existing> HOME=<REVIEW_EXERCISE_DIR>/home TMPDIR=<REVIEW_EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap characterization.test.ts 
(node:19) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
OBSERVATION changed_subject=true changed_hash=true stale_hash_rejected=true wrong_owner_rejected=true provider_calls=0
# Subtest: changed payload with a new operation key changes the review hash and rejects the old hash
ok 1 - changed payload with a new operation key changes the review hash and rejects the old hash
  ---
  duration_ms: 987.867311
  type: 'test'
  ...
OBSERVATION changed_subject=true reused_key=true original_payload_returned=true action_count=1
# Subtest: same operation key with changed payload returns the original persisted proposal
ok 2 - same operation key with changed payload returns the original persisted proposal
  ---
  duration_ms: 636.319596
  type: 'test'
  ...
OBSERVATION provider_calls=1 reopened_database=true final_status=outcome_unknown replay_calls=0
# Subtest: uncertain provider outcome survives real PGlite reopen and repeated approval does not replay
ok 3 - uncertain provider outcome survives real PGlite reopen and repeated approval does not replay
  ---
  duration_ms: 1013.68201
  type: 'test'
  ...
OBSERVATION same_process=true virtual_clock_advanced_ms=60001 claims=2 stale_checkpoint_rejected=true old_guarded_effects=0 new_handler_calls=1 final_result=new_worker
# Subtest: expired-lease takeover rejects an old worker checkpoint and its next guarded effect
ok 4 - expired-lease takeover rejects an old worker checkpoint and its next guarded effect
  ---
  duration_ms: 645.923679
  type: 'test'
  ...
1..4
# tests 4
# suites 0
# pass 4
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 3476.737314
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:52:32Z
2026-10-05T11:52:28Z
COMMAND: env -i PATH=<existing> HOME=<REVIEW_EXERCISE_DIR>/home TMPDIR=<REVIEW_EXERCISE_DIR>/tmp node --experimental-transform-types --import ./offline-guard.mjs --test --test-isolation=none --test-concurrency=1 --test-reporter=tap characterization.test.ts 
(node:19) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
TAP version 13
OBSERVATION changed_subject=true changed_hash=true stale_hash_rejected=true wrong_owner_rejected=true provider_calls=0
# Subtest: changed payload with a new operation key changes the review hash and rejects the old hash
ok 1 - changed payload with a new operation key changes the review hash and rejects the old hash
  ---
  duration_ms: 987.867311
  type: 'test'
  ...
OBSERVATION changed_subject=true reused_key=true original_payload_returned=true action_count=1
# Subtest: same operation key with changed payload returns the original persisted proposal
ok 2 - same operation key with changed payload returns the original persisted proposal
  ---
  duration_ms: 636.319596
  type: 'test'
  ...
OBSERVATION provider_calls=1 reopened_database=true final_status=outcome_unknown replay_calls=0
# Subtest: uncertain provider outcome survives real PGlite reopen and repeated approval does not replay
ok 3 - uncertain provider outcome survives real PGlite reopen and repeated approval does not replay
  ---
  duration_ms: 1013.68201
  type: 'test'
  ...
OBSERVATION same_process=true virtual_clock_advanced_ms=60001 claims=2 stale_checkpoint_rejected=true old_guarded_effects=0 new_handler_calls=1 final_result=new_worker
# Subtest: expired-lease takeover rejects an old worker checkpoint and its next guarded effect
ok 4 - expired-lease takeover rejects an old worker checkpoint and its next guarded effect
  ---
  duration_ms: 645.923679
  type: 'test'
  ...
1..4
# tests 4
# suites 0
# pass 4
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 3476.737314
NETWORK_GUARD attempts=0

EXIT_CODE=0
2026-10-05T11:52:32Z
SOURCE_SHA256_OK files=15 commit=b06caad7005ac5b6d2b451752a3794a6ae1759c1
NPM_LOCK_INTEGRITY_OK packages=16 lifecycle_scripts_not_needed=true
RUN_EXIT_CODE=0 CAT_EXIT_CODE=0 VERIFY_EXIT_CODE=0
2026-10-05T11:52:32Z

```

## 独立复跑机器可读结论

```json
{
  "verified_at": "2026-10-05T11:52:54.630777+00:00",
  "zip_sha256": "714ca8560289c4ec076a6b0ecb87a6c40b921fadd12c62cec89142d878994157",
  "zip_bytes": 211031,
  "zip_members": 37,
  "all_manifest_members_checked": 36,
  "source_copies_verified_pristine": 15,
  "runs": [
    {
      "log": "fresh-exercise/openmuse-core-exercise/rawlogs/03-original-actions.log",
      "bytes": 3170,
      "sha256": "47b7a976d37b7c5b5254d7979e19bdb389c51891feaf87d2cc37e9cb87e6292f",
      "pass": 12,
      "fail": 0,
      "network_guard_attempts": 0,
      "timestamps": [
        "2026-10-05T11:51:48Z",
        "2026-10-05T11:51:49Z"
      ]
    },
    {
      "log": "fresh-exercise/openmuse-core-exercise/rawlogs/04-original-engine.log",
      "bytes": 2254,
      "sha256": "7ddb01cf33724ab637ce885da4cc1ebe451f883bb29f0b2c9bc206c74742c145",
      "pass": 8,
      "fail": 0,
      "network_guard_attempts": 0,
      "timestamps": [
        "2026-10-05T11:51:58Z",
        "2026-10-05T11:52:04Z"
      ]
    },
    {
      "log": "fresh-exercise/openmuse-core-exercise/rawlogs/05-original-persistence.log",
      "bytes": 1032,
      "sha256": "83cfdebdfa12d44412f07202235664cbbe80dce3b4cc274705f5d296968d69f0",
      "pass": 1,
      "fail": 0,
      "network_guard_attempts": 0,
      "timestamps": [
        "2026-10-05T11:52:16Z",
        "2026-10-05T11:52:18Z"
      ]
    },
    {
      "log": "fresh-exercise/openmuse-core-exercise/rawlogs/06-changed-input-characterization.log",
      "bytes": 2221,
      "sha256": "df84ccebb36f4438cacd4c7c77f439f0001fc56fe5c54bee5e475951e5574d55",
      "pass": 4,
      "fail": 0,
      "network_guard_attempts": 0,
      "timestamps": [
        "2026-10-05T11:52:28Z",
        "2026-10-05T11:52:32Z"
      ]
    }
  ],
  "original_test_cases": 21,
  "author_characterizations": 4,
  "reviewer_new_test_cases": 0,
  "counts_note": "These are independent reruns of same cases; do not add reviewer runs to unique case count."
}
```

## 产物验收范围

历史指南由 ReportLab 直接生成；PDF 逐页视觉检查与 HTML 结构检查分别记录。浏览器视觉及 HTML 转 PDF 原路线受环境限制，本次未重试。公开整理不增加任何完整应用、真实服务或系统故障验收。


## 当前公开副本检查

公开 PDF 由 ReportLab 直接重新生成并逐页渲染查看；HTML 仅结构检查。ZIP 新增 README 说明、规范化历史日志中的位置路径、概括来源清单中的私有映射说明并重算成员摘要；上游源码与 MIT LICENSE、自编变式、运行脚本、数据和依赖锁保持原字节。历史 21 项选取原测试与 4 项自编变式的结果不变。22 个原测试定义中的 1 项池错误测试未选择，TAP skipped=0；不将同用例复跑累加为覆盖。当前独立审核另见第六份日志。

当前公开 ZIP：211314 字节；SHA-256 000c275f9603644f0aecd9313a1a6ccd1e066e3099a9aeaf580ff93c0f0cc8d5

experiment-result.json 中的四组 sha256 保留历史原始日志指纹，指向路径规范化之前的字节；当前公开成员以 bundle-file-sha256.json 的摘要为准。两份清单的用途不同，测试结果没有改变。
