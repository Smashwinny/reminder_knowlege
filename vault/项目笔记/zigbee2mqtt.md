---
tags: [项目笔记]
类别: 开源项目类
完成日期: 2026-10-02
---

# zigbee2mqtt

**是什么**：开源的 Zigbee→MQTT 桥接器（github.com/Koenkk/zigbee2mqtt，Node.js，GPL-3.0，实测 v2.14.2）。把小米/Aqara、宜家、飞利浦 Hue 等 400+ 品牌的 Zigbee 设备统一接入 MQTT，再对接 Home Assistant / ioBroker，用一个 30~150 元的协调器 USB 棒取代所有品牌私有网关，全程本地运行。

**来源链接**：https://x.com/yiyirats/status/2091547511177535775 （拾遗任务 1787578575807）

## 带来了哪些概念

- [[MQTT协议与发布订阅]] —— Z2M 的对外语言，`zigbee2mqtt/设备名` 放状态、`/set` 收指令
- [[Zigbee与网状网络]] —— 协调器/路由器/终端三种角色，Mesh 组网
- [[型号指纹与转换器词典]] —— zigbee-herdsman-converters，4560 定义/467 厂商的社区词典
- [[HomeAssistant自动发现]] —— homeassistant/.../config 发现消息让 HA 零配置建档

## 架构（四零件）

各品牌设备 → 协调器硬件（CC2531/CC2652P/EFR32）→ **zigbee-herdsman**（协议栈）→ **herdsman-converters**（翻译词典）→ **MQTT 发布器** → Home Assistant / ioBroker / 任何 MQTT 客户端；外加 :8080 Web 前端管配对。

## 实验做了什么（全部真实运行，无硬件）

本机 Windows 11 + Node 24 + pnpm 11.26，无 Docker 无 Zigbee 硬件，材料在 `zigbee2mqtt\exercise\`：

1. **源码编译**：clone + `pnpm install`(5m46s) + `pnpm run build` 成功
2. **本地 broker**：aedes 起 MQTT broker 于 1883（坑：aedes 1.2.0 必须 `await Aedes.createBroker()`，否则客户端 connack timeout）
3. **无硬件启动 Z2M**：ZIGBEE2MQTT_DATA 指向实验配置、串口写假 COM99 → 真实输出：herdsman 适配器发现失败（No valid USB adapter found）退出；且退出前**不连 MQTT**——协调器硬件是系统大门
4. **查词典**：`prepareDefinition()` 展开 extend 定义，实测 4560 定义/467 厂商；Aqara WSDCGQ11LM 报温湿压电，IKEA LED1623G12 支持调光/上电行为
5. **模拟自动发现**：40 行脚本复现 Z2M 行为，observer 真实收到 3 条 homeassistant/.../config + 6 条 zigbee2mqtt/ 状态消息

## 坑与结论

- typescript 7.0.2 原生版平台包会被 pnpm 装成空目录且拒绝重装，`npm pack` 手动解包修复
- 官方宣称 5600+ 设备是把白牌变体也算上，本地定义库原始条目 4560（实测数字更诚实）
- Zigbee 信道选 15/20/25 避 Wi-Fi 干扰；升级前备份 database.db；MQTT 要配认证
- 和 ZHA 对比：Z2M 独立进程+MQTT 解耦，离了 HA 也能被 ioBroker/脚本接管

## 产出

- 指南 PDF：`zigbee2mqtt/zigbee2mqtt-小白指南.pdf`（10 页，14 疑问 + 5 实验）
- 实验材料：`zigbee2mqtt/exercise/`（broker/observer/模拟设备/查词典 4 个脚本 + 实验记录.md）
