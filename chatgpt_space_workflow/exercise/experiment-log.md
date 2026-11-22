# ChatGPT Space 页面工作流 · 实验日志（task 9ab3f8bd-3512-4a6d-8be3-1340a9039c7a）

初跑：2026-10-28；审核修订：2026-11-22。
性质：官方当前产品文档学习 + 自定义 HTML→Markdown 单向模拟。无 ChatGPT 账号，未创建 Space。

## 2026-11-22 官方复核

- Space 总览：https://learn.chatgpt.com/docs/space
- 协作：https://learn.chatgpt.com/docs/space/collaboration

当前总览介绍 Pages、Slides、表格和 Sites；人与 ChatGPT 可共同编辑。所读总览没有文档化初稿的“四种块”、页面内交互可视化或 @ 块，初稿相关说法只保留为原截图观察和本地模拟元素，不再称当前官方确认。

当前协作页列出 View/Comment/Edit；Slides 为 View/Edit，权限可随 Space/父页继承。链接来源保留原权限；复制/摘要进页面的内容可能对页面访问者可见。总览明确分享页面不共享私人聊天或保存的记忆。Link access/Copy link 不等于文档已定义匿名公开状态。

## 初稿实验问题

1. `space_export.py` 只有 HTML→Markdown 单向转换，却写“往返转换”。
2. 输入/输出使用 cwd 相对路径，指南从项目根目录运行会找不到文件。
3. 自定义 viz/ref/file 的降级规则被写成 Space 的真实导出边界，证据越界。
4. “所有导出必然死快照”过度绝对，其他活格式与在线分享未验证。

## 修订后的真实复跑

新版用脚本目录定位输入，默认新增 `space-demo-export-v2.md`，明确单向、本地模拟、非 Space 导出器。实际命令：

```bash
python -I chatgpt_space_workflow/exercise/space_export.py
python -I chatgpt_space_workflow/exercise/test_space_export.py
```

主程序断言通过；5 项 unittest 全部通过：6 块顺序、viz 静态占位、ref 不带实时上下文、file 未复制/修改、源文件不变。初次测试把 6 块误写为 5 块导致 1 个计数失败，按实际输出修正为 6 块后通过，没有修改导出逻辑迁就测试。

## PDF 与边界

修订 HTML 后新增 v2 PDF，共 8 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→能力/总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `e731e9a01ad9c06c5c2fea095ab92ad6d2d7e618532694b91610dc34d63484dc`。未验证真实 Space 页面、Markdown 导出、历史版本、原位文件编辑或公开访问。
