# 订单利润日报工具 · 交付包

全自动模板产物（xianyu_automation_workflow 实验）。

## 交付物清单

- `order_profit_daily.py` —— 主程序（Python 3.10+，零第三方依赖）
- `ARCHITECTURE.md` —— 架构/异常处理/定时配置说明
- `示例数据/` —— 5 笔示例订单（含 1 笔负毛利异常单）
- `日报.html` —— 示例输出（真实运行生成）

## 快速开始

```bash
python order_profit_daily.py 示例数据 --out 日报.html
```

## 二次开发（模板复用点）

- 改数据源：换 `load_orders` 的 glob（支持 xlsx 需装 pandas/pyxlsb）
- 改推送：在 `render()` 后加微信/邮件 webhook（对应工作流"改推送方式十分钟出货"）
- 改扣点：`PLATFORM_FEES` 字典
- 改异常阈值：`ABNORMAL_LOW_PROFIT_RATE`
