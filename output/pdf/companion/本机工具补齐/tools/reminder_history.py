"""Audit/repair legacy Markdown indexes without inventing completed work."""
import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SHANGHAI = timezone(timedelta(hours=8))


def completion_rows(text):
    rows = []
    for line in text.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) < 6:
            raise ValueError("纲要表格列不足，停止修复")
        # Three trailing columns are stable even when prose contains unescaped pipes.
        row = cells[:2] + [" | ".join(cells[2:-3]).replace("\\|", "|")] + cells[-3:]
        datetime.strptime(row[1], "%Y-%m-%d %H:%M")
        rows.append(row)
    return rows


def pdf_exists(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        return False
    with path.open("rb") as stream:
        return stream.read(5) == b"%PDF-"


def repair(snapshot, apply=False, coordinator=None):
    if apply:
        from reminder_coordinator import require_owner
        if not coordinator:
            raise ValueError("修复共享索引需要 --coordinator 和有效协调者租约")
        require_owner(ROOT, coordinator)
    outline = ROOT / "完成/00-纲要.md"
    queue = ROOT / "完成/学习队列.md"
    original_outline = outline.read_text(encoding="utf-8")
    original_queue = queue.read_text(encoding="utf-8")
    rows = completion_rows(original_outline)
    stats = {"legacy_completion_rows": len(rows), "duplicate_numbers": {
        number: count for number, count in Counter(row[0] for row in rows).items() if count > 1
    }, "out_of_order_pairs": sum(rows[i][1] < rows[i - 1][1] for i in range(1, len(rows)))}
    path_fixes = 0
    for row in rows:
        if row[4] == "codex-dual-home" and pdf_exists(row[5].replace("codex-dual-home/", "codex_dual_home/")):
            row[4] = "codex_dual_home"
            row[5] = row[5].replace("codex-dual-home/", "codex_dual_home/")
            path_fixes += 1
    stats["path_fixes"] = path_fixes
    stats["missing_or_invalid_pdfs"] = [row[5] for row in rows if not pdf_exists(row[5])]
    rows.sort(key=lambda row: row[1])
    formatted = ["| " + " | ".join([str(i), row[1], row[2].replace("|", "\\|"), *row[3:]]) + " |"
                 for i, row in enumerate(rows, 1)]
    lines = original_outline.splitlines()
    row_indices = [i for i, line in enumerate(lines) if re.match(r"^\|\s*\d+\s*\|", line)]
    if row_indices and any(lines[i].strip() for i in range(row_indices[0], row_indices[-1] + 1) if i not in row_indices):
        raise ValueError("纲要数据行之间含其他正文，停止自动修复")
    if row_indices:
        lines[row_indices[0]:row_indices[-1] + 1] = formatted
    new_outline = "\n".join(lines) + "\n"

    live = json.loads(Path(snapshot).read_text(encoding="utf-8"))
    if isinstance(live, dict):
        live = live["tasks"]
    by_id = {str(task["id"]): task for task in live if not task.get("deleted")}
    verified_sources = {row[3] for row in rows if pdf_exists(row[5])}
    qlines = original_queue.splitlines()
    counts = Counter()
    reconciled = []
    for i, line in enumerate(qlines):
        match = re.match(r"^\|\s*(待处理|进行中|已完成|跳过\(非学习\))\s*\|\s*([^|]+)\|", line)
        if not match:
            continue
        state, task_id = match[1], match[2].strip()
        task = by_id.get(task_id)
        if state in {"待处理", "进行中"} and task and task.get("state") == 3:
            if any(source and source in task.get("text", "") for source in verified_sources):
                qlines[i] = line.replace("| " + state + " |", "| 已完成 |", 1)
                if qlines[i] != line:
                    reconciled.append(task_id)
                    state = "已完成"
        counts[state] += 1
    header = (f"> 历史队列核对：已完成 {counts['已完成']} / 非学习 {counts['跳过(非学习)']} / "
              f"进行中待核查 {counts['进行中']} / 待处理 {counts['待处理']}；共 {sum(counts.values())} 条。"
              "新记录及实时状态见 [流水线纲要](流水线纲要.md)。")
    for i, line in enumerate(qlines):
        if line.startswith("> 进度：") or line.startswith("> 历史队列核对："):
            qlines[i] = header
        elif line.startswith("# 拾遗学习队列"):
            qlines[i] = "# 拾遗历史学习队列（保留原始人工分类）"
        elif line.startswith("> 调度规则："):
            qlines[i] = "> 新任务由 reminder_pipeline.py 领取；worker 提交独立产物，协调者维护共享索引。历史未核查项不自动标为完成。"
    new_queue = "\n".join(qlines) + "\n"
    stats["reconciled_task_ids"] = reconciled
    stats["legacy_queue_states"] = dict(counts)
    stats["site_states"] = dict(Counter(str(task.get("state")) for task in by_id.values()))
    stats["applied"] = apply
    if apply:
        stamp = datetime.now(SHANGHAI).strftime("%Y%m%dT%H%M%S%f")
        backup = ROOT / "完成/.pipeline/history" / stamp
        backup.mkdir(parents=True)
        for path in (outline, queue):
            shutil.copy2(path, backup / path.name)
        stats["backup"] = str(backup.relative_to(ROOT))
        stats["original_sha256"] = {outline.name: hashlib.sha256(original_outline.encode()).hexdigest(),
                                   queue.name: hashlib.sha256(original_queue.encode()).hexdigest()}
        if new_outline != original_outline:
            outline.write_text(new_outline, encoding="utf-8")
        if new_queue != original_queue:
            queue.write_text(new_queue, encoding="utf-8")
        (backup / "audit.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--apply", action="store_true", help="备份后修复；默认仅审计")
    parser.add_argument("--coordinator", help="修改共享索引时的全局协调者名称")
    args = parser.parse_args()
    print(json.dumps(repair(args.snapshot, args.apply, args.coordinator), ensure_ascii=False, indent=2))
