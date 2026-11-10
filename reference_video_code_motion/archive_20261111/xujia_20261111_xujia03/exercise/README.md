# 原创可复现练习：KINETIC CPU 3D STUDY

本实验不是原作者工程，不调用Opus/NotionAI，不运行Blender、Three.js/WebGL或上游onetake渲染器。它用同构方法实际生成三维面片动画与程序音频，帮助理解时间函数/随机寻址/快门积分/事件共表。无账号、无外部资产、无付费服务。

## 环境
Python3、NumPy、Pillow、FFmpeg/ffprobe，系统DejaVuSans字体。依赖如未安装可自行在隔离环境运行`python3 -m pip install numpy pillow`；本次环境已有，未安装新工具。

## 一键重做
```bash
cd exercise
python3 run_all.py
```
输出out/study.mp4（640×360，24fps，13秒）、out/score.wav、312帧PNG和结果JSON。渲染约十几秒只是本次小场景机器耗时，不是视频实时FPS或第三方性能承诺。完整逐条命令和真实输出见上级experiment-log.md。

## 五步
1. `python3 lab.py source_audit`：固定onetake渲染源中6项接口/参数核验，不执行上游。交付包不附上游代码，如无上级sources快照，会只读下载固定SHA检查（需联网）。
2. `python3 lab.py timeline`：顺序/逆序寻址、边界差、sRGB/线性光黑白均值验证；写beat-sheet.json。
3. `python3 lab.py audio`：共享BEATS生成48kHz单声道原创建模音效与简易谐波底床，验证624000样本、事件量化和削波。不是AI音乐服务或原片音乐。
4. `python3 lab.py render`：8顶点厚片图标、透视投影、面片绘制、每帧4个180°快门子采样线性光合成。没有纹理/PBR/骨骼/景深/硬切检测，不冒称Three.js成片复刻。
5. `python3 lab.py encode`：FFmpeg编码H264/AAC，ffprobe计帧312、两路13秒、完整解码，抽帧联系表与6个不同帧散列。

## 来源
见../sources.md和source-manifest.json。lab.py完全原创，参考的是公开接口与标准数学，未复制上游渲染代码。onetake为PolyForm非商业许可；上游只读审计不是商用授权或安全审计。

## 不能据此声称
模型视频理解成功、Blender/Three.js或onetake运行成功、原片同款、真人观感通过、跨设备声画延迟为0或4K60性能达标。字体路径若不同，请将frame()里的DejaVuSans路径改为本机可用字体。
