# HowToLiveBetter 真实只读练习

固定版本：bc149af3a02e721f0e3d03a673a0ec64fca765c4
来源：https://github.com/eternity4719/HowToLiveBetter

## 先运行
解压后，在本README所在的exercise目录打开终端。需要Python 3，只有标准库依赖，不联网，不执行任何上游代码，只写results目录。

python3 run_experiment.py

端到端命令和以下六个显示检查点的命令已在本轮云端真实执行。每次运行都重验全部断言，--show只筛选显示内容。Windows若要改用已有Python启动器，需要在该电脑另行核对，云端未验证该替代命令。

python3 run_experiment.py --show 1
python3 run_experiment.py --show 2
python3 run_experiment.py --show 3
python3 run_experiment.py --show 4
python3 run_experiment.py --show 5
python3 run_experiment.py --show 6

输出results/experiment_result.json。11类校验通过；真实第7条的未知百分比为null。第999条不存在时弃答；内存删来源时弃答；追加字节的内存副本被哈希检测拒绝。原始source文件不会改写。缺少输入、哈希不匹配或任何断言失败时退出码为1。

## 中间结果看哪里
1 显示commit和三文件哈希
2 显示README入口与完整条目行号
3 显示6个DOI到核实记录的定位
4 显示仓库事实、研究断言、作者算账假设、行动推论、适用性待证
5 显示未知弃答和记录差异
6 显示输入不变与11类校验结果

## 已知范围
本实验解析第4节18条，深查3/6/7条。不能证明全书正确、原论文被重新核验或个人适用性。source/保留4个相关原始正文文件以及LICENSE-CODE许可原文，其中项目skill只供阅读，没有执行。核实记录日期为2026-09-07，记录中条号不能一概与新正文直接连接；本实验用DOI连接。

真实缺口：第3条正文出现4.11场，而旧核实记录仍说未确认、未写入。这里只标记更新依据待调和，不判数字错误。第6条异步沟通替代是仓库明标的作者推论；其不存在直接比较研究的表述也只是仓库作者的说法，不是本次全面文献检索的结论。

本脚本没有读取外部论文。补充外源记录见evidence/source_audit.json：只到搜索返回的官方摘要与元数据层，直接开页受限、全文未读。X正文云端403，Windows此前核对不可冒充云端访问。

## 文件
run_experiment.py：自建分析代码
manifest.json：固定源版本、SHA-256、Git blob
source/：未经修改的真实原文
results/experiment_result.json：最后一次作者运行结果
expected_result.json：作者结果的只读对照副本，时间字段随重跑变化
exercise-answers.md：六个练习与验收点
diagram-01.svg 至 diagram-12.svg：每问一图
evidence/：来源访问、五篇旧笔记核对、方法参考及字体许可

## 版权
正文来源：《高性价比人生指南》，作者albert4719 / eternity4719，仓库链接如上。文字许可CC BY 4.0：https://creativecommons.org/licenses/by/4.0/ 。source/文件字节未改；学习指南、问题、图示和实验另行编写，属于改编与说明。项目skill代码/文档许可遵循source/LICENSE-CODE（MIT），版权与许可原文已附。随PDF嵌入的Noto字体子集的许可见evidence/noto-font-license.txt。
