# 真实实验日志

环境：云端Linux；Node v24.22.1；北京时间2026-11-11。所有测试顺序运行，未调用付费模型。

## 1. 固定输入、查重与版本
目的：防止把当前文档套到旧CLI。
```bash
git -C ../repo rev-parse HEAD
git -C ../repo log -1 --format="%H %cI"
node --version
```
真实结果：b30d54b8aebe6408e02d1473446d25f8083da68f；Node v24.22.1。提交时间转换为北京时间：2026-11-11 00:38。
验证：SHA与sources一致；旧0.84.2仅对照不安装。

## 2. 准备隔离依赖和源码解析
目的：依赖只在隔离目录；bootstrap会执行整个测试链。
```bash
npm ci --ignore-scripts --no-audit --no-fund
# 完整安装/源码链接命令已保存在本包：
bash ma-laoshi-20261111-bootstrap.sh
```
真实结果：本轮初次npm install实装131个包，用时6秒，未执行生命周期脚本。初跑83测试通过、4套件解析失败；映射修正后全过，失败日志保留。
验证：package-lock锁依赖；最终config精确匹配包名，源码未改。

## 3. 两个prefix共用真实SQLite
目的：验证不是Python仿制表，而是运行上游SqliteStorage。
```bash
node_modules/.bin/vitest run --config ma-laoshi-20261111-vitest.config.ts -t "two prefixes" --reporter verbose
```
真实结果：首个与后续全链运行实际执行同名测试：aId=bId=2，18张表；隔离与重开断言通过。
验证：alpha读ALPHA ONLY；beta先无对应记录，写入后重开BETA ONLY。

## 4. 压缩、上下文与睡眠回归
目的：真实运行压缩后system置前、raw history不删、sleep/onWake行为。
```bash
node_modules/.bin/vitest run --config ma-laoshi-20261111-vitest.config.ts repo/packages/durable/test/harness-compaction.test.ts repo/packages/durable/test/harness-context.test.ts repo/packages/durable/test/harness-sleep.test.ts --reporter verbose
```
真实结果：同一次顺序全链中这些文件全部通过；压缩后下一请求角色序列被官方断言逐项比较。
验证：faux模型不发付费请求；sleep为受控时钟/运行时测试，不是Cloudflare实测。

## 5. 改变持久化窗并测批次数
目的：同样faux流对比0与400ms；避免引用作者性能当自己测量。
```bash
node_modules/.bin/vitest run --config ma-laoshi-20261111-vitest.config.ts -t "measure committed" --reporter verbose
```
真实结果：实际全链同名测试输出：0ms总27批/文档25批；400ms总9批/文档7批；两者done。
验证：断言第二组文档批次更少；不推断真实网络写入与费用。

## 6. 全链验收并保存故障边界
目的：覆盖SQLite恢复/中断/正常close/压缩/休眠，再核对全部结果。
```bash
node_modules/.bin/vitest run --config ma-laoshi-20261111-vitest.config.ts --reporter verbose
# 日志文件：../raw/ma-laoshi-20261111-tests-final.log
```
真实结果：6文件、245测试通过，首次成功耗时14.85秒；最终可移植配置再次运行结果见原始日志。
验证：不包含真实SIGKILL、断电、跨进程争用、真实模型质量和生产宿主计费。

## 本轮真实命令轨迹与失败
初次clone早于暂停，恢复后复用repo/raw。git ls-remote核得当前HEAD，复用既有查重main快照。
```bash
git ls-remote https://github.com/earendil-works/pi HEAD
git ls-remote https://github.com/Smashwinny/reminder_knowlege refs/heads/main
git clone --depth 1 https://github.com/earendil-works/pi <隔离目录>/repo
npm install --ignore-scripts --no-audit --no-fund
# packages/durable内，默认配置首次测试：
../../node_modules/.bin/vitest run test/sqlite-storage.test.ts test/harness-compaction.test.ts test/harness-context.test.ts test/harness-deferred-progress.test.ts test/harness-sleep.test.ts --maxWorkers 1 --no-file-parallelism --reporter verbose
# exercise内，修复源码解析后最终运行：
node_modules/.bin/vitest run --config ma-laoshi-20261111-vitest.config.ts --reporter verbose
```
第一次83测试过、4套件因pi-ai发布dist入口不存在而加载失败；第二次配置alias根包前缀误匹配，6套件加载失败；第三次精确匹配源码入口后245过。仅改实验配置，不改上游源码。最后再改为相对动态配置验证。不是安全拒绝，没有通过替换工具绕过。

### ma-laoshi-20261111-official-tests.log
```text
Error: Failed to resolve entry for package "@earendil-works/pi-ai". The package may have incorrect main/module/exports specified in its package.json.
Error: Failed to resolve entry for package "@earendil-works/pi-ai". The package may have incorrect main/module/exports specified in its package.json.
Error: Failed to resolve entry for package "@earendil-works/pi-ai". The package may have incorrect main/module/exports specified in its package.json.
Error: Cannot find package '@earendil-works/pi-ai/utils/estimate' imported from /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-5-pi-durable/repo/packages/durable/src/harness/compaction.ts
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }
 Test Files  4 failed | 1 passed (5)
      Tests  83 passed (83)
   Duration  2.34s (transform 548ms, setup 443ms, import 184ms, tests 966ms, environment 0ms)
```
完整原文保留raw同名文件。

### ma-laoshi-20261111-tests-rerun.log
```text
Error: Cannot find package '@earendil-works/chord/context' imported from /workspace/ma-laoshi-20261111/ma-laoshi-20261111-item-5-pi-durable/repo/packages/durable/src/session/session.ts
Serialized Error: { code: 'ERR_MODULE_NOT_FOUND' }
 Test Files  6 failed (6)
      Tests  no tests
   Duration  838ms (transform 88ms, setup 0ms, import 0ms, tests 0ms, environment 0ms)
```
完整原文保留raw同名文件。

### ma-laoshi-20261111-tests-final.log
```text
{"experiment":"sqlite-isolation","sameFile":true,"aId":2,"bId":2,"tableCount":18,"names":["alpha_durable_schema","alpha_durable_metadata","alpha_record_ids","alpha_conversations","alpha_entries","alpha_submissions","alpha_documents","alpha_document_revisions","alpha_tasks","beta_durable_schema","beta_durable_metadata","beta_record_ids","beta_conversations","beta_entries","beta_submissions","beta_documents","beta_document_revisions","beta_tasks"],"reopen":"BETA ONLY","pass":true}
{"experiment":"faux-write-count","rows":[{"persistWithinMs":0,"totalBatches":27,"documentBatches":25,"status":"done"},{"persistWithinMs":400,"totalBatches":9,"documentBatches":7,"status":"done"}],"unit":"ControlledStorage batch, NOT remote I/O or disk write"}
 Test Files  6 passed (6)
      Tests  245 passed (245)
   Duration  14.85s (transform 1.04s, setup 478ms, import 1.41s, tests 12.30s, environment 0ms)
```
完整原文保留raw同名文件。

### ma-laoshi-20261111-portable-config-check.log
```text
{"experiment":"sqlite-isolation","sameFile":true,"aId":2,"bId":2,"tableCount":18,"names":["alpha_durable_schema","alpha_durable_metadata","alpha_record_ids","alpha_conversations","alpha_entries","alpha_submissions","alpha_documents","alpha_document_revisions","alpha_tasks","beta_durable_schema","beta_durable_metadata","beta_record_ids","beta_conversations","beta_entries","beta_submissions","beta_documents","beta_document_revisions","beta_tasks"],"reopen":"BETA ONLY","pass":true}
{"experiment":"faux-write-count","rows":[{"persistWithinMs":0,"totalBatches":27,"documentBatches":25,"status":"done"},{"persistWithinMs":400,"totalBatches":9,"documentBatches":7,"status":"done"}],"unit":"ControlledStorage batch, NOT remote I/O or disk write"}
 Test Files  6 passed (6)
      Tests  245 passed (245)
   Duration  14.92s (transform 992ms, setup 521ms, import 1.34s, tests 12.40s, environment 0ms)
```
完整原文保留raw同名文件。

## 边界
模拟crash使用上游Session.fail，不是SIGKILL/断电。睡眠测试使用受控时钟/宿主回调，不创建任何用户任务或通知。批次数以ControlledStorage记录为单位，不测网络/磁盘/计费。PDF打印与逐页查看另记最终STATUS。

## PDF真实打印与检查
```bash
/home/box/.cache/ms-playwright/chromium_headless_shell-1254/chrome-headless-shell-linux64/chrome-headless-shell --no-sandbox --headless --no-pdf-header-footer --print-to-pdf=ma-laoshi-20261111-item-5-pi-durable.pdf file://<本目录>/ma-laoshi-20261111-index.html
pdfinfo ma-laoshi-20261111-item-5-pi-durable.pdf
pdftoppm -scale-to 950 -png ma-laoshi-20261111-item-5-pi-durable.pdf rendered/ma-laoshi-20261111-page
```
实际结果：exit=0，10页A4，923490字节。逐页Read查看01—10，未发现溢出/截断/缺SVG/空白页。详见ma-laoshi-20261111-pdf-check.md。
