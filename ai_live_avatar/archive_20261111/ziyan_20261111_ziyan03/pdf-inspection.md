# PDF打印与逐页自检

检查完成：2026-11-11T01:11:21.047254+08:00（Asia/Shanghai UTC+8）。Chrome headless实际打印11页A4（594.96×841.92 pt）。pdftoppm逐页输出1300像素PNG，使用Read分别打开并人工视觉检查全部11页，不是只看拼图或只做文本提取。

- 第01页：封面、用途与查重；渐变标题、重点和SHA均完整；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-01.png。
- 第02页：问题01—02；中文、SVG与来源链接清晰；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-02.png。
- 第03页：问题03—04；意图与FIFO说明未裁切；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-03.png。
- 第04页：问题05—06；容量反例、暖场图和空池边界完整；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-04.png。
- 第05页：问题07—08；估算参数与换装待验标记完整；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-05.png。
- 第06页：问题09—10；风险与历史费用数字完整；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-06.png。
- 第07页：问题11—12；OBS及上线边界说明完整；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-07.png。
- 第08页：步骤1—2；命令块和完整哈希可读；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-08.png。
- 第09页：步骤3—4；模拟输出与AST边界完整；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-09.png。
- 第10页：步骤5—6；费用与核验命令可读；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-10.png。
- 第11页：证据列表及待验证清单完整；未见重叠、溢出或缺字。PNG=evidence/pdf-pages/page-11.png。

原PDF 961959 bytes，经pypdf内容流level9与对象去重压到912036 bytes。压缩后重新转11页PNG，与此前Read检查的每页PNG字节完全一致；完整hash记录evidence/pdf-raster-verification.txt。两次压缩调用因pypdf 7参数改名在写入前失败，改正后完成，无隐藏内容变更。

此为同一worker自检，不是独立审查；轻包不附PNG，全部PNG和PDF原版留在工作目录。
