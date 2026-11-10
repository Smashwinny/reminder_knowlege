---
tags: [候选成果, 增量学习, 未合入]
created: 2026-11-11
---
# 第3项 knowledge proposal：四个ESP32语音项目怎样分层

## 查重与差异
固定main：a8674777e18302b8804b137212b1396cbfe5a747。已读00-总览及相关概念正文。总览未列本批七条原帖的专门项目记录；没有据此断言全仓库绝无重叠。
沿用已有Muse硬件/云端分工、级联语音与接缝概念，补充小智生态四层角色及按设备路由隔离；不重复写基础MCP介绍。

## 建议追加的项目案例（待协调者审核）
来源：https://x.com/i/status/2113083667417608344；一手SHA见sources.md。

### OTA地址就是模型API地址吗？
不是。配网中的OTA入口向设备提供配置或更新信息；后端再给出连接语音服务所需信息。模型API和Bot Webhook属于后端到服务的另一段，填错层会导致设备无法取得配置。

### 只喊名字也应派任务吗？
引用长文说只呼名可先回应我在，等待下一句。应将选路与实际提交分开，否则一句唤醒就会产生空任务。教学路由器没有完整实现此状态机，真实产品行为还需针对固定版本单测和设备验收。

### 星数和板价能当可靠性证据吗？
不能。原帖星数和128元是作者当时的记录，既非当前报价，也非测试成功率。真正选择依据应是当前板型清单、许可、版本约束、数据路径和可复现实验；本批没有任何购物或硬件采购。

## 建议互链，不新建同义概念
[[接缝与桩实现StubSeam]]、[[级联语音管线]]、[[证据优先质检ProofOverClaims]]、[[规格书先行SpecDriven]]。按实际概念选择落点，禁止把整个案例机械加到全部笔记。

## 本批状态
待验证：原帖、引用长文与四仓库README已读；合成设备路由和状态保存完成。未运行语音服务、CLI、模型、硬件；内部接口接入未尝试。

## 可复核结果
# 第3项真实实验日志
执行时间：2026-11-11T00:58:16.493075+08:00 Asia/Shanghai
环境：Linux云电脑；全部为受控数据。

## 步骤 1
```sh
cd /workspace/reminder-batch-2026-11-11/item03/exercise
python3 lab.py 1
```
退出码：0
```text
{"layers": ["设备固件", "ASR/TTS网关", "Agent或模型"], "python": "3.13.5", "scope": "合成输入路由，不是上游网关集成"}

```

## 步骤 2
```sh
cd /workspace/reminder-batch-2026-11-11/item03/exercise
python3 lab.py 2
```
退出码：0
```text
{"device_isolation": true, "routes": [["A", "claude"], ["B", "deepseek"], ["A", "claude"], ["B", "deepseek"]]}

```

## 步骤 3
```sh
cd /workspace/reminder-batch-2026-11-11/item03/exercise
python3 lab.py 3
```
退出码：0
```text
{"persistence": "仅本地JSON正常写读；非崩溃一致性证明", "reloaded": {"A": "claude", "B": "deepseek"}, "unknown_alias_policy": "保留既有路由或默认，不执行未知命令"}

```

## 步骤 4
```sh
cd /workspace/reminder-batch-2026-11-11/item03/exercise
python3 lab.py 4
```
退出码：0
```text
{"played": false, "retry_submissions": 0, "states": ["accepted", "waiting", "timed_out", "reply_ready"], "warning": "超时不是取消，也不是可以重新派单的证据"}

```

## 合入边界
仅为隔离候选提案，没有合入共享vault、改变网站标签、勾选Reminder或Git发布。自检不是独立审核；待协调者复核。
