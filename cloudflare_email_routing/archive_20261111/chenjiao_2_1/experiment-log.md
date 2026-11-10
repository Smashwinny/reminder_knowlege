# 真实离线实验日志

执行日期 2026-11-11 01:20:18 北京时间 UTC+8

均为自编教学夹具；第6项调用上游geo.py。合成数据不代表生产服务实测。

## 1. dns
```bash
cd /workspace/chen-jiao-batch2-20261111/item01
python3 exercise/lab.py dns
```
退出码 0
```text
fixture invalid mail proxy: ['mail']
corrected fixture: PASS (not live DNS)

```
## 2. tls
```bash
cd /workspace/chen-jiao-batch2-20261111/item01
python3 exercise/lab.py tls
```
退出码 0
```text
redirect model: flexible+origin HTTPS redirect -> loop; strict -> no modeled loop

```
## 3. web
```bash
cd /workspace/chen-jiao-batch2-20261111/item01
python3 exercise/lab.py web
```
退出码 0
```text
loopback HTTP: 200 cloud-lab-local ; NOT Cloudflare deployment

```
## 4. storage
```bash
cd /workspace/chen-jiao-batch2-20261111/item01
python3 exercise/lab.py storage
```
退出码 0
```text
local object bytes= 16 sha256= 9b11158fd50b595fc943d16d33e2f4ba545e8be99177246948ae209e97d6de26

```

## 逐步目的和验证
- 步骤1 DNS分类夹具：目的 识别mail主机误用网页代理。；验证 输出invalid mail后修正PASS，明确不是线上DNS。
- 步骤2 TLS循环模型：目的 对照回源HTTP与重定向关系。；验证 flexible+redirect为循环，strict分支为否；不替代握手测试。
- 步骤3 回环HTTP真实请求：目的 验证状态码之外的响应体。；验证 本地200且字节等于cloud-lab-local；不算Workers部署。
- 步骤4 本地对象完整性：目的 对写入与读回做哈希对账。；验证 16字节与预期SHA256一致；非R2 API。

## 未验证边界
真实DNS切换、证书签发、Workers部署、邮件收发、R2 API、Workers AI推理及cf命令均未执行；本地HTTP是Python夹具，不是workerd或Wrangler。

## PDF机器检查
Chromium真实打印A4，pdftoppm渲染9页；DOM溢出检查：[]。等待逐页视觉自查；不等于独立审核。


## PDF逐页自查结论
2026-11-11 01:28:26 北京时间 UTC+8：查看pdftoppm生成的page-1..9.png（contact.png汇总），九页均未见裁切/重叠/空白；DOM溢出=[]；pdftotext回读5003字符、替换字符0。为本人自查，非独立审核。
