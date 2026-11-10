# Mesh Avatar Studio：一张图到分层网格底稿 · 实验日志

运行时间：2026-11-11 01:29:55 北京时间 UTC+8

范围：公开来源+合成夹具。自编实验不冒充上游实现；仅 item16 明确调用上游 runtime API。

## 前置安装与夹具失败（真实记录）
`npm install --prefix exercise/runtime --ignore-scripts --no-audit --no-fund mesh-avatar@0.7.2`
输出：added 2 packages in 405ms，exit=0。
首次 validateRig 返回 `[rig.view: margins must leave a positive viewport]`；将夹具 padTop/padSide 由误填 10 改为 .05 后，通过。上游代码未改。

## 步骤 1：核对隔离安装的真实 runtime
目的：核对隔离安装的真实 runtime

```bash
cd /workspace/chen-jiao-batch2-20261111/item16
node exercise/lab.mjs version
```
真实结果 exit=0：
```text
0.7.2

```
验证：版本必须是 0.7.2

## 步骤 2：运行上游 rig 与文件验证
目的：运行上游 rig 与文件验证

```bash
cd /workspace/chen-jiao-batch2-20261111/item16
node exercise/lab.mjs validate
```
真实结果 exit=0：
```text
rig_errors= []
file_errors= []

```
验证：两个错误数组均空；保留初次夹具失败记录

## 步骤 3：运行上游头像归档往返
目的：运行上游头像归档往返

```bash
cd /workspace/chen-jiao-batch2-20261111/item16
node exercise/lab.mjs pack
```
真实结果 exit=0：
```text
roundtrip files= 14 archive bytes= 10500

```
验证：每个文件名及字节逐一相等

## 步骤 4：运行三个坏 manifest
目的：运行三个坏 manifest

```bash
cd /workspace/chen-jiao-batch2-20261111/item16
node exercise/lab.mjs negative
```
真实结果 exit=0：
```text
avatar.json.format: expected "mesh-avatar"
avatar.json.version: unsupported version 999 (expected 1)
avatar.json.name: expected a non-empty string
invalid_manifests_rejected= 3

```
验证：三种错误均被真实 parseManifest 拒绝

## 未验证边界
待验证：Studio 编辑器、WebGL 渲染、眼口自然度、Agent 自动生成、ImageGen、真实声音/摄像头和全链路体验。只完成上游文件与归档 API 实验，不冒称可视化运行。
