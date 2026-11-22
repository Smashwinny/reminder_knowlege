# Manus Studio 视频工作流 · 实验日志（task ab9eb890-494c-4eb5-b014-33e36147b454）

初跑：2026-10-28；独立审核修订与复跑：2026-11-22。
性质：官方产品机制学习 + 自写本地交接协议实验。未登录 Manus，未生成或导出视频。

## 官方来源复核

2026-11-22 读取 https://manus.im/blog/introducing-video-editor ：

- 明确提到生成镜头、图片、字幕、动效、旁白、音乐和音效占据独立时间轴轨道，项目保持可编辑，“不是 flattened MP4”。
- 明确提到人工 reposition/trim、修改字幕、调整音量、导入本地 footage，以及“Manus picks up from your edits instead of starting over”。
- 页面未提锁定控件、`locked` 字段或 AI 跳过锁定元素的承诺，也未给具体导出格式/分辨率/编解码工作流。页面没提不等于功能不存在，但不能由本地脚本补写成官方事实。

另读 https://manus.im/blog/introducing-manus-2-0 作为产品背景。原帖 Cue 案例的 140 万与厂商 170 万播放口径不作流量审计，24 小时全流程无工程文件佐证。

## 审核发现并修复的实验问题

1. 初稿把自写 `locked` 说成“人机接力的信任基础”，容易冒充 Manus 内部机制；现统一标为本地保守协议。
2. 初稿“品牌四项约束 80% 偏差”无实验或官方依据，已删除；四项仅保留为起步检查表，不称官方最小集。
3. 原 `ai_polish` 只修改 note，不修改 value；即使删除 locked 判断，人工替换的素材值也不会被覆盖，原破坏测试无效。
4. 初稿“24 小时案例瓶颈不是生成质量而是修改成本”是未经证实的归因，已改为分层工程的一般局部修改优势，不反推案例事实。

## 修订后的真实复跑

`timeline_relay.py` 现在用深拷贝分别运行两条路径：

- 尊重锁定：5 个未锁元素被润色，`shots/s2` 的人工值与“人工修改”备注均保留，跳过列表恰为 `['shots/s2']`。
- 删除保护：同一 `shots/s2` 的值被改成“AI 二轮统一润色版本”，证明破坏测试确实能覆盖人工值。

实际命令（仓库根目录，`PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python -I`）：

```bash
python -I manus_studio_workflow/exercise/timeline_relay.py
python -I manus_studio_workflow/exercise/timeline_relay.py --slogan "把复杂留给流程" --replacement "authorized-demo-footage.mp4"
```

两次均正常退出，两条路径的全部断言 PASS。第二次使用明确标注的自定义合成文件名，保护路径保留 `authorized-demo-footage.mp4`，破坏路径覆盖它。

## PDF 审核

修订后重印 PDF 共 10 页，全部使用 Windows 11 自带 `Windows.Data.Pdf` 渲染并生成联系表逐页检查：封面→Q1…Q10→能力/总结→来源，未见裁切或空白页。审核 PNG 留系统临时目录。覆盖原 PDF 的动作被权限层拒绝，故原件保留，审核版新增为 `manus_studio_workflow/Manus-Studio视频工作流-小白指南-v2.pdf`；SHA-256 `b9849f7e943774613e39d9704b413911b8f2037c0e9e6e58715e21ee6d864810`，与临时渲染源一致。

## 结论

- 可学习的官方事实：分层可编辑工程、人工修改、从人工修改继续。
- 可复用的本地方法：锁/快照/变更清单等保守交接协议；其有效性必须用保护路径与破坏路径一起验。
- 未验证：Manus 是否提供相同锁定功能、真实 AI 接力行为、导出能力、播放量和 24 小时案例归因。
