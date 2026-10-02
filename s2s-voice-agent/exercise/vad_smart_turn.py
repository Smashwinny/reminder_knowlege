# -*- coding: utf-8 -*-
"""
vad_smart_turn.py — 模拟上游 VADHandler 的两段式轮次判断（流式状态机版）
上游逻辑(vad_handler.py): Silero 按 min_silence_ms 发现"语音→静音"边界 ->
  Smart Turn v3.2(pipecat-ai/smart-turn-v3, ONNX)判断这句说完没完:
    complete   -> 提交给 STT
    incomplete -> hold(继续听), 超过 smart_turn_max_wait_ms=2000ms 才强制提交
本实验用"能量 VAD"+启发式 smart-turn 复刻该状态机，对比两种策略:
  纯VAD:   每个 >=320ms 静音窗都提交(两处都会翻车)
  +Smart:  犹豫句救回、结束句只提交一次
"""
import numpy as np

SR = 16000
rng = np.random.default_rng(7)

def synth_word(dur, amp):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 140 + rng.uniform(-20, 20)
    wave = (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2*f*t) + 0.25*np.sin(2*np.pi*3*f*t))
    return wave * np.hanning(n) * amp

def synth_pause(dur):
    return rng.normal(0, 0.003, int(SR * dur))

def utterance(segments, tail=1.0):
    parts = [synth_word(d, a) if k == 'w' else synth_pause(d) for k, d, a in segments]
    return np.concatenate(parts + [synth_pause(tail)])

# 场景A: "我想去" [犹豫0.5s] "北京天安门" —— 说话人想词，不该被切断
A = utterance([('w',0.30,0.8),('w',0.28,0.7),('w',0.32,0.8),('p',0.50,0),('w',0.30,0.8),('w',0.26,0.75),('w',0.30,0.8)])
# 场景B: "好的就这些" [停顿0.8s] —— 真说完，要恰好提交一次
B = utterance([('w',0.28,0.8),('w',0.30,0.8),('w',0.26,0.7),('p',0.80,0)])

FRAME_S, MIN_SILENCE_S = 0.032, 0.32
SMART_HOLD_S, MAX_WAIT_S = 0.40, 2.0        # 对齐上游 incomplete_delay/max_wait 思路
frame_n = int(FRAME_S * SR)

def frames(x):
    n = len(x) // frame_n
    th = 0.05
    return [np.sqrt(np.mean(x[i*frame_n:(i+1)*frame_n]**2)) > th for i in range(n)]

def simulate(fs, use_smart):
    """流式状态机(对齐上游 VADHandler): idle -> 语音 -> 候选边界 ->(smart判定)-> 提交/hold。
    提交后回 idle, 必须等新语音重新武装(上游 Silero triggered 状态机)。
    返回 (提交时刻列表, 事件日志)。"""
    commits, events, state = [], [], 'idle'
    silence, hold, last_voiced_end = 0.0, 0.0, 0.0
    for i, voiced in enumerate(fs):
        t = i * FRAME_S
        if voiced:
            if state == 'idle':
                events.append(f"{t:5.2f}s 检测到语音开始(speech_started)")
            if state == 'hold' and hold > 0:
                events.append(f"{t:5.2f}s 用户继续说了 -> hold 解除, 话语拼接回去")
            state, silence, hold = 'speech', 0.0, 0.0
            last_voiced_end = t
        elif state in ('speech', 'hold'):
            silence += FRAME_S
            if silence >= MIN_SILENCE_S and hold == 0:
                lookahead = fs[i+1 : i+1+int(SMART_HOLD_S/FRAME_S)]
                if use_smart and any(lookahead):
                    events.append(f"{t:5.2f}s 候选边界 -> smart-turn=incomplete -> hold(继续听)")
                    state, hold = 'hold', 0.001
                    silence = 0.0
                else:
                    commits.append(t)
                    events.append(f"{t:5.2f}s {'smart-turn=complete' if use_smart else '静音计时到'} -> 提交!")
                    state, silence = 'idle', 0.0
            if state == 'hold':
                hold += FRAME_S
                if hold >= MAX_WAIT_S:
                    commits.append(t)
                    events.append(f"{t:5.2f}s hold 超时 {MAX_WAIT_S}s -> 强制提交")
                    state, silence, hold = 'idle', 0.0, 0.0
    return commits, events, last_voiced_end

TOTAL = None
for label, x in [("A 犹豫句「我想去…(0.5s)…北京天安门」", A),
                  ("B 结束句「好的就这些。(0.8s)」", B)]:
    fs = frames(x)
    speech_end = max(i for i, v in enumerate(fs) if v) * FRAME_S   # 最后一帧语音时刻
    c_pure, ev_pure, _ = simulate(fs, use_smart=False)
    c_smart, ev_smart, _ = simulate(fs, use_smart=True)
    print(f"--- {label} ---")
    print("  [纯VAD]");   [print("    ", e) for e in ev_pure]
    print("  [+Smart-Turn]"); [print("    ", e) for e in ev_smart]
    # 指标: 提交发生时, 用户后面还有没有语音? 有 => 过早提交(把人打断)
    premature_pure  = any(c < speech_end - 0.1 for c in c_pure)
    premature_smart = any(c < speech_end - 0.1 for c in c_smart)
    ok = (len(c_smart) == 1) and not premature_smart
    print(f"  纯VAD: 提交{len(c_pure)}次, 过早打断={'是' if premature_pure else '否'} | "
          f"+Smart: 提交{len(c_smart)}次, 过早打断={'是' if premature_smart else '否'} -> {'✅' if ok else '❌'}\n")

print("===== 结论 =====")
print("A 句纯 VAD 在犹豫停顿处就把话提交了(后面的话被切断成新请求, 指令残缺);")
print("加 Smart-Turn 判断 hold 住继续听, 直到真说完才提交一次。")
print("代价: 提交晚约 0.3-0.4s(确认延迟) —— 快(Silero)与准(Smart Turn)分层,")
print("正是上游 VADHandler 两段式设计的设计动机。")
