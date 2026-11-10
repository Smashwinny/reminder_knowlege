# 真实离线实验日志

执行日期 2026-11-11 01:20:20 北京时间 UTC+8

均为自编教学夹具；第6项调用上游geo.py。合成数据不代表生产服务实测。

## 1. shape
```bash
cd /workspace/chen-jiao-batch2-20261111/item04
python3 exercise/lab.py shape
```
退出码 0
```text
{"model": "fixture-not-a-real-model", "messages": [{"role": "user", "content": "hello"}], "max_tokens": 8}
request shape only; no inference

```
## 2. http
```bash
cd /workspace/chen-jiao-batch2-20261111/item04
python3 exercise/lab.py http
```
退出码 0
```text
loopback actual HTTP 200 {'object': 'chat.completion', 'model': 'MOCK', 'choices': [{'message': {'role': 'assistant', 'content': 'MOCK ONLY'}}]}

```
## 3. limit
```bash
cd /workspace/chen-jiao-batch2-20261111/item04
python3 exercise/lab.py limit
```
退出码 0
```text
actual HTTP rejection: 400 {"error": "fixture token cap"}

```
## 4. memory
```bash
cd /workspace/chen-jiao-batch2-20261111/item04
python3 exercise/lab.py memory
```
退出码 0
```text
hypothetical 8B INT4 raw weights= 4000000000 bytes; sample GQA KV= 536870912 bytes; overhead excluded; no model loaded

```


## 逐步目的和验证
- 步骤1 构造兼容请求形状：目的 先排最小JSON字段错误。；验证 明确fixture-not-a-real-model，不调用推理。
- 步骤2 回环兼容API模拟：目的 测试真实HTTP传输与JSON回读。；验证 200，model=MOCK，内容MOCK ONLY。
- 步骤3 拒绝超预算请求：目的 验证自编服务的边界分支。；验证 max_tokens=17，夹具上限16，HTTP400。
- 步骤4 显存理论预算：目的 分开权重与KV缓存。；验证 裸INT4约40亿字节，KV示例536870912字节；未加载模型。

## 未验证边界
无V100、未下载模型权重、未执行推理或Pi Agent安装。云relay、真实认证、多供应商兼容与性能未验证；不复现逆向和绕过额度。

## PDF机器检查
Chromium真实打印A4，pdftoppm渲染9页；DOM溢出检查：[]。等待逐页视觉自查；不等于独立审核。

## PDF逐页自查结论
2026-11-11 01:28:26 北京时间 UTC+8：查看pdftoppm生成的page-1..9.png（contact.png汇总），九页均未见裁切/重叠/空白；DOM溢出=[]；pdftotext回读4968字符、替换字符0。为本人自查，非独立审核。
