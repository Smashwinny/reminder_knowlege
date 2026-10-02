# -*- coding: utf-8 -*-
"""
mini_s2s.py — 复刻 huggingface/speech-to-speech 的级联架构（文本级模拟）
对应上游 src/speech_to_speech/s2s_pipeline.py 的 8 队列 4 段 handler 设计：
  recv_audio -> [VAD] -> spoken_prompt -> [STT] -> text_prompt -> [LLM] -> lm_response -> [TTS] -> send_audio
本机无声卡，"音频"用文本块模拟；关键是验证【流式接力】：
  LLM 一边生成、TTS 一边合成，首块音频(ttfa)远早于 LLM 全部完成。
"""
import queue, threading, time

# ---------- 模拟上游 audio 输入（一句话，切成 8 个"音频块"） ----------
UTTERANCE = "嗯…… 我想去北京旅游 你帮我 计划一下 三天的 行程"
AUDIO_BLOCKS = UTTERANCE.split()

def log(tag, msg):
    print(f"[{time.perf_counter()-T0:7.3f}s] [{tag:^8}] {msg}")

T0 = time.perf_counter()

# ---------- 四段 handler：模仿 BaseHandler(in_queue, out_queue, process) ----------
def vad_handler(q_in, q_out):
    """VAD：攒块，检测到 64ms 静音(这里模拟为收到全部块)就提交一句话"""
    buf = []
    while True:
        item = q_in.get()
        if item is None:                      # 模拟 speech_stopped
            if buf:
                text = "".join(buf)
                log("VAD", f"静音达标, 提交话语: 「{text}」")
                q_out.put(("user_text", text))
                buf = []
        else:
            buf.append(item)

def stt_handler(q_in, q_out):
    """STT：文本级模拟 = 原样透传，但记录耗时"""
    while True:
        kind, text = q_in.get()
        time.sleep(0.18)                      # 模拟 Parakeet 转写 ~0.18s
        log("STT", f"转写完成(0.18s): 「{text}」")
        q_out.put(("prompt", text))

REPLY = "好的 你可以先去 故宫 然后下午 逛 景山公园 傍晚 到 南锣鼓巷 吃小吃"

def llm_handler(q_in, q_out):
    """LLM：流式逐词吐出（模仿 token 流）"""
    while True:
        _, prompt = q_in.get()
        log("LLM", f"收到 prompt, 开始流式生成…")
        for word in REPLY.split():
            time.sleep(0.12)                  # 模拟逐 token 生成
            q_out.put(("token", word))

def tts_handler(q_in, q_out):
    """TTS：每攒 3 个词合成一个"音频块"，记录 ttfa"""
    buf, n = [], 0
    while True:
        kind, tok = q_in.get()
        buf.append(tok)
        if len(buf) == 3:
            n += 1
            time.sleep(0.05)                  # 模拟合成首包延迟
            log("TTS", f"音频块#{n} 出厂: 「{''.join(buf)}」")
            q_out.put(("audio", "".join(buf)))
            buf = []

# ---------- 组装：4 线程 + 队列（ThreadManager 的极简版） ----------
q_audio, q_spoken, q_text, q_lm, q_out = (queue.Queue() for _ in range(5))
threads = [
    threading.Thread(target=vad_handler, args=(q_audio, q_spoken), daemon=True),
    threading.Thread(target=stt_handler, args=(q_spoken, q_text), daemon=True),
    threading.Thread(target=llm_handler, args=(q_text, q_lm), daemon=True),
    threading.Thread(target=tts_handler, args=(q_lm, q_out), daemon=True),
]
[t.start() for t in threads]

# ---------- 播放"用户说话"：块间隔 60ms，然后静音触发 VAD 提交 ----------
t_speech_end = None
for b in AUDIO_BLOCKS:
    q_audio.put(b)
    time.sleep(0.06)
t_speech_end = time.perf_counter()
log("MIC", "用户说完, 进入静音…")
time.sleep(0.3)
q_audio.put(None)                             # speech_stopped 事件

# ---------- 收"音频块"，统计 ttfa 与 e2e ----------
ttfa = first_block_end = None
blocks = 0
t_deadline = time.time() + 30
while time.time() < t_deadline:
    try:
        _, chunk = q_out.get(timeout=1)
    except queue.Empty:
        break
    blocks += 1
    now = time.perf_counter()
    if ttfa is None:
        ttfa = now - t_speech_end             # 首块音频距说完的延迟
    first_block_end = now

e2e = first_block_end - t_speech_end
print("\n===== 延迟账本（对齐上游 response-latency.md 字段） =====")
print(f"音频块总数        : {blocks}")
print(f"tts_ttfa(说完→首块): {ttfa:.3f}s   <- 流式接力的意义：不必等 LLM 生成完")
print(f"e2e(说完→末块)     : {e2e:.3f}s")
print(f"结论: ttfa 是 e2e 的 {ttfa/e2e*100:.0f}%，用户提前 {(e2e-ttfa)*1000:.0f}ms 听到声音")
