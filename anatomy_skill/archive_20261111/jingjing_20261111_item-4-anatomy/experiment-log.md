# Anatomy Skill 与原理讲解形式 · 真实实验日志

执行时间：2026-11-11 01:25:08 CST（UTC+8）前后，PDF 视觉自检至 2026-11-11 01:27:27 CST（UTC+8）。

只读公共研究＋云端隔离实验。教学页是手写模型，不是上游官方图，除明确标出的官方构建。

## 步骤 1 · 用官方脚本重建拨针量表
目的：确认已复制的 kit 能在本地重建官方浅色示例页，并与仓库提交字节一致

```bash
cd /workspace/reminder-batch-2026-11-11/item-4-anatomy/exercise/upstream/examples/dial-indicator
node build.mjs --light
sha256sum dial-indicator-light.html
sha256sum /tmp/dial-indicator-light.html
```

真实输出（exit=0）：
```text
wrote dial-indicator-light.html
bc1810e340d916a25cc1749589b44096b7e41970f22fa7fce569bbefc0613093  dial-indicator-light.html
bc1810e340d916a25cc1749589b44096b7e41970f22fa7fce569bbefc0613093  /tmp/dial-indicator-light.html
```
`/tmp/dial-indicator-light.html` 是从 `https://raw.githubusercontent.com/wheresryan22/anatomy/1482e8469b0a9e0d8cc18ea2740a01423d29ae80/examples/dial-indicator/dial-indicator-light.html` 下载的对照文件，大小都是 136,489 字节。
验证：重建页与该提交原始文件哈希相同。

## 步骤 2 · 无头浏览器驱动官方示例
目的：验证官方图在禁止外网、降低动态效果时，仍能用键盘改变量块读数

```bash
cd /workspace/reminder-batch-2026-11-11/item-4-anatomy
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 exercise/check.py browser
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 exercise/check.py verify
```

真实输出（exit=0）：
```text
{
  "rows": [
    {
      "key": "Home",
      "want": 18,
      "aria": "18",
      "readout": "block 1 · reads 18.0 px",
      "needle": "M350.3 151.4L355.9 138.2"
    },
    {
      "key": "ArrowLeft",
      "want": 14,
      "aria": "14",
      "readout": "block 2 · reads 14.0 px",
      "needle": "M355.4 150.3L332 143.5"
    },
    {
      "key": "End",
      "want": 10,
      "aria": "10",
      "readout": "block 3 · reads 10.0 px",
      "needle": "M354.8 147.5L334.7 156.6"
    }
  ],
  "errors": [],
  "network_attempts": [],
  "paths": 342
}
PASS 6 checks: no JS errors, no HTTP attempts, path count, 3 readouts, 3 needle paths, different rendered poses; not a mechanical accuracy or pedagogy audit
```
验证：退出码 0；6 项检查全部 PASS。这不是机械精度或教学法审计。

## 步骤 3 · 运行 RFC 793 图 6 纯模型
目的：在不打开浏览器、不调用模型的情况下，核对三次握手的状态和序号

```bash
cd /workspace/reminder-batch-2026-11-11/item-4-anatomy
python3 exercise/tcp_model.py
```

真实输出（exit=0）：
```text
PASS step0_states CLOSED/LISTEN
PASS step0_no_segment 
PASS step1_states 
PASS step1_syn 
PASS step2_asymmetric A already ESTABLISHED, B still SYN-RECEIVED
PASS step2_synack 
PASS syn_occupies_seq ACK of SYN is ISS+1
PASS step3_both_established 
PASS step3_ack 
PASS ack_no_seq_space ACK segment reuses SEQ=101; ACK does not occupy sequence space
PASS readout_step0 
PASS readout_step1 
PASS readout_step2 
PASS readout_step3 
assertions=14 failed=0
```
验证：退出码 0；assertions=14 failed=0。

## 步骤 4 · 无头浏览器驱动教学页
目的：确认手写邮筒索道页可键盘操作，并与纯模型输出同一读数

```bash
cd /workspace/reminder-batch-2026-11-11/item-4-anatomy
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 exercise/lab.py tcp
```

真实输出（exit=0）：
```text
{
  "rows": [
    {
      "key": "Home",
      "want": 0,
      "step": "0",
      "client": "CLOSED",
      "server": "LISTEN",
      "segment": "—",
      "readout": "step 0/3 | A CLOSED | B LISTEN | —"
    },
    {
      "key": "ArrowRight",
      "want": 1,
      "step": "1",
      "client": "SYN-SENT",
      "server": "SYN-RECEIVED",
      "segment": "A->B SEQ=100 CTL=SYN",
      "readout": "step 1/3 | A SYN-SENT | B SYN-RECEIVED | A->B SEQ=100 CTL=SYN"
    },
    {
      "key": "ArrowRight",
      "want": 2,
      "step": "2",
      "client": "ESTABLISHED",
      "server": "SYN-RECEIVED",
      "segment": "B->A SEQ=300 ACK=101 CTL=SYN,ACK",
      "readout": "step 2/3 | A ESTABLISHED | B SYN-RECEIVED | B->A SEQ=300 ACK=101 CTL=SYN,ACK"
    },
    {
      "key": "End",
      "want": 3,
      "step": "3",
      "client": "ESTABLISHED",
      "server": "ESTABLISHED",
      "segment": "A->B SEQ=101 ACK=301 CTL=ACK",
      "readout": "step 3/3 | A ESTABLISHED | B ESTABLISHED | A->B SEQ=101 ACK=301 CTL=ACK"
    }
  ],
  "errors": [],
  "network_attempts": [],
  "title": "邮筒索道 · TCP 三次握手教学模型"
}
```
验证：tcp-results.json 中 errors 与 network_attempts 都是空列表；四步读数与 tcp_model.py 一致。

## 步骤 5 · 核对不对称状态与截图
目的：确认第 2 步的教学要点被页面真实渲染，且起止画面不同

```bash
cd /workspace/reminder-batch-2026-11-11/item-4-anatomy
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 exercise/lab.py verify-tcp
```

真实输出（exit=0）：
```text
PASS tcp-step-0 step 0/3 | A CLOSED | B LISTEN | —
PASS tcp-step-1 step 1/3 | A SYN-SENT | B SYN-RECEIVED | A->B SEQ=100 CTL=SYN
PASS tcp-step-2 step 2/3 | A ESTABLISHED | B SYN-RECEIVED | B->A SEQ=300 ACK=101 CTL=SYN,ACK
PASS tcp-step-3 step 3/3 | A ESTABLISHED | B ESTABLISHED | A->B SEQ=101 ACK=301 CTL=ACK
PASS tcp checks: no JS errors, no HTTP, 4 RFC 793 Fig 6 states, asymmetric step 2, different screenshots
```
验证：退出码 0。第 2 步客户端 ESTABLISHED、服务端 SYN-RECEIVED。

## 步骤 6 · 留下源文件指纹
目的：给官方构建脚本、kit、重建页和教学模型留下不可混淆的哈希

```bash
cd /workspace/reminder-batch-2026-11-11/item-4-anatomy
python3 exercise/lab.py hash
```

真实输出（exit=0）：
```text
e4eaa2324af7f2630650ca72e52a78d56159213a786e14fba8321344789f990d upstream/examples/dial-indicator/build.mjs
6d3ecc725d30c3b0346da309cf61dfa5a65017c23620bbd4093009d4fb104018 upstream/kit/iso-kit.mjs
bc1810e340d916a25cc1749589b44096b7e41970f22fa7fce569bbefc0613093 upstream/examples/dial-indicator/dial-indicator-light.html
d75b90015c4f3d256766b77f6fbb1cebdb1d67d6eb872ec74bd8e677ce0cd9fb tcp_model.py
caf9a37ede297826a3524d85bc8b6d702380c2a5a6769b38b8ad1a19a5742bdb tcp-handshake.html
```
验证：同样输入再次重建，官方浅色页哈希不变。

未把作者宣称的额度、耗时或视频质量当成本次测量。没有第三方独立审核。
