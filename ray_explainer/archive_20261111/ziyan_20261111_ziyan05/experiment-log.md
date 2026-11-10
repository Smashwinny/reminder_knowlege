# 第5项真实实验日志：ray-explainer离线执行与失败门禁

日期：2026-11-11（Asia/Shanghai，UTC+8）。单一路worker续做已有候选材料，不重做第2/3/4项，不写共享vault、不发布、不勾任务。可复用部分包括原版公开源码快照、固定依赖、原三幕fixture与旧样式；本轮另建resume-local隔离项目重跑，不把旧未验证草稿直接算完成。

## 状态与边界
- 真实完成：公开原帖/引用精确ID复读；固定源码与查重；37条上游ok检查；12秒原版Canvas/Chrome/FFmpeg渲染；ffprobe核验；QA失败证据；两次独立进程同帧哈希；HTML、12页A4 PDF逐页PNG+Read、练习ZIP与交付包。
- 负例正确暴露：渲染退出0，但两次直接QA退出1；静音夹具-70 LUFS、峰值None不满足旁白门槛。音轨存在不等于音频内容合格。0.6–4.0秒缺乏明显变化为质量警告，不宣称成熟可发布视频。
- 待验证/未尝试：Claude/Opus、付费API、真实TTS/Whisper、人物/克隆音色、完整1.5–3分钟影片、增长与观众效果。没用用户密钥、没执行check_setup.sh、没改变安全设置。
- 未触发平台限额/速率错误；不生成虚构blocked消息。旧source-post.json实际为另帖，发现后隔离history并以精确ID公共读取更正，原错误文件未入包。

## 6步主实验：目的、完整操作与实测

### 1. 来源/环境/去重
目的：证明研究对象和已有知识基线。X公共工具实际调用：
```json
{"ids":"2110558713996275853,2110343390911160489","post.fields":"created_at,public_metrics,author_id,lang,conversation_id,note_tweet,entities,referenced_tweets","expansions":"author_id,referenced_tweets.id","user.fields":"description,public_metrics,verified"}
```
操作：读取返回的两个ID、全文、referenced_tweets和entities.expanded_url，正确原文保存source-post.json；作者增长自述/截图不作为独立数据。源码固定ca254f09a17e2e2c0aba7651c36688c322b1f2b2；vault基线a8674777e18302b8804b137212b1396cbfe5a747，复读四篇相关笔记，仅提案增量，来源范围见sources.md。
```bash
cd /workspace/reminder-batch/item05
node --version
npm --version
```
验证：64个本地上游文件按SHA1("blob "+字节数+NUL+原始字节)与保存的固定Git tree比较一致；没有把全部已存文件都称为已全文审读。

### 2. 原版scaffold+明确静音输入
目的：建立不读作者身份/API配置的最小项目。依赖沿用本批既有puppeteer-core 25.17.0，锁文件完整保留；本轮未重新联网安装。
```bash
cd /workspace/reminder-batch/item05
bash upstream/scripts/new_project.sh resume-local /workspace/reminder-batch/item05/exercise
python3 exercise/prepare_fixture.py /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local
```
真实结果：均退出0；初始化器写入3幕×4秒、手工timeline及48kHz单声道16bit全零WAV（12秒）。chars=[]，不是逐字对齐。初始化器拒绝已有timeline，重跑请换新slug。

### 3. 真实上游离线测试与分镜
目的：检验小数字幕、锚点重算等，不冒充真人/语音模型。
```bash
cd /workspace/reminder-batch/item05
python3 upstream/scripts/test_hf_template.py
python3 upstream/scripts/test_hf_anchors.py
python3 upstream/scripts/storyboard.py exercise/2026-11-11-resume-local
```
真实结果：两套脚本9+28=37条ok检查、均退出0（不是37个pytest测试）；分镜估时器输出约11秒（文本42字，标注基准5.8字/秒），不能取代fixture12秒实测。测试用合成timeline和空占位素材。

### 4. 先sheet再真实原版视频
目的：检查可读布局再用真正上游执行层编码，不用Remotion仿制。
```bash
cd /workspace/reminder-batch/item05
export CHROME=/usr/bin/google-chrome
export RAY_EXPLAINER_DEPS="$PWD/exercise/runtime-deps"
node upstream/scripts/render.js exercise/2026-11-11-resume-local sheet 12
# Read单独看contact.jpg；执行真正360帧渲染
node upstream/scripts/render.js exercise/2026-11-11-resume-local video 30
```
真实结果：1080×1920、30fps、360帧、12.000秒H.264/AAC，1,370,899字节。render退出0但内置音频QA打印失败；不能将退出0等同合格视频。sheet中三幕层级可读，切幕后有短暂留白，未发觉字幕越界。

### 5. 将QA失败传播与真实画面切点分开
目的：验证render吞QA失败的行为，并检查真正4.0/8.0秒边界。
```bash
cd /workspace/reminder-batch/item05
python3 upstream/scripts/qa_video.py exercise/2026-11-11-resume-local/out.mp4 --timeline exercise/2026-11-11-resume-local/timeline.json --out research/resume/qa-timeline
python3 upstream/scripts/qa_video.py exercise/2026-11-11-resume-local/out.mp4 --scenes exercise/2026-11-11-resume-local/scenes.json --out research/resume/qa-actual
ffprobe -v error -count_frames -show_streams -show_format -of json exercise/2026-11-11-resume-local/out.mp4
```
实测：两次QA均退出1，音轨与同长通过；LUFS=-70、true peak=None失败；无黑场/无中段空画面/蓝紫底0%通过。变化不足提示0.6–4.0秒。review.py使用首句start=4.35/8.35推断切点，实际画面在4/8；另提供scenes.json重查。已Read查看实际QA contact/opening、proof_4.00与gate_8.00切点条：看到淡出淡入，并非独立审核或全帧审片。当前成片另抽2.5/6.5/10.5秒三帧，每张Read检查汉字、字幕、卡片无溢出；对应research/final/video-scene-*.jpg。

### 6. 确定性、真实打印、可重放练习与轻量包
目的：交付可检查而非仅计划的成果。
```bash
cd /workspace/reminder-batch/item05
export CHROME=/usr/bin/google-chrome
export RAY_EXPLAINER_DEPS="$PWD/exercise/runtime-deps"
node upstream/scripts/render.js exercise/2026-11-11-resume-local stills 2.5
cp exercise/2026-11-11-resume-local/stills/t002.5.jpg research/resume/repeat-A.jpg
node upstream/scripts/render.js exercise/2026-11-11-resume-local stills 2.5
cp exercise/2026-11-11-resume-local/stills/t002.5.jpg research/resume/repeat-B.jpg
sha256sum research/resume/repeat-{A,B}.jpg
python3 research/build-guide.py
../item04/research/pdf-venv/bin/python -m weasyprint guide.html guide.pdf
pdfinfo guide.pdf
pdffonts guide.pdf
mkdir -p pdf-pages
pdftoppm -scale-to 1300 -png guide.pdf pdf-pages/page
```
真实结果：两次独立浏览器进程同一t=2.5的JPEG SHA256均为deb8de45772ac6d3713d45a4001ac85730451418640d3f59817389c229b50412；只保证本环境相同输入，不推广到不同字体/OS。WeasyPrint70.0实际打印12页A4，PDF 922,309字节；所有嵌入字体为子集，不含字体集；HTML约87KB、只有3张300px JPEG。12张1300px逐页PNG均逐张Read，自检结果附后。

exercise.zip用Python zipfile/DEFLATE9生成并testzip，再解包跑两套上游测试（37检查）、scaffold、prepare_fixture及stills2.5，均退出0；另Read包内重放静帧确认。这个包验证沿用本批已安装Node依赖和现有单个字体，未声称新机器的npm ci/下载过程已联网验证。ZIP不含node_modules/视频/WAV/字体集；公开固定字体下载助手带SHA256校验，仅供需要时手动执行。root许可CC BY-NC4.0、huashu MIT及字体OFL清单齐全。

## 原始执行记录（真实stdout与退出码）

### research/resume/versions.txt
```text
2026-11-11T01:26:23.447856 Asia/Shanghai UTC+8
$ node --version
v24.22.1

exit_code=0
```

### research/resume/npm.txt
```text
2026-11-11T01:26:23.526305 Asia/Shanghai UTC+8
$ npm --version
11.21.1

exit_code=0
```

### research/resume/scaffold.txt
```text
2026-11-11T01:26:23.534471 Asia/Shanghai UTC+8
$ bash upstream/scripts/new_project.sh resume-local /workspace/reminder-batch/item05/exercise
/workspace/reminder-batch/item05/exercise/2026-11-11-resume-local

exit_code=0
```

### research/resume/fixture.txt
```text
2026-11-11T01:26:23.556170 Asia/Shanghai UTC+8
$ python3 exercise/prepare_fixture.py /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local
fixture prepared: /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local duration=12s PCM silence, NOT narration

exit_code=0
```

### research/resume/hf-template.txt
```text
2026-11-11T01:26:23.659606 Asia/Shanghai UTC+8
$ python3 upstream/scripts/test_hf_template.py
ok    make_beats.py runs
ok    decimal stays in one caption ['最后只有 2.5%', '的人留了下来', '剩下的人都去找', '下一个热门产品了']
ok    no split-number warning
ok    host_build.py runs
ok    adjacent big segments return to the corner once, not twice
ok    build.py runs
ok    ray-ip-dark → light top bar on dark ground
ok    caption styles scoped to #root > .cap
ok    top-bar backing is a see-through gradient
hf-template: OK

exit_code=0
```

### research/resume/hf-anchors.txt
```text
2026-11-11T01:26:24.099428 Asia/Shanghai UTC+8
$ python3 upstream/scripts/test_hf_anchors.py
ok    make_beats.py runs
ok    build.py runs
ok    first build: x-v2 data-start = 1.800 (got ('phrase:0:飞起来+0.2', 1.8))
ok    first build: x-v3 data-start = 2.600 (got ('clip:c1', 2.6))
ok    first build: x-v4 data-start = 4.600 (got ('clip:c1:end', 4.6))
ok    first build: x-v5 data-start = 4.900 (got ('line:1', 4.9))
ok    first build: x-v6 data-start = 2.500 (got ('cap:1-0.1', 2.5))
ok    first build: plain data-start="0" left alone
ok    no {{…}} left in the scene file after build
ok    hard-coded video data-start is flagged
ok    playback-rate below 0.35 is flagged
ok    make_beats.py runs
ok    build.py runs
ok    after re-voice (+1.3 s): x-v2 data-start = 3.100 (got ('phrase:0:飞起来+0.2', 3.1))
ok    after re-voice (+1.3 s): x-v3 data-start = 3.900 (got ('clip:c1', 3.9))
ok    after re-voice (+1.3 s): x-v4 data-start = 5.900 (got ('clip:c1:end', 5.9))
ok    after re-voice (+1.3 s): x-v5 data-start = 6.200 (got ('line:1', 6.2))
ok    after re-voice (+1.3 s): x-v6 data-start = 3.800 (got ('cap:1-0.1', 3.8))
ok    after re-voice (+1.3 s): plain data-start="0" left alone
ok    make_beats.py runs
ok    build.py runs
ok    narration.m4a is encoded from narration.wav
ok    make_beats.py runs
ok    build.py runs
ok    narration.m4a up to date → not re-encoded
ok    make_beats.py runs
ok    build.py runs
ok    newer narration.wav → m4a re-encoded
hf-anchors: OK

exit_code=0
```

### research/resume/storyboard.txt
```text
2026-11-11T01:26:24.120472 Asia/Shanghai UTC+8
$ python3 upstream/scripts/storyboard.py exercise/2026-11-11-resume-local
# 分镜表：ray-explainer离线渲染与失败门禁

**核心判断**：成片文件存在不代表QA通过

| # | 幕 | 讲什么 | 画法 | 画面 | 真实素材（▶ 动态 · ⛶全屏 / ▭整幅 / ▢窗口） | 卡点 | 时长 |
|---|---|---|---|---|---|---|---|
| 1 | hook | 有成片，还不够 | 手绘·定制 | 三张手绘卡片依次出现，箭头连接，底部标明这是静音测试夹具 | （无真实素材） | 固定时间：场景开始后0.5、1.2、1.9秒；不是语音识别时间 | 3s |
| 2 | proof | 时间轴要有证据 | 手绘·定制 | 三张手绘卡片依次出现，箭头连接，底部标明这是静音测试夹具 | （无真实素材） | 固定时间：场景开始后0.5、1.2、1.9秒；不是语音识别时间 | 3s |
| 3 | gate | 失败要向上传递 | 手绘·定制 | 三张手绘卡片依次出现，箭头连接，底部标明这是静音测试夹具 | （无真实素材） | 固定时间：场景开始后0.5、1.2、1.9秒；不是语音识别时间 | 2s |

**预计时长**：约 0 分 11 秒（42 字，按 5.8 字/秒估）
**画法分布**：手绘·定制 ×3
**音色**：none-offline-fixture
**画幅**：竖屏 1080×1920

**主题外壳**
- 边界：12秒视觉管线样本，不是原版1.5–3分钟完整成片

**真实素材**：0/3 幕有真实素材，其中 0 幕是动态的（录屏 / 视频 / 实跑）

**⚠ 动态真实素材太少**：不到一半的幕有录屏、视频或实跑画面。先按 hyperframes.md「取材」补，缺的列出来问 Ray 要。

**待确认**
- 无TTS、无Whisper；时间轴为worker手工测试夹具
- 未验证Claude导演及涨粉效果
- 不使用Ray头像或复刻声音

## 逐字稿

**1. hook**

> 先区分渲染成功和质量通过。

**2. proof**

> 没有配音，就不能冒称逐字对齐。

**3. gate**

> 静音样本的响度检查应当失败。


exit_code=0
```

### research/resume/sheet.txt
```text
ready { duration: 12, scenes: 'hook:kit proof:kit gate:kit' }
times 0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5
/workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/contact.jpg
exit_code=0
```

### research/resume/video.txt
```text
2026-11-11T01:26:54.905639 Asia/Shanghai UTC+8
$ node upstream/scripts/render.js /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local video 30
ready { duration: 12, scenes: 'hook:kit proof:kit gate:kit' }
frame 0/360  0s
wrote /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/out.mp4
# 成片检查：out.mp4

- [x] 有音轨：有
- [x] 音画长度一致（2 帧内）：画面 12.000s，声音 12.000s
- [ ] 响度在 -21 ±1.5 LUFS：-70.0 LUFS
- [ ] 峰值 ≤ −1 dBFS：None dBFS
- [x] 没有黑场：无
- [x] 中段没有空画面（≥0.3 秒几乎没有边缘）：无
- [x] 蓝紫底 < 30%：0%
- 尺寸：1080×1920
- 帧率：30 fps
- 3 秒以上没有明显变化的段落（匀速慢推几个百分点也算没变化；按长短排）：0.6–4.0s（3.4s）

再用 Read 看 contact.jpg、opening.jpg 和 cuts/ 下 2 张切点图（每张是切点前后各 5 帧）。

文件在 /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/qa/out

exit_code=0
```

### research/resume/qa-timeline.txt
```text
$ python3 upstream/scripts/qa_video.py /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/out.mp4 --timeline /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/timeline.json --out /workspace/reminder-batch/item05/research/resume/qa-timeline
# 成片检查：out.mp4

- [x] 有音轨：有
- [x] 音画长度一致（2 帧内）：画面 12.000s，声音 12.000s
- [ ] 响度在 -21 ±1.5 LUFS：-70.0 LUFS
- [ ] 峰值 ≤ −1 dBFS：None dBFS
- [x] 没有黑场：无
- [x] 中段没有空画面（≥0.3 秒几乎没有边缘）：无
- [x] 蓝紫底 < 30%：0%
- 尺寸：1080×1920
- 帧率：30 fps
- 3 秒以上没有明显变化的段落（匀速慢推几个百分点也算没变化；按长短排）：0.6–4.0s（3.4s）

再用 Read 看 contact.jpg、opening.jpg 和 cuts/ 下 2 张切点图（每张是切点前后各 5 帧）。

文件在 /workspace/reminder-batch/item05/research/resume/qa-timeline

exit_code=1
```

### research/resume/qa-actual.txt
```text
$ python3 upstream/scripts/qa_video.py /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/out.mp4 --scenes /workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/scenes.json --out /workspace/reminder-batch/item05/research/resume/qa-actual
# 成片检查：out.mp4

- [x] 有音轨：有
- [x] 音画长度一致（2 帧内）：画面 12.000s，声音 12.000s
- [ ] 响度在 -21 ±1.5 LUFS：-70.0 LUFS
- [ ] 峰值 ≤ −1 dBFS：None dBFS
- [x] 没有黑场：无
- [x] 中段没有空画面（≥0.3 秒几乎没有边缘）：无
- [x] 蓝紫底 < 30%：0%
- 尺寸：1080×1920
- 帧率：30 fps
- 3 秒以上没有明显变化的段落（匀速慢推几个百分点也算没变化；按长短排）：0.6–4.0s（3.4s）

再用 Read 看 contact.jpg、opening.jpg 和 cuts/ 下 2 张切点图（每张是切点前后各 5 帧）。

文件在 /workspace/reminder-batch/item05/research/resume/qa-actual

exit_code=1
```

### research/resume/repeat-A.txt
```text
ready { duration: 12, scenes: 'hook:kit proof:kit gate:kit' }
/workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/stills

exit_code=0
```

### research/resume/repeat-B.txt
```text
ready { duration: 12, scenes: 'hook:kit proof:kit gate:kit' }
/workspace/reminder-batch/item05/exercise/2026-11-11-resume-local/stills

exit_code=0
```

### research/resume/repeat-hashes.txt
```text
deb8de45772ac6d3713d45a4001ac85730451418640d3f59817389c229b50412
deb8de45772ac6d3713d45a4001ac85730451418640d3f59817389c229b50412
```

### research/final/package-smoke-0.txt
```text
$ python3 upstream/scripts/test_hf_template.py
ok    make_beats.py runs
ok    decimal stays in one caption ['最后只有 2.5%', '的人留了下来', '剩下的人都去找', '下一个热门产品了']
ok    no split-number warning
ok    host_build.py runs
ok    adjacent big segments return to the corner once, not twice
ok    build.py runs
ok    ray-ip-dark → light top bar on dark ground
ok    caption styles scoped to #root > .cap
ok    top-bar backing is a see-through gradient
hf-template: OK

exit_code=0
```

### research/final/package-smoke-1.txt
```text
$ python3 upstream/scripts/test_hf_anchors.py
ok    make_beats.py runs
ok    build.py runs
ok    first build: x-v2 data-start = 1.800 (got ('phrase:0:飞起来+0.2', 1.8))
ok    first build: x-v3 data-start = 2.600 (got ('clip:c1', 2.6))
ok    first build: x-v4 data-start = 4.600 (got ('clip:c1:end', 4.6))
ok    first build: x-v5 data-start = 4.900 (got ('line:1', 4.9))
ok    first build: x-v6 data-start = 2.500 (got ('cap:1-0.1', 2.5))
ok    first build: plain data-start="0" left alone
ok    no {{…}} left in the scene file after build
ok    hard-coded video data-start is flagged
ok    playback-rate below 0.35 is flagged
ok    make_beats.py runs
ok    build.py runs
ok    after re-voice (+1.3 s): x-v2 data-start = 3.100 (got ('phrase:0:飞起来+0.2', 3.1))
ok    after re-voice (+1.3 s): x-v3 data-start = 3.900 (got ('clip:c1', 3.9))
ok    after re-voice (+1.3 s): x-v4 data-start = 5.900 (got ('clip:c1:end', 5.9))
ok    after re-voice (+1.3 s): x-v5 data-start = 6.200 (got ('line:1', 6.2))
ok    after re-voice (+1.3 s): x-v6 data-start = 3.800 (got ('cap:1-0.1', 3.8))
ok    after re-voice (+1.3 s): plain data-start="0" left alone
ok    make_beats.py runs
ok    build.py runs
ok    narration.m4a is encoded from narration.wav
ok    make_beats.py runs
ok    build.py runs
ok    narration.m4a up to date → not re-encoded
ok    make_beats.py runs
ok    build.py runs
ok    newer narration.wav → m4a re-encoded
hf-anchors: OK

exit_code=0
```

### research/final/package-smoke-2.txt
```text
$ bash upstream/scripts/new_project.sh package-smoke /workspace/reminder-batch/item05/research/final/exercise-smoke/ray-explainer-offline/exercise
/workspace/reminder-batch/item05/research/final/exercise-smoke/ray-explainer-offline/exercise/2026-11-11-package-smoke

exit_code=0
```

### research/final/package-smoke-3.txt
```text
$ python3 exercise/prepare_fixture.py /workspace/reminder-batch/item05/research/final/exercise-smoke/ray-explainer-offline/exercise/2026-11-11-package-smoke
fixture prepared: /workspace/reminder-batch/item05/research/final/exercise-smoke/ray-explainer-offline/exercise/2026-11-11-package-smoke duration=12s PCM silence, NOT narration

exit_code=0
```

### research/final/package-smoke-4.txt
```text
$ node upstream/scripts/render.js /workspace/reminder-batch/item05/research/final/exercise-smoke/ray-explainer-offline/exercise/2026-11-11-package-smoke stills 2.5
ready { duration: 12, scenes: 'hook:kit proof:kit gate:kit' }
/workspace/reminder-batch/item05/research/final/exercise-smoke/ray-explainer-offline/exercise/2026-11-11-package-smoke/stills

exit_code=0
```

## PDF逐页自检记录
# A4 PDF逐页Read自检

2026-11-11 Asia/Shanghai；WeasyPrint 70.0实际渲染，pdfinfo确认12页、595.276×841.89pt。pdftoppm -scale-to 1300 -png逐页生成PNG，全部12页均通过Read单独查看；不是独立审核。

|页|PNG|观察|SHA256|
|---|---|---|---|
|1|page-01.png|封面与大号重点完整，SHA可读|5dc659b40a1961d86f4391c7a6c1211509f3a5ce1ad20756c3a77348153e8e33|
|2|page-02.png|Q01/02文字、SVG无截断|d515341caf9fa05c741f900f4e90a7141801ca80d716151e19ee566af2d8101c|
|3|page-03.png|Q03/04文字、SVG无截断|0271878b339e4237a0b0d826eade130e2deeefe61bf7d151a85b71a40d902b27|
|4|page-04.png|Q05/06文字、SVG无截断|0efaa7a27c31d52997f3a9c08052886120cc3c6fa45b42bfdebc6ba960b9479a|
|5|page-05.png|Q07/08文字、SVG无截断|3b63f5c35193449050f77f35ee395b445ab8d1e3e60bc6e1f41712299705b3c6|
|6|page-06.png|Q09/10失败门禁与0.35秒差异可读|f56432cb5d6493773cdf8d6e351a2d54ad644e1feac69255e7702ae203017bc5|
|7|page-07.png|Q11/12字体边界与许可完整|48c00a9bf179a81a36d67edcce0c91ebaa1547815d90ec5c3b860f4bfa5254dd|
|8|page-08.png|4种用途及文件契约完整|82645611e015fbe9da28c9c03460eb334d9c6c54dcb543d96faf7cf1c615a2d4|
|9|page-09.png|步骤1–2命令块、结果与验证完整|f1164dd0cbac1a378d6f941b0c2afa5705cb68a0d30a8928984c09a53f473b1c|
|10|page-10.png|步骤3–4命令块、结果与验证完整|07d518c3365147544ca9724d093826449d39606e38a9a5f8aaab53211c947373|
|11|page-11.png|步骤5–6长命令自动折行，无越界，底部验证仍可读|2180d619fcac0838a8586198cfe5f33f6aacdecce766282cec5a8847c3f09eee|
|12|page-12.png|3幕小图可读、状态表完整，无横向裁切|03f16e3176f11002dcbf609b28815cf093bdc8f0511ef0fc788a5a33a7747768|

## 机器可核验证据
- 完整ffprobe输出：evidence/resume/ffprobe.json。
- 64文件Git blob验证：evidence/resume/source-blob-check.txt。
- PDF原始PNG在云端pdf-pages/，轻量包仅收检查记录与哈希，不收大图。
- 完整视频在exercise/2026-11-11-resume-local/out.mp4，轻量包不含视频。

## 轻量打包实际命令
```bash
python3 research/final/package_light.py
```
该脚本显式选择本项文件，Python zipfile.ZIP_DEFLATED、compresslevel=9；生成MANIFEST.sha256，testzip并逐文件重算SHA256。源码保留云端；exercise的文本payload同样用以下Python标准库操作打包（完整初始化器和锁文件在ZIP内）：
```python
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
p=Path('/workspace/reminder-batch/item05')
root=p/'research/final/exercise-payload'
with ZipFile(p/'exercise.zip','w',ZIP_DEFLATED,compresslevel=9) as z:
    for f in sorted(root.rglob('*')):
        if f.is_file():
            z.write(f,'ray-explainer-offline/'+f.relative_to(root).as_posix())
with ZipFile(p/'exercise.zip') as z:
    assert z.testzip() is None
```
轻量包不包含整套字体/大图/视频；完整成片路径是云端证据，不是公开分享链接。最终大小与清单见STATUS.md及bundle-check.json。
