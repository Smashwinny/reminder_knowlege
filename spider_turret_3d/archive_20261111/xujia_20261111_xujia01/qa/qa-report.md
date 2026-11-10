# PDF作者自检记录（非独立审核）

实际打印：Google Chrome Headless 156，A4，10页；最终版PDF逐页由pdftoppm渲染PNG，10张均已用Read逐页查看。未使用浏览器登录/用户账号。

```bash
google-chrome --headless --disable-dev-shm-usage --no-pdf-header-footer --print-to-pdf=/workspace/reminder-batch/item01/guide.pdf file:///workspace/reminder-batch/item01/guide.html
pdftoppm -scale-to 1400 -png /workspace/reminder-batch/item01/guide.pdf /workspace/reminder-batch/item01/qa/page
pdftotext -layout /workspace/reminder-batch/item01/guide.pdf /workspace/reminder-batch/item01/qa/pdf-text.txt
```

## 逐页结论
1. 导读、五用途与适用范围完整；青蓝大标题、橙色警示可读。
2. Q01–02完整各自成卡；单图多解SVG与新增bpy说明/来源链接正常。
3. Q03–04完整；层级图、两连杆示意与术语行完整，未跨页。
4. Q05–06完整；可达圆环、四腿错相图文字未压盖，目标/真实末端边界清楚。
5. Q07–08完整；悬挂流程与双阈值图清晰，注释/实际实现差异保留。
6. Q09–10完整；事件阈值图与热量流程图无裁切。
7. Q11–12完整；换装/渲染循环图正常，未把源码参数作实测耗时。
8. 实验1–3完整；完整命令块、真实结果、验证均同页；代码字体可读。
9. 实验4–5完整；大留白是预留版面，非漏页；待验证警示完整。
10. 来源/查重表完整，长代码路径自动换行；无正文溢出或表格跨页。

结论：12问与12个内联SVG齐全，所有问答卡未跨页，文字/图示可读，无裁切；HTML外部依赖0；PDF文本回读无U+FFFD。机器统计与问答页码映射见checks.json。不是独立内容审核，也不等于浏览器3D应用运行成功。
