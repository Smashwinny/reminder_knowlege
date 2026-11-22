# Qiaomu RSS for DeepSeek Harness · 实验日志（task 6665d851-dedd-4a8d-8cb2-cb2ae78b020e）

初跑：2026-10-28；审核修订：2026-11-22。
上游：joeseesun/qiaomu-rss-dsh，固定 commit `349398b feat(reader): default to the 乔木改写 version`。该版本 package.json 为 0.9.0 / GPL-3.0-only。未安装 DeepSeek Harness 0.2.0-rc.2，未运行上游插件。

## 固定源码审计

- 8 个 rss_* 工具在源码确认：add/remove_subscription、list_channels、list_articles、read_article、search_articles、refresh、generate_version。
- 固定版本中 README 安装段为 v0.7.0，package.json 为 0.9.0；只陈述该 commit 的漂移，不冒称当前 main 仍相同。
- 维护者版本验证记录不是本轮实测；插件许可与内置博客名单许可分开。
- 社区插件非 DeepSeek 官方维护；实验室收录的隐私行为按原学习源码记录保留。

## 初学期真实 feed 与本轮边界

初学期曾访问 blog.python.org 并读取 Python Insider RSS。原复刻把 `content[:1500]` 输出为“背景-整篇”，名实不符：截断内容只能是背景摘录。本轮不重复联网，历史记录不当作当前 feed 快照。

## 修订后的离线实验

`rss_companion_demo.py` 默认读取明确标注的合成 RSS 夹具，只有显式 `--feed-url` 才联网。`build_scope` 返回背景长度、原文长度、`truncated` 和选段；截断时不再称整篇。

初次构造夹具时分别只有 623、1199、1497 字符，长文测试正确失败；没有降低 1500 断言，补足合成内容后最终为 1525 字符。实际命令：

```bash
python -I qiaomu_rss_dsh/exercise/rss_companion_demo.py
python -I qiaomu_rss_dsh/exercise/test_rss_companion.py
```

最终输出：5 篇合成文章，背景 `1500/1525 字符；truncated=True`，请求选段为第一段。6 项 unittest 全部通过：5 项解析、长文截断、短文完整、选段属于原文、精确长度和非法预算 fail-closed。

## 重要边界

- 范围声明只控制输入；提示“只能引用选段”不证明模型实际遵守，仍需保存回答并核对引用。
- 自动首段不一定包含足够限定条件，不称“最小充分上下文”。
- GPL 段改为区分私人使用与对外分发义务，不用一句话代替许可证全文或法律意见。

## PDF

修订 HTML 后新增 v2 PDF，共 8 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→能力/总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `85e67f2b31ad70cf4f2d3b2878e382c6870060dc9ed39c8bf644a64092cbf251`。
