# Agent Reach 动手实验记录（2026-10-02，本机真实执行）

> 实验设计思路：Agent Reach 是"胶水层/能力层"，本身不抓取数据——每个渠道底层都指向一个具体上游接口或 CLI。因此我们直接验证这些底层事实（与 `repo/agent_reach/channels/` 源码逐行核对过），等于验证 doctor 探测的对象。
>
> ⚠️ 环境说明：本机权限策略禁止执行本会话新克隆的外部仓库代码（`pip install -e repo` 被拒），故 `agent-reach install / doctor` 本体未运行。下列 5 个实验全部真实执行并附原始输出。

## 实验 1：Jina Reader 读网页（web 渠道首选后端）

```bash
curl -s -m 20 "https://r.jina.ai/https://example.com"
```

对应源码：`repo/agent_reach/channels/web.py` → Jina Reader。

输出（截断）：

```
Title: Test Document

URL Source: https://example.com/

Warning: This is a cached snapshot of the original page, consider retry with caching opt-out.

Markdown Content:
## Test Article
```

结论：✅ 通过。任意 URL 前拼 `https://r.jina.ai/` 即可免费拿到清洗后的 Markdown，零配置零 Key。

## 实验 2：B站搜索 API（bilibili 渠道零依赖兜底）

```bash
curl -s -m 15 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=agent&page=1"
```

对应源码：`repo/agent_reach/channels/bilibili.py` 的 `_check_search_api()`，判定标准 `data.get("code") == 0`。

输出（截断）：

```json
{"code":0,"message":"OK","ttl":1,"data":{"seid":"2703748024416911767","page":1,"pagesize":20,...,"numResults":1000,"numPages":50,...}}
```

结论：✅ 通过，`code:0` —— 与 doctor 的判定逻辑一致，"至少搜索可用"。

## 实验 3：V2EX 热帖公共 API（v2ex 渠道底层）

```bash
curl -s -m 15 "https://www.v2ex.com/api/topics/hot.json"
```

输出（截断）：

```json
[{"node": {"name": "programmer", "title": "程序员", "topics": 73680, ...}, ...]
```

结论：✅ 通过。V2EX 公共 API 无需登录即可读热帖，属 tier 0 零配置渠道。

## 实验 4：GitHub 官方 API（github 渠道 gh CLI 的底层）

```bash
curl -s -m 15 "https://api.github.com/repos/Panniantong/Agent-Reach"
```

输出（经 python 格式化）：

```
full_name: Panniantong/Agent-Reach
stars: 88005
license: MIT
description: Give your AI agent eyes to see the entire internet. Read & search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu — one CLI, zero API fees.
```

结论：✅ 通过。**实测 88,005 stars**（推文传播极快；搜索时还是 10K+ 口径）。GitHub 渠道零配置可读公开仓库，认证后解锁私有库/PR。

## 实验 5：RSS 源零依赖解析（rss 渠道概念验证）

```python
import urllib.request, xml.etree.ElementTree as ET
req = urllib.request.Request('https://www.ruanyifeng.com/blog/atom.xml', headers={'User-Agent':'Mozilla/5.0'})
root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
ns = {'a':'http://www.w3.org/2005/Atom'}
entries = root.findall('a:entry', ns)
print('feed title:', root.find('a:title', ns).text)
print('entries:', len(entries))
for e in entries[:3]:
    print('-', e.find('a:title', ns).text)
```

输出：

```
feed title: 阮一峰的网络日志
entries: 3
- 科技爱好者周刊（第 413 期）：再见了，React Native
- 科技爱好者周刊（第 412 期）：禁止 issue，只用 PR
- 科技爱好者周刊（第 411 期）：OpenClaw 2.0 是一个缩影
```

结论：✅ 通过。RSS/Atom 本质是 XML，标准库即可解析（项目本身用 feedparser）。

## 如果要在本机跑完整 agent-reach

```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto        # 默认只读安全检查
agent-reach doctor                    # 全渠道体检
agent-reach install --dry-run         # 预览 --system 会做什么
```

注意：不要从 PyPI 装同名 `agent-reach` 包，那不是本项目（README 明示）。
