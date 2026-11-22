# Today 选题工作流 · 实验日志（task 18c3612c-4197-492a-90a2-e722f38274d3）

初跑：2026-10-28；审核修订：2026-11-22。
性质：原引用帖工作流学习 + 本地排序原型。无 Today 账号，未实机；未代发帖或付款。

## 历史真实 API 记录（保留但不当作今天榜单）

2026-10-28 初版从 GitHub Search API 与 Hacker News API 取得 11 条候选并输出 `radar-draft.md`。当时记录包括 android-ad-cleaner、t3dotgg/tstack 和 HN 讨论等。该记录只证明当时访问过公开 API，不保证榜单数字今天仍准确，也不证明外链原报道已核实。

## 审核发现的问题

1. 初版声称“时效/普适/一手料/脱水/叙事轮换五阀”，实际只有四类加分，完全没有叙事轮换。
2. 所有候选无条件得 2 个时效分，包括 HN；没有读取发布日期。
3. “AI 关键词=普适”混淆目标受众匹配与普遍适用；现改为当前 AI 受众关键词。
4. HN 是直接讨论信号，不等于原报道事实核验。
5. 缺少少量标题情绪词只能算脱水初筛，不能证明内容脱水。

## 2026-11-22 官方页面复核

https://today.ai/ 描述用户可控记忆、主动提示、计划与工具执行、连接器和云电脑。页面未承诺独立“选题雷达”功能、免费无限使用、任意任务成功、发布/付款授权或 Token 赠送。指南把原引用帖工作流与官方产品事实分开。

## 修订后的离线实验

新版五项各 1 分：时效、目标受众、直接信号、标题脱水初筛、叙事轮换。默认读取明确标注的合成夹具，不联网；`--live` 才访问公开 API。输出只产草稿。

实际命令：

```bash
python -I today_topic_radar/exercise/topic_radar.py --today 2026-11-22
python -I today_topic_radar/exercise/test_topic_radar.py
```

输出 `radar-draft-v2.md`：5 条合成候选，cache-cost-lab 5/5；agent-safety-replay 因近期同主题 4/5；old-model-news 因过期 4/5；garden-sensor-diary 因受众不符 4/5；标题情绪+二手来源候选 3/5。

7 项 unittest 全部通过：五项完整、叙事轮换、时效、二手来源与标题、受众、缺日期 fail-closed、输入不变和草稿来源保留。本轮未重跑实时 API。

## PDF

修订 HTML 后新增 v2 PDF，共 9 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→能力/总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `bc714a05a3623b84de98966380681abb58cd79302e6a9ce7c30dcd9a738def96`。
