# Ultra-Water 最终独立质量审核

审核者：Codex 独立审查代理 `coordination_check`，独立于 Grok 教材作者、本地 claude_kimi 实验/合稿者和浏览器操作协调者。
日期：2026-11-11，Asia/Shanghai。

**结论：本报告绑定的最终教材、实验材料、PDF与知识候选质量审核通过，可以由协调者继续合入和发布。** 所有本轮发现的实质或口径问题均已修正。本结论不代表共享vault已经合入、Git已经提交/推送、Reminder已经保存报告或用户任务已经勾选完成。

## 1. 最终审查对象与哈希

上游固定提交：`30ea65ecb0a66b137aa200d099965634bdd84d51`。本地只读源码位于 `F:\reminder\ultra_water\repo`。

| 最终文件 | bytes | SHA256 |
|---|---:|---|
| ultra-water-final.html | 67,521 | 465cd87f83797a43e520e47fb11841729fdbdf3a28adc4b3c8890391ffb7b561 |
| ultra-water-final.pdf | 808,457 | 5b23ae66e03ef4cc1ce5dc2f8084f4030d31ccbd286c3f00ab049971d86fdfd7 |
| ultra-exercise.zip | 17,565 | da3f23bdfa8439cdfb4072bdbbd88a420be1c47f138e477963347d5b285e92fa |
| ultra-knowledge-candidate/knowledge-notes.md | 15,083 | e155c2c2feb67ac4bf888ab76c2c1ef7ab38756b7576cb8ce88c6db7d5f4edac |
| browser-experiment-evidence.txt | 2,419 | addf74eca00694afaa27e7b72d2fed3759a7e4abfdcb198a3816e4451f824335 |

这些文件位于 `D:\agenttry\reminder-learning-20261110`。只批准上述字节版本；后续正文、图片或数值变化须重新审查相应部分。移动同一原字节到最终项目目录不改变本结论。

## 2. 教材机制与来源

- q1–q12共12问，每问各1张内联SVG；5项具体用途；5步主实验。结构要求满足。
- 50个去重后的固定GitHub源码行范围，均属于指定SHA、存在的文件与有效行号。范围有效性不是语义证明；本轮同时沿用并复核此前逐问源码审查，重点重新检查所有改动处与新增实验口径。
- Q1已正确区分：反射在相机低于查询水面约0.3m时跳过；水下合成覆盖水面以下及高出水面不足约1.2m；深潜优化没有被误写为跳过整个水下合成。
- 四级世界尺度、256²单层/256×1024图集、横纵各8个IFFT阶段、前三层位移/四层坡度与源码相符。
- JONSWAP双谱、重力/毛细色散、300秒量化相位、Jacobian泡沫恢复、光学近似、三深度焦散、水下单散射、单元浮力、延迟读回及容量/tag边界均有明确源码依据。没有把视觉近似写成完整流体求解或工程精度证明。
- Q11和实验页正确区分HUD、可选GPU query、批量基准。`main.js:454–475`暂停的是常规循环：20个预热帧和300个测量帧均调用 `renderFrame(1/200)`，模拟继续推进。当前稿已不再将其写成冻结同一场景。
- `GpuTimer.drain()`未重新检查disjoint的限制保留；当前稿明确本轮也未独立捕获该状态。

此前逐问证据细表见 `independent-content-review.md`。该旧文件的“不完整”状态属于旧草稿，不能单独用于最终通过；本报告在其基础上完成了实验、PDF与知识候选审核。

## 3. 实验与证据核对

本审查没有重新安装依赖、运行海洋程序或再次进行GPU benchmark，避免把重复执行当作额外必要性。审核对象是实际原日志、源码、数值输出、打包原件和协调者实际浏览器观察记录；明确区分“审阅执行证据”和“审核者重新执行”。

### 安装、构建与CPU检查

- Node24.21.0/npm11.19.0、固定HEAD、`npm ci --ignore-scripts --no-audit --no-fund`与Vite构建的实际记录齐全；主包751.48kB的提示没有被隐去或误称性能失败/通过。
- `verify-ocean.mjs`直接导入上游常量/默认参数，并执行提取的原JONSWAP函数；其Stockham CPU算术与固定GLSL索引、twiddle符号和末端checkerboard一致，对照是独立朴素二维逆DFT。
- 数值输出确有14项自建PASS，N=4/8误差约3.95e-15/1.72e-14，pack2/Hermitian读数与日志一致。源码、脚本、输出哈希已复核。
- 第03项只是源码字符串检查；CPU小尺寸对照不证明GPU shader、真实256×1024图集隔离、MRT/fp16精度。固定J泡沫的6步/60步样例均饱和到0.8，不能扩写为动态泡沫验证。最终教材和知识笔记均保留这些边界。
- 三次开发断言失败与oracle修正被保留；没有通过放宽容差或改上游源码隐藏失败。
- PDF第1–4步现为实际Git Bash命令，第5步为协调者实际使用的PowerShell启动命令；已纠正混淆Shell的旧说明。README中的首次clone/固定SHA、放置exercise和PowerShell复现路径清晰标为读者复现指引，不伪装成额外实跑历史。

### 真实浏览器证据

协调者的记录覆盖本机真实Vite启动、Lagoon水面、caustics=1→0→1单参数操作、Underwater画面及一次内置benchmark。记录注明Chrome页面、RTX4070显示名称、1660×1053、4×MSAA和desktop profile。

- 焦散置0时沙底网状亮纹消失而波浪/沙纹仍在，恢复后水下焦散可见；这是实际可见效果证据，补足了仅CPU检查无法证明项目出图的问题。
- 时间继续流动，因此不是固定模拟时刻的像素差分，也不证明焦散物理精度。caustics强度变化不是停止焦散GPU计算的性能实验。
- `2.38 ms/frame = 420 fps (GPU 2.34 ms)`仅作为项目内置基准的一次UI报告保留；不等于显示器实际刷新率、持续性能、优化收益或跨硬件结论。没有disjoint/热态/多轮分布证据，教材如实说明。
- 新标签日志无warn/error与早先精度警告分别记录，没有泛化为所有运行均无警告。
- 浏览器画面是协调者在会话工具中实际观察；本审查阅读其记录，没有声称自己重新操作浏览器或从ZIP看到不存在的本地截图。

五步各有操作、目的、实际结果和检测口径，覆盖固定版本、构建、源码参数、数值对照与真实可见变化。满足本项目所选学习实验范围；未覆盖项不被包装为已经验证。

## 4. PDF真实视觉审核

最终PDF真实17页A4，无PDF JavaScript、无加密。先对上一版17页全部用本机Poppler重新渲染并逐页完整查看，再对最终SHA版本全部重新渲染：17张新PNG中仅第14页发生字节变化，其余16页与已目检PNG逐字节相同。最后重新完整查看最终第14页。

证据目录：`ultra-independent-final-pages-v2/page-01.png`至`page-17.png`；比较记录 `ultra-pdf-final-diff.json`。

- 第1页：封面、四层证据、5用途完整，无压出页界。
- 第2–13页：12问的中文、定义、图解、重点框与固定行号来源均可读，SVG无裁切、乱码或重叠。
- 第12页：Q11的计时区别、一次UI观察及disjoint限制完整，没有旧“未执行基准”语句。
- 第14页：已执行Git Bash命令、原输出、用途与验收完整；最新Shell说明正确，长命令未溢出。
- 第15页：CPU命令、误差、失败修正与GPU未覆盖边界完整。
- 第16页：真实参数对照与一次基准记录完整；暂停常规循环/连续推进模拟的语义已修正。
- 第17页：来源双栏、长SHA、全部代码范围与最终状态框完整，没有旧“基准未执行”结论。

视觉结果通过。本次没有把“HTML有SVG”或“PDF可打开”替代逐页目检。

## 5. 练习包与知识候选

### 练习包

ZIP CRC检查通过；7个成员均为安全相对路径，无路径穿越/符号链接。逐个与 `ultra-exercise-final` 原件比对，全部一致：README、数值脚本、数值输出、本地实验日志、浏览器记录、MIT许可和第三方声明。源码脚本SHA仍为 `ba679c5cf42315dbd07ba074e6d5a71051dcd6bd4db6242509b9fbed54755f99`；数值输出SHA为 `625f49e69e32a149d98e169577840235731aedbc02aba05f16e5461b901f2ecc`。

README已把错误的“最后一行SUMMARY”改为“输出中出现SUMMARY且进程退出0”；实际最后一行METRICS不会被误判。包不含上游repo、node_modules、凭据或虚构截图。

### 知识增量

对manifest中的5个候选文件逐字阅读或检查完整差异，并复算bytes、SHA256及Git blob，全部符合最终manifest。基线为知识仓库main `a8674777e18302b8804b137212b1396cbfe5a747`；MOC原blob `efccc5ac22422c02922e80a665530830d3d15112`与已下载基线原字节一致。

| 候选文件 | bytes | SHA256 |
|---|---:|---|
| vault/概念/FFT海面级联.md | 3292 | eddcf343990ffed005f72eeb65897c13dc7ffc238c1cd33afa922013c8584783 |
| vault/概念/异步GPU读回与计时.md | 3289 | fa5ae273d0f4cf3242d5be48f6fe465d4b8b07253efb01f844220ffa5f9dcf1b |
| vault/概念/泡沫压缩与恢复.md | 2564 | 6a83c5c49d89581a03aa0b00495b42775016596a37fd75fac46e327e0f55ff91 |
| vault/项目笔记/ultra_water.md | 5564 | 9f5e24cfb96b36f99cd35f5669de34b9f06e7583350432c6baea78721fe2ef97 |
| vault/00-总览.md | 140696 | 24f5d0b53329b0d69782973b2d4c0e9dd7654781a6982944409a3ef1ee2c0ac7 |

三个新概念聚焦具体海洋机制与异步数据协议；旧Three.js基础、性能测量纪律、证据优先方法通过双链复用。笔记准确区分相位周期/全场景周期、fence完成同步/数值正确性、读回数据/计时query和固定J示例/动态泡沫，没有重复新建通用“GPU Timer Query”或“构建不等于通过”。

MOC的语义差异只有两个新增块：领域概念区与项目索引行；没有删除/重写原内容，LF保留。fence条目已修为“确认完成同步”，不再把同步等同于正确性。候选固定源码行号均有效。

查重证据范围也被准确写出：完整文件树、MOC、三篇相关旧笔记、网站35篇/193块的关键词核对；它不是精读整个vault，也不能证明用户从未学过相关概念。合入前协调者仍须核对最新main与原blob，保护用户手改；本质量签字不替代这一步并发合并检查。

## 6. 审核回执与后续状态

```text
reviewer = codex-independent-coordination-check
qualityReviewApproved = true
contentReviewed = true
experimentEvidenceReviewed = true
pdfRenderedAndReviewed = true
knowledgeCandidateReviewed = true
exerciseArchiveVerified = true
remainingRequiredQualityCorrections = none
```

**未由本审查执行或证明**：共享知识合入、Git提交/推送、网站报告保存/标签更新、用户任务勾选。最终六类上传文件仍应按实际原字节复算合计与SHA；不得以本文签字代替上传结果核验。

质量审核通过不等于GPU数值正确性认证、稳定性能保证或全平台兼容性承诺。上述边界已属于最终教材内容，无需为扩大结论而补跑与本项目目标无关的实验。
