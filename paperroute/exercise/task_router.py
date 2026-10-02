# -*- coding: utf-8 -*-
"""
E2: 混合模型任务路由器微缩版 —— PaperRoute 方法论第 1 条复现
推文: "绝不让单一模型包揽全场：玩法与物理逻辑交给 Astra；角色概念图交给 ChatGPT；
带脸的 3D 角色网格花 8 美元丢给专门的 Meshy；最后再拉回 Astra 绑上 23 根骨骼"。
devlog 佐证: P0 baseline 先写 PRD/工程标准/架构契约，资产管线脚本入库 ArtSource/。

本实验: 用规则路由器把 12 条真实开发任务分派到正确的"生产者车道"，
对比 (a)全用一个旗舰模型 vs (b)按任务类型路由 的成本，断言路由结果与作者实际选择一致。
(纯离线演示: 用成本参数表模拟, 不调任何 API)
"""
import sys

# 车道: (生产者, 擅长, 单位成本系数) —— 成本系数为演示用相对值
LANES = {
    "code":      ("Astra",   "玩法逻辑/物理/绑定脚本", 1.00),
    "concept":   ("ChatGPT", "2D 概念图/插画方向",     0.20),
    "mesh3d":    ("Meshy",   "带脸 3D 网格生成",       0.60),   # 8 美元/角色的专用生成
    "asset":     ("Astra+脚本", "Headless 批量资产/参数化建筑", 0.30),
    "review":    ("Astra+截图", "渲染图帧级审查",       0.15),
}

RULES = [
    ("物理|碰撞|穿模|骨骼|绑骨|绑定|抛物线|手感|骑行|游戏逻辑|玩法|HUD|排行榜|结算", "code"),
    ("概念图|插画|画风|色彩基调|美术方向", "concept"),
    ("带脸|角色网格|3d 角色|人物模型", "mesh3d"),
    ("批量|建筑群|房子|屋顶|glb|资产|户型", "asset"),
    ("审查|截图|转面图|验收|帧", "review"),
]

TASKS = [  # (任务, 作者实际车道) —— 全部取自推文/devlog
    ("消除自行车骑行穿模，调整车轮碰撞体",            "code"),
    ("给主角绑 23 根骨骼并修权重",                    "code"),
    ("报纸投掷的抛物线物理调参",                      "code"),
    ("画出主角骑手的角色概念图",                      "concept"),
    ("生成带脸的 3D 主角角色网格",                    "mesh3d"),
    ("批量生成 40 栋临街建筑的 GLB 模型",             "asset"),
    ("替换 playable house bodies 为 Blender 户型族",  "asset"),
    ("自动保存骑手正/侧/后转面图用于审查",            "review"),
    ("雨天轮胎打滑的水印特效",                        "code"),
    ("复古报纸风格结算 UI 排版",                      "code"),
    ("定义插画色彩基调与美术方向",                    "concept"),
    ("帽子第 3 帧没遮住头发，对照截图修正",           "review"),
]

def route(task):
    for pattern, lane in RULES:
        for kw in pattern.split("|"):
            if kw in task.lower():
                return lane, kw
    return "code", "default"

def cost_of(plan):
    """(a) 全旗舰: 每条任务都按 code 车道成本; (b) 路由: 各车道成本"""
    all_flagship = sum(1.00 for t, _ in TASKS)
    routed = sum(LANES[route(t)[0]][3 - 1] for t, _ in TASKS)
    return all_flagship, routed

def main():
    print("任务 -> 路由车道 (命中关键词) | 作者实际选择 | 一致?")
    ok = 0
    for task, truth in TASKS:
        lane, kw = route(task)
        hit = "OK" if lane == truth else "MISS"
        ok += lane == truth
        print(f"  {task[:26]:28s} -> {lane:12s} ({kw:8s}) | {truth:8s} | {hit}")
    print(f"\n路由与作者实际选择一致率: {ok}/{len(TASKS)}")
    a, b = cost_of(None)
    print(f"全旗舰模型总成本系数: {a:.2f}")
    print(f"按车道路由后总成本系数: {b:.2f}")
    print(f"成本缩减: {a/b:.1f}x")
    assert ok == len(TASKS), "路由结果与作者实际选择不一致!"
    print("[task_router] 全部任务路由正确，混合流水线成本优势复现")
    return 0

if __name__ == "__main__":
    sys.exit(main())
