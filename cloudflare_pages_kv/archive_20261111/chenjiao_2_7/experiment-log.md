# 真实离线实验日志

执行日期 2026-11-11 01:20:21 北京时间 UTC+8

均为自编教学夹具；第6项调用上游geo.py。合成数据不代表生产服务实测。

## 1. snapshot
```bash
cd /workspace/chen-jiao-batch2-20261111/item07
python3 exercise/lab.py snapshot
```
退出码 0
```text
benign fixture namespaces: production/preview separated

```
## 2. binding
```bash
cd /workspace/chen-jiao-batch2-20261111/item07
python3 exercise/lab.py binding
```
退出码 0
```text
case-sensitive binding contract PASS; lowercase mismatch rejected (simulation)

```
## 3. deploy
```bash
cd /workspace/chen-jiao-batch2-20261111/item07
python3 exercise/lab.py deploy
```
退出码 0
```text
immutable local snapshot v1 -> redeploy snapshot v2; NOT Cloudflare deployment

```
## 4. assets
```bash
cd /workspace/chen-jiao-batch2-20261111/item07
python3 exercise/lab.py assets
```
退出码 0
```text
generic static zip root: ['index.html']
NO proxy code, tunnel, subscription, registration or deployment

```

## 逐步目的和验证
- 步骤1 良性环境配置：目的 明确生产/预览不是一份配置。；验证 两套命名空间分开保存，没有云资源。
- 步骤2 大小写契约：目的 按代码字段精确匹配绑定名。；验证 CATALOG通过，catalog不匹配。
- 步骤3 不可变快照模型：目的 解释更改配置与重新发布的区别。；验证 旧快照v1保持，生成新快照才v2。
- 步骤4 普通静态ZIP：目的 检查无代理的静态入口包。；验证 根目录仅index.html；无节点/订阅代码。

## 未验证边界
代理相关复现出于本批合规边界明确不做；无节点、隧道、订阅、账号注册、KV远程资源、真实Pages部署或域名接入。通用离线实验完成不改变本条受阻状态。

## PDF机器检查
Chromium真实打印A4，pdftoppm渲染9页；DOM溢出检查：[]。等待逐页视觉自查；不等于独立审核。


## PDF逐页自查结论
2026-11-11 01:28:26 北京时间 UTC+8：查看pdftoppm生成的page-1..9.png（contact.png汇总），九页均未见裁切/重叠/空白；DOM溢出=[]；pdftotext回读4667字符、替换字符0。为本人自查，非独立审核。
