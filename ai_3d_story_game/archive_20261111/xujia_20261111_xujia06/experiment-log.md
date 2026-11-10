# 第6项真实实验日志
2026-11-11（Asia/Shanghai）
## 原作者HTML：未执行
Notion正文通过WebFetch可读，文件块下载直链未返回；直接读公开页HTTP403；没有浏览器子代理。没有游戏仓库SHA，未伪造。没有加载作者HTML。
## 以下为原创方法层实验
### 1 固定原创输入与依赖 已执行
目的：记录本次文件指纹和Three版本，同时保留原游戏未取得事实。
命令：`python3 audit.py`
真实结果：Three0.170.0；作者HTML下载=false，非原游戏源码；两个SHA256见JSON。
验证/边界：审计字段明确阻止把教学文件当作者源码。

### 2 检查剧情图引用 已执行
目的：检查四节点的next引用，不靠截图猜章节关系。
命令：`node test.cjs graph`
真实结果：nodes=4、broken_edges=0。
验证/边界：只检查原创小图，不是原作剧情覆盖率。

### 3 验证门槛与重复动作 已执行
目的：测试未经收集旅行、重复收集、第二门槛。
命令：`node test.cjs gates`
真实结果：三个条件均通过，合法收集后地点ridge。
验证/边界：assert对状态深比较；没有调用模型。

### 4 通关路径与重放 已执行
目的：对同一动作序列重复执行。
命令：`node test.cjs route`
真实结果：5次动作到ending；背包memory/stone、visited含四节点，两次一致。
验证/边界：逻辑层，不等于浏览器叙事全链路。

### 5 真实WebGL加载与资源更换 已执行
目的：启动临时本地HTTP，CLI headless Chrome加载原创scene.html、dump DOM及截图。
命令：`python3 browser.py`
真实结果：Chrome退出0；WebGL=true、r170；初建+12次更换，共13次记录点；12个geometry count均1；1 draw call、180 triangles。
验证/边界：scene.png已查看；原作者HTML没有加载。软件后端/性能未确认，不报告FPS。

```text
执行日期 2026-11-11 01:19:31 Asia/Shanghai
v24.22.1
Python 3.13.5
Google Chrome 156.0.8078.47 
$ python3 audit.py
{
  "story_sha256": "c9ed5e314b7cd97c9cb83b14d41d5e198adcbbff718a85fad26cec0f5a947a58",
  "scene_sha256": "c4c98ab83497b65d2c92424fe6db20dc4a251d955b0c5758e5bc3de029a2638a",
  "three_version": "0.170.0",
  "is_original_game_source": false,
  "author_html_downloaded": false
}
$ node test.cjs graph
{
  "mode": "graph",
  "nodes": 4,
  "broken_edges": 0
}
$ node test.cjs gates
{
  "mode": "gates",
  "early_travel_blocked": true,
  "duplicate_item_prevented": true,
  "second_gate_blocked": true,
  "place": "ridge"
}
$ node test.cjs route
{
  "mode": "route",
  "actions": 5,
  "state": {
    "place": "ending",
    "bag": [
      "memory",
      "stone"
    ],
    "visited": [
      "grove",
      "ridge",
      "observatory",
      "ending"
    ],
    "ended": true
  },
  "replay_equal": true
}
$ python3 browser.py
COMMAND ['/usr/bin/google-chrome', '--headless', '--no-sandbox', '--no-pdf-header-footer', '--window-size=900,1100', '--virtual-time-budget=3000', '--screenshot=scene.png', '--dump-dom', 'http://127.0.0.1:36939/scene.html']
chrome_exit 0
{
  "three_revision": "170",
  "webgl": true,
  "scene_switches": 13,
  "geometry_counts": [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
  ],
  "all_one": true,
  "draw_calls": 1,
  "triangles": 180
}

```
真实截图scene.png已查看：青色低多边形球、按钮与记录。逻辑测试与浏览器demo未集成完整剧情。
