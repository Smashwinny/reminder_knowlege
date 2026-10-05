# HowToLiveBetter：证据组织与可追溯检索

11 页彩色[指南](HowToLiveBetter-小白指南.pdf)、[HTML 源文件](guide.html)、[实际实验日志](experiment_log.txt)和[练习](exercise/README.md)。上游固定在 bc149af3a02e721f0e3d03a673a0ec64fca765c4，研究其证据组织，不验证全部人生建议。

在本项目的 exercise 目录运行：

```powershell
python -X utf8 run_experiment.py
python -X utf8 run_experiment.py --show 1
python -X utf8 run_experiment.py --show 2
python -X utf8 run_experiment.py --show 3
python -X utf8 run_experiment.py --show 4
python -X utf8 run_experiment.py --show 5
python -X utf8 run_experiment.py --show 6
```

以上 Windows 参数形式于 2026-10-05 用 Python 3.12.14 实际复跑七次：每次 11 类校验通过；稳定结果与云端原件逐字段一致，只排除运行时间。额外三种坏输入均拒绝，不改写原始源文件。详细范围与许可见 exercise/README.md；Windows 结果与云端结果分开记录。

PDF 采用 ReportLab 直接生成，云端及 Windows 均逐页检查全部 11 页。云端 HTML 浏览器视觉检查及 HTML→PDF 受阻；HTML 是静态源文件，其视觉表现未据此宣称通过。

知识入库见 [项目笔记](../vault/项目笔记/how_to_live_better.md)；实验与审核范围见 [独立核验](independent-review.md)。原网站记录、账户标识及私密报告不在本目录。
