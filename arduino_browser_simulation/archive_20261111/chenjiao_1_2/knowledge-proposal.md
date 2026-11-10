---
tags: [候选成果, 增量学习, 未合入]
created: 2026-11-11
---
# 第2项 knowledge proposal：浏览器学 Arduino：从演示到可检验的模型

## 查重与差异
固定main：a8674777e18302b8804b137212b1396cbfe5a747。已读00-总览及相关概念正文。总览未列本批七条原帖的专门项目记录；没有据此断言全仓库绝无重叠。
复用已有 PWM/舵机与确定性脚本概念；新增教学界面的版本漂移与传感器状态机边界案例。

## 建议追加的项目案例（待协调者审核）
来源：https://x.com/i/status/2113649512581415249；一手SHA见sources.md。

### setup 和 loop 分别负责什么？
setup用于初始化，loop反复执行控制逻辑。当前首页片段只把LED写HIGH并delay，没有LOW，因此从这段文本不能断言它会闪烁。真正Blink必须有亮/灭两次写入和相应等待。

### 交通灯的阈值如何写清楚？
练习定义小于20cm红灯、20到不足50cm黄灯、50cm及以上绿灯。边界样本19.9、20、49.9、50分别命中对应分支；每个输入只返回一个状态，避免独立if导致多灯同时亮。

### 怎么知道真正学会而不是只看动画？
先预测每个边界样本的输出，再运行自己的代码核对CSV和断言；然后才去页面接线、运行并解释差异。网页交互、编译能力、真实电气安全和学习效果是四类不同证据，本批只完成数值层。

## 建议互链，不新建同义概念
[[接缝与桩实现StubSeam]]、[[级联语音管线]]、[[证据优先质检ProofOverClaims]]、[[规格书先行SpecDriven]]。按实际概念选择落点，禁止把整个案例机械加到全部笔记。

## 本批状态
待验证：原帖、转述帖、作者官网和应用文本可读；数值实验完成。没有操作原应用接线/运行按钮，没有 AVR 仿真或实体测量。

## 可复核结果
# 第2项真实实验日志
执行时间：2026-11-11T00:58:16.400898+08:00 Asia/Shanghai
环境：Linux云电脑；全部为受控数据。

## 步骤 1
```sh
cd /workspace/reminder-batch-2026-11-11/item02/exercise
python3 lab.py 1
```
退出码：0
```text
{"python": "3.13.5", "scope": "HC-SR04往返时间算术与迟滞交通灯状态机"}

```

## 步骤 2
```sh
cd /workspace/reminder-batch-2026-11-11/item02/exercise
python3 lab.py 2
```
退出码：0
```text
{"echo_us_distance_cm": [[580, 9.947], [1160, 19.894], [2915, 49.992]], "temperature_assumption": "声速343 m/s；没有温度/硬件校准"}

```

## 步骤 3
```sh
cd /workspace/reminder-batch-2026-11-11/item02/exercise
python3 lab.py 3
```
退出码：0
```text
{"colours": ["RED", "RED", "AMBER", "AMBER", "GREEN", "GREEN"], "mutual_exclusion": true, "samples": [10, 19.9, 20, 49.9, 50, 100]}

```

## 步骤 4
```sh
cd /workspace/reminder-batch-2026-11-11/item02/exercise
python3 lab.py 4
```
退出码：0
```text
{"hysteresis_transitions": 0, "noisy_cm": [19, 21, 19, 21, 19, 21], "raw_transitions": 5, "warning": "迟滞仅演示17/23cm边界，不是安全刹车系统"}

```

## 合入边界
仅为隔离候选提案，没有合入共享vault、改变网站标签、勾选Reminder或Git发布。自检不是独立审核；待协调者复核。
