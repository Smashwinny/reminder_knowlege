# PDF实际打印与逐页制作者检查

2026-11-11 01:10（Asia/Shanghai）。Google Chrome Headless实际打印guide.html；pdfinfo核验9页、A4 594.96×841.92pt、887567字节。PDF使用字体子集；HTML无内嵌字体/图片，仅12个内联SVG。首版17页发现空白溢出，已改为flow-root/260mm页面并重渲染为9页。

最终9页全部经pdftoppm转PNG，使用Read逐张实际查看，未仅检查文本或拼贴缩略图：
1. final-page-1.png：封面/4用途/查重，青蓝橙配色，大标题和边界可读，无裁切。
2. final-page-2.png：问题1–3及3个SVG完整，无断字溢出。
3. final-page-3.png：问题4–6及3个SVG完整，版本和尾帧说明可读。
4. final-page-4.png：问题7–9及3个SVG完整，时间映射/QA字段无裁切。
5. final-page-5.png：问题10–12及3个SVG完整，GPU待验证边界可读。
6. final-page-6.png：实验1–2，命令换行可读、卡片未拆页。
7. final-page-7.png：实验3–4，完整映射/QA命令可读，误差结果完整。
8. final-page-8.png：实验5–6，测试命令、结果与边界完整。
9. final-page-9.png：来源URL自动换行，SHA完整，状态框完整。

检查结论：9页无空白页、无可见裁切或重叠，正文和命令可读。这是制作者自查，不是独立审核。PNG仅保留box，不纳入轻量包。
