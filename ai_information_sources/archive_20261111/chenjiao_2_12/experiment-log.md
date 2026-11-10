# 七个 AI 信息入口：发现、原文与评测分工 · 实验日志

运行时间：2026-11-11 01:29:55 北京时间 UTC+8

范围：公开来源+合成夹具。自编实验不冒充上游实现；仅 item16 明确调用上游 runtime API。

## 步骤 1：核对七个官网请求记录
目的：核对七个官网请求记录

```bash
cd /workspace/chen-jiao-batch2-20261111/item12
python3 exercise/lab.py prepare
```
真实结果 exit=0：
```text
[('AI-News.html', 200, 102899), ('The-Batch.html', 200, 152643), ('HF-Papers.html', 200, 507098), ('alphaXiv.html', 200, 915635), ('arXiv.html', 200, 99558), ('Arena.html', 200, 115565), ('Artificial-Analysis.html', 200, 1474660)]

```
验证：manifest 必须有七条入口 HTML 记录

## 步骤 2：从真实页面提取论文链接
目的：从真实页面提取论文链接

```bash
cd /workspace/chen-jiao-batch2-20261111/item12
python3 exercise/lab.py extract
```
真实结果 exit=0：
```text
link observations= 99 unique papers= 92

```
验证：生成观察记录与唯一 ID 计数，不伪造论文列表

## 步骤 3：验证跨站规范化
目的：验证跨站规范化

```bash
cd /workspace/chen-jiao-batch2-20261111/item12
python3 exercise/lab.py dedupe
```
真实结果 exit=0：
```text
3 synthetic links => 1 canonical paper; versions must also be recorded separately

```
验证：三条合成 URL 规范为同一 ID

## 步骤 4：检查阅读覆盖和证据边界
目的：检查阅读覆盖和证据边界

```bash
cd /workspace/chen-jiao-batch2-20261111/item12
python3 exercise/lab.py audit
```
真实结果 exit=0：
```text
sources_with_paper_ids= ['HF-Papers.html', 'alphaXiv.html', 'arXiv.html', 'paper-2611.12865.html']
HTTP 200 != paper reviewed; rankings != universal quality; no schedule created

```
验证：输出实际含论文 ID 的来源集合

## 未验证边界
待验证：论文 PDF 全文、代码与方法复现；Arena/AA 完整方法和实测；页面动态数据未全面读取。没有建立监控或登录账号。
