"""Verify cloud Git receipts and copy reviewed knowledge without overwriting local edits.

This is a consumer of the existing delivery ledger, never a second learning queue.
It does not run a model, commit, push, change task completion, or steal task owners.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import subprocess
import uuid
from pathlib import Path

if __package__:
    from .reminder_pipeline import PipelineError, atomic_write
    from .reminder_coordinator import require_owner
else:
    from reminder_pipeline import PipelineError, atomic_write
    from reminder_coordinator import require_owner

REPOSITORY = "Smashwinny/reminder_knowlege"
REMOTE = "https://github.com/" + REPOSITORY + ".git"
PRIVATE = "完成/.pipeline"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def public_path(root, value, project):
    if (not isinstance(value, str) or len(value) > 250 or "\\" in value or
            any(ord(x) < 32 for x in value) or ":" in value or
            any(x in {"", ".", ".."} for x in value.split("/"))):
        raise PipelineError("云端回执路径无效。")
    parts = value.split("/")
    if any(re.fullmatch(r"(?:con|prn|aux|nul|com\d|lpt\d)(?:\..*)?", x, re.I) for x in parts):
        raise PipelineError("云端回执含设备路径。")
    if any(x.lower() in {"repo", "node_modules", ".git", ".pipeline", ".aws", ".ssh", ".venv", "venv", "__pycache__", "cloud-reference", "backups"} or x.lower().startswith(".env") for x in parts):
        raise PipelineError("云端回执含私有或缓存目录。")
    permitted = (value.startswith(project + "/") and bool(re.search(r"\.(pdf|html|md|txt|py|js|mjs|jsx|ts|tsx|json|csv|svg|png|jpg|yml|yaml|sh|sql|go|rs|toml|ipynb|c|h|cpp|java|kt|css|log)$", value, re.I))) or value in {
        "vault/00-总览.md", "vault/项目笔记/" + project + ".md"} or bool(re.fullmatch(r"vault/概念/[^/]+\.md", value))
    target = root / value
    for candidate in [target, *target.parents]:
        if candidate == root:
            break
        if candidate.is_symlink() or (hasattr(candidate, "is_junction") and candidate.is_junction()):
            raise PipelineError("本机知识目标含符号链接或目录联接，保留原文件。")
    destination = target.resolve()
    if not permitted or not destination.is_relative_to(root):
        raise PipelineError("云端回执超出项目/知识库范围，或含仓库外链接。")
    return destination


def receipt(report):
    delivery = report.get("cloudDelivery")
    if delivery is not None and not isinstance(delivery, dict):
        raise PipelineError("云端交付状态格式无效。")
    if not delivery or delivery.get("state") != "pushed":
        return None
    value = delivery.get("receipt")
    if (report["analysis"].get("stage") != "full" or not isinstance(value, dict) or
            value.get("schema") != "reminder-cloud-publication-v1" or
            value.get("repository") != REPOSITORY or value.get("branch") != "main" or
            value.get("reportId") != report["id"] or value.get("sourceHash") != report["sourceHash"] or
            not re.fullmatch(r"[a-f0-9]{40}", value.get("commit", "")) or
            not re.fullmatch(r"[a-f0-9]{40}", value.get("baseCommit", "")) or
            not re.fullmatch(r"[a-f0-9]{64}", value.get("fingerprint", "")) or
            not value.get("reviewer") or not isinstance(value.get("files"), list) or
            not 2 <= len(value["files"]) <= 650):
        raise PipelineError("云端 Git 回执缺少完整身份、审核或文件绑定，未认定推送成功。")
    return value


def git(repo, *args, binary=False):
    result = subprocess.run(["git", "--git-dir", str(repo), *args], capture_output=True, timeout=120)
    if result.returncode:
        raise PipelineError("公开知识 Git 核验失败；私有备份保留，未标记本机知识已同步。")
    return result.stdout if binary else result.stdout.decode("utf-8", errors="strict").strip()


def local_owner_held(root, report, project):
    database=root/PRIVATE/"queue.sqlite3"
    if not database.exists():
        return False
    try:
        connection=sqlite3.connect(database.as_uri()+"?mode=ro",uri=True)
        try:
            return connection.execute("SELECT 1 FROM tasks WHERE owner IS NOT NULL AND (task_id=? OR project_key=?) LIMIT 1",(report['taskId'],project.casefold())).fetchone() is not None
        finally:
            connection.close()
    except sqlite3.Error:
        raise PipelineError("无法核对原共享队列 owner，原件已保留，未覆盖项目知识。") from None


class PublicMirror:
    def __init__(self, root):
        self.path = (root / PRIVATE / "cloud-knowledge-replica.git").resolve()
        if not self.path.is_relative_to(root):
            raise PipelineError("知识缓存目录超出工作区。")
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(["git", "init", "--bare", str(self.path)], capture_output=True, timeout=30)
            if result.returncode:
                raise PipelineError("无法初始化本机私有知识缓存。")
            git(self.path, "remote", "add", "origin", REMOTE)
        if git(self.path, "remote", "get-url", "--all", "origin") != REMOTE:
            raise PipelineError("知识缓存远端配置不符，未联网。")
        git(self.path, "fetch", "--no-tags", "--filter=blob:none", "origin", "refs/heads/main:refs/remotes/origin/main")

    def verify_commit(self, commit):
        git(self.path, "merge-base", "--is-ancestor", commit, "refs/remotes/origin/main")

    def file(self, commit, name):
        data = git(self.path, "show", commit + ":" + name, binary=True)
        if len(data) > 2_000_000:
            raise PipelineError("公开知识文件超过回迁限制。")
        return data

    def file_if_exists(self, commit, name):
        if not git(self.path, "ls-tree", "-z", commit, "--", name, binary=True):
            return None
        return self.file(commit, name)

    def is_ancestor(self, older, newer):
        value = subprocess.run(["git", "--git-dir", str(self.path), "merge-base", "--is-ancestor", older, newer], capture_output=True, timeout=30)
        if value.returncode not in (0, 1):
            raise PipelineError("无法核对云端提交的先后关系。")
        return value.returncode == 0


def apply_cloud_receipts(root, bundle, coordinator, mirror_factory=PublicMirror):
    """Caller owns the existing coordinator lock. All receipt bytes remain private."""
    root = Path(root).resolve()
    require_owner(root, coordinator)
    candidates = [(report, receipt(report)) for report in bundle["reports"]]
    candidates = [(report, value) for report, value in candidates if value and not report["stale"] and not report["activeClaim"]]
    if not candidates:
        return {"cloudPublished": 0, "localKnowledgeSynced": 0, "conflicts": []}
    staged = subprocess.run(["git", "-C", str(root), "diff", "--cached", "--name-only"], capture_output=True, timeout=30)
    if staged.returncode or staged.stdout.strip():
        raise PipelineError("原工作区暂存区非空或无法核对；原件已备份，未覆盖本机知识。")
    mirror = mirror_factory(root)
    folder = root / PRIVATE / "dot" / bundle["accountId"] / bundle["list"]["id"]
    handoff_path = folder / "handoff.json"
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    if handoff.get("schema") != "reminder-dot-handoff-v1" or handoff.get("accountId") != bundle["accountId"] or handoff.get("listId") != bundle["list"]["id"]:
        raise PipelineError("本机交接账本不属于此账户/列表。")
    # Determine the newest reviewed version per path from actual Git ancestry.
    # Older receipts remain verified history and must not roll back newer knowledge.
    winners, valid_baselines, verified_files = {}, {}, {}
    for report, value in candidates:
        mirror.verify_commit(value["commit"])
        mirror.verify_commit(value["baseCommit"])
        if not mirror.is_ancestor(value["baseCommit"], value["commit"]):
            raise PipelineError("云端审核基线不是实际交付提交的祖先。")
        seen = set()
        for file in value["files"]:
            if not isinstance(file, dict):
                raise PipelineError("云端文件清单格式无效。")
            name = file.get("path")
            public_path(root, name, report["analysis"]["completion"]["project"])
            if name.casefold() in seen or "baseSha256" not in file or not re.fullmatch(r"[a-f0-9]{64}", file.get("sha256", "")) or file["baseSha256"] is not None and not re.fullmatch(r"[a-f0-9]{64}", file["baseSha256"]):
                raise PipelineError("云端文件清单重复或缺少哈希。")
            seen.add(name.casefold())
            data = mirror.file(value["commit"], name)
            baseline = mirror.file_if_exists(value["baseCommit"], name)
            base_hash = sha(baseline) if baseline is not None else None
            if sha(data) != file["sha256"] or base_hash != file["baseSha256"]:
                raise PipelineError("云端回执哈希与实际 Git 文件或基线不符。")
            verified_files[(report["id"], name)] = data
            valid_baselines.setdefault(name, set()).update((base_hash, file["sha256"]))
            old = winners.get(name)
            if not old or mirror.is_ancestor(old, value["commit"]):
                winners[name] = value["commit"]
            elif not mirror.is_ancestor(value["commit"], old):
                raise PipelineError("云端提交历史分叉，保留本机知识。")
    result = {"cloudPublished": len(candidates), "localKnowledgeSynced": 0, "conflicts": []}
    for report, value in sorted(candidates, key=lambda x: (x[1].get("pushedAt", ""), x[0]["id"])):
        project = report["analysis"]["completion"]["project"]
        if not re.fullmatch(r"[a-z][a-z0-9_-]{0,100}", project):
            raise PipelineError("云端项目目录需另行核对。")
        mirror.verify_commit(value["commit"])
        writes, conflicts, seen = [], [], set()
        if local_owner_held(root,report,project):
            conflicts.append(project+'/')
        for item in value["files"]:
            name = item.get("path")
            destination = public_path(root, name, project)
            if name.casefold() in seen or "baseSha256" not in item or not re.fullmatch(r"[a-f0-9]{64}", item.get("sha256", "")) or item.get("baseSha256") is not None and not re.fullmatch(r"[a-f0-9]{64}", item.get("baseSha256", "")):
                raise PipelineError("云端文件清单重复或缺少哈希。")
            seen.add(name.casefold())
            data = verified_files[(report["id"], name)]
            if winners[name] != value["commit"]:
                continue
            before = destination.read_bytes() if destination.exists() else None
            if before == data:
                continue
            if before is not None and sha(before) not in valid_baselines[name]:
                conflicts.append(name)
            elif before is None:
                tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", "--", name], capture_output=True, timeout=30)
                if tracked.returncode == 0:
                    conflicts.append(name)
                else:
                    writes.append((destination, data, before))
            else:
                writes.append((destination, data, before))
        # The new guide bytes must still be the original independently reviewed cloud artifact.
        artifacts = {a["role"]: a for a in report["analysis"]["completion"]["artifacts"]}
        listed = {f["path"]: f["sha256"] for f in value["files"]}
        for name, role in [(project + "/" + project + "-小白指南.pdf", "guide_pdf"), (project + "/guide.html", "guide_html"), (project + "/experiment_log.txt", "experiment_log")]:
            if listed.get(name) != artifacts[role]["sha256"]:
                raise PipelineError("Git 回执未绑定本条原始学习产物。")
        if "vault/00-总览.md" not in listed or "vault/项目笔记/" + project + ".md" not in listed:
            raise PipelineError("Git 回执缺少知识入库。")
        # A previous partial copy is safe to retry: already matching files are skipped.
        for destination, data, before in writes:
            current = destination.read_bytes() if destination.exists() else None
            if current != before:
                conflicts.append(destination.relative_to(root).as_posix())
        item = handoff["reports"][report["id"]]
        item["cloudDelivery"] = {"status": "verified", "receipt": value}
        item["git"] = {"status": "pushed", "skillStep": 9, "executor": "cloud_coordinator", "commit": value["commit"], "pushedAt": value.get("pushedAt")}
        item["knowledge"] = {"status": "merged", "skillStep": 8, "executor": "cloud_coordinator", "commit": value["commit"]}
        if conflicts:
            item["localKnowledge"] = {"status": "conflict", "paths": sorted(set(conflicts))}
            result["conflicts"].append({"reportId": report["id"], "paths": sorted(set(conflicts))})
        else:
            for destination, data, before in writes:
                destination.parent.mkdir(parents=True, exist_ok=True)
                temporary = destination.with_name(destination.name + ".cloud-sync-" + uuid.uuid4().hex)
                try:
                    with temporary.open("xb") as stream:
                        stream.write(data); stream.flush()
                        import os
                        os.fsync(stream.fileno())
                    # Keep a private undo copy; preserve the exact previous bytes.
                    if before is not None:
                        undo = root / PRIVATE / "cloud-sync-history" / sha(before)
                        undo.parent.mkdir(parents=True, exist_ok=True)
                        if not undo.exists():
                            undo.write_bytes(before)
                    current = destination.read_bytes() if destination.exists() else None
                    public_path(root, destination.relative_to(root).as_posix(), project)
                    if current != before:
                        raise PipelineError("回迁期间本机文件被修改，保留修改并停止；重试时将报告冲突。")
                    temporary.replace(destination)
                finally:
                    temporary.unlink(missing_ok=True)
            item["localKnowledge"] = {"status": "synced", "commit": value["commit"]}
            result["localKnowledgeSynced"] += 1
        atomic_write(handoff_path, json.dumps(handoff, ensure_ascii=False, indent=2) + "\n")
    return result


def acknowledge_local_backups(root, bundle, coordinator, backup_bundle, post=None):
    """Only attest bytes just backed up; a server receipt is not a remote disk audit."""
    if post is None:
        if __package__:
            from .reminder_dot_agent import post
        else:
            from reminder_dot_agent import post
    root=Path(root).resolve(); require_owner(root,coordinator)
    folder=root/PRIVATE/"dot"/bundle["accountId"]/bundle["list"]["id"]
    path=folder/"handoff.json"; handoff=json.loads(path.read_text(encoding="utf-8"))
    archive=Path(backup_bundle).resolve()
    if not archive.is_relative_to(folder/"exports"):
        raise PipelineError("本机备份归档超出授权列表目录。")
    raw=archive.read_bytes()
    if json.loads(raw)!=bundle:
        raise PipelineError("本机备份归档与当前导出不符。")
    backup_hash=sha(raw)
    result={"acknowledged":0,"pending":0}
    for report in bundle["reports"]:
        item=handoff["reports"].get(report["id"],{})
        delivery=report.get("cloudDelivery") or {}
        if not receipt(report) or report["stale"] or report["activeClaim"] or item.get("cloudDelivery",{}).get("status")!="verified":
            continue
        relative="reports/"+report["taskId"]+"/"+report["id"]
        if sha((folder/(relative+".md")).read_bytes())!=report["markdownSha256"]:
            raise PipelineError("本机报告在核验后被修改，未确认网站备份状态。")
        extensions={"guide_pdf":".pdf","guide_html":".html","exercise_archive":".zip","experiment_log":".txt","knowledge_notes":".md","review_log":".md"}
        artifacts=report["analysis"]["completion"]["artifacts"]
        for file in artifacts:
            data=(folder/(relative+"-files")/(file["role"]+extensions[file["role"]])).read_bytes()
            if sha(data)!=file["sha256"]:
                raise PipelineError("本机原件在核验后被修改，未确认网站备份状态。")
        args={"deliveryId":delivery["id"],"commit":item["git"]["commit"],"reportSha256":report["markdownSha256"],"backupBundleSha256":backup_hash,
              "artifactHashes":[{"role":f["role"],"sha256":f["sha256"]} for f in artifacts],"localKnowledge":item.get("localKnowledge",{}).get("status","pending")}
        try:
            response=post(bundle["list"]["id"],"reminder_delivery_ack_local_backup",args)
            if response.get("acknowledged") is not True or response.get("reportId")!=report["id"] or response.get("localBackup",{}).get("commit")!=args["commit"]:
                raise PipelineError("网站未确认本机备份回执。")
            item["websiteBackupAcknowledgement"]={"status":"acknowledged","receipt":response["localBackup"]}
            result["acknowledged"]+=1
        except PipelineError:
            item["websiteBackupAcknowledgement"]={"status":"pending"}
            result["pending"]+=1
        atomic_write(path,json.dumps(handoff,ensure_ascii=False,indent=2)+"\n")
    return result
