> 公开归档版说明：下文是原完整实验包的历史README。本轮已移除第三方源码，请先阅读项目根目录[ARCHIVE_DEPENDENCIES.md](../ARCHIVE_DEPENDENCIES.md)。本轮未恢复依赖或重跑，不代表当前目录直接可运行。

# 第5项练习：ray-explainer 离线层

这是非商业学习的最小可重放练习，不是完整技能安装。保留上游原版执行脚本；worker新增 prepare_fixture.py、fetch_font.py 与说明。没有 Opus、付费API、密钥、人物/克隆音色、字体集、视频或 node_modules。

上游：imraywang/rayskills，固定 ca254f09a17e2e2c0aba7651c36688c322b1f2b2。上游根许可 CC BY-NC 4.0；huashu 为 MIT，字体 OFL，详见 upstream/LICENSE、assets/huashu/LICENSE、NOTICE.md 与 fonts/LICENSES.md。本文件夹只提供 kit 场景和离线 HF 构建测试所需文本子集，不声称包含8种grammar/完整工作流。

## 环境
Python3、Node（实测24.22.1）、npm（11.21.1）、Chrome、ffmpeg/ffprobe；Python Pillow/numpy用于QA图像。Node运行依赖通过锁文件恢复，网络下载不是模型调用。PDF不由此ZIP生成，请读同包 guide.pdf。

## 完整本地命令（在本README所在目录，选择尚未存在slug）
```bash
export TZ=Asia/Shanghai
(cd exercise/runtime-deps && npm ci)
# 可选；要与本次字幕字体一致则下载这一个固定SHA字体，约1.4MB：
python3 fetch_font.py
python3 upstream/scripts/test_hf_template.py
python3 upstream/scripts/test_hf_anchors.py
bash upstream/scripts/new_project.sh replay "$PWD/exercise"
PROJECT="$PWD/exercise/$(date +%F)-replay"
python3 exercise/prepare_fixture.py "$PROJECT"
python3 upstream/scripts/storyboard.py "$PROJECT"
export CHROME=/usr/bin/google-chrome  # 按已有Chrome实际路径修改
export RAY_EXPLAINER_DEPS="$PWD/exercise/runtime-deps"
node upstream/scripts/render.js "$PROJECT" sheet 12
# 人工查看PROJECT/contact.jpg，再运行视频：
node upstream/scripts/render.js "$PROJECT" video 30
# 预期返回1：全零WAV的LUFS/峰值应失败。不要因为render返回0就当QA通过。
python3 upstream/scripts/qa_video.py "$PROJECT/out.mp4" --scenes "$PROJECT/scenes.json" --out "$PROJECT/qa-explicit"
ffprobe -v error -count_frames -show_streams -show_format -of json "$PROJECT/out.mp4"
```
不要运行未随包提供的 API 自检/身份配置。初始化器拒绝已有timeline，重复执行请换新slug；render的stills会重建该项目stills子目录。若使用其他系统、字体、依赖版本，不保证逐像素一致。

## 预期而非伪造的结果
本次实际：37条ok检查（9+28），12秒1080×1920/30fps/360帧；有音轨但全静音，直接QA退出1；render退出0。手工timeline不是Whisper。完整原始输出在交付包experiment-log.md和evidence/，本练习未把这些结果当作新机器自动通过的保证。
