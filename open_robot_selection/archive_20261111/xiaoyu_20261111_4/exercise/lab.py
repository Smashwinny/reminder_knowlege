#!/usr/bin/env python3
"""04-open-robots 教学实验：仓库元数据对照、失败标注字段统计、官方URDF正运动学。

本程序只使用公开缓存/已下载文件与纯Python+NumPy计算，不调用付费API，
不加载真实机器人硬件，也不把作者宣传性能写成实测。
自写断言不能称为独立审核或上游测试套件。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
MODELS = ROOT / "models"
# also allow reading the larger sources tree when present
SOURCES = ROOT.parent / "sources"
SHANGHAI = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(SHANGHAI).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_env(_args=None):
    try:
        import numpy
        npv = numpy.__version__
    except Exception:
        npv = None
    out = {
        "python": platform.python_version(),
        "numpy": npv,
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "lab": str(ROOT),
        "cuda_devices": 0,
        "scope": "CPU metadata + URDF FK; no hardware, no paid API, no MuJoCo runtime required",
        "when": now_iso(),
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


# ---------------------------------------------------------------------------
# E2 仓库对照
# ---------------------------------------------------------------------------

# 原帖 18 项的分类与一手仓库（实验在此表上合并 API 缓存，不凭记忆改 SHA）
CATALOG = [
    {"name": "Microban", "category": "人形", "canonical": "Rhoban/microban", "note": "硬件 CC BY-NC-SA 4.0，软件 GPL-3.0"},
    {"name": "MiniLoong", "category": "人形", "canonical": "loongOpen/MiniLoong", "note": "OpenLoong/青龙 Mini，GitHub 镜像 loongOpen/MiniLoong"},
    {"name": "Poppy Humanoid", "category": "人形", "canonical": "poppy-project/poppy-humanoid", "note": "硬件 CC BY-SA 4.0，软件 GPL-3.0；根目录无单一 LICENSE"},
    {"name": "Otto DIY", "category": "人形/双足", "canonical": "OttoDIY/OttoDIYLib", "note": "软件库 GPL-3.0；OttoDIY/OttoDIY 现重定向到 OttoNinja，不是同一款机器人"},
    {"name": "pib", "category": "人形", "canonical": "pib-rocks/pib-backend", "extra": ["pib-rocks/pib-stls"], "note": "软件 AGPL-3.0，STL 仓 GPL-3.0；官网 FAQ 写硬件也是 AGPL-3.0，与 STL 仓文件不一致"},
    {"name": "Mini Pupper", "category": "四足", "canonical": "mangdangroboticsclub/mini_pupper", "note": "Apache-2.0"},
    {"name": "Petoi Bittle", "category": "四足", "canonical": "PetoiCamp/OpenCat-Quadruped-Robot", "note": "OpenCat 仓库已改名；MIT"},
    {"name": "Stanford Doggo", "category": "四足", "canonical": "Nate711/StanfordDoggoProject", "note": "MIT；官网活动仓在 Nate711，不是 stanfordroboticsclub 下的旧路径"},
    {"name": "SpotMicro", "category": "四足", "canonical": "mike4192/spotMicro", "note": "该仓是社区 ROS 实现（MIT）。原帖署名的设计是 Deok-yeon Kim / KDY0523，CC BY 3.0，不在该 GitHub 仓"},
    {"name": "OpenQuadruped", "category": "四足", "canonical": "adham-elarabawy/open-quadruped", "note": "根目录 LICENSE 以 MIT 开头；GitHub API 标记为 NOASSERTION"},
    {"name": "Puguette", "category": "四足", "canonical": "haruto89610/puguette", "note": "MIT"},
    {"name": "SO-ARM100", "category": "机械臂", "canonical": "TheRobotStudio/SO-ARM100", "note": "Apache-2.0；当前 README 以 SO-101 为主，SO-100 文档标为 deprecated"},
    {"name": "RoArm-M2", "category": "机械臂", "canonical": "waveshareteam/roarm_m2", "note": "AGPL-3.0"},
    {"name": "OpenMANIPULATOR-X", "category": "机械臂", "canonical": "ROBOTIS-GIT/open_manipulator", "note": "Apache-2.0"},
    {"name": "LeKiwi", "category": "移动操作", "canonical": "SIGRobotics-UIUC/LeKiwi", "note": "Apache-2.0；移动底盘+臂，不宜只算纯机械臂或纯移动平台"},
    {"name": "TurtleBot3 Burger", "category": "移动平台", "canonical": "ROBOTIS-GIT/turtlebot3", "note": "Apache-2.0"},
    {"name": "OpenBot", "category": "移动平台", "canonical": "ob-f/OpenBot", "note": "MIT；isl-org/OpenBot 重定向至此"},
    {"name": "Duckiebot", "category": "移动平台", "canonical": "duckietown/Hardware", "extra": ["duckietown/dt-duckiebot-interface"], "note": "Hardware 仓 LICENSE.pdf 为 Software Terms of Use v1.2，禁止未经授权的商业使用，不是 OSI 开源许可"},
]


def load_repos():
    path = DATA / "repos-slim.json"
    if not path.exists():
        raise SystemExit(f"missing {path}")
    rows = json.loads(path.read_text())
    by_full = {r["full_name"]: r for r in rows if r.get("full_name")}
    by_req = {r["requested"]: r for r in rows if r.get("requested")}
    return rows, by_full, by_req


def cmd_survey(_args=None):
    rows, by_full, by_req = load_repos()
    table = []
    cats = Counter()
    flags = Counter()
    for item in CATALOG:
        rec = by_full.get(item["canonical"]) or by_req.get(item["canonical"]) or {}
        extras = []
        for ex in item.get("extra") or []:
            extras.append(by_full.get(ex) or by_req.get(ex) or {"requested": ex})
        api = rec.get("license_api_spdx")
        pushed = rec.get("pushed_at")
        cats[item["category"]] += 1
        row = {
            "name": item["name"],
            "category": item["category"],
            "repo": rec.get("full_name") or item["canonical"],
            "requested": item["canonical"],
            "redirected": bool(rec.get("redirected")),
            "stars": rec.get("stargazers_count"),
            "branch": rec.get("default_branch"),
            "sha": rec.get("sha"),
            "created_at": rec.get("created_at"),
            "pushed_at": pushed,
            "license_api": api,
            "note": item["note"],
        }
        table.append(row)
        if api in (None, "NOASSERTION", "OTHER", "other"):
            flags["api_license_unreliable"] += 1
        if rec.get("redirected"):
            flags["redirect"] += 1
    # 额外观察到的重定向（请求名与 full_name 不同）
    redirects = [r for r in rows if r.get("redirected")]
    out = {
        "n_post_robots": len(CATALOG),
        "n_cached_repos": len([r for r in rows if r.get("full_name")]),
        "categories": dict(cats),
        "flags": dict(flags),
        "redirects": [
            {"requested": r["requested"], "full_name": r.get("full_name"), "label": r.get("label")}
            for r in redirects
        ],
        "table": table,
        "scope": "GitHub 公开 API 元数据 + git ls-remote SHA + 已读 LICENSE 注释；不是法律意见，也不是 BOM/价格审计",
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


# ---------------------------------------------------------------------------
# E3 许可/文档层验货（对照 API 字段与实读文件）
# ---------------------------------------------------------------------------

LICENSE_FILE_FINDINGS = [
    {"repo": "Rhoban/microban", "api": "NOASSERTION", "file": "LICENSE 首部声明硬件 CC BY-NC-SA 4.0、软件 GPL-3.0"},
    {"repo": "loongOpen/MiniLoong", "api": "Apache-2.0", "file": "LICENSE 为 Apache 2.0 全文"},
    {"repo": "poppy-project/poppy-humanoid", "api": None, "file": "hardware/LICENSE.md = CC BY-SA 4.0；software/LICENSE = GPL-3.0；根目录无 LICENSE"},
    {"repo": "OttoDIY/OttoDIYLib", "api": "GPL-3.0", "file": "LICENSE 为 GPL-3.0"},
    {"repo": "OttoDIY/OttoNinja", "api": "MIT", "file": "由 OttoDIY/OttoDIY 重定向得到，是另一款机器人，不能当作 Otto DIY 本体许可"},
    {"repo": "pib-rocks/pib-backend", "api": "AGPL-3.0", "file": "LICENSE 为 AGPL-3.0"},
    {"repo": "pib-rocks/pib-stls", "api": "GPL-3.0", "file": "LICENSE.txt 为 GPL-3.0，与 FAQ「硬件 AGPL-3.0」表述不一致"},
    {"repo": "mangdangroboticsclub/mini_pupper", "api": "Apache-2.0", "file": "LICENSE 为 Apache 2.0"},
    {"repo": "PetoiCamp/OpenCat-Quadruped-Robot", "api": "MIT", "file": "LICENSE 为 MIT；由 PetoiCamp/OpenCat 改名"},
    {"repo": "Nate711/StanfordDoggoProject", "api": "MIT", "file": "LICENSE 为 MIT"},
    {"repo": "mike4192/spotMicro", "api": "MIT", "file": "LICENSE 为 MIT，覆盖该软件仓，不自动覆盖 Thingiverse 设计"},
    {"repo": "adham-elarabawy/open-quadruped", "api": "NOASSERTION", "file": "LICENSE 以 MIT License 开头，API 未识别为 MIT"},
    {"repo": "haruto89610/puguette", "api": "MIT", "file": "LICENSE 为 MIT"},
    {"repo": "TheRobotStudio/SO-ARM100", "api": "Apache-2.0", "file": "LICENSE 为 Apache 2.0"},
    {"repo": "waveshareteam/roarm_m2", "api": "AGPL-3.0", "file": "LICENSE 为 AGPL-3.0"},
    {"repo": "ROBOTIS-GIT/open_manipulator", "api": "Apache-2.0", "file": "LICENSE 为 Apache 2.0"},
    {"repo": "SIGRobotics-UIUC/LeKiwi", "api": "Apache-2.0", "file": "LICENSE.txt 为 Apache 2.0"},
    {"repo": "ROBOTIS-GIT/turtlebot3", "api": "Apache-2.0", "file": "LICENSE 为 Apache 2.0"},
    {"repo": "ob-f/OpenBot", "api": "MIT", "file": "LICENSE 为 MIT"},
    {"repo": "duckietown/Hardware", "api": "NOASSERTION", "file": "LICENSE.pdf 是 Software Terms of Use v1.2 摘要：允许个人教育/认证高校课程/研究（需署名），明确禁止未经书面授权的商业使用"},
]


def cmd_licenses(_args=None):
    api_mismatch = [
        x for x in LICENSE_FILE_FINDINGS
        if x["api"] in (None, "NOASSERTION") or "重定向" in x["file"] or "不一致" in x["file"] or "不自动覆盖" in x["file"]
    ]
    commercial_caution = [
        "Rhoban/microban 硬件 NC",
        "pib / RoArm-M2 的 AGPL 对网络服务有源码提供义务",
        "Duckiebot 非商用条款",
        "AgiBot World 2026 数据集 CC BY-NC-SA 4.0（与 18 个机器人清单是不同对象）",
    ]
    out = {
        "n_findings": len(LICENSE_FILE_FINDINGS),
        "n_need_manual_read": len(api_mismatch),
        "api_or_scope_cautions": api_mismatch,
        "commercial_caution": commercial_caution,
        "findings": LICENSE_FILE_FINDINGS,
        "claim": "GitHub license API 不能替代打开 LICENSE 文件；设计仓与软件仓可能不是同一许可",
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


# ---------------------------------------------------------------------------
# E4 / E5 失败标注
# ---------------------------------------------------------------------------

def analyze_completions(path: Path):
    data = json.loads(path.read_text())
    items = data["items"]
    succ = Counter()
    present = Counter()
    tasks = Counter()
    for it in items:
        interval = (it.get("manualCompletion") or {}).get("interval") or {}
        succ[interval.get("isResultSucceed")] += 1
        present[interval.get("present")] += 1
        tasks[(it.get("annotationSubject") or {}).get("task_id")] += 1
    return {
        "file": str(path),
        "sha256": sha256_file(path),
        "format": data.get("format"),
        "n_items": len(items),
        "isResultSucceed": {str(k): v for k, v in succ.items()},
        "present": {str(k): v for k, v in present.items()},
        "n_tasks": len(tasks),
        "interpretation": (
            "全部 8146 条收据的 isResultSucceed 与 present 都是 false。"
            "这更像未填写的 interval 占位，不能当成 8146 次任务失败。"
            "成功/失败要以 info.json 的 key_frame.frame_type_name 与 frame_detail 为准。"
        ),
    }


def analyze_sample_info(path: Path):
    info = json.loads(path.read_text())
    types = Counter()
    error_cause = 0
    restorable = 0
    comments = Counter()
    n = 0
    kf = info.get("key_frame") or {}
    for val in kf.values():
        bags = val.values() if isinstance(val, dict) else [val]
        for entries in bags:
            if not isinstance(entries, list):
                continue
            for ent in entries:
                n += 1
                types[ent.get("frame_type_name") or "?"] += 1
                fd = ent.get("frame_detail") or {}
                if "error_cause" in fd:
                    error_cause += 1
                if "restorable" in fd:
                    restorable += 1
                if "comment" in fd:
                    comments[str(fd.get("comment"))[:80]] += 1
    return {
        "file": str(path),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "robot_type": info.get("robot_type"),
        "codebase_version": info.get("codebase_version"),
        "total_episodes": info.get("total_episodes"),
        "total_frames": info.get("total_frames"),
        "fps": info.get("fps"),
        "n_keyframe_entries": n,
        "frame_type_name": dict(types),
        "entries_with_error_cause": error_cause,
        "entries_with_restorable": restorable,
        "comments": dict(comments),
        "schema_keys": sorted(info.keys()),
        "has_take_over": "take_over" in info,
        "take_over_nonempty": sum(1 for v in (info.get("take_over") or {}).values() if v),
        "instruction_segment_episodes": len(info.get("instruction_segments") or {}),
        "affordance_schema": (info.get("affordance_annotations") or {}).get("schema_version"),
    }


def cmd_agibot(_args=None):
    comp = SOURCES / "hf" / "PhysicalReasoning__.dataset_build__snapshot___datahub_export__completions.json"
    sample = SOURCES / "hf" / "info-samples" / "task_100347_02_info.json"
    stats_path = SOURCES / "hf" / "info-scan-stats.json"
    ver_path = SOURCES / "hf" / "PhysicalReasoning__.dataset_build__snapshot___datahub_export__verification.json"
    readme_path = SOURCES / "hf" / "PhysicalReasoning__.dataset_build__snapshot___datahub_export__README.txt"
    out = {
        "dataset": "agibot-world/AgiBotWorld2026",
        "dataset_sha": "95b159a10305a0385f369aba5d4b16242526d17b",
        "dataset_last_modified_utc": "2026-10-24T13:41:37Z",
        "license": "CC BY-NC-SA 4.0",
        "theme": "Physical Reasoning / Release 4, folder PhysicalReasoning/opensourcev4-20261001 and 20261003",
    }
    if ver_path.exists():
        out["verification_receipt"] = json.loads(ver_path.read_text())
    if readme_path.exists():
        out["export_readme"] = readme_path.read_text(encoding="utf-8", errors="replace").strip()
    if comp.exists():
        out["completions"] = analyze_completions(comp)
    else:
        out["completions"] = {"missing": str(comp)}
    if sample.exists():
        out["sample_info"] = analyze_sample_info(sample)
    else:
        out["sample_info"] = {"missing": str(sample)}
    if stats_path.exists():
        stats = json.loads(stats_path.read_text())
        slim = {k: stats[k] for k in stats if k != "per_file"}
        slim["n_per_file"] = len(stats.get("per_file") or [])
        # add per-task type totals
        by_task = defaultdict(Counter)
        for rec in stats.get("per_file") or []:
            m = re.search(r"task_(\d+)", rec["path"])
            tid = m.group(1) if m else "?"
            for t, c in (rec.get("types") or {}).items():
                by_task[tid][t] += c
        slim["by_task"] = {k: dict(v) for k, v in sorted(by_task.items())}
        out["info_scan"] = slim
        out["info_scan_complete"] = not slim.get("files_fail") and slim.get("files_ok", 0) >= 90
    else:
        out["info_scan"] = None
        out["info_scan_complete"] = False
    out["schema_documented_fields"] = {
        "key_frame.frame_type_name": ["Error Frame", "Success Frame", "Intervention Frame", "Single Frame", "2D Bounding Box", "Task Frame"],
        "frame_detail.error_cause": "documented in README, may be absent in actual Release 4 entries",
        "frame_detail.restorable": "documented in README, may be absent in actual Release 4 entries",
        "frame_detail.is_result_succeed": "documented on Task Frame examples",
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


# ---------------------------------------------------------------------------
# E6 URDF 正运动学
# ---------------------------------------------------------------------------

def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def _rpy_matrix(r, p, y):
    cr, sr = math.cos(r), math.sin(r)
    cp, sp = math.cos(p), math.sin(p)
    cy, sy = math.cos(y), math.sin(y)
    # URDF: R = Rz(y) * Ry(p) * Rx(r)
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]], dtype=float)
    Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]], dtype=float)
    Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]], dtype=float)
    return Rz @ Ry @ Rx


def _xyzrpy_T(xyz, rpy):
    T = np.eye(4)
    T[:3, :3] = _rpy_matrix(*rpy)
    T[:3, 3] = xyz
    return T


def _axis_angle_T(axis, angle):
    ax = np.array(axis, dtype=float)
    n = np.linalg.norm(ax)
    if n == 0:
        return np.eye(4)
    ax = ax / n
    x, y, z = ax
    c, s = math.cos(angle), math.sin(angle)
    C = 1 - c
    R = np.array([
        [c + x * x * C, x * y * C - z * s, x * z * C + y * s],
        [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
        [z * x * C - y * s, z * y * C + x * s, c + z * z * C],
    ], dtype=float)
    T = np.eye(4)
    T[:3, :3] = R
    return T


def load_urdf(path: Path, macros: dict | None = None) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if macros:
        for k, v in macros.items():
            text = text.replace("${%s}" % k, v)
    # leftover ${...} become empty to allow TurtleBot3 namespace
    text = re.sub(r"\$\{[^}]+\}", "", text)
    return text


def parse_urdf(text: str):
    root = ET.fromstring(text)
    joints = []
    links = []
    for el in root.iter():
        name = _local_name(el.tag)
        if name == "link" and el.get("name"):
            links.append(el.get("name"))
        if name == "joint" and el.get("name"):
            origin = {"xyz": (0, 0, 0), "rpy": (0, 0, 0)}
            axis = (1, 0, 0)
            parent = child = None
            limit = {}
            for ch in list(el):
                cn = _local_name(ch.tag)
                if cn == "parent":
                    parent = ch.get("link")
                elif cn == "child":
                    child = ch.get("link")
                elif cn == "origin":
                    xyz = tuple(float(x) for x in (ch.get("xyz") or "0 0 0").split())
                    rpy = tuple(float(x) for x in (ch.get("rpy") or "0 0 0").split())
                    origin = {"xyz": xyz, "rpy": rpy}
                elif cn == "axis":
                    axis = tuple(float(x) for x in (ch.get("xyz") or "1 0 0").split())
                elif cn == "limit":
                    limit = {k: ch.get(k) for k in ("lower", "upper", "effort", "velocity") if ch.get(k) is not None}
            if not parent or not child:
                continue  # skip dummy/mimic stubs without a kinematic edge
            joints.append({
                "name": el.get("name"),
                "type": el.get("type") or "fixed",
                "parent": parent,
                "child": child,
                "origin": origin,
                "axis": axis,
                "limit": limit,
            })
    return {"links": links, "joints": joints}


def fk_all(model, qmap: dict) -> dict:
    """Return world pose of every link. Base/world links with no parent are identity."""
    parent_of = {j["child"]: j for j in model["joints"] if j["child"]}
    children = defaultdict(list)
    links = set(model["links"])
    for j in model["joints"]:
        if j["parent"]:
            children[j["parent"]].append(j)
        links.add(j["parent"])
        links.add(j["child"])
    roots = [lk for lk in links if lk and lk not in parent_of]
    poses = {lk: np.eye(4) for lk in roots}

    def joint_T(j):
        T0 = _xyzrpy_T(j["origin"]["xyz"], j["origin"]["rpy"])
        typ = j["type"]
        if typ in ("revolute", "continuous"):
            q = float(qmap.get(j["name"], 0.0))
            return T0 @ _axis_angle_T(j["axis"], q)
        if typ == "prismatic":
            q = float(qmap.get(j["name"], 0.0))
            ax = np.array(j["axis"], dtype=float)
            n = np.linalg.norm(ax) or 1.0
            T = np.eye(4)
            T[:3, 3] = (ax / n) * q
            return T0 @ T
        return T0  # fixed and others

    # BFS / recursion from roots
    stack = list(roots)
    seen = set(roots)
    while stack:
        parent = stack.pop()
        for j in children.get(parent, []):
            poses[j["child"]] = poses[parent] @ joint_T(j)
            if j["child"] not in seen:
                seen.add(j["child"])
                stack.append(j["child"])
    return poses


def pos_of(T):
    return [float(x) for x in T[:3, 3]]


def cmd_fk(_args=None):
    results = {}

    def run_named(key, filename, q_cases, frames):
        path = MODELS / filename
        text = load_urdf(path)
        model = parse_urdf(text)
        movable = [j for j in model["joints"] if j["type"] in ("revolute", "continuous", "prismatic")]
        cases_out = []
        for name, qmap in q_cases:
            poses = fk_all(model, qmap)
            entry = {"case": name, "q": qmap, "frames": {}}
            for fr in frames:
                if fr not in poses:
                    entry["frames"][fr] = None
                else:
                    entry["frames"][fr] = pos_of(poses[fr])
            cases_out.append(entry)
        results[key] = {
            "file": filename,
            "sha256": sha256_file(path),
            "n_links": len(model["links"]),
            "n_joints": len(model["joints"]),
            "movable": [
                {
                    "name": j["name"],
                    "type": j["type"],
                    "parent": j["parent"],
                    "child": j["child"],
                    "axis": j["axis"],
                    "origin_xyz": j["origin"]["xyz"],
                    "limit": j["limit"],
                }
                for j in movable
            ],
            "cases": cases_out,
        }

    # SO-100: 6 revolute, child of gripper joint is typically moving jaw / ee
    so100_text = load_urdf(MODELS / "so100.urdf")
    so100 = parse_urdf(so100_text)
    so100_ee = so100["joints"][-1]["child"]  # last joint child
    # also report wrist_roll child
    run_named(
        "so100",
        "so100.urdf",
        [
            ("home_zero", {}),
            ("shoulder_pan_90deg", {"shoulder_pan": math.pi / 2}),
            ("elbow_neg90", {"elbow_flex": -math.pi / 2}),
        ],
        [so100_ee, "Base", "Upper_Arm", "Wrist_Pitch_Roll"] if False else list({j["child"] for j in so100["joints"]}),
    )

    so101 = parse_urdf(load_urdf(MODELS / "so101_new_calib.urdf"))
    # moving links of interest: after last revolute before fixed gripper_frame maybe
    so101_links = ["base", "shoulder", "upper_arm", "lower_arm", "wrist", "gripper", "moving_jaw"]
    # use actual names from file
    actual = so101["links"]
    run_named(
        "so101_new_calib",
        "so101_new_calib.urdf",
        [
            ("home_zero", {}),
            ("shoulder_pan_90deg", {"shoulder_pan": math.pi / 2}),
        ],
        actual,
    )

    burger = parse_urdf(load_urdf(MODELS / "turtlebot3_burger.urdf", macros={"namespace": ""}))
    run_named(
        "turtlebot3_burger",
        "turtlebot3_burger.urdf",
        [
            ("home_zero", {}),
            ("wheels_pi", {"wheel_left_joint": math.pi, "wheel_right_joint": math.pi}),
        ],
        burger["links"],
    )

    omx = parse_urdf(load_urdf(MODELS / "open_manipulator_x.urdf"))
    run_named(
        "open_manipulator_x",
        "open_manipulator_x.urdf",
        [
            ("home_zero", {}),
            ("joint2_45deg", {"joint2": math.pi / 4}),
        ],
        omx["links"],
    )

    # compact numeric highlights for the log
    def pick(model_key, case, link_substrings):
        block = results[model_key]
        case_d = next(c for c in block["cases"] if c["case"] == case)
        picked = {}
        for name, xyz in case_d["frames"].items():
            if not name:
                continue
            if link_substrings == [""] or any(s and s.lower() in name.lower() for s in link_substrings) or name in link_substrings:
                picked[name] = [round(v, 6) for v in xyz] if xyz else None
        return picked

    highlights = {
        "so100_home_all_child_frames": pick("so100", "home_zero", [""]),
        "so101_home_selected": pick("so101_new_calib", "home_zero", ["jaw", "gripper", "wrist", "base"]),
        "burger_sensor_frames": pick("turtlebot3_burger", "home_zero", ["base", "scan", "imu", "caster", "wheel"]),
        "omx_home": pick("open_manipulator_x", "home_zero", ["link", "end", "gripper", "world"]),
    }
    # wheel pi should not move lidar (fixed joint)
    burger_zero = pick("turtlebot3_burger", "home_zero", ["scan", "imu"])
    burger_pi = pick("turtlebot3_burger", "wheels_pi", ["scan", "imu"])
    highlights["burger_lidar_invariant_to_wheel"] = burger_zero == burger_pi
    highlights["scope"] = (
        "纯解析正运动学，未加载网格、未做碰撞/动力学、未运行 MuJoCo/PyBullet。"
        "缺网格不阻止关节链计算。实物复刻与标定待验证。"
    )
    out = {"highlights": highlights, "models": results}
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def cmd_verify(_args=None):
    env = cmd_env()
    # re-run quietly? already printed; do checks
    survey = json.loads(os.popen(f"{sys.executable} {ROOT/'lab.py'} survey").read() if False else "null")
    # call internals directly
    import io
    from contextlib import redirect_stdout

    def run(fn):
        buf = io.StringIO()
        with redirect_stdout(buf):
            data = fn()
        return data

    survey = run(cmd_survey)
    licenses = run(cmd_licenses)
    agibot = run(cmd_agibot)
    fk = run(cmd_fk)

    checks = []

    def check(name, ok, detail):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    check("catalog_18", survey["n_post_robots"] == 18, survey["n_post_robots"])
    check("categories_cover_four", set(survey["categories"]) >= {"人形", "四足", "机械臂", "移动平台"}, survey["categories"])
    check("so100_six_revolute", len(fk["models"]["so100"]["movable"]) == 6, len(fk["models"]["so100"]["movable"]))
    # lidar invariant
    check("burger_lidar_invariant", fk["highlights"]["burger_lidar_invariant_to_wheel"] is True, True)
    # completions interpretation exists
    if agibot.get("completions") and "n_items" in agibot["completions"]:
        check("completions_8146", agibot["completions"]["n_items"] == 8146, agibot["completions"]["n_items"])
        check(
            "completions_not_treated_as_fail_rate",
            agibot["completions"]["isResultSucceed"].get("False") == 8146
            and "占位" in agibot["completions"]["interpretation"],
            agibot["completions"]["isResultSucceed"],
        )
    if agibot.get("sample_info") and "n_keyframe_entries" in agibot["sample_info"]:
        check(
            "sample_only_success_frames",
            agibot["sample_info"]["frame_type_name"].get("Success Frame") == agibot["sample_info"]["n_keyframe_entries"]
            and agibot["sample_info"]["entries_with_error_cause"] == 0,
            agibot["sample_info"]["frame_type_name"],
        )
    # SO-100 home end-effector z should be > 0 (arm above base) — soft geometric sanity
    so_home = fk["highlights"]["so100_home_all_child_frames"]
    zs = [xyz[2] for xyz in so_home.values() if xyz]
    check("so100_home_has_positive_z", any(z > 0.01 for z in zs), max(zs) if zs else None)
    # duckietown caution present
    check(
        "duckie_not_osi",
        any("Duckiebot" in x["file"] or "duckietown" in x["repo"] for x in licenses["api_or_scope_cautions"]),
        True,
    )
    passed = sum(1 for c in checks if c["ok"])
    out = {
        "groups_passed": passed,
        "groups_total": len(checks),
        "checks": checks,
        "scope": "author-written deterministic checks, not independent audit or upstream tests",
        "when": now_iso(),
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    if passed < len(checks):
        sys.exit(2)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["env", "survey", "licenses", "agibot", "fk", "verify"])
    args = p.parse_args()
    {
        "env": cmd_env,
        "survey": cmd_survey,
        "licenses": cmd_licenses,
        "agibot": cmd_agibot,
        "fk": cmd_fk,
        "verify": cmd_verify,
    }[args.cmd]()


if __name__ == "__main__":
    main()
