# 04-open-robots 练习代码

原创教学脚本，不包含上游机器人源码（只含官方 URDF 文本副本，许可见各上游仓库）。

## 运行

在 `exercise/` 的上一级：

```bash
python3 exercise/lab.py env
python3 exercise/lab.py survey
python3 exercise/lab.py licenses
python3 exercise/lab.py agibot
python3 exercise/lab.py fk
python3 exercise/lab.py verify
```

需要 Python 3.10+ 与 NumPy。`agibot` 会读取本批落盘的 `../sources/hf/` 统计与 completions；若你只解压了 exercise.zip，该子命令会标记 missing，不伪造 8259/2 的计数。

`data/repos-slim.json` 是读取日公开 GitHub API 的精简缓存；SHA 已用 `git ls-remote` 固定。重新联网拉取不是本脚本的默认行为。

## 范围

- 做了：仓库对照、许可字段对照、标注类型计数（若源文件在）、URDF 解析正运动学。
- 没做：真机、付费 API、MuJoCo/PyBullet 带网格仿真、完整数据集下载。
- `verify` 的 9 组检查是同一作者自写断言，不是独立审核。
