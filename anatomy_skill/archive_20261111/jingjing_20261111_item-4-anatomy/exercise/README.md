> 公开归档版说明：下文是原完整实验包的历史README。本轮已移除第三方源码，请先阅读项目根目录[ARCHIVE_DEPENDENCIES.md](../ARCHIVE_DEPENDENCIES.md)。本轮未恢复依赖或重跑，不代表当前目录直接可运行。

# Anatomy 练习：官方拨针量表 + 邮筒索道教学模型

这些文件都在云端隔离目录里。没有调用付费模型，也没有安装官方技能到用户代理目录。

## 官方示例（上游，MIT）

来源：https://github.com/wheresryan22/anatomy  提交 `1482e8469b0a9e0d8cc18ea2740a01423d29ae80`

```bash
cd upstream/examples/dial-indicator
node build.mjs --light
# 然后在仓库根的练习目录：
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 check.py browser
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 check.py verify
python3 check.py hash
```

`check.py` 来自此前工作者，仍然有效。它用无头 Chrome 按 Home / ArrowLeft / End，检查读数 18、14、10，并且禁止外网。

## 教学模型（本次手写，不是官方技能产物）

隐喻取自官网把 TCP 握手画成 mail ropeway；数字与状态按 RFC 793 图 6。

```bash
python3 tcp_model.py
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 lab.py tcp
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 lab.py verify-tcp
python3 lab.py hash
# 或一次跑完官方检查和教学页：
PYTHONPATH=/workspace/reminder-batch-2026-11-11/vendor python3 lab.py all
```

成功标准：四步状态和序号与 RFC 793 图 6 一致，页面无脚本错误、无外网请求。不声称达到 Anatomy 官方 40–80 零件工艺，也不验证配音视频。
