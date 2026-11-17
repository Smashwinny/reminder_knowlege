#!/usr/bin/env python3
"""Read-only static indicators for defensive review. Never imports or runs upstream code."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

RULES = {
    "camera_capture": {
        "pattern": r"getUserMedia\(constraints\)|facingMode|toDataURL\(\"image/png\"\)",
        "why": "摄像头帧采集与图像编码指示器；授权后应审计目的、频率和去向。",
    },
    "microphone_capture": {
        "pattern": r"audio:\s*true|exportWAV|audio_data",
        "why": "麦克风录制与音频上传指示器；应检查持续时间和停止轨道。",
    },
    "geolocation": {
        "pattern": r"navigator\.geolocation|getCurrentPosition|coords\.latitude|coords\.longitude",
        "why": "精确位置 API 指示器；拒绝、超时也可能被回传，需按敏感事件处理。",
    },
    "device_fingerprint": {
        "pattern": r"ClientJS|getCurrentResolution|hardwareConcurrency|getTimeZone|getLanguage",
        "why": "无需弹窗也可能暴露的设备指纹面；不等于能绕过摄像头/定位权限。",
    },
    "third_party_ip_lookup": {
        "pattern": r"api\.ipify\.org",
        "why": "页面向第三方发起公网 IP 查询，产生额外数据接收方和日志。",
    },
    "periodic_upload": {
        "pattern": r"setInterval|setTimeout\(startRecording|XMLHttpRequest|\$\.ajax|move_uploaded_file",
        "why": "周期性处理与回传指示器；检测时关注重复连接、上传体量和后台行为。",
    },
    "weak_default_credential": {
        "pattern": r"[\"']password[\"']\s*=>\s*[\"']admin[\"']",
        "why": "默认管理凭据指示器；任何自有测试服务都不应暴露到网络。",
    },
}


def iter_source_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".js", ".html", ".php", ".py", ".md"}:
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    if not root.is_dir():
        raise SystemExit(f"repository not found: {root}")

    commit = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True, encoding="utf-8",
    ).stdout.strip()
    findings = {name: [] for name in RULES}
    scanned = 0
    for path in iter_source_files(root):
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        relative = path.relative_to(root).as_posix()
        for name, rule in RULES.items():
            regex = re.compile(rule["pattern"], re.IGNORECASE)
            for number, line in enumerate(lines, 1):
                if regex.search(line):
                    findings[name].append({
                        "file": relative,
                        "line": number,
                        "excerpt": line.strip()[:220],
                    })

    missing = [name for name, items in findings.items() if not items]
    result = {
        "schema": "storm-breaker-static-defense-audit-v1",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mode": "read-only static source inspection; upstream code not executed",
        "repository": "https://github.com/ultrasecurity/Storm-Breaker",
        "commit": commit,
        "files_scanned": scanned,
        "summary": {name: len(items) for name, items in findings.items()},
        "explanations": {name: rule["why"] for name, rule in RULES.items()},
        "findings": findings,
        "missing_expected_categories": missing,
        "safety": {
            "network_requests": 0,
            "upstream_code_executed": False,
            "sensor_access": False,
            "third_party_targets": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"STATIC_AUDIT commit={commit} files={scanned}")
    for name, items in findings.items():
        print(f"{name}={len(items)}")
    print(f"missing_expected_categories={len(missing)}")
    print(f"output={args.output.resolve()}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
