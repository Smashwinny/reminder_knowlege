# yigezi：一个字的形音义族时间轴 · 真实实验日志

执行时间：2026-11-11 01:20:12 CST（UTC+8）

只读公共研究＋云端隔离实验。自编程序不是上游实现，除明确标出的官方构建。

## 从快照提取并查询
目的：读取只读快照，计数并查询江、水、木、为、射等字

```bash
cd /workspace/reminder-batch-2026-11-11/item-6-yigezi
python3 exercise/query.py query
```

真实输出（exit=0）：
```text
html /workspace/reminder-batch-2026-11-11/sources/yigezi-index.html sha256 276d116fc0818183f03ce6542856718007d63619d75cf4c57252c331e269ddcd bytes 1752111
counts {"seal": 10249, "oracle": 1425, "shuowen": 9815, "series": 740, "corrections": 10, "trad_map": 2151}
match {'seal': True, 'oracle': True, 'shuowen': True, 'series': True}
LOOKUP 江: seal=江 oracle=— py=jiānɡ mc=kaewng oc=*krˤoŋ ocsrc=bzd series=工:21 shuowen=水。出蜀湔氐徼外崏山，入海。从水工聲。…
LOOKUP 水: seal=水 oracle=水 py=shuǐ mc=sywijX oc=*stuiʔ ocsrc=bzd series=None:0 shuowen=凖也。北方之行。象眾水並流，中有微陽之气…
LOOKUP 木: seal=木 oracle=木 py=mù mc=muwk oc=*mˤok ocsrc=bzd series=None:0 shuowen=冒也。冒地而生。東方之行。从屮，下象其根…
LOOKUP 为: seal=爲 oracle=爲 py=wéi mc=hjwe;hjweH oc=None ocsrc=None series=爲:10 shuowen=母猴也。其爲禽好爪。爪，母猴象也。下腹爲…
  XZ: 甲骨文从「又」（手）从「象」，会以手牵象劳作之意（罗振玉说）。《说文》训「母猴也」，是未见甲骨文而致误。
LOOKUP 射: seal=射 oracle=射 py=— mc=— oc=— ocsrc=— series=None:0 shuowen=—
  XZ: 甲骨文像手拉弓搭箭之形。《说文》析为「从矢从身」，于古文字无据。
LOOKUP 龙: seal=龍 oracle=龍 py=lónɡ mc=ljowng oc=*roŋ ocsrc=bzd series=龍:20 shuowen=鱗蟲之長。能幽，能明，能細，能巨，能短，…
LOOKUP 氵: seal=— oracle=氵 py=— mc=— oc=— ocsrc=— series=None:0 shuowen=—

```
验证：输出含 counts 与 match 四项为 True

## 核对计数与缺省规则
目的：确认规模与README一致，且纠正条目存在、未编造读音

```bash
cd /workspace/reminder-batch-2026-11-11/item-6-yigezi
python3 exercise/query.py verify
```

真实输出（exit=0）：
```text
html /workspace/reminder-batch-2026-11-11/sources/yigezi-index.html sha256 276d116fc0818183f03ce6542856718007d63619d75cf4c57252c331e269ddcd bytes 1752111
counts {"seal": 10249, "oracle": 1425, "shuowen": 9815, "series": 740, "corrections": 10, "trad_map": 2151}
match {'seal': True, 'oracle': True, 'shuowen': True, 'series': True}
LOOKUP 江: seal=江 oracle=— py=jiānɡ mc=kaewng oc=*krˤoŋ ocsrc=bzd series=工:21 shuowen=水。出蜀湔氐徼外崏山，入海。从水工聲。…
LOOKUP 水: seal=水 oracle=水 py=shuǐ mc=sywijX oc=*stuiʔ ocsrc=bzd series=None:0 shuowen=凖也。北方之行。象眾水並流，中有微陽之气…
LOOKUP 木: seal=木 oracle=木 py=mù mc=muwk oc=*mˤok ocsrc=bzd series=None:0 shuowen=冒也。冒地而生。東方之行。从屮，下象其根…
LOOKUP 为: seal=爲 oracle=爲 py=wéi mc=hjwe;hjweH oc=None ocsrc=None series=爲:10 shuowen=母猴也。其爲禽好爪。爪，母猴象也。下腹爲…
  XZ: 甲骨文从「又」（手）从「象」，会以手牵象劳作之意（罗振玉说）。《说文》训「母猴也」，是未见甲骨文而致误。
LOOKUP 射: seal=射 oracle=射 py=— mc=— oc=— ocsrc=— series=None:0 shuowen=—
  XZ: 甲骨文像手拉弓搭箭之形。《说文》析为「从矢从身」，于古文字无据。
LOOKUP 龙: seal=龍 oracle=龍 py=lónɡ mc=ljowng oc=*roŋ ocsrc=bzd series=龍:20 shuowen=鱗蟲之長。能幽，能明，能細，能巨，能短，…
LOOKUP 氵: seal=— oracle=氵 py=— mc=— oc=— ocsrc=— series=None:0 shuowen=—
verify_failed 0
VERIFY PASS

```
验证：退出码0

## 检测在线演示并制作占位GIF
目的：对官方演示做只读HTTP检测，并生成明确标注的占位演变GIF

```bash
cd /workspace/reminder-batch-2026-11-11/item-6-yigezi
python3 exercise/live_and_gif.py
```

真实输出（exit=0）：
```text
{
  "checked_at": "2026-11-11 01:20:12 CST（UTC+8）",
  "demo": {
    "url": "https://ivan666jjj.github.io/yigezi/",
    "final_url": "https://ivan666jjj.github.io/yigezi/",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "bytes_preview": 2048,
    "elapsed_s": 0.09,
    "contains_title": true
  },
  "repo": {
    "url": "https://api.github.com/repos/Ivan666jjj/yigezi",
    "status": 200,
    "full_name": "Ivan666jjj/yigezi",
    "sha_pushed_at": "2026-10-26T07:23:00Z",
    "stargazers": 135,
    "default_branch": "main",
    "homepage": "https://ivan666jjj.github.io/yigezi/",
    "license": "MIT"
  },
  "gif": {
    "path": "/workspace/reminder-batch-2026-11-11/item-6-yigezi/exercise/placeholder-evolution.gif",
    "bytes": 17320,
    "note": "system-font placeholder, not official glyphs"
  }
}
LIVE+GIF PASS

```
验证：输出 LIVE+GIF PASS；不得把GIF当成官方字形

## 留下快照与脚本指纹
目的：锁定查询脚本与结果

```bash
cd /workspace/reminder-batch-2026-11-11/item-6-yigezi
sha256sum exercise/query.py exercise/results.json exercise/live.json
```

真实输出（exit=0）：
```text
a9aa90aca66906b21e4d9a3a124d44e59e22b0df861250040b9cb9cf2ebb03fc  exercise/query.py
34da927ad87ceab1f149c74c2ec81a0ae32bf9591bbdc536d7288a153a0e885e  exercise/results.json
adb99761ef46db94d2393a71c4e98dbfbf6ed0958b86cbaa480726c227cf83b5  exercise/live.json

```
验证：results.json 中 html_sha256 仍为 276d116f…


## 未验证边界
未把官方 seal.woff2 / orac.woff2 打进练习包，也未运行项目自研 GIF89a 编码器；占位GIF使用系统字体，不能当作甲骨文或小篆原形。未核验全部 9815 条说文的文献准确性，只核验了计数与抽样查询。上古音再分发授权仍待向来源站确认。
