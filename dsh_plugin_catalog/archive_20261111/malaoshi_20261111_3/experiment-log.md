# 真实experiment-log

时间2026-11-11 Asia/Shanghai(UTC+8)；目录/workspace/reminder-batch/item-3-dsh-plugins-57。准备仅公开资料下载，无clone、插件安装、模型、用户配置、SSH账户或定时任务。

## 准备真实输出
```text
node --version
v24.22.1
python3 exercise/verify.py
PASS 60 SHA-256 source/input fingerprints; no registry/model/SSH connection
```

## 分层
真实执行：自写数据分析器、真实mountOnce源码。替代：ctx.effect/dispose桩与合成包名。真实读取：原帖/引用全文、52根仓库元数据、8重点插件仓库文件与旧vault。没有执行被检插件入口、依赖脚本、浏览器前端或DSH loader。

## run-catalog.txt
```text
Asia/Shanghai 2026-11-11T01:04:33.620269
CWD /workspace/reminder-batch/item-3-dsh-plugins-57
$ node exercise/lab.mjs catalog
EXIT 0
PASS 57 article entries
PASS 52 distinct repository roots
PASS 51 public metadata successes
PASS one HTTP404 observation
same display-name groups [["dsh-pet",["zhu1090093659/dsh-pet","PC2005-cloud/dsh-pet"]],["dsh-code-review",["MichengAI/dsh-code-review","f-e-n-g-0531/dsh-code-review"]]]
PASS 2 same-display-name groups
PASS same display name does not mean same repository
HTTP404 is a point-in-time response, not proof of permanent nonexistence.
RESULT stage=catalog; checks=6; model/SSH/host not invoked

STDERR

```

## run-cost.txt
```text
Asia/Shanghai 2026-11-11T01:04:34.452386
CWD /workspace/reminder-batch/item-3-dsh-plugins-57
$ node exercise/lab.mjs cost
EXIT 0
{"label":"context","name":"billion-context","manifestBytes":4287,"prodDeps":2,"peerDeps":0,"parseMedianMs":0.006604728999999999,"iterations":14000,"checksum":308000}
PASS context parse workload actually ran
{"label":"sidebar","name":"dsh-better-sidebar","manifestBytes":8431,"prodDeps":33,"peerDeps":18,"parseMedianMs":0.013370081499999997,"iterations":14000,"checksum":280000}
PASS sidebar parse workload actually ran
{"label":"task","name":"@linxin666/dsh-client-ui-task-board","manifestBytes":3614,"prodDeps":2,"peerDeps":2,"parseMedianMs":0.005418239499999999,"iterations":14000,"checksum":224000}
PASS task parse workload actually ran
{"label":"ssh","name":"@linxin666/dsh-ssh","manifestBytes":3437,"prodDeps":5,"peerDeps":3,"parseMedianMs":0.0057566565000000194,"iterations":14000,"checksum":252000}
PASS ssh parse workload actually ran
{"label":"all","name":"@linxin666/dsh-web-all","manifestBytes":9334,"prodDeps":23,"peerDeps":1,"parseMedianMs":0.012078403999999978,"iterations":14000,"checksum":210000}
PASS all parse workload actually ran
PASS all manifest fan-out is greater than 2 selections
Timing measures warm JSON.parse + Object.keys ONLY; not plugin startup/import/render/network latency.
RESULT stage=cost; checks=6; model/SSH/host not invoked

STDERR

```

## run-guard.txt
```text
Asia/Shanghai 2026-11-11T01:04:33.768098
CWD /workspace/reminder-batch/item-3-dsh-plugins-57
$ node exercise/lab.mjs guard
EXIT 0
PASS only holder mounts
PASS waiter takes over after dispose
PASS disposed waiter is not resurrected
PASS several waiters keep one next owner
PASS second waiter handover
PASS separate module copies share global registry
PASS different package names mount independently
PASS foreign registry shape repaired to Set
PASS all synthetic package names released
Real mountOnce; fake ctx.effect/dispose; no DSH loader, browser or SSH connection.
RESULT stage=guard; checks=9; model/SSH/host not invoked

STDERR
(node:158277) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///workspace/reminder-batch/item-3-dsh-plugins-57/evidence/zhu1090093659/dsh-web/shared/host/mount-once.ts?copy=A is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /workspace/reminder-batch/item-3-dsh-plugins-57/evidence/zhu1090093659/dsh-web/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)

```

## run-overlap.txt
```text
Asia/Shanghai 2026-11-11T01:04:33.672929
CWD /workspace/reminder-batch/item-3-dsh-plugins-57
$ node exercise/lab.mjs overlap
EXIT 0
aggregate dependencies 23 redundant selections ["@linxin666/dsh-client-ui-task-board","@linxin666/dsh-ssh"]
PASS aggregate contains task-board and SSH dependencies
PASS aggregate patch really mounts both package names
PASS standalone and aggregate have different row IDs
PASS both task/SSH use package-name mountOnce
Static overlap != actual startup failure: current code has a guard.
RESULT stage=overlap; checks=4; model/SSH/host not invoked

STDERR

```

## 非成功与限制
RevolutionLA/dsh-dream-skin公共API返回404；其余51根可读。部分许可API为NOASSERTION，已以重点LICENSE读回而非误判无许可。Node在导入上游纯ts模块时有MODULE_TYPELESS_PACKAGE_JSON警告，未修改其元数据；保留日志。没有付费或免费模型推理，真实Host/SSH/cron/UI兼容都待验证。微基准没有冷启动或实际import延迟。

## 步骤6回读与PDF实际渲染
证据回读命令已真实执行：4份run-*.txt全部含EXIT 0，退出0。

PDF命令：
```bash
/usr/bin/google-chrome --headless --no-sandbox --disable-dev-shm-usage --no-pdf-header-footer --print-to-pdf=/workspace/reminder-batch/item-3-dsh-plugins-57/dsh-plugins-57.pdf file:///workspace/reminder-batch/item-3-dsh-plugins-57/index.html
pdfinfo dsh-plugins-57.pdf
pdftoppm -scale-to 1100 -png dsh-plugins-57.pdf evidence/final-page
```
打印时间：2026-11-11 01:07:03 Asia/Shanghai(UTC+8)。真实结果：14页，A4(594.96×841.92pt)，1095886字节，PDF1.4。只打开自有静态HTML，没有接管用户浏览器或更改系统设置。HTML不含字体集合/大型图片，图为内联SVG。

制作者已用Read逐页查看final-page-01.png至final-page-14.png，不是他人独立审核：
1封面/用途完整；2四件套/版本表完整；3疑问1—2与SVG完整；4疑问3—4与SVG完整；5疑问5—6与SVG完整；6疑问7—8与SVG完整；7疑问9—10与SVG完整；8步骤1—3完整；9步骤4—6命令折行完整；10候选1—15完整；11候选16—30完整；12候选31—45完整；13候选46—57完整；14成本表/证据索引完整。无截断、列溢出或额外空白页。
