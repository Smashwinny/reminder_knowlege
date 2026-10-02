# -*- coding: utf-8 -*-
"""
实验步骤1：生成分镜表（对标 Pixelle-Video 的 generate_content / plan_visuals 阶段）
真实项目里这一步由 LLM 完成；本实验用预写文案离线复刻，
数据结构 1:1 对齐上游 pixelle_video/models/storyboard.py 的 StoryboardFrame。
运行：python ex1_storyboard.py
"""
import json
import sys
from pathlib import Path

EX = Path(__file__).parent
OUT = EX / "output"
OUT.mkdir(exist_ok=True)

# 主题：模仿用户在 WebUI 里输入的"主题"，正常由 LLM 扩写成 5 句解说词
TOPIC = "为什么人工智能短剧正在爆火"

# 每帧 = 一句解说 + 一段图像提示词（真实项目由 LLM 按提示词模板生成，
# 模板见上游 pixelle_video/prompts/topic_narration.py，要求 5~20 词/句、30~60 词/提示词）
FRAMES = [
    {
        "narration": "十年前，做一支视频需要摄像机、演员和剪辑台。",
        "image_prompt": "cinematic wide shot, vintage film set, camera crew, warm light",
    },
    {
        "narration": "今天，一句话就能让 AI 写文案、画配图、配音、剪辑成片。",
        "image_prompt": "futuristic AI studio, holographic screens, neon blue glow",
    },
    {
        "narration": "短剧平台把这条流水线推到了极致：剧本、分镜、角色一个都不放过。",
        "image_prompt": "storyboard wall, comic panels, production desk, dramatic light",
    },
    {
        "narration": "开源社区给出了八套答案，从抽卡式生成到工业化工作台。",
        "image_prompt": "github repository constellation, glowing nodes, dark background",
    },
    {
        "narration": "而真正的分水岭，是角色一致性：换个镜头不能变脸。",
        "image_prompt": "character concept art, identity anchor, multiple angles, same face",
    },
]


def main():
    storyboard = {"topic": TOPIC, "frames": []}
    for i, f in enumerate(FRAMES):
        storyboard["frames"].append({
            "index": i,
            "narration": f["narration"],
            "image_prompt": f["image_prompt"],
            # 以下字段对齐 StoryboardFrame，由后续步骤填充
            "image_path": None,
            "audio_path": None,
            "video_segment_path": None,
            "duration": 0.0,
        })

    sb_path = OUT / "storyboard.json"
    sb_path.write_text(json.dumps(storyboard, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[ex1] 主题: {TOPIC}")
    print(f"[ex1] 分镜帧数: {len(storyboard['frames'])}")
    for fr in storyboard["frames"]:
        print(f"  帧{fr['index']}: {fr['narration']}")

    # 验证：JSON 可解析、帧数 >= 3、每帧两个字段非空
    data = json.loads(sb_path.read_text(encoding="utf-8"))
    assert len(data["frames"]) >= 3
    assert all(fr["narration"] and fr["image_prompt"] for fr in data["frames"])
    print(f"[ex1] PASS -> {sb_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
