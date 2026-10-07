# 实验日志 · Twilio 试用号（twilio_trial_number）

- 任务：df222942-997b-4ebc-be4a-952cc5535c79
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 实验位置：`exercise/trial_simulator.py`（纯 Python 标准库，131 行）

## 实验设计

不注册真实 Twilio 账户（需真实邮箱/手机号并创建外部账户，超出本机范围）。实验目标：把官方文档（how-to-use-your-free-trial-account）宣称的试用机制写成代码 + 断言逐条验证。

## 依据（真实 WebFetch，2026-10-07）

官方文档提取：免费额度按产品固定（100 SMS/100 WhatsApp/3000 邮件/75 分钟，非共享余额）；试用账户 30 天过期；试用号系统分配不可自选；只能发给已验证号码（约 5 个上限）；必须用 Twilio 模板（自定义正文不可用）；试用 SMS/Voice 限注册国；A2P 10DLC 需付费；额度用尽需升级。

## 运行记录

`python trial_simulator.py`（exit=0，完整输出 `exercise/run_output.txt`）：

- **9/9 断言通过**（另含 1 条额度数字与官方一致性的硬断言 T1）：试用号不可自选；未验证 recipient 拒发；验证后可发+计数；自定义正文拒发；跨国 SMS 拒发；验证 recipient 上限 5；30 天过期拒发；额度用尽拒发；邮件渠道无需试用号。
- 演示场景：三渠道发送 + 额度报告（数字与官方文档一致）。

## 结论

- 教程宣称的额度数字与官方 100% 吻合；教程未写的五条限制（验证 recipient/模板/地理/30 天/不可自选号）全部经文档核实并由实验建模。
- 未验证（诚实声明）：真实注册流程（密码规则/分配号段/收信 UI）、试用号段被各平台风控识别的实际比例、30 天后 Console 具体表现。

## 产物

- `exercise/trial_simulator.py`、`exercise/run_output.txt`
