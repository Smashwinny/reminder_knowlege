# 第5项真实实验日志
2026-11-11（Asia/Shanghai）
原创方法层实验，不是第三方技能效果/微信完整复现。
依赖沿用本批隔离目录Playwright；锁文件写入exercise，复现可npm ci。
## 1 输入与来源审计（已执行）
目的：核对入口固定与核心文件指纹。
命令：`python3 audit.py`
真实结果：11个入口/10个仓库，11个下载成功，SHA均40位；核心sha256见JSON。
验证：下载成功计数不等于宿主加载/完整语义审核。

## 2 固定序列复放（已执行）
目的：同种子、同600步输入重复执行，断言深度相等。
命令：`node lab.cjs replay`
真实结果：两次一致；tick600、x60、score1、coinX260。
验证：只证明这一环境与序列的确定性，不是玩法质量。

## 3 边界与暂停（已执行）
目的：连续1000步向右推进，再令paused=true试图继续移动。
命令：`node lab.cjs boundaries`
真实结果：右边界x308，score2；暂停后tick和x不变。
验证：画布宽320、玩家半径12，所以中心最大308。

## 4 反馈与规则分离（已执行）
目的：120步双路核心复放；外层flash消费拾取事件并衰减。
命令：`node lab.cjs feedback`
真实结果：2次pickup，flash最终0；核心两路状态逐步一致。
验证：自写单元检查，不是独立审核或真人手感测评。

## 5 真实浏览器链路（已执行）
目的：实际Chrome推进、截图、暂停、重置及碎片时间对照。
命令：`node browser.cjs`
真实结果：500ms→tick30/x120/score1；暂停再1000ms仍30；10×1ms为0步，再7ms为1步；溢出false、pageerror=[]。
验证：查看gameplay.png/paused.png，并比对render_game_to_text；360px宽测试。

## 真实原始输出
```text
执行日期 2026-11-11 01:13:26 Asia/Shanghai
Python 3.13.5
v24.22.1
Google Chrome 156.0.8078.47 
$ python3 audit.py
{
  "source_entries": 11,
  "read_ok": 11,
  "unique_repos": 10,
  "pinned": true,
  "core_sha256": "76b7dd6aa6ead0db8222fda85c970816043ddfbad6fa3ee44ddaecafffe01817"
}
$ node lab.cjs replay
{
  "mode": "replay",
  "steps": 600,
  "equal": true,
  "final": {
    "tick": 600,
    "x": 60,
    "y": 150,
    "r": 12,
    "coinX": 260,
    "coinY": 150,
    "score": 1,
    "paused": false,
    "seed": 1042201148,
    "events": []
  }
}
$ node lab.cjs boundaries
{
  "mode": "boundaries",
  "right_x": 308,
  "score": 2,
  "pause_tick_frozen": true
}
$ node lab.cjs feedback
{
  "mode": "feedback",
  "steps": 120,
  "pickup_events": 2,
  "feedback_does_not_change_simulation": true,
  "flash_final": 0
}
$ NODE_PATH=../../item04/test-tools/node_modules node browser.cjs
{
  "pickup": {
    "tick": 30,
    "x": 120,
    "y": 150,
    "r": 12,
    "coinX": 260,
    "coinY": 150,
    "score": 1,
    "paused": false,
    "seed": 1042201148,
    "events": [],
    "coordinate": "origin top-left; +x right; +y down",
    "remainder_ms": 0,
    "flash": 0
  },
  "paused_tick": 30,
  "ten_1ms_ticks": 0,
  "then_7ms_ticks": 1,
  "overflow": false,
  "errors": []
}

```
待验证：宿主加载、付费模型、外部生成、联机/Unity/UE/3D、微信真机与发布。

## 交付ZIP全新解压重放（已执行）
2026-11-11（Asia/Shanghai）。从exercise.zip新解压后执行README全部命令；npm ci --ignore-scripts；五步均成功，结果与初次相同。不是独立审核。完整输出：
```text
$ npm ci --ignore-scripts --no-audit --no-fund

added 2 packages in 296ms
{
  "source_entries": 11,
  "read_ok": 11,
  "unique_repos": 10,
  "pinned": true,
  "core_sha256": "76b7dd6aa6ead0db8222fda85c970816043ddfbad6fa3ee44ddaecafffe01817"
}
{
  "mode": "replay",
  "steps": 600,
  "equal": true,
  "final": {
    "tick": 600,
    "x": 60,
    "y": 150,
    "r": 12,
    "coinX": 260,
    "coinY": 150,
    "score": 1,
    "paused": false,
    "seed": 1042201148,
    "events": []
  }
}
{
  "mode": "boundaries",
  "right_x": 308,
  "score": 2,
  "pause_tick_frozen": true
}
{
  "mode": "feedback",
  "steps": 120,
  "pickup_events": 2,
  "feedback_does_not_change_simulation": true,
  "flash_final": 0
}
{
  "pickup": {
    "tick": 30,
    "x": 120,
    "y": 150,
    "r": 12,
    "coinX": 260,
    "coinY": 150,
    "score": 1,
    "paused": false,
    "seed": 1042201148,
    "events": [],
    "coordinate": "origin top-left; +x right; +y down",
    "remainder_ms": 0,
    "flash": 0
  },
  "paused_tick": 30,
  "ten_1ms_ticks": 0,
  "then_7ms_ticks": 1,
  "overflow": false,
  "errors": []
}

```
