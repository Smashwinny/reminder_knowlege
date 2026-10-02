# -*- coding: utf-8 -*-
"""
E3: "渲染图代替形容词"审查环微缩版 —— PaperRoute 方法论第 3 条复现
推文: "别对着对话框说把动作改得更自然点，大模型根本听不懂这种玄学！
作者搭了自动抓取脚本：让骑手做动作，自动保存正/侧/后/黏土转面图。
指着具体某一帧截图说'帽子第 3 帧没遮住头发'，改动成功率直接飙到 70%"

模拟: 24 帧骑行动画，骑手参数含 hat_offset(帽子偏移)。
  资产流改参数 -> capture() 逐帧"截图"(参数快照) -> 审查器检查哪一帧出问题
  两种反馈模式:
    vague(形容词): "动作再自然一点" -> 修复器只能全参数盲调(加随机扰动)
    framed(帧索引): "第 3 帧帽子偏移 0.4" -> 修复器定点回改
  各跑 200 轮统计修复成功率，复现"帧级反馈成功率高"的结论。
"""
import random, sys

FRAMES = 24
random.seed(42)

class Rider:
    def __init__(self):
        self.hat_offset = [0.0] * FRAMES     # 每帧帽子-头发相对偏移
        self.lean = [random.uniform(-0.05, 0.05) for _ in range(FRAMES)]
    def inject_defect(self, frame, amount):
        self.hat_offset[frame] = amount
    def capture(self):
        """自动抓取脚本: 逐帧存正/侧/后三视图的检查值(简化为帧快照)"""
        return [{"frame": f, "hat": self.hat_offset[f],
                 "views": ["front", "side", "rear"]} for f in range(FRAMES)]

def review(captures, mode):
    """审查器: 找 hat 偏移超阈值(0.12)的帧。vague 模式=对着对话框喊形容词(信息为零)"""
    if mode == "vague":
        defects = [c["frame"] for c in captures if c["hat"] > 0.12]
        return "动作再自然一点", None            # 不给帧信息!
    worst = max(captures, key=lambda c: c["hat"])
    if worst["hat"] <= 0.12:
        return "pass", None
    return f"第 {worst['frame']} 帧帽子偏移 {worst['hat']:.2f}", worst["frame"]

def fix(rider, feedback, frame, mode):
    if mode == "vague":
        for f in range(FRAMES):                  # 盲调所有帧
            rider.hat_offset[f] = max(0.0, rider.hat_offset[f] + random.uniform(-0.3, 0.05))
    else:
        rider.hat_offset[frame] = 0.0             # 定点修复

def run_trial(mode):
    r = Rider()
    r.inject_defect(3, random.uniform(0.15, 0.6)) # 缺陷注入第 3 帧
    fb, frame = review(r.capture(), mode)
    if fb == "pass": return True
    fix(r, fb, frame, mode)
    return all(v <= 0.12 for v in r.hat_offset)   # 修复成功判定

def main():
    print(f"{'模式':10s} {'试验':>6s} {'修复成功':>8s} {'成功率':>8s}")
    rates = {}
    for mode, label in [("vague", "形容词反馈"), ("framed", "帧索引反馈")]:
        wins = sum(run_trial(mode) for _ in range(200))
        rates[mode] = wins / 2.0
        print(f"{label:10s} {200:6d} {wins:8d} {wins/2.0:7.1f}%")
    print(f"\n帧索引反馈成功率 / 形容词反馈成功率 = {rates['framed']/max(rates['vague'],0.1):.1f}x")
    print("推文口径: 指着帧截图提意见，改动成功率飙到 70% —— 方向一致:")
    print("把'玄学形容词'换成'带帧号/视图名的运行时证据'，反馈才可执行。")
    assert rates["framed"] > rates["vague"], "实验结果与预期方向不符"
    print("[frame_review_loop] 帧级证据反馈优势复现")
    return 0

if __name__ == "__main__":
    sys.exit(main())
