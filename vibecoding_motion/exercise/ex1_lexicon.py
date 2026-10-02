# ex1 动效描述词表 → CSS 生成器（零依赖）
# 把"结构化动效描述"翻译成 AI/浏览器都能精确执行的 CSS
# 词表四大件：触发 trigger / 对象 property / 缓动 easing / 时序 timing

EASING = {
    # 名词 → CSS 值。性格备注用于生成注释
    "linear":        ("linear",                     "匀速，机械感，进度条专用"),
    "ease-out":      ("cubic-bezier(0, 0, 0.2, 1)", "快进慢出，刹车感，入场首选"),
    "ease-in":       ("cubic-bezier(0.4, 0, 1, 1)", "慢起加速，离场/消失"),
    "ease-in-out":   ("cubic-bezier(0.4, 0, 0.2, 1)","两头慢中间快，位移换位"),
    "spring":        ("cubic-bezier(0.34, 1.56, 0.64, 1)", "过冲回弹，果冻感（模拟弹簧）"),
    "bounce":        ("cubic-bezier(0.28, 0.84, 0.42, 1)", "落地弹跳，夸张强调"),
}

PRIMITIVE = {
    # 名词 → (CSS 初始态属性, 结束值)。动作原语词汇表
    "fade":  [("opacity", "0", "1")],
    "slide-up":    [("opacity", "0", "1"), ("transform", "translateY(24px)", "translateY(0)")],
    "slide-down":  [("opacity", "0", "1"), ("transform", "translateY(-24px)", "translateY(0)")],
    "slide-left":  [("opacity", "0", "1"), ("transform", "translateX(24px)", "translateX(0)")],
    "scale-in":    [("opacity", "0", "1"), ("transform", "scale(0.8)", "scale(1)")],
    "blur-in":     [("opacity", "0", "1"), ("filter", "blur(8px)", "blur(0)")],
    "pop":         [("opacity", "0", "1"), ("transform", "scale(0.5)", "scale(1)")],
}

def generate(spec: dict) -> str:
    """spec = {"selector": ".card", "primitive": "slide-up", "easing": "ease-out",
               "duration_ms": 300, "stagger_ms": 60, "count": 5}"""
    sel, prim = spec["selector"], spec["primitive"]
    ease_css, ease_note = EASING[spec["easing"]]
    dur = spec["duration_ms"]
    lines = [f"/* 动效描述: {prim} + {spec['easing']} + {dur}ms"
             + (f" + stagger {spec['stagger_ms']}ms" if spec.get("stagger_ms") else "")
             + f"  |  缓动性格: {ease_note} */"]
    props = []
    for prop, a, b in PRIMITIVE[prim]:
        lines.append(f"{sel} {{ {prop}: {a}; }}")                      # 初始态
        props.append(f"{prop} {dur}ms {ease_css}")                     # transition 条目
    lines.append(f"{sel}.enter {{ opacity: 1; transform: none; filter: none; }}")
    lines.append(f"{sel} {{ transition: {', '.join(props)}; }}")
    if spec.get("stagger_ms"):
        for i in range(1, spec.get("count", 1)):
            lines.append(f"{sel}:nth-child({i+1}) {{ transition-delay: {i*spec['stagger_ms']}ms; }}")
    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    # 场景 A：一张卡片的入场（视频里的典型需求）
    a = generate({"selector": ".card", "primitive": "slide-up",
                  "easing": "ease-out", "duration_ms": 300})
    print(a)
    # 场景 B：5 张卡片排队入场（错峰 stagger）
    b = generate({"selector": ".list .card", "primitive": "slide-up",
                  "easing": "ease-out", "duration_ms": 300,
                  "stagger_ms": 60, "count": 5})
    print(b)
    # 场景 C：强调弹窗（spring）
    c = generate({"selector": ".dialog", "primitive": "pop",
                  "easing": "spring", "duration_ms": 250})
    print(c)
    with open("ex1_out_sceneA.css", "w", encoding="utf-8") as f: f.write(a)
    with open("ex1_out_sceneB.css", "w", encoding="utf-8") as f: f.write(b)
    with open("ex1_out_sceneC.css", "w", encoding="utf-8") as f: f.write(c)
    print("[OK] 3 个场景 CSS 已生成")
