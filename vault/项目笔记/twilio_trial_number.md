---
tags: [项目笔记, 基础设施, 通信, Twilio, 免费额度]
created: 2026-10-07
---

# Twilio 试用号（免费 +1 美国号）

- 来源：@太阳 taiyanghere 推文 https://x.com/taiyanghere/status/2107100030687686680（自写五步教程完整可读）
- 核实依据：Twilio 官方文档 how-to-use-your-free-trial-account（2026-10-07 WebFetch）+ 本地模拟器 9/9 断言

## 是什么

Twilio 试用账户送系统分配的 +1 美国号 + 按产品固定免费额度（100 SMS/100 WhatsApp/3000 邮件/75 分钟通话，非共享余额），不绑卡，能收短信、能发（限已验证号码）。注册：邮箱+手机号验证（+86 可），Console "Send an SMS" 流程分配试用号，"Receive an SMS" 标签页收信。

## 五条隐藏条款（教程没写，文档核实）

① 只能发给已验证 recipient（约 5 个上限，注册号自动验证）；② 必须用官方模板，自定义正文不可用；③ 试用 SMS/Voice 限注册国；④ 30 天账户过期，试用号失效；⑤ 试用号系统分配不可自选。A2P 10DLC 营销短信需付费账户。

## 定位

验证收发机制的免费沙盒 + 学习 Twilio API 的环境 + 程序联调的免费收信端。<b>不是长期通信号码</b>：30 天耗材，别绑定重要账户。与 [[cloudflare_email_routing]] 组合 = 邮件+短信双通道免费接收端。

## 本机实证

trial_simulator.py（131 行纯标准库）按官方文档建模试用机制，9/9 断言通过（额度数字/不可自选号/验证 recipient/模板/地理限制/30 天/用尽拒发/邮件免号）。未实注册（需真实邮箱手机号建外部账户）。

## 关联

- [[项目笔记/cloudflare_email_routing]]（同作者同系列，姊妹篇）
- [[证据优先质检ProofOverClaims]]（"能收短信"的边界辨析）
- 概念提案：免费层额度墙设计（见项目目录 knowledge-proposal.md，协调者终审）
