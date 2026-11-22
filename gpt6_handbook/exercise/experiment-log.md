# GPT-6 使用手册 · 实验日志（task 586bf976-da85-49cf-b295-8d283dbc5b97）

初跑：2026-10-28；独立审核修订与复跑：2026-11-22。
性质：原手册方法学习 + 官方当前文档复核 + 本地确定性成本模型。无 API key，未发任何真实计费请求。

## 初次实验记录

原脚本以当时 `vault/00-总览.md` 为样本，记录 60,073 token 粗估前缀：10 次调用不缓存 $3.0137、缓存 $0.6560、节省 78.2%、平衡 2 次。该数字是当时输入和假设下的历史结果，不应因总览后续变化而伪装成今天仍能逐字复现。

## 审核发现的口径问题

2026-11-22 读取官方 Prompt caching 文档与模型页面后，初稿以下说法不能保留：

1. GPT-5.6+ 不是固定“128 token 断点”；隐式断点跟随最新合格消息，也支持显式断点。128 是部分旧模型回执向下取整的粒度。
2. “差一个 token 整段 miss”过度绝对；准确说法是变化点之后不能复用。
3. 命中读价并非统一 0.1×：官方当前列出 GPT-6.2 Astra/Sol、GPT-6.1 Sol、GPT-6.1 Terra 为 0.05×。
4. 当前模型索引已列出 6.2 Astra/Sol 等；旧 `gpt-6-sol` 与 `gpt-6.1-sol` 页面仍可读取，但初稿“官方总览主推 6.1 Sol”已过时。旧 Sol 支持 `none`，6.1/6.2 Sol 页面不接收 `none`。
5. “前缀稳定+调用≥2 次就该吃缓存”只属于原示例全命中假设，不是通用结论。

官方来源：
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/models/gpt-6-sol
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://developers.openai.com/api/docs/models/gpt-6.2-sol

## 修订后的真实复跑

修订 `cache_economics.py`：移除无效循环和未使用变量，改用仓库相对样本路径；加入样本、调用次数、新增 token、普通读价、命中读价和写入倍率参数；逐次比较缓存/不缓存总成本求平衡次数。明确假设首次写入、后续每次全部命中。

实际命令（仓库根目录，`PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python -I`）：

```bash
python -I gpt6_handbook/exercise/cache_economics.py
python -I gpt6_handbook/exercise/cache_economics.py --cached-read-multiplier 0.05
```

两次均正常退出。当前 `vault/00-总览.md` 粗估前缀 65,903 token，每次新增 200 token、共 10 次、普通读价假设 $5/M、30m 写入 1.25×：

| 命中读价假设 | 不缓存 | 缓存（含首次写入） | 节省 | 平衡次数 |
|---|---:|---:|---:|---:|
| 0.1× | $3.3052 | $0.7187 | 78.3% | 2 |
| 0.05× | $3.3052 | $0.5704 | 82.7% | 2 |

第一行首次写入 $0.4131。上述成本全部是模型估算；粗分词不替代真实 tokenizer，后续全命中不替代 usage 回执，TTL/路由/实际价格仍需按官方与账单核对。

## PDF 审核

- 原 PDF 经 Windows 11 自带 `Windows.Data.Pdf` 实际逐页渲染，共 7 页；发现物理页序为 Q3/Q4 → 封面/Q1 → Q2 → Q5/Q6 → 能力/总结 → Q10 → Q7–Q9，不能通过。
- 从修订后的 HTML 重新用 Edge 无头打印；新 PDF 共 12 页，全部经同一 Windows API 渲染并生成 3 列联系表逐页检查，封面/Q1 在第 1 页，后续按 Q2…Q10、能力、总结、来源排列，无裁切或空白页。Q10 因内容较高自然跨页。审核缩略图只存系统临时目录，不进入公开仓库。
- 覆盖原 PDF 的动作被权限层拒绝，故原件保留，审核版新增为 `gpt6_handbook/GPT-6使用手册-小白指南-v2.pdf`；SHA-256 `fe92abf9239f237d9f3f5eb627725202837814cbefcf841e73478fd5ae821884`，与临时渲染源一致。
- 临时安装 PyMuPDF/Pillow 的动作被权限层拒绝，未安装、未绕过；最终使用操作系统自带 API。

## 结论

- 保留原手册“按任务选型、锁参数、缓存分账”的学习价值，同时把机制事实更新到 2026-11-22 官方口径。
- 本地脚本验证的是成本公式和参数敏感性，不是 OpenAI 真实缓存命中、延迟、质量或价格全量验收。
- 原手册的发布日期、基准数值、客户案例和灰度范围仍未逐项核实，不写成事实。
