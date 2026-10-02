#!/usr/bin/env python3
"""publish_lite.py — Windows 版 Godogen 发布器（复现 repo/publish.sh 的核心逻辑）。

publish.sh 依赖 rsync（Windows Git Bash 默认没有），本脚本用 shutil.copytree
等价复现它的发布流程，验证 Godogen "thin runtime" 发布模型：

    godogen 源仓库 --publish--> 游戏仓库骨架（manifest + 引擎指南 + asset-gen skill）

用法:
    python publish_lite.py --engine godot --agent claude --out my-game
    python publish_lite.py --engine babylon --agent codex --out my-game-codex
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent / "repo"          # godogen 源仓库
RENDER = REPO / "scripts" / "render_dir.py"

ENGINES = {"godot": "Godot", "bevy": "Bevy", "babylon": "Babylon.js"}

# 与 publish.sh 保持一致的渲染时变量
def runtime_asset_dir(engine: str) -> str:
    return "src/assets" if engine == "babylon" else "assets"


def publish(engine: str, agent: str, out: Path) -> None:
    engine_display = ENGINES[engine]
    if agent == "claude":
        manifest, skills_rel, cmd = "CLAUDE.md", ".claude/skills", "/asset-gen"
    else:
        manifest, skills_rel, cmd = "AGENTS.md", ".agents/skills", "$asset-gen"
    guide = f"{engine}.md"

    out.mkdir(parents=True, exist_ok=True)

    # --- 1. asset-gen skill：整目录复制（publish.sh 用 rsync，这里用 copytree）---
    skill_src = REPO / "asset-gen"
    skill_dst = out / skills_rel / "asset-gen"
    if skill_dst.exists():
        shutil.rmtree(skill_dst)
    shutil.copytree(skill_src, skill_dst,
                    ignore=shutil.ignore_patterns("__pycache__"))

    # --- 2. 变量渲染：${AGENT_NAME} 等占位符替换（调用上游 render_dir.py）---
    subs = [f"AGENT_NAME=Claude" if agent == "claude" else "AGENT_NAME=Codex",
            f"ASSET_GEN_SKILL_DIR={skills_rel}/asset-gen",
            f"ASSET_SKILL_COMMAND={cmd}",
            f"RUNTIME_ASSET_DIR={runtime_asset_dir(engine)}"]
    subprocess.run([sys.executable, str(RENDER), str(skill_dst), *subs], check=True)

    # --- 3. manifest：prompts/runtime.md 渲染成 CLAUDE.md / AGENTS.md ---
    manifest_text = (REPO / "prompts" / "runtime.md").read_text(encoding="utf-8")
    for k, v in {"ENGINE_NAME": engine_display, "ENGINE_GUIDE_FILE": guide,
                 "ASSET_SKILL_COMMAND": cmd}.items():
        manifest_text = manifest_text.replace("${%s}" % k, v)
    (out / manifest).write_text(manifest_text, encoding="utf-8")

    # --- 4. 引擎指南（原样复制）---
    shutil.copyfile(REPO / "engines" / f"{engine}.md", out / guide)

    # --- 5. .gitignore ---
    gi = [".claude\nCLAUDE.md\n" if agent == "claude" else ".agents\nAGENTS.md\n.codex\n",
          guide + "\n", "/tripo-out\n"]
    gi += {"godot": "assets\nscreenshots\n.godot\n*.import\nbin/\nobj/\n",
           "bevy": "/target\n/screenshots\n",
           "babylon": "/node_modules\n/dist\n/screenshots\n"}[engine]
    (out / ".gitignore").write_text("".join(gi), encoding="utf-8")

    print(f"published {engine}/{agent} -> {out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True, choices=ENGINES)
    ap.add_argument("--agent", required=True, choices=["claude", "codex"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    publish(args.engine, args.agent, Path(args.out))


if __name__ == "__main__":
    main()
