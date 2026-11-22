#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""运镜结构化工单编译实验；只生成文本与检查表，不调用视频生成服务。

generic 保留负向约束；runway-gen4 使用人工给出的正向改写。没有正向改写的
约束会列入 unresolved，不能静默宣称转换成功。
"""
import argparse


def compile_shot(spec, dialect="generic"):
    if dialect not in {"generic", "runway-gen4"}:
        raise ValueError(f"未知方言：{dialect}")
    parts = [f"{spec['stabilizer']}拍摄", f"沿{spec['path']}运动",
             f"{spec['viewpoint']}视角"]
    if spec.get("trigger"):
        parts.append(f"当{spec['trigger']}时执行{spec['trigger_action']}")
    parts.append(spec["timing"])
    unresolved = []
    if dialect == "generic":
        parts.extend(f"禁止{negative}" for negative in spec.get("negatives", []))
    else:
        rewrites = spec.get("positive_rewrites", {})
        for negative in spec.get("negatives", []):
            if negative in rewrites:
                parts.append(rewrites[negative])
            else:
                unresolved.append(negative)
    return "，".join(parts), unresolved


def acceptance(spec):
    checks = ["起终点明确", "路径节点可数", "主体大小变化有指标"]
    if spec.get("trigger"):
        checks.append("触发点动作可观察")
    if "连续" in spec["timing"] or "长镜头" in spec["timing"]:
        checks.append("剪切约束：全程无剪辑（数剪接口）")
    if "Dolly Zoom" in spec["path"] or "dolly" in spec["path"].lower():
        checks += ["Dolly Zoom 双条件①主体在画面中尺度基本恒定",
                   "Dolly Zoom 双条件②背景透视明显压缩/拉伸（只看出缩放不算过）"]
    return checks


DEFAULT = {
    "stabilizer": "稳定器", "path": "缓慢推近→环绕主体半圈（Dolly Zoom 收尾）",
    "viewpoint": "POV", "trigger": "主体抬手", "trigger_action": "镜头随之上摇",
    "timing": "单镜头连续 8 秒无剪辑", "negatives": ["切镜", "穿模"],
    "positive_rewrites": {
        "切镜": "从起始动作到结束动作保持同一个连续镜头",
        "穿模": "主体与场景保持合理空间关系，结构完整稳定",
    },
}

FPV = {
    "stabilizer": "FPV 无人机稳定增稳", "path": "低空前进→穿窗→落地后跟拍主体",
    "viewpoint": "FPV", "trigger": "无人机落地", "trigger_action": "转为低机位跟拍",
    "timing": "单镜头连续 10 秒无剪辑", "negatives": ["切镜"],
    "positive_rewrites": {"切镜": "穿窗、落地和跟拍之间保持连续飞行画面"},
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--example", choices=["default", "fpv"], default="default")
    args = parser.parse_args()
    spec = DEFAULT if args.example == "default" else FPV

    generic, generic_unresolved = compile_shot(spec, "generic")
    runway, runway_unresolved = compile_shot(spec, "runway-gen4")
    assert not generic_unresolved and not runway_unresolved
    assert all(f"禁止{negative}" in generic for negative in spec["negatives"])
    assert "禁止" not in runway
    assert all(text in runway for text in spec["positive_rewrites"].values())
    assert len(acceptance(spec)) == (7 if args.example == "default" else 5)

    print("=== generic 方言 ===\n" + generic)
    print("\n=== runway-gen4 方言（真实正向改写）===\n" + runway)
    print("\n未转换约束：", runway_unresolved)
    print("\n=== 验收清单 ===")
    for check in acceptance(spec):
        print(" -", check)
    print("\nPASS：generic 保留负向；Gen-4 无‘禁止’且包含全部正向改写")
    print("边界：文本编译与断言通过，不代表真实生成视频满足运镜效果")


if __name__ == "__main__":
    main()
