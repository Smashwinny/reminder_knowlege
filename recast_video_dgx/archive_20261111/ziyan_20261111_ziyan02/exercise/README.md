> 公开归档版说明：下文是原完整实验包的历史README。本轮已移除第三方源码，请先阅读项目根目录[ARCHIVE_DEPENDENCIES.md](../ARCHIVE_DEPENDENCIES.md)。本轮未恢复依赖或重跑，不代表当前目录直接可运行。

# CPU 合成媒体实验
依赖Python3、ffmpeg、ffprobe，无GPU或API。
解压到新目录（已有输出会按上游不可变原则拒绝），从item02工作目录执行：
```bash
for n in 1 2 3 4 5 6; do python3 exercise/lab.py "$n"; done
python3 exercise/build_guide.py
```
原始脚本在evidence/upstream；未修改。lab.py为自写编排器，测试仅选择3个上游测试。视频为自行合成的testsrc2；不分发MV或名人素材。PDF打印与检查需额外浏览器/poppler，不由lab执行。
