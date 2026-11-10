# 第4项：无口播中文动效验收实验
这是worker直接编写的React/Remotion组件，不是调用原帖宣称的模型/付费API的产物。
Node 24.22.1; npm 11.21.1; Remotion及CLI 4.0.542。

复现：
```sh
npm ci
npx remotion render src/index.tsx CaptionLab ../caption-lab.mp4 --concurrency=2 --browser-executable=/usr/bin/google-chrome
ffprobe -v error -show_streams -show_format -of json ../caption-lab.mp4
```
需Chrome及Noto Sans CJK SC字体；本实验完全无音轨、无外部素材。镜头各90帧，共360帧。
