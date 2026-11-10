# 出海工具选型清单与官网可达探测

离线解析长文目录，并对公开官方 URL 做只读 HTTP GET。不注册、不登录、不付款、不采购外链、不使用原文推荐码。

```bash
cd exercise
python3 checklist.py
python3 check_urls.py
python3 -m unittest test_catalog.py -v
```

`tools.json` 里的 `confidence`：

- official_known / search_confirmed：按公开资料填写的官方站点
- inferred：作者只写了简称（Customer），URL 是推断
- missing：原文缺号，不探测

官网返回 200 只说明「这个地址现在能打开」，不是对工具质量、价格或作者用法的核实。
