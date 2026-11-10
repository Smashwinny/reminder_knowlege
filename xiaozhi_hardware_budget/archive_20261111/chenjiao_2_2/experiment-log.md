# 真实离线实验日志

执行日期 2026-11-11 01:20:18 北京时间 UTC+8

均为自编教学夹具；第6项调用上游geo.py。合成数据不代表生产服务实测。

## 1. bom
```bash
cd /workspace/chen-jiao-batch2-20261111/item02
python3 exercise/lab.py bom
```
退出码 0
```text
author-quote arithmetic, 2 breadboards: mandatory= 45.0 73 CNY; optional OLED -> 50.0 80 ; NOT current price

```
## 2. clock
```bash
cd /workspace/chen-jiao-batch2-20261111/item02
python3 exercise/lab.py clock
```
退出码 0
```text
fixture fs=16000 stereo slots=2 slotwidth=32: BCLK= 1024000 Hz; mono PCM16 10s= 320000 bytes

```
## 3. buffer
```bash
cd /workspace/chen-jiao-batch2-20261111/item02
python3 exercise/lab.py buffer
```
退出码 0
```text
RGB565 320x240 single= 153600 double= 307200 bytes; 40-line partial= 25600 bytes

```
## 4. compat
```bash
cd /workspace/chen-jiao-batch2-20261111/item02
python3 exercise/lab.py compat
```
退出码 0
```text
{"memory_spec_ok": true, "flash_authorized": false, "reason": "pin map, voltage and exact board not verified"}

```

## 逐步目的和验证
- 步骤1 作者BOM区间算术：目的 明确数量与可选项口径。；验证 两块面包板；必需45–73元；可选50–80元，均非实时价格。
- 步骤2 I2S与PCM预算：目的 区分传输时隙与保存样本。；验证 BCLK=1024000Hz，10秒PCM=320000字节。
- 步骤3 显示缓冲预算：目的 量化双缓冲与局部刷新差异。；验证 单帧153600、双帧307200、40行25600字节。
- 步骤4 兼容性拒绝门：目的 内存规格匹配也不得跳过板级确认。；验证 memory_spec_ok=true，flash_authorized=false。

## 未验证边界
未接麦克风/功放/喇叭/开发板；无焊接、电气测量、IDF编译、刷机、音频录放或真实Bot接入。作者报价非当前价格。

## PDF机器检查
Chromium真实打印A4，pdftoppm渲染9页；DOM溢出检查：[]。等待逐页视觉自查；不等于独立审核。


## PDF逐页自查结论
2026-11-11 01:28:26 北京时间 UTC+8：查看pdftoppm生成的page-1..9.png（contact.png汇总），九页均未见裁切/重叠/空白；DOM溢出=[]；pdftotext回读4930字符、替换字符0。为本人自查，非独立审核。
