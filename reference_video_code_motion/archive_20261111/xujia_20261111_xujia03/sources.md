# 第3项来源与证据边界

整理时间：2026-11-11T01:22:46.037467+08:00（Asia/Shanghai）。原始读取时间见read-manifest.json、源文件mtime和source-lock.json。

## 原帖、作者线程与引用
- 主帖：https://x.com/leaf_sanren/status/2113479153182019804；发布于2026-10-23 11:54:31（Asia/Shanghai）。完整note_tweet见sources/x-post.txt（费用/onetake段在完整字段，不在截断text里）。
- 作者线程：sources/x-thread.txt、x-thread-end.txt；分页末尾result_count=0，已读完本次作者回复。
- 作者明确指出最早参照：https://x.com/leaf_sanren/status/2113494941389459583，引用https://x.com/ChrisHKAI/status/2112802465607479654（当前用户名ChrisHKAI，作者回复提及旧用户名Chris62771610）。Chris原帖写Made With DeepSeek，不应全归功Opus；见x-earliest-reference.txt。其引用演讲文章与本次动效无直接技术关系，仅保存扩展正文，不展开无关文章。
- 13秒效果原帖：https://x.com/leaf_sanren/status/2113332432275701886，来源x-reference.txt。该帖又引用2112912416380190815水闸柜项目，扩展正文已读，但不是动效工具链源码。
- 作者只说onetake名字，未给owner/repo及自己工程；本次一手候选不能冒充作者实际版本，更不能证明其“只有渲染脚本有用”的普遍结论。

## 视频证据
- 原片固定媒体URL：https://video.twimg.com/amplify_video/2113332199894503424/vid/avc1/640x360/S2gPYV4P2w1QGdhx.mp4
- 本地sources/reference.mp4；SHA256 `38d8c9ae2080ce1b8d630a0be200de6e2749915c0fcf1a2ceac223a285a85a15`；ffprobe见reference-probe.json。未嵌入HTML，也不把原片音轨/品牌素材装入原创实验。
- 明确0/2/4/6/8/10/12秒抽帧见qa/reference-timed.png及video-observations.md；未冒称逐帧完整观看或参考配乐试听。抽帧可见倾斜UI平面/小图标/黑底收尾字卡；不能由成片断言用哪个模型。

## onetake固定一手候选
- https://github.com/feitangyuan/onetake
- 固定SHA：`abb6d17279cdc749e27e99aa534a062d8fd01ced`，提交元数据sources/onetake-commit.json。当前快照可能晚于原帖，不倒推作者当时实现。
- 许可证：PolyForm Noncommercial 1.0.0；Required Notice: Copyright (c) 2026 Patrick. onetake is free for noncommercial use only. **源代码可读不等于OSI开放源码或可任意商用**。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/README.md；读取2026-11-11T01:19:08.046030+08:00（Asia/Shanghai）；本地sources/onetake/README.md。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/LICENSE；读取2026-11-11T01:19:08.274031+08:00（Asia/Shanghai）；本地sources/onetake/LICENSE。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/SKILL.md；读取2026-11-11T01:19:08.456792+08:00（Asia/Shanghai）；本地sources/onetake/SKILL.md。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/scripts/render.py；读取2026-11-11T01:19:08.611003+08:00（Asia/Shanghai）；本地sources/onetake/scripts/render.py。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/scripts/analyze_ref.py；读取2026-11-11T01:19:08.828611+08:00（Asia/Shanghai）；本地sources/onetake/scripts/analyze_ref.py。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/scripts/sfx_palette.py；读取2026-11-11T01:19:09.020439+08:00（Asia/Shanghai）；本地sources/onetake/scripts/sfx_palette.py。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/references/3d.md；读取2026-11-11T01:19:09.194340+08:00（Asia/Shanghai）；本地sources/onetake/references/3d.md。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/references/rhythm.md；读取2026-11-11T01:19:09.413893+08:00（Asia/Shanghai）；本地sources/onetake/references/rhythm.md。
- https://github.com/feitangyuan/onetake/blob/abb6d17279cdc749e27e99aa534a062d8fd01ced/references/reference-deconstruction.md；读取2026-11-11T01:19:09.609577+08:00（Asia/Shanghai）；本地sources/onetake/references/reference-deconstruction.md。

精读定位：render.py行11–22读取__meta/await __seek与线性光积分；43–95 sRGB变换；98 GPU_ARGS为Metal路径；112–149 Playwright打开file://、await __ready、子帧采样与静止跳过；187–243参数、FFmpeg编码与.render.json。references/3d.md说明Blender/GLB/Three.js分工、IIFE打包与平台GPU限制；rhythm.md说明节奏验收不等于连贯或创意；sfx_palette.py说明48kHz事件配器，未执行上游模块。

## 官方补充
- Blender 5.3手册：https://docs.blender.org/manual/en/latest/animation/keyframes/introduction.html；2026-11-11读取。关键帧是“时间点存属性”，F曲线定义插值；“不用手工关键帧”不等于没有时间控制点。未安装/运行Blender。
- Three.js在线manual/en/fundamentals.html请求404；manual/#en/fundamentals仅返回索引，不据此虚构正文。已转读同一官方公开仓库r174固定引用的基础文档，见three-r174-ref.json/three-fundamentals.html；早先错误请求commits/main返回422，默认分支假设不成立，未把它当仓库不存在。

## 查重
- https://github.com/Smashwinny/reminder_knowlege 固定SHA `a8674777e18302b8804b137212b1396cbfe5a747`。
- 已读reference/00-总览.md与本项sources内Three.js与场景图、补间动画与缓动函数、分镜表驱动生成、确定性快进与真渲染取证、词锚定语义时间。具体路径见dedupe-paths.json与dedupe-overview.txt。只读，不修改仓库。
- 已有补间/场景图/分镜/确定性取证不另立重复条目；新增候选聚焦seek合约、快门线性光积分、事件音画共表与跨平台/许可证边界。

## 实验实现归属
- exercise/lab.py、run_all.py为原创教学实现，用Python/NumPy/Pillow计算真实三维顶点、透视投影、CPU面片栅格化，并程序化生成原创音频，再FFmpeg编码。不是Three.js/WebGL、Blender、上游onetake脚本执行，更不是Opus输出。
- 两端纯函数seek/时间线与线性光积分借鉴上述公开方法；没有复制原帖UI、配乐或品牌资产。包内不附上游代码；sources快照保留于box以供只读复核，复现审计可只读下载固定SHA。
- 实际命令、JSON输出、MP4散列在experiment-log.md与exercise/out/*-result.json。源文件身份审计不是独立代码安全审计或工具链端到端性能测试。

Three.js r174固定对象SHA：`3f755be7d5e73698e34da5da9dee730a8d7d40cd`。

## 额外读取结果与纠正
- Three.js r174为附注标签。直接把标签对象SHA当提交取raw文件曾404；解析git/tags后得到真实提交`c6620cee323838ead14035b37008f401edbc2ea1`，已成功读取27561字节官方fundamentals.html。标签对象`3f755be7d5e73698e34da5da9dee730a8d7d40cd`不是该文件的提交SHA。
- Chris最早参照片的640×360媒体URL下载HTTP403，未继续换接口或伪造其画面：`https://video.twimg.com/amplify_video/2112801028030726145/vid/avc1/640x360/tCzMIrYwOHcKHDQu.mp4`。其原帖文字与引用已读，视频待验证。
