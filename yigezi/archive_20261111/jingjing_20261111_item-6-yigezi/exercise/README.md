# 第 6 项练习：yigezi 数据核验

默认读取本批次只读快照 `sources/yigezi-index.html`（对应仓库 main SHA `948c3f3778c4ef2da094fe782d98c118282df91a`）。练习包不附带完整页面和字体，以免把第三方字形数据再分发。

```bash
python3 query.py query
python3 query.py verify
python3 live_and_gif.py
sha256sum query.py live_and_gif.py results.json live.json
```

- 成功标准：快照中小篆/甲骨/说文/谐声计数与 README 声明一致；「江」「为」「射」等查询不编造缺失项；在线演示 HTTP 200 且含标题；占位 GIF 明确标注非官方字形。
- `placeholder-evolution.gif` 使用系统字体，不得当作甲骨文或小篆原形。
