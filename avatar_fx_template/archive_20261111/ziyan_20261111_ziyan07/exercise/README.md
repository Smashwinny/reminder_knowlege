# 第7项：三层占位模板
只支持几何人物占位与voice=none；没有数字人、音色克隆、Opus或作者原模板。基于第4/6项Remotion组件重用，保留锁文件；Remotion自身许可见REMOTION-LICENSE.md，本次为非商业评估。
在本README所在的exercise目录运行：
```bash
npm ci
python3 validate_template.py
./node_modules/.bin/tsc --noEmit
npm run render
mkdir -p ../research/resume
python3 verify.py
```
Node/Chrome/ffmpeg/ffprobe/Python3须可用；本批复用既有依赖，未重测新机器安装。默认Chrome路径/usr/bin/google-chrome，按实际环境修改。输出../template-final.mp4；不随轻量包附视频。
1个正例及4个预期拒绝覆盖：框重叠、真人mode、去掉标识、克隆声音；不是通用身份授权审核，也不替代像素/听感/观众效果检查。不要用python -O运行断言校验。
