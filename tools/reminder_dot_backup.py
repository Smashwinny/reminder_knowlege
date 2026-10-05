"""Dot 报告的私有本机备份、恢复及受保护的共享队列导入。

默认复制并记录后续知识入库与 Git 交接，不删除云端内容，不安装 Windows 定时任务。
实际知识合并和 Git 使用 learn-project 第 8、9 步，由唯一协调者执行。
凭据只从既有 SHIYI_TOKEN/tools/.shiyi_token 读取，不接受命令行明文令牌。
"""
from __future__ import annotations

import argparse
import base64
import re
import contextlib
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request

if __package__:
    from .reminder_pipeline import ROOT, Pipeline, PipelineError, atomic_write, task_hash, valid_id, canonical_url
    from .reminder_dot_http import SITE, MAX_BUNDLE_BYTES, HTTP_USER_AGENT
else:
    from reminder_pipeline import ROOT, Pipeline, PipelineError, atomic_write, task_hash, valid_id, canonical_url
    from reminder_dot_http import SITE, MAX_BUNDLE_BYTES, HTTP_USER_AGENT

MAX_ARCHIVE_BYTES = 512 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_bundle(bundle, expected_account, expected_list):
    if not isinstance(bundle, dict) or bundle.get("schema") != "reminder-dot-export-v1":
        raise PipelineError("不是已支持的 Dot 报告导出格式。")
    if bundle.get("accountId") != expected_account or bundle.get("list", {}).get("id") != expected_list:
        raise PipelineError("账户或分析列表与明确配置不符，停止导入。")
    valid_id(expected_account)
    valid_id(expected_list)
    reports = bundle.get("reports")
    if not isinstance(reports, list):
        raise PipelineError("缺少报告清单。")
    ids = set()
    for report in reports:
        if not isinstance(report, dict):
            raise PipelineError("报告格式损坏。")
        report_id, task_id = valid_id(report.get("id", "")), valid_id(report.get("taskId", ""))
        if report_id in ids:
            raise PipelineError("导出中有重复报告 ID。")
        ids.add(report_id)
        if report.get("userId") != expected_account or report.get("listId") != expected_list:
            raise PipelineError("报告包含授权范围外的数据。")
        md = report.get("markdown")
        if not isinstance(md, str) or digest(md.encode("utf-8")) != report.get("markdownSha256"):
            raise PipelineError("报告校验失败，保留原件，不导入。")
        record = report.get("record")
        if not isinstance(record, dict) or record.get("id") != task_id or task_hash(record) != report.get("sourceHash"):
            raise PipelineError("报告与原记录的来源版本不符。")
        analysis = report.get("analysis")
        if not isinstance(analysis, dict) or analysis.get("kind") not in {"learning", "non_learning", "duplicate", "needs_review", "blocked", "non_link"}:
            raise PipelineError("报告缺少有效分类。")
        for key in ("title", "recordContent", "reason", "knownKnowledge", "nextStep", "uncertainties"):
            if not isinstance(analysis.get(key), str) or not analysis[key].strip():
                raise PipelineError("报告缺少来源判断、知识关联或下一步。")
        sources = analysis.get("sources")
        if not isinstance(sources, list) or (not sources and analysis["kind"] != "non_link"):
            raise PipelineError("报告缺少核对来源。")
        for source in sources:
            if not isinstance(source, dict) or not source.get("facts") or not source.get("status"):
                raise PipelineError("核对来源格式损坏。")
            canonical_url(source.get("url", ""))
        if analysis["kind"] == "non_link" and re.search(r"(?:https?://|www\.)[^\s<>]+", record.get("text", ""), re.I):
            raise PipelineError("含链接的记录不能导入非链接标签。")
        if analysis["kind"] not in {"needs_review", "blocked", "non_link"} and not any(s["status"] == "read" for s in sources):
            raise PipelineError("未读来源不能直接归入学习、重复或非学习。")
        if analysis.get("stage", "preliminary") not in {"preliminary", "full"}:
            raise PipelineError("分析阶段无效。")
        if analysis.get("stage") == "full":
            completion = analysis.get("completion", {})
            roles = {"guide_pdf", "guide_html", "exercise_archive", "experiment_log", "knowledge_notes", "review_log"}
            artifacts = completion.get("artifacts", [])
            if not isinstance(artifacts, list) or len(artifacts) != 6 or any(not isinstance(a, dict) for a in artifacts) or {a.get("role") for a in artifacts} != roles:
                raise PipelineError("完整学习缺少实际产物。")
            if not completion.get("reviewer") or completion.get("reviewer") == report.get("owner") or not all(completion.get(k) is True for k in ("pdfRendered", "experimentChecked", "knowledgeChecked")):
                raise PipelineError("完整学习缺少独立审核。")
            total_bytes = 0
            for artifact in artifacts:
                try:
                    data = base64.b64decode(artifact.get("base64", ""), validate=True)
                except (ValueError, TypeError):
                    raise PipelineError("学习产物编码损坏。") from None
                total_bytes += len(data)
                if len(data) < 20 or total_bytes > 1000000:
                    raise PipelineError("完整产物为空或超过网站上限。")
                if artifact['role'] == 'guide_pdf' and (not data.startswith(b'%PDF-') or b'%%EOF' not in data[-1024:]):
                    raise PipelineError("PDF 产物格式损坏。")
                if artifact['role'] == 'guide_html' and not re.search(rb'<(?:!doctype html|html)\b', data, re.I):
                    raise PipelineError("HTML 产物格式损坏。")
                if artifact['role'] == 'exercise_archive' and not data.startswith(b'PK\x03\x04'):
                    raise PipelineError("实验材料归档格式损坏。")
                if len(data) != artifact.get("bytes") or digest(data) != artifact.get("sha256"):
                    raise PipelineError("学习产物校验失败。")
        for attempt in report.get("learningAttempts", []):
            if not isinstance(attempt, dict) or any(attempt.get(k) != report.get(k) for k in ("userId", "listId", "taskId", "sourceHash")) or attempt.get('status') != 'blocked' or not isinstance(attempt.get('reason'), str):
                raise PipelineError("学习阻碍记录超出报告范围或格式无效。")
            valid_id(attempt.get('id', ''))
        if not isinstance(report.get("stale"), bool) or not isinstance(report.get("activeClaim"), bool):
            raise PipelineError("缺少导出时的来源新鲜度和领取状态。")
    return bundle


def read_bundle(file, expected_account, expected_list):
    raw = Path(file).read_bytes()
    if len(raw) > MAX_ARCHIVE_BYTES:
        raise PipelineError("恢复归档超过 512 MiB，停止导入。")
    try:
        bundle = json.loads(raw)
    except (ValueError, UnicodeError):
        raise PipelineError("导出文件损坏，未导入。") from None
    return raw, validate_bundle(bundle, expected_account, expected_list)


def download(expected_account, expected_list):
    if __package__:
        from .shiyi_sync import get_token
    else:
        from shiyi_sync import get_token
    token = get_token()
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl): return None
    reports, cursors, cursor, merged = [], set(), None, None
    for page in range(10000):
        request = urllib.request.Request(SITE + "/api/dot/export", data=json.dumps({"listId": expected_list, "limit": 5, "cursor": cursor}).encode("utf-8"), headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": HTTP_USER_AGENT}, method="POST")
        try:
            with urllib.request.build_opener(NoRedirect).open(request, timeout=45) as response:
                raw = response.read(MAX_BUNDLE_BYTES + 1)
        except urllib.error.HTTPError as error:
            raise PipelineError(f"网站导出失败 HTTP {error.code}；本地原状态保留。") from None
        except (OSError, TimeoutError):
            raise PipelineError("网站导出受网络或认证阻碍；未使用旧缓存。") from None
        if len(raw) > MAX_BUNDLE_BYTES: raise PipelineError("单页导出超过 32 MiB，未保存截断数据。")
        try: bundle = json.loads(raw)
        except (ValueError, UnicodeError): raise PipelineError("网站导出不是完整 JSON。") from None
        validate_bundle(bundle, expected_account, expected_list)
        if merged is None: merged = bundle.copy()
        elif bundle.get("totalReports") != merged.get("totalReports"):
            raise PipelineError("导出期间报告数量变化，请重新备份。")
        reports.extend(bundle["reports"])
        cursor = bundle.get("nextCursor")
        if not cursor:
            merged["reports"] = reports
            merged["nextCursor"] = None
            if merged.get("totalReports") is not None and len(reports) != merged["totalReports"]:
                raise PipelineError("网站导出分页不完整，停止备份。")
            validate_bundle(merged, expected_account, expected_list)
            return json.dumps(merged, ensure_ascii=False).encode("utf-8"), merged
        if cursor in cursors: raise PipelineError("网站分页游标重复，停止备份。")
        cursors.add(cursor)
    raise PipelineError("分页数量异常，停止备份。")


def restore(root, raw, bundle):
    folder = Path(root).resolve() / "完成/.pipeline/dot" / valid_id(bundle["accountId"]) / valid_id(bundle["list"]["id"])
    folder.mkdir(parents=True, exist_ok=True)
    lock = folder / ".restore.lock"
    try:
        handle = lock.open("x", encoding="utf-8")
    except FileExistsError:
        raise PipelineError("此列表正在备份/恢复，或上次恢复被中断；确认原执行者停止后再处理锁。") from None
    try:
        handle.write(datetime.now(timezone.utc).isoformat())
        handle.close()
        bundle_hash = digest(raw)
        archive = folder / "exports" / (bundle_hash + ".json")
        # Store original bytes exactly; reserialization must not invalidate the checksum.
        archive.parent.mkdir(parents=True, exist_ok=True)
        if archive.exists():
            if archive.read_bytes() != raw:
                raise PipelineError("同名本地备份内容冲突，未覆盖。")
        else:
            tmp = archive.with_suffix(".partial")
            with tmp.open("xb") as stream:
                stream.write(raw)
                stream.flush()
                import os
                os.fsync(stream.fileno())
            tmp.replace(archive)
        atomic_write(archive.with_suffix(".sha256"), bundle_hash + "\n")
        added = 0
        for report in bundle["reports"]:
            file = folder / "reports" / valid_id(report["taskId"]) / (valid_id(report["id"]) + ".md")
            if file.exists():
                if digest(file.read_bytes()) != report["markdownSha256"]:
                    raise PipelineError("本地同名报告与云端原件冲突，未覆盖。")
            else:
                atomic_write(file, report["markdown"])
                added += 1
            for artifact in report["analysis"].get("completion", {}).get("artifacts", []):
                ext = {"guide_pdf": ".pdf", "guide_html": ".html", "exercise_archive": ".zip", "experiment_log": ".txt", "knowledge_notes": ".md", "review_log": ".md"}[artifact["role"]]
                target = file.parent / (report["id"] + "-files") / (artifact["role"] + ext)
                data = base64.b64decode(artifact["base64"], validate=True)
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    if digest(target.read_bytes()) != artifact["sha256"]: raise PipelineError("本地学习产物有冲突，未覆盖。")
                else:
                    partial = target.with_suffix(target.suffix + ".partial")
                    with partial.open("xb") as stream:
                        stream.write(data); stream.flush()
                        import os
                        os.fsync(stream.fileno())
                    partial.replace(target)
            for attempt in report.get("learningAttempts", []):
                target = folder / "attempts" / (valid_id(attempt['id']) + '.json')
                content = json.dumps(attempt, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
                if target.exists():
                    if target.read_text(encoding='utf-8') != content: raise PipelineError("本地学习阻碍记录冲突，未覆盖。")
                else: atomic_write(target, content)
            record_file = file.with_suffix(".json")
            content = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
            # The report is immutable; export-time flags may differ across later backups.
            if not record_file.exists():
                atomic_write(record_file, content)
        rows = ["# Dot 云端报告与学习产物的本机副本", "", "这些是分类报告，分析时间不等于学习完成时间。云端原件未删除。", ""]
        for r in sorted(bundle["reports"], key=lambda r: (r.get("createdAt", ""), r["id"]), reverse=True):
            file = folder / "reports" / r["taskId"] / (r["id"] + ".md")
            state = "来源已变化，待复核" if r["stale"] else "完整学习受阻" if r.get("learningAttempts") and r["analysis"].get("stage") != "full" else "已备份"
            rows.append(f"- {r.get('createdAt', '')} · {r['analysis']['kind']} · {state} · [{r['analysis']['title']}]({file.as_posix()})")
        atomic_write(folder / "index.md", "\n".join(rows) + "\n")
        handoff = record_handoff(folder, bundle)
        return {"reports": len(bundle["reports"]), "added": added, "archive": str(archive), "index": str(folder / "index.md"), "cloudDeleted": False,
                "handoff": str(folder / "handoff.json"), "gitPending": sum(item["git"].get("status") not in {"pushed", "not_applicable"} for item in handoff["reports"].values())}
    finally:
        handle.close()
        lock.unlink(missing_ok=True)


def record_handoff(folder, bundle):
    """Backup bookkeeping only: never start learning, merge vault or mark Git success.

    The coordinator resumes the existing skill, retaining prior step receipts on
    repeat copies. Export flags are observations, never a lease or current authority.
    """
    path = folder / "handoff.json"
    state = {"schema": "reminder-dot-handoff-v1", "accountId": bundle["accountId"],
             "listId": bundle["list"]["id"], "primaryExecutor": "dot",
             "backupTargets": ["local", "git"], "reports": {}}
    if path.exists():
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            raise PipelineError("本机回迁交接账本损坏；副本已保留，停止更新账本。") from None
        if (not isinstance(state, dict) or state.get("schema") != "reminder-dot-handoff-v1" or
                state.get("accountId") != bundle["accountId"] or
                state.get("listId") != bundle["list"]["id"] or not isinstance(state.get("reports"), dict)):
            raise PipelineError("本机交接账本不属于此账户/列表，停止更新。")
        if any(not isinstance(item, dict) or not isinstance(item.get("git"), dict) for item in state["reports"].values()):
            raise PipelineError("本机交接阶段记录损坏，停止更新。")
    state.update(gitRepository="https://github.com/Smashwinny/reminder_knowlege.git",
                 gitScope="learning_artifacts_only", privateRecordsTargets=["website", "local"])
    for report in bundle["reports"]:
        full = report["analysis"].get("stage") == "full"
        relative = "reports/" + report["taskId"] + "/" + report["id"]
        previous = state["reports"].get(report["id"], {})
        if not isinstance(previous, dict) or any(key in previous and not isinstance(previous[key], dict) for key in ("knowledge", "git")):
            raise PipelineError("本机交接阶段记录损坏，停止更新。")
        if previous and (previous.get("sourceHash") != report["sourceHash"] or previous.get("markdownSha256") != report["markdownSha256"]):
            raise PipelineError("交接账本与已备份报告版本冲突，停止更新。")
        state["reports"][report["id"]] = {
            "taskId": report["taskId"], "sourceHash": report["sourceHash"],
            "markdownSha256": report["markdownSha256"], "analysisStage": "full" if full else "preliminary",
            "cloud": {"status": "saved", "exportedAt": bundle.get("exportedAt"),
                      "staleAtExport": report["stale"], "claimedAtExport": report["activeClaim"]},
            "local": {"status": "verified", "report": relative + ".md",
                      "artifacts": relative + "-files" if full else None},
            "knowledge": previous.get("knowledge", {"status": "pending_coordinator" if full else "not_applicable", "skillStep": 8}),
            "git": previous.get("git", {"status": "pending_coordinator" if full else "not_applicable", "skillStep": 9,
                                        "reason": "只提交学习成果；完整学习须先完成本机知识合并。私密分类报告不提交公开仓库。"}),
            "taskCompletion": "user_only",
        }
    atomic_write(path, json.dumps(state, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    return state


def integrate(root, bundle):
    """Import through the existing queue, never replace its DB or claim another owner.

    Fresh site sync is mandatory. No legacy adoption is implicit in a cloud export.
    """
    if __package__:
        from .reminder_coordinator import acquire, release as release_coordinator
    else:
        from reminder_coordinator import acquire, release as release_coordinator
    owner = "dot-import-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    acquire(root, owner)
    results = []
    try:
        pipeline = Pipeline(root=root)
        # Historical backups are not current authorization or lease evidence.
        _, current_cloud = download(bundle["accountId"], bundle["list"]["id"])
        cloud_reports = {r["id"]: r for r in current_cloud["reports"]}
        pipeline.sync()  # A failure preserves state and prevents classification imports.
        # Latest report per task only. Older versions remain in the private backup.
        latest = {}
        for report in sorted(bundle["reports"], key=lambda r: (r.get("createdAt", ""), r["id"])):
            latest[report["taskId"]] = report
        for task_id, report in latest.items():
            current = cloud_reports.get(report["id"])
            if current is None:
                results.append({"task": task_id, "status": "backup_only", "reason": "report not in current allowed cloud list"})
                continue
            if current["stale"] or current["activeClaim"]:
                results.append({"task": task_id, "status": "backup_only", "reason": "cloud source stale or claim held"})
                continue
            with contextlib.closing(pipeline._connection()) as connection:
                row = connection.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            if row is None:
                results.append({"task": task_id, "status": "backup_only", "reason": "record absent from current site"})
                continue
            local = pipeline.status(task_id)
            if local.get("source_hash") != report["sourceHash"]:
                results.append({"task": task_id, "status": "backup_only", "reason": "current site source differs"})
                continue
            if row is None or row["owner"] or row["learning_started"] or row["kind"] or row["protection"] or row["phase"] != "pending":
                results.append({"task": task_id, "status": "backup_only", "reason": "local ownership, classification or legacy protection"})
                continue
            if report["analysis"]["kind"] == "non_link":
                results.append({"task": task_id, "status": "backup_only", "reason": "non-link routing retained; local queue requires actual HTTP evidence"})
                continue
            task_owner = owner + "-" + report["id"]
            pipeline.claim(task_owner, task_id=task_id)
            try:
                a = report["analysis"]
                pipeline.classify(task_id, task_owner, ("needs_review" if a["kind"] == "non_link" else a["kind"]),
                    "已核对来源版本的 Dot 报告迁入。原始分析时间：" + report["createdAt"] + "\n\n" + report["markdown"],
                    [s["url"] for s in a["sources"]])
                results.append({"task": task_id, "status": "classified_imported"})
            finally:
                pipeline.release(task_id, task_owner)
        pipeline.render()
    finally:
        release_coordinator(root, owner)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["backup", "restore"])
    parser.add_argument("--account-id", required=True, help="明确允许的真实账户 UUID")
    parser.add_argument("--list-id", required=True, help="明确允许的服务端分析列表 UUID")
    parser.add_argument("--bundle", type=Path, help="restore 的导出文件；backup 直接只读下载")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--import-queue", action="store_true", help="备份后，核对实时网站并通过共享领取接口导入；不启动学习")
    args = parser.parse_args()
    try:
        if args.command == "restore" and args.bundle is None:
            parser.error("restore 需要 --bundle")
        if args.command == "backup":
            raw, bundle = download(args.account_id, args.list_id)
        else:
            raw, bundle = read_bundle(args.bundle, args.account_id, args.list_id)
        result = restore(args.root, raw, bundle)
        if args.import_queue:
            result["queue"] = integrate(args.root, bundle)
        print(json.dumps(result, ensure_ascii=False))
    except (PipelineError, OSError, ValueError, RuntimeError) as error:
        parser.exit(2, "错误：" + str(error) + "\n")


if __name__ == "__main__":
    main()
