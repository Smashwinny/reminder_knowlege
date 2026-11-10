# A4 PDF逐页自查

日期：2026-11-11 Asia/Shanghai UTC+8；检查者：本续跑worker，非独立审核。

初次Chrome打印超过2分钟挂起，定向终止该worker PID；第二次bounded尝试60秒超时（exit 124）。保持sandbox原状，没有改安全设置。改用已装的WeasyPrint 70.0打印最终HTML，exit 0，575607 bytes、7页、595.276×841.89 pt A4。未修改或重做第4项，只借用其已经安装的渲染环境。

命令：
```bash
/workspace/reminder-batch/item04/research/pdf-venv/bin/python -m weasyprint /workspace/reminder-batch/item01/item01.html /workspace/reminder-batch/item01/item01.pdf
pdfinfo /workspace/reminder-batch/item01/item01.pdf
pdftoppm -scale-to 1500 -png /workspace/reminder-batch/item01/item01.pdf /workspace/reminder-batch/item01/evidence/checked-page
```

已对7张PNG逐一使用Read实际目视：
1. 封面、4用途、查重：无截字，三色图清楚。
2. Q01–03：3张卡片及SVG全部入页。
3. Q04–06：节拍与1ms数字清晰，无跨页卡片。
4. Q07–09：重心/相机例外图清楚，脚注正常。
5. Q10–12：补充校验器边界未溢出，3张SVG完整。
6. 5步实验：命令完整可读，结果与验证未被截断，脚注入页。
7. 来源/状态表/待验证：SHA长行可读，表格和橙色卡片完整。

最终PDF保留矢量文本与字体子集，未栅格化，不嵌整套字体。PNG只留本云目录，不加入轻量包。
- checked-page-1.png SHA256 `1ac52e4eec6183794211ada3938eb27eea533f090b3ecb2985c59d323b645524`
- checked-page-2.png SHA256 `c004ffefd52d946d1d6fc0d49831228103c8ec58aa74a1917ac3e571acee45f1`
- checked-page-3.png SHA256 `149bbbd6bfc623dae8c533ae52eed5827c8d04670a3a409303e27bb224bc22b8`
- checked-page-4.png SHA256 `bb369af379a035442ab9f0ad28d5e719a9a19c6892449502867d689b94ed4ca9`
- checked-page-5.png SHA256 `e3852c9cf9ff449f66141115e0669a677103718c5ede8845266b43ba89434241`
- checked-page-6.png SHA256 `0f9fa7069e8c09bac005c0d2ba590764df479fa6bb3ae5609e7477ce5853a415`
- checked-page-7.png SHA256 `a736aea146b17c26d8922e9147ac8fb00fa9f1fd2a24747a00c2ece3461acd90`
