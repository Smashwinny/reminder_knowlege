# 实验真实日志

运行时间：2026-11-11 01:01:48（Asia/Shanghai）。工作目录：/workspace/learn-batch/04-poster-prompt。Python 3.13.5；标准库；无付费API、用户密钥、模型推理或真实订单。

## 1. 初始化自写库
目的：把输入结构固定，不依赖网上提示词的转售授权。
```bash
python3 exercise/lab.py init
```
真实结果：templates=3；model_calls=0；private_inputs=0。
验证：打开out/library.json检查来源、rights与engine；三个品牌NOVA/TIDE/ORBIT均为虚构演示，不代表商标检索结论。

## 2. 执行结构与负向检查
目的：把缺陷挡在出图前，同时展示校验器到底能查什么。
```bash
python3 exercise/lab.py lint
```
真实结果：3条有效模板通过；unknown-rights、bad-layout、bad-color、long-brand、bad-keywords共5例拒收。
验证：看out/lint.json中的逐项errors；这5例通过仅代表自写政策被触发，不代表授权或生产安全认证。

## 3. 输出提示规格与SVG
目的：用确定性裁切排版生成可编辑样张，不把无模型条件变成停工理由。
```bash
python3 exercise/lab.py render
```
真实结果：3个SVG＋3个prompt文本；每图600×800；model_inference=false。
验证：打开lamp/bottle/disc.svg检查轮廓与文字；prompt.txt写明未被模型执行。输入库只提供A/C，B横斜构图没有实现。

## 4. 验证并重建字节
目的：检查尺寸、裁切、品牌、标语、无外部图像、无脚本、确定性重建。
```bash
python3 exercise/lab.py verify
```
真实结果：3文件×7断言=21项通过；out/verification.json记录各文件SHA256。
验证：XML解析与重新生成字节完全一致；这不是OCR，不保证任意系统字体渲染。PDF中嵌入实际SVG，另做人眼版面检查。

## 5. 计算单位经济情景
目的：把收入叙事拆成可审计公式，暴露人工成本敏感性。
```bash
python3 exercise/lab.py economics
```
真实结果：假设每单2/5/10分钟：贡献2.7/1.2/−1.3元；真实订单0。5×20000只算得毛流水100000。
验证：看out/economics.json。公式=5×(1−0.1)−0.8−分钟÷60×30−0；费率0仅为假设，未核实现行平台收费。

## 原样stdout
```text
2026-11-11T01:01:48+08:00
Python 3.13.5
COMMAND: python3 exercise/lab.py init
{"templates": 3, "model_calls": 0, "private_inputs": 0}
COMMAND: python3 exercise/lab.py lint
{"valid_templates": 3, "negative_rejected": 5, "scope": "structure_only"}
COMMAND: python3 exercise/lab.py render
{"svg_files": 3, "prompt_files": 3, "size": [600, 800], "model_inference": false}
COMMAND: python3 exercise/lab.py verify
{"files": 3, "structural_checks": 21, "deterministic": true}
COMMAND: python3 exercise/lab.py economics
{"hypothetical_margins": [2.7, 1.2, -1.3], "claimed_gross_arithmetic": 100000, "real_orders": 0}
```

所有断言由本worker编写；没有冒称独立审核。PDF打印与逐页检查记录另见pdf-inspection.md。HTTP下载CAC返回403，但WebFetch已成功读取正文；没有绕过访问限制。

## 逐页检查实际发现及修复
初版内联样张clipPath ID相同，导致PDF第8页三种轮廓显示成同一灯形。修复build_guide.py内联阶段的唯一ID前缀，重印11页PDF并重新逐页转图；只有第8页图像变化，Read复核已呈灯/瓶/圆盘。新增HTML ID唯一性自查通过（3个），不计入原21项XML断言；没有伪称独立审核。
