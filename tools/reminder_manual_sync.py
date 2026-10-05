"""手动回迁 Dot 私有原件，并推送协调者已审核的明确公开文件清单。

不运行学习、不合并知识、不修改网站任务；Git 日志是交接回执，不是学习队列。
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3
import subprocess
import sys
import uuid

from reminder_coordinator import acquire, release, require_owner
from reminder_dot_backup import download, read_bundle, restore
from reminder_pipeline import Pipeline, PipelineError, ROOT, atomic_write, valid_id, IGNORED_EXERCISE_DIRS

PUBLIC_REPO = "https://github.com/Smashwinny/reminder_knowlege.git"
PRIVATE = Path("完成/.pipeline")
DENIED = {".git", ".pipeline", "repo", "node_modules", "__pycache__", ".venv", "venv", "vendor"}
EXTENSIONS = {"guide_pdf": ".pdf", "guide_html": ".html", "exercise_archive": ".zip",
              "experiment_log": ".txt", "knowledge_notes": ".md", "review_log": ".md"}


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        raise PipelineError("本机配置或同步回执无法读取；保留原文件。") from None
    if not isinstance(value, dict):
        raise PipelineError("本机配置或同步回执格式无效。")
    return value


def save(path, value):
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


@contextmanager
def coordinator(root):
    owner = "manual-sync-" + uuid.uuid4().hex
    acquire(root, owner, ttl=7200)
    try:
        yield owner
    finally:
        release(root, owner)


@contextmanager
def handoff_lock(folder, owner):
    """Share the existing backup lock with logon restore; never overwrite its ledger."""
    path = folder / ".restore.lock"
    try:
        handle = path.open("x", encoding="utf-8")
    except FileExistsError:
        raise PipelineError("登录备份正在更新交接账本，或上轮有未释放锁；不抢占，稍后重试。") from None
    try:
        handle.write(owner)
        handle.close()
        yield
    finally:
        handle.close()
        path.unlink(missing_ok=True)


def git(repo, *args, stdin=None, accepted=(0,)):
    try:
        result = subprocess.run(["git", "-C", str(repo), *args], input=stdin,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}, timeout=180)
    except (OSError, subprocess.TimeoutExpired):
        raise PipelineError("Git 无法执行或超时；已保存副本和待推送回执。") from None
    if result.returncode not in accepted:
        # Git/credential helper stderr can contain URLs or credentials: never echo it.
        raise PipelineError("Git " + args[0] + " 失败；不重置、不强推。检查网络、认证或远端冲突后重试。")
    return result.stdout


def names(raw):
    return {name.decode("utf-8") for name in raw.split(b"\0") if name}


def public_path(root, name, projects, maintenance=False):
    if (not isinstance(name, str) or not name or "\\" in name or ":" in name or
            "\n" in name or "\r" in name or "\0" in name):
        raise PipelineError("公开清单必须使用单个仓库相对文件路径。")
    parts = name.split("/")
    if any(part in {"", ".", ".."} or part.casefold() in DENIED for part in parts):
        raise PipelineError("公开清单包含私有目录、源码克隆、缓存或越界路径。")
    if maintenance:
        allowed = parts[0] == "tools" or name in {"sync-reminder.cmd", ".gitattributes"}
    else:
        allowed = parts[0] in projects or parts[0] == "vault"
    if (not allowed or any(part.casefold() in {".env", ".shiyi_token", "dot-backup-config.json"} for part in parts)
            or name.endswith((".sqlite", ".sqlite3", ".pem", ".key"))):
        raise PipelineError("文件不属于本批次获准的公开学习成果或工具。")
    target = root.joinpath(*parts)
    # Reject links, including a link within the workspace to a private original.
    for candidate in [target, *target.parents]:
        if candidate == root:
            break
        if candidate.is_symlink() or (hasattr(candidate, "is_junction") and candidate.is_junction()):
            raise PipelineError("公开文件不能通过链接或目录联接引用其他目录。")
    if not target.resolve().is_relative_to(root) or not target.is_file():
        raise PipelineError("公开清单中的文件不存在、不是文件或超出仓库。")
    if target.stat().st_size > 99 * 1024 * 1024:
        raise PipelineError("公开文件超过 GitHub 普通文件大小范围。")
    return target


def task_row(root, task_id):
    db_path = root / PRIVATE / "queue.sqlite3"
    try:
        with sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True) as db:
            db.row_factory = sqlite3.Row
            row = db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            if not row:
                raise PipelineError("原共享队列中没有此学习任务。")
            return dict(row)
    except sqlite3.Error:
        raise PipelineError("原共享队列无法只读核对；不另建队列。") from None


def check_learning(root, report, handoff):
    row = task_row(root, report["taskId"])
    item = handoff["reports"].get(report["id"], {})
    receipt = json.loads(row.get("analysis_receipt") or "null")
    review = json.loads(row.get("review") or "null")
    if (report["analysis"].get("stage") != "full" or report["stale"] or report["activeClaim"] or
            item.get("local", {}).get("status") != "verified" or
            item.get("sourceHash") != report["sourceHash"] or
            item.get("knowledge", {}).get("status") != "merged" or row.get("owner") or
            row.get("phase") != "analysis_confirmed" or row.get("invalidated") or
            row.get("deleted") or row.get("missing") or row.get("content_hash") != report["sourceHash"] or
            not receipt or receipt.get("report_id") != report["id"] or
            receipt.get("source_hash") != report["sourceHash"] or
            not review or review.get("approved") is not True or not review.get("reviewer") or
            review.get("reviewer") == report.get("owner")):
        raise PipelineError("学习成果尚未通过当前来源核对、独立验收和知识合并，或仍由其他执行者持有。")
    pipeline = object.__new__(Pipeline)
    pipeline.root = root
    manifest, fingerprint = pipeline._validate_manifest(row, json.loads(row["manifest"]))
    if fingerprint != row["artifact_fingerprint"] or review.get("artifact_fingerprint") != fingerprint:
        raise PipelineError("学习产物在验收后有变化；重新 ready/review，不能直接上传。")
    return manifest


def prepare(root, config, files_file, message, task_ids=(), maintenance=False, review_notes=""):
    if not review_notes.strip() or not message.strip() or "\n" in message or "\r" in message:
        raise PipelineError("协调者需提供具体内容/隐私审阅说明和单行提交说明。")
    settings = load(config)
    account, list_id = valid_id(settings.get("accountId", "")), valid_id(settings.get("listId", ""))
    folder = root / PRIVATE / "dot" / account / list_id
    handoff = load(folder / "handoff.json")
    projects, reports = set(), []
    recent_reports = {}
    if task_ids:
        archives = list((folder / "exports").glob("*.json"))
        if not archives:
            raise PipelineError("缺少已校验的本机完整导出；先手动同步一次。")
        latest = max(archives, key=lambda p: p.stat().st_mtime_ns)
        raw, latest_bundle = read_bundle(latest, account, list_id)
        if sha(raw) != latest.stem:
            raise PipelineError("最近导出原件与 SHA256 文件名不符。")
        recent_reports = {r["id"]: r for r in latest_bundle["reports"]}
    for task_id in task_ids:
        valid_id(task_id)
        row = task_row(root, task_id)
        receipt = json.loads(row.get("analysis_receipt") or "null")
        if not receipt:
            raise PipelineError("协调者尚未确认此任务的完整学习交付。")
        report = recent_reports.get(valid_id(receipt["report_id"]))
        if not report or report["taskId"] != task_id:
            raise PipelineError("最近导出不包含此任务已验收的报告。")
        manifest = check_learning(root, report, handoff)
        projects.add(PurePosixPath(manifest["project_dir"]).parts[0])
        reports.append({"reportId": report["id"], "sourceHash": report["sourceHash"]})
    if not maintenance and not reports or maintenance and task_ids:
        raise PipelineError("学习清单需绑定已验收任务；工具清单不能假装学习交付。")
    paths = [line.strip() for line in Path(files_file).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if not paths or len(paths) != len(set(paths)):
        raise PipelineError("需要非空且无重复的明确文件清单。")
    files = [{"path": name, "sha256": sha(public_path(root, name, projects, maintenance).read_bytes())} for name in paths]
    manifest = {"schema": "reminder-git-publication-v1", "id": uuid.uuid4().hex,
                "kind": "maintenance" if maintenance else "learning", "repository": PUBLIC_REPO,
                "accountId": account, "listId": list_id, "reports": reports,
                "message": message, "reviewNotes": review_notes, "privateContentReviewed": True,
                "files": files, "status": "prepared", "createdAt": now()}
    manifest["author"] = {
        "name": settings.get("gitAuthorName") or git(root, "config", "--get", "user.name").decode().strip(),
        "email": settings.get("gitAuthorEmail") or git(root, "config", "--get", "user.email").decode().strip()}
    path = root / PRIVATE / "git-publications" / (manifest["id"] + ".json")
    save(path, manifest)
    return path


def check_publication(root, manifest, bundle, handoff):
    if (manifest.get("schema") != "reminder-git-publication-v1" or
            manifest.get("repository") != PUBLIC_REPO or manifest.get("kind") not in {"maintenance", "learning"} or
            manifest.get("accountId") != bundle["accountId"] or manifest.get("listId") != bundle["list"]["id"] or
            manifest.get("privateContentReviewed") is not True or not manifest.get("reviewNotes")):
        raise PipelineError("Git 清单缺少审核、隐私检查或授权范围不符。")
    if not re.fullmatch(r"[0-9a-f]{32}", manifest.get("id", "")):
        raise PipelineError("Git 批次标识无效。")
    author = manifest.get("author", {})
    if any(not isinstance(author.get(key), str) or not author[key].strip() or
           any(char in author[key] for char in "\r\n\0") for key in ("name", "email")):
        raise PipelineError("Git 清单未保存有效的提交署名。")
    projects, forbidden = set(), {bundle["accountId"], bundle["list"]["id"]}
    reports = {report["id"]: report for report in bundle["reports"]}
    for report in bundle["reports"]:
        forbidden.update((report["id"], report["taskId"]))
    for entry in manifest["reports"]:
        report = reports.get(entry["reportId"])
        if not report or report["sourceHash"] != entry["sourceHash"]:
            raise PipelineError("Git 清单未对应本次网站真值中的报告。")
        checked = check_learning(root, report, handoff)
        projects.add(PurePosixPath(checked["project_dir"]).parts[0])
    maintenance = manifest["kind"] == "maintenance"
    if not maintenance and not projects or maintenance and manifest["reports"]:
        raise PipelineError("Git 清单学习范围无效。")
    blobs = {}
    for item in manifest["files"]:
        name = item["path"]
        if name in blobs:
            raise PipelineError("Git 清单包含重复文件。")
        data = public_path(root, name, projects, maintenance).read_bytes()
        if sha(data) != item["sha256"]:
            raise PipelineError("公开文件在审阅后有变化；请协调者重新核对文件清单。")
        lowered = data.lower()
        if (any(value.lower().encode() in lowered for value in forbidden) or
                re.search(rb"chatgpt\.com/dots/[a-z0-9_-]+", lowered) or
                re.search(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", data) or
                re.search(rb"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", data)):
            raise PipelineError("公开成果中发现私有身份、Dot 会话或凭据；不上传。")
        blobs[name] = data
    if not blobs:
        raise PipelineError("Git 清单为空。")
    if not maintenance:
        required = {"vault/00-总览.md"}
        for entry in manifest["reports"]:
            checked = check_learning(root, reports[entry["reportId"]], handoff)
            required.update(checked[key] for key in ("pdf", "html", "experiment_log", "vault_note"))
            exercise = root / checked["exercise_dir"]
            for directory, dirs, file_names in os.walk(exercise, followlinks=False):
                dirs[:] = [d for d in dirs if d.casefold() not in IGNORED_EXERCISE_DIRS]
                for file_name in file_names:
                    file = Path(directory) / file_name
                    if file.is_file() and file.stat().st_size:
                        required.add(file.relative_to(root).as_posix())
        if not required.issubset(blobs):
            raise PipelineError("学习清单遗漏指南、练习材料、实测日志、已合并项目笔记或知识总览。")
    return blobs


def publication_repo(root):
    repo = root / PRIVATE / "knowledge-publication"
    if not repo.exists():
        git(root, "clone", "--single-branch", "--branch", "main", PUBLIC_REPO, str(repo))
    if repo.is_symlink() or not repo.resolve().is_relative_to((root / PRIVATE).resolve()):
        raise PipelineError("公开提交工作区超出本机私有目录。")
    if git(repo, "rev-parse", "--show-toplevel").decode().strip().replace("\\", "/").casefold() != repo.as_posix().casefold():
        raise PipelineError("公开提交工作区不是独立仓库。")
    if git(repo, "symbolic-ref", "--short", "HEAD").strip() != b"main":
        raise PipelineError("公开提交工作区不在 main，停止自动同步。")
    for args in (("remote", "get-url", "--all", "origin"), ("remote", "get-url", "--push", "--all", "origin")):
        if git(repo, *args).decode().splitlines() != [PUBLIC_REPO]:
            raise PipelineError("Git 远端不是已确认的公开知识仓库。")
    return repo


def publish(root, owner, repo, path, manifest, blobs):
    require_owner(root, owner)
    if git(root, "diff", "--cached", "--name-only", "-z"):
        raise PipelineError("主工作区暂存区非空，归属未核定；停止 Git 同步。")
    marker = "Reminder-Sync-Batch: " + manifest["id"]
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    # Recover a crash between successful commit and writing its local receipt.
    if manifest["status"] == "committing" and marker in git(repo, "log", "-1", "--format=%B").decode():
        manifest.update(status="committed", commit=head)
        save(path, manifest)
    git(repo, "fetch", "origin", "main")
    remote = git(repo, "rev-parse", "FETCH_HEAD").decode().strip()
    if manifest["status"] != "committed":
        staged = names(git(repo, "diff", "--cached", "--name-only", "-z"))
        recovering = manifest["status"] in {"staging", "committing"}
        if staged and (not recovering or not staged.issubset(blobs)):
            raise PipelineError("公开工作区暂存区有归属不明的文件，保留现场。")
        if not recovering and git(repo, "status", "--porcelain", "-z"):
            raise PipelineError("公开工作区存在未处理改动；不覆盖、不重置。")
        if recovering:
            if manifest.get("baseCommit") != head:
                raise PipelineError("中断后公开工作区 HEAD 已变化，需协调者核查。")
            changed = names(git(repo, "diff", "HEAD", "--name-only", "-z"))
            untracked = names(git(repo, "ls-files", "--others", "--exclude-standard", "-z"))
            if not (changed | untracked).issubset(blobs):
                raise PipelineError("中断后的公开工作区有额外文件；不自动接管。")
            for name in changed | untracked:
                if (repo / name).read_bytes() != blobs[name]:
                    raise PipelineError("中断后的公开文件被其他操作者修改，保留现场。")
            for name in staged:
                expected = git(repo, "hash-object", "--path=" + name, "--stdin", stdin=blobs[name]).strip()
                if git(repo, "rev-parse", ":" + name).strip() != expected:
                    raise PipelineError("中断后的暂存字节发生变化，归属不明；保留现场。")
        elif head != remote:
            # --ff-only rejects both divergence and unreviewed local-ahead commits below.
            git(repo, "merge", "--ff-only", remote)
            head = git(repo, "rev-parse", "HEAD").decode().strip()
            if head != remote:
                raise PipelineError("公开工作区有未归属此批次的本地提交，停止推送。")
        manifest.update(status="staging", baseCommit=head)
        save(path, manifest)
        for name, data in blobs.items():
            target = repo / name
            if target.exists() and target.read_bytes() == data:
                continue
            for candidate in [target, *target.parents]:
                if candidate == repo:
                    break
                if candidate.is_symlink() or (hasattr(candidate, "is_junction") and candidate.is_junction()):
                    raise PipelineError("公开工作区目标路径是链接，停止写入。")
            if not target.resolve().is_relative_to(repo):
                raise PipelineError("公开工作区目标路径越界。")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        # NUL pathspec: explicit files, no glob expansion and no directory-wide add.
        git(repo, "--literal-pathspecs", "add", "--pathspec-from-file=-", "--pathspec-file-nul",
            stdin=b"".join(name.encode() + b"\0" for name in blobs))
        staged = names(git(repo, "diff", "--cached", "--name-only", "-z"))
        if not staged.issubset(blobs):
            raise PipelineError("Git 暂存清单出现额外文件，停止提交。")
        for name in blobs:
            expected = git(repo, "hash-object", "--path=" + name, "--stdin", stdin=blobs[name]).strip()
            if git(repo, "rev-parse", ":" + name).strip() != expected:
                raise PipelineError("Git 暂存字节与审核文件不同，停止提交。")
        manifest["gitBlobs"] = {name: git(repo, "rev-parse", ":" + name).decode().strip() for name in blobs}
        git(repo, "diff", "--cached", "--check")
        if staged:
            # Existing approved identity only; never change global Git configuration.
            author = manifest["author"]["name"]
            email = manifest["author"]["email"]
            manifest.update(status="committing", stagedPaths=sorted(staged))
            save(path, manifest)
            git(repo, "-c", "user.name=" + author, "-c", "user.email=" + email, "commit",
                "-m", manifest["message"] + "\n\n" + marker)
            head = git(repo, "rev-parse", "HEAD").decode().strip()
        manifest.update(status="committed", commit=head)
        save(path, manifest)
    commit = manifest["commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or commit != git(repo, "rev-parse", "HEAD").decode().strip():
        raise PipelineError("待推送提交与当前公开工作区不同，停止推送。")
    if git(repo, "status", "--porcelain", "-z"):
        raise PipelineError("待推送工作区有额外改动，保留现场。")
    if set(manifest.get("gitBlobs", {})) != set(blobs):
        raise PipelineError("待推送回执缺少实际 Git 文件对象校验。")
    for name, expected in manifest["gitBlobs"].items():
        if git(repo, "rev-parse", commit + ":" + name).decode().strip() != expected:
            raise PipelineError("提交中的文件与审核字节不同，停止推送。")
    # Only the batch commit may be ahead; never push another person's commits.
    ancestor = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", commit, remote],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ancestor.returncode not in (0, 1):
        raise PipelineError("Git 远端祖先检查失败。")
    if ancestor.returncode != 0:
        if manifest.get("baseCommit") != git(repo, "rev-parse", commit + "^").decode().strip():
            raise PipelineError("待推送提交父版本与本批次回执不符。")
        if marker not in git(repo, "log", "-1", "--format=%B", commit).decode():
            raise PipelineError("待推送提交缺少本批次标记。")
        if names(git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", commit)) != set(manifest.get("stagedPaths", [])):
            raise PipelineError("待推送提交文件与回执不符。")
        git(repo, "push", "origin", commit + ":refs/heads/main")
    git(repo, "fetch", "origin", "main")
    remote = git(repo, "rev-parse", "FETCH_HEAD").decode().strip()
    # merge-base needs its exit status (stdout is empty for both outcomes).
    verified = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", commit, remote],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if verified.returncode:
        raise PipelineError("推送后未确认远端包含本批次提交；保留待推送状态。")
    manifest.update(status="pushed", pushedAt=now(), remoteCommit=remote)
    save(path, manifest)


def sync(root, config, local_only=False):
    status_path = root / PRIVATE / "manual-sync-status.json"
    state = {"schema": "reminder-manual-sync-v1", "startedAt": now(), "local": "pending",
             "git": "pending", "knowledgeMergedByScript": False, "taskCompletionChanged": False}
    acquired = False
    try:
        with coordinator(root) as owner:
            acquired = True
            save(status_path, state)
            settings = load(config)
            account, list_id = valid_id(settings.get("accountId", "")), valid_id(settings.get("listId", ""))
            raw, bundle = download(account, list_id)  # Fresh truth; never substitute old export on failure.
            result = restore(root, raw, bundle)
            state.update(local="verified", reports=result["reports"], added=result["added"],
                         fullReports=sum(r["analysis"].get("stage") == "full" for r in bundle["reports"]),
                         backupIndex=result["index"], backupBundle=result["archive"])
            save(status_path, state)
            folder = Path(result["handoff"]).parent
            published = 0
            with handoff_lock(folder, owner):
                handoff = load(result["handoff"])
                if not local_only:
                    manifests = sorted((root / PRIVATE / "git-publications").glob("*.json"), key=lambda p: p.stat().st_mtime_ns)
                    for path in manifests:
                        manifest = load(path)
                        if manifest.get("status") == "pushed":
                            # A crash after Git confirmation must not lose the handoff receipt.
                            for entry in manifest.get("reports", []):
                                if (manifest.get("repository") == PUBLIC_REPO and
                                        manifest.get("accountId") == account and manifest.get("listId") == list_id and
                                        entry["reportId"] in handoff["reports"] and
                                        entry["sourceHash"] == handoff["reports"][entry["reportId"]]["sourceHash"] and
                                        handoff["reports"][entry["reportId"]]["git"].get("status") != "pushed"):
                                    handoff["reports"][entry["reportId"]]["git"] = {
                                        "status": "pushed", "skillStep": 9, "commit": manifest["commit"],
                                        "pushedAt": manifest["pushedAt"], "publicationReceipt": str(path.relative_to(root))}
                                    save(folder / "handoff.json", handoff)
                            continue
                        blobs = check_publication(root, manifest, bundle, handoff)
                        repo = publication_repo(root)
                        publish(root, owner, repo, path, manifest, blobs)
                        for entry in manifest["reports"]:
                            handoff["reports"][entry["reportId"]]["git"] = {
                                "status": "pushed", "skillStep": 9, "commit": manifest["commit"],
                                "pushedAt": manifest["pushedAt"], "publicationReceipt": str(path.relative_to(root))}
                        save(folder / "handoff.json", handoff)
                        published += 1
            full = [item for item in handoff["reports"].values() if item["analysisStage"] == "full"]
            state.update(git="local_only" if local_only else "pushed" if published else "no_ready_batch", publishedBatches=published,
                         knowledgePending=sum(i["knowledge"].get("status") != "merged" for i in full),
                         gitPending=sum(i["git"].get("status") != "pushed" for i in full), finishedAt=now())
            rows = ["# 手动同步结果", "", "本次检查：" + state["finishedAt"], "",
                    f"网站报告 {state['reports']} 份，完整报告 {state['fullReports']} 份；本机原件校验通过。",
                    f"本次推送 {published} 批；待知识合并 {state['knowledgePending']} 项，待 Git 备份 {state['gitPending']} 项。",
                    "", f"[私有报告与产物入口]({Path(result['index']).as_posix()})", "",
                    "任务完成由本人点击。脚本不运行模型或自动声称知识合并/内容验收成功。"]
            atomic_write(root / PRIVATE / "手动同步结果.md", "\n".join(rows) + "\n")
            save(status_path, state)
            return state
    except Exception as error:
        state.update(git="pending" if state["local"] == "verified" else "not_run", failedAt=now(),
                     error=str(error) if isinstance(error, (PipelineError, RuntimeError)) else "同步中断，原件与回执保留。")
        if acquired:
            save(status_path, state)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--config", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    cmd = sub.add_parser("sync")
    cmd.add_argument("--local-only", action="store_true")
    sub.add_parser("status")
    cmd = sub.add_parser("prepare", help="唯一协调者在实际验收和隐私检查后登记明确文件清单")
    cmd.add_argument("--files-file", type=Path, required=True)
    cmd.add_argument("--message", required=True)
    cmd.add_argument("--task", action="append", default=[])
    cmd.add_argument("--maintenance", action="store_true")
    cmd.add_argument("--review-notes", required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    config = args.config or root / PRIVATE / "dot-backup-config.json"
    try:
        if args.command == "status":
            value = load(root / PRIVATE / "manual-sync-status.json")
        elif args.command == "prepare":
            with coordinator(root):
                path = prepare(root, config, args.files_file, args.message, args.task, args.maintenance, args.review_notes)
                value = {"receipt": str(path), "status": "prepared", "pushed": False}
        else:
            value = sync(root, config, args.local_only)
            print(f"本机同步通过：{value['reports']} 份报告，含 {value['fullReports']} 份完整学习报告。")
            print(f"本次 GitHub 推送 {value['publishedBatches']} 批；待验收/入库 {value['knowledgePending']} 项，待 Git 备份 {value['gitPending']} 项。")
            print("结果：" + str(root / PRIVATE / "手动同步结果.md"))
            return
        print(json.dumps(value, ensure_ascii=False, indent=2))
    except Exception as error:
        message = str(error) if isinstance(error, (PipelineError, RuntimeError)) else "同步中断；原件、工作区和回执保留，请查看本机状态。"
        parser.exit(1, "错误：" + message + "\n")


if __name__ == "__main__":
    main()
