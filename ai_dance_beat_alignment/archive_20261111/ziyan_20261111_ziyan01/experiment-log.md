# Item01 真实实验日志

续跑日期：2026-11-11 Asia/Shanghai UTC+8。本worker复核与复跑；不是独立审核。

## 环境与范围
Python 3.13.5，标准库wave/array/statistics；云端CPU，无第三方包，无原曲/肖像材料，无模型/API调用。基准仓库SHA见sources.md。原文530行（含内嵌歌曲帖文字）全部读取。此前受阻版只保留history，不再代表最终状态。

## 主实验：五步
工作目录 `/workspace/reminder-batch/item01/exercise`。解压exercise ZIP后也可进入其exercise目录重跑。

1. `python3 dance_lab.py synth`：目的为建立确定性音频夹具；实际写出48kHz、16-bit单声道522048采样，10.876秒，25个脉冲。验证：WAV读回样本计数及truth.json，不用原歌曲。
2. `python3 dance_lab.py analyze`：目的为检测实际PCM与端点差；25起音，估计132.4990798675 BPM，最大起音误差0.020833333ms；261帧/24=10.875秒，误差-1ms。验证：起音逐个对合成真值。仅适合孤立点击的阈值检测，不是通用歌曲节拍追踪。
3. `python3 dance_lab.py template`：目的为编译三类参考角色与六段时间表；输出6区间/3参考，VALID，产生timeline.json和prompt.txt。验证：区间从0连续到10.876秒；未提交模型，模板不是最终生成成果。
4. `python3 dance_lab.py test`：目的为正反例验收；12项通过（1正例+9反例拒绝+2数值断言）。验证：角色碰撞、歌词动作、姿势迁移身份、fps错误、区间空洞、裁切字段、锚点越界、跨段开场例外、总长不匹配均拒绝。自写规则不做完整schema或六段数量约束，不证明图像/动作语义。
5. `python3 -c "import json; print(json.load(open('output/analysis.json'))['detected_pulses'])"`：目的为从真实文件核对结果；输出25，与运行stdout和analysis.json一致。保存所有产物；模型视频生成状态待验证。

## 原始stdout与退出码（实际复跑）
```text
[2026-11-11T01:20:51.586881 Asia/Shanghai UTC+8] $ /usr/bin/python3 --version
Python 3.13.5
exit_code=0

[2026-11-11T01:20:51.637609 Asia/Shanghai UTC+8] $ /usr/bin/python3 dance_lab.py synth
SYNTH samples=522048 duration=10.876000s pulses=25 BPM=132.5; NOT original audio
exit_code=0

[2026-11-11T01:20:51.694401 Asia/Shanghai UTC+8] $ /usr/bin/python3 dance_lab.py analyze
{
  "detected_pulses": 25,
  "estimated_BPM": 132.49907986750094,
  "max_onset_error_ms": 0.020833333333333332,
  "beat_s": 0.4528301886792453,
  "bar_s": 1.8113207547169812,
  "phrase_s": 3.6226415094339623,
  "phrase_anchors": [
    0.0,
    3.622642,
    7.245283,
    10.867925
  ],
  "audio_duration": 10.876,
  "nearest_24fps_frames": 261,
  "nearest_24fps_duration": 10.875,
  "duration_error_ms": -0.9999999999994458,
  "scope": "threshold onset detector on isolated synthetic clicks only; not a music beat tracker"
}
exit_code=0

[2026-11-11T01:20:51.726996 Asia/Shanghai UTC+8] $ /usr/bin/python3 dance_lab.py template
TEMPLATE phases=6 references=3 VALID; no model invocation
exit_code=0

[2026-11-11T01:20:51.758061 Asia/Shanghai UTC+8] $ /usr/bin/python3 dance_lab.py test
REJECT negative1: reference role collision
REJECT negative2: identity/lyric semantic leakage
REJECT negative3: identity/lyric semantic leakage
REJECT negative4: output contract
REJECT negative5: gap/overlap
REJECT negative6: feet/head/hands must remain visible
REJECT negative7: anchor outside audio
REJECT negative8: opening exception only segment01
REJECT negative9: duration coverage
PASS checks=12 (1 valid,9 rejected,2 numeric); VIDEO_NOT_GENERATED
exit_code=0

[2026-11-11T01:20:51.775015 Asia/Shanghai UTC+8] $ /usr/bin/python3 -c import json; print(json.load(open('output/analysis.json'))['detected_pulses'])
25
exit_code=0
```

## 未运行
H3、GPU舞蹈生成、原曲解析、身份/姿态识别、真实视觉连续性、跨段视频剪辑、成片声画同步与容器端点均未验证。不购买、不改安全设置、不上传私密原记录、不用用户密钥，不操作任务或日程。

## PDF真实打印与逐页检查

# A4 PDF逐页自查

日期：2026-11-11 Asia/Shanghai UTC+8；检查者：本续跑worker，非独立审核。

初次Chrome打印超过2分钟挂起，定向终止该worker PID；第二次bounded尝试60秒超时（exit 124）。保持sandbox原状，没有改安全设置。改用已装的WeasyPrint 70.0打印最终HTML，exit 0，575607 bytes、7页、595.276×841.89 pt A4。未修改或重做第4项，只借用其已经安装的渲染环境。

命令：
```bash
/workspace/reminder-batch/item04/research/pdf-venv/bin/python -m weasyprint /workspace/reminder-batch/item01/item01.html /workspace/reminder-batch/item01/item01.pdf
pdfinfo /workspace/reminder-batch/item01/item01.pdf
pdftoppm -scale-to 1500 -png /workspace/reminder-batch/item01/item01.pdf /workspace/reminder-batch/item01/evidence/checked-page
```

已对7张PNG逐一使用Read实际目视：
1. 封面、4用途、查重：无截字，三色图清楚。
2. Q01–03：3张卡片及SVG全部入页。
3. Q04–06：节拍与1ms数字清晰，无跨页卡片。
4. Q07–09：重心/相机例外图清楚，脚注正常。
5. Q10–12：补充校验器边界未溢出，3张SVG完整。
6. 5步实验：命令完整可读，结果与验证未被截断，脚注入页。
7. 来源/状态表/待验证：SHA长行可读，表格和橙色卡片完整。

最终PDF保留矢量文本与字体子集，未栅格化，不嵌整套字体。PNG只留本云目录，不加入轻量包。
- checked-page-1.png SHA256 `1ac52e4eec6183794211ada3938eb27eea533f090b3ecb2985c59d323b645524`
- checked-page-2.png SHA256 `c004ffefd52d946d1d6fc0d49831228103c8ec58aa74a1917ac3e571acee45f1`
- checked-page-3.png SHA256 `149bbbd6bfc623dae8c533ae52eed5827c8d04670a3a409303e27bb224bc22b8`
- checked-page-4.png SHA256 `bb369af379a035442ab9f0ad28d5e719a9a19c6892449502867d689b94ed4ca9`
- checked-page-5.png SHA256 `e3852c9cf9ff449f66141115e0669a677103718c5ede8845266b43ba89434241`
- checked-page-6.png SHA256 `0f9fa7069e8c09bac005c0d2ba590764df479fa6bb3ae5609e7477ce5853a415`
- checked-page-7.png SHA256 `a736aea146b17c26d8922e9147ac8fb00fa9f1fd2a24747a00c2ece3461acd90`
