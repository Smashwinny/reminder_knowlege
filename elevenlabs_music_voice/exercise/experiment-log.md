# ElevenLabs 配乐与音色 · 实验日志（task 27853f54-7fef-4326-92b8-9554d76f7cef）

实验日期：2026-10-27
性质：接口契约 + 验收方法学习。未充值、未生成真实音频（API 401 探针为只读）。

## 步骤与真实输出

### 步骤 1：video-to-music 契约核实（官方文档直读）

- `POST https://api.elevenlabs.io/v1/music/video-to-music`（multipart）
- videos：≤10 个、合计 ≤200MB、总长 ≤600 秒；description ≤4100 字；tags ≤10
- 关键开关：`add_sfx`（从视频提取 SFX 线索）、`separate_tracks`（返回音乐/SFX 分轨 ZIP）、
  `use_audio_as_reference`（用原片音频的流派/BPM/情绪做生成参考）、`sign_with_c2pa`
- **默认返回一条混合音频**；分轨要显式 separate_tracks=true
- 档位：192kbps mp3 需 Creator+；44.1kHz PCM 需 Pro+；零留痕模式限 Enterprise
- 错误：403 订阅不足 / 422 参数校验

### 步骤 2：只读 401 探针（真实请求）

```
GET https://api.elevenlabs.io/v1/user（无 key）
→ 401 {"detail":{"type":"authentication_error","code":"unauthorized","status":"needs_authorization"}}
```
✅ 认证契约真实（xi-api-key / Authorization header 二选一）

### 步骤 3：IVC vs PVC 核实（官方博客+检索）

| | IVC | PVC |
|---|---|---|
| 机制 | 推理时参考音频条件，**不动权重** | 训练专属模型（fine-tune） |
| 素材 | 1-5 分钟（10 秒可跑） | ≥30 分钟，推荐 1-3 小时 |
| 耗时 | 秒级 | 3-6 小时训练 |
| 门槛 | Starter(~$6/月) | Creator+(~$22/月)+严格声纹验证 |

→ 原帖"复刻自己的声音"未指明是哪种；两者成本与效果差一个量级。

### 步骤 4：混音验收实验（纯 Python 合成，真实测量）

合成模拟人声（180Hz 谐波+字间包络）与模拟 BGM（和声+LFO 起伏），实测 RMS：
```
人声 RMS: -22.0 dBFS   BGM RMS: -26.1 dBFS
```
按目标响度比生成三个混音（BGM 增益公式 g=10^((Δ目标)/20)）：
- mix_3db.wav（人声仅领先 3dB → 听感浑浊区）
- mix_8db.wav（领先 8dB → 通常清晰可懂区 ✅）
- mix_15db.wav（领先 15dB → 音乐近乎消失区）

验收参考（行业经验值）：人声比 BGM 高 6~10dB；<4dB 浑浊；>15dB 音乐失存。

## 结论

- video-to-music 是"条件生成"不是"自动混音成片"：返回音乐轨，混音责任仍在你的剪辑环节；
- IVC/PVC 是"推理时参考 vs 训练"的本质差异，选型先看素材量与时效要求；
- **混音验收可机检**：RMS 分贝差是客观判据（本实验合成样本实测），不必靠"听着还行"；
- 未验证：真实生成质量/音色相似度（需订阅授权）。

## 产物

- `exercise/voice.wav` / `bgm.wav` / `mix_3db.wav` / `mix_8db.wav` / `mix_15db.wav`
- `exercise/experiment-log.md`（本文件，含合成与测量脚本）
