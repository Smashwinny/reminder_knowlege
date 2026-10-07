# -*- coding: utf-8 -*-
"""拾遗共享队列：分类与学习分阶段，启动范围由工作流授权策略决定。

SQLite 为认领与发布的唯一协调点；所有 Claude/Codex 必须共用本工具，
不得绕过它直接修改网站。租约到期仍占有任务，必须明确 release。
这不是学习执行器：它验证交付文件和审核记录，不能证明实验内容真实。
网站 API 没有版本条件写入，因此无法防止不合作的外部写入者在读写间改动。
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import time
import uuid
import zipfile
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
SHANGHAI = dt.timezone(dt.timedelta(hours=8), "Asia/Shanghai")
KINDS = ("learning", "non_learning", "needs_review", "duplicate", "blocked")
PENDING_MARKER = "<!-- PIPELINE_ANALYSIS_PENDING -->"
IGNORED_EXERCISE_DIRS = {"node_modules", ".venv", "venv", "env", ".git", "__pycache__",
                         "target", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache"}
PHASE_LABELS = {"pending": "待分析", "protected": "旧状态保护", "claimed": "分析已领取",
                "learning_queued": "待用户选择学习", "learning": "学习中", "ready": "学习产物待审核/发布",
                "publish_pending": "待网站确认", "synced": "网站已确认", "needs_review": "待核实",
                "analysis_confirmed": "已完成完整分析（任务由用户完成）"}
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
 task_id TEXT PRIMARY KEY, snapshot TEXT NOT NULL, content_hash TEXT NOT NULL,
 urls TEXT NOT NULL, canonical_urls TEXT NOT NULL, site_state INTEGER NOT NULL,
 deleted INTEGER NOT NULL DEFAULT 0, missing INTEGER NOT NULL DEFAULT 0,
 position INTEGER NOT NULL, legacy_status TEXT NOT NULL DEFAULT '',
 protection TEXT NOT NULL DEFAULT '', duplicate_of TEXT NOT NULL DEFAULT '',
 phase TEXT NOT NULL DEFAULT 'pending', owner TEXT, lease_until REAL,
 claim_hash TEXT, baseline_state INTEGER, baseline_legacy TEXT,
 adopted INTEGER NOT NULL DEFAULT 0, invalidated INTEGER NOT NULL DEFAULT 0,
 kind TEXT, reason TEXT, evidence TEXT, classified_hash TEXT,
 project_key TEXT, learning_started INTEGER NOT NULL DEFAULT 0,
 manifest TEXT, artifact_fingerprint TEXT, review TEXT,
 analysis_completed_at TEXT, analysis_receipt TEXT, analysis_history TEXT,
 publish_intent TEXT, publication_history TEXT, publisher TEXT, synced_at TEXT, completed_at TEXT,
 last_error TEXT, first_seen TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS resource_locks (
 resource_key TEXT PRIMARY KEY, task_id TEXT NOT NULL,
 FOREIGN KEY(task_id) REFERENCES tasks(task_id)
);
CREATE INDEX IF NOT EXISTS tasks_phase ON tasks(phase, position);
"""


class PipelineError(Exception):
    """可显示给用户的错误，不包含网站 token 或底层网络报文。"""


def dumps(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def stamp(now=None):
    return dt.datetime.fromtimestamp(time.time() if now is None else now,
                                     SHANGHAI).isoformat(timespec="seconds")


def task_hash(task):
    return hashlib.sha256(dumps({"text": task.get("text", ""),
                                 "summary": task.get("summary", "")}).encode("utf-8")).hexdigest()


def extract_urls(text):
    """保留完整原文；这里只提取 HTTP(S) 链接，不按关键词判断任务类别。"""
    result = []
    for match in re.findall(r"https?://[^\s<>\"'`，。；！？【】]+", str(text), re.I):
        value = match.rstrip(".,;:!?）]}")
        while value.endswith(")") and value.count(")") > value.count("("):
            value = value[:-1]
        try:
            if urlsplit(value).hostname and value not in result:
                result.append(value)
        except ValueError:
            continue
    return result


def canonical_url(url):
    try:
        parsed = urlsplit(url)
        if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
            raise ValueError
        if parsed.username or parsed.password:
            raise ValueError
        host = parsed.hostname.lower()
        if host in ("www.x.com", "twitter.com", "www.twitter.com", "mobile.twitter.com"):
            host = "x.com"
        port = parsed.port
        authority = "[" + host + "]" if ":" in host else host
        if port and not ((port == 443 and parsed.scheme == "https") or
                         (port == 80 and parsed.scheme == "http")):
            authority += ":" + str(port)
        query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
                 if not k.lower().startswith("utm_") and k.lower() not in
                 {"fbclid", "gclid", "mc_cid", "mc_eid"}]
        if host == "x.com":
            query = [(k, v) for k, v in query if k.lower() not in {"s", "t"}]
        scheme = "https" if host in {"x.com", "github.com"} else parsed.scheme.lower()
        return urlunsplit((scheme, authority, parsed.path.rstrip("/"),
                           urlencode(sorted(query)), ""))
    except (ValueError, TypeError):
        raise PipelineError("证据链接必须是无凭据的完整 HTTP(S) URL。") from None


def valid_id(value):
    value = str(value)
    if (not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,149}", value) or
            value.endswith(".") or value.split(".")[0].upper() in
            {"CON", "PRN", "AUX", "NUL", *["COM" + str(i) for i in range(1, 10)],
             *["LPT" + str(i) for i in range(1, 10)]}):
        raise PipelineError("任务 ID 不能安全用作文件名。")
    return value


def atomic_write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix="." + path.name + ".", suffix=".tmp",
                                    dir=str(path.parent))
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class SiteAPI:
    def __init__(self):
        try:
            from . import shiyi_sync
        except ImportError:
            import shiyi_sync
        self.module = shiyi_sync
        token = os.environ.get("SHIYI_TOKEN", "").strip()
        if not token:
            try:
                token = Path(shiyi_sync.TOKEN_FILE).read_text(encoding="utf-8").strip()
            except OSError:
                pass
        if not token:
            raise PipelineError("缺少网站凭据：配置 SHIYI_TOKEN 或 tools/.shiyi_token。")
        self._token = token

    def download(self):
        try:
            return self.module.download_tasks(self._token)
        except Exception:
            raise PipelineError("网站读取失败；可重试，尚未确认完成。") from None

    def upload(self, task):
        try:
            return self.module.upload_task(self._token, task)
        except Exception:
            raise PipelineError("网站写入结果不确定；将读取确认，可重试。") from None

    def read_analysis(self, account_id, list_id, task_id):
        """只调用 scoped identity/read 工具，不获取或写任务完成权限。"""
        if __package__:
            from .reminder_dot_http import scoped_request, ScopedRequestError
        else:
            from reminder_dot_http import scoped_request, ScopedRequestError
        try:
            def read(tool, arguments):
                return scoped_request(list_id, tool, arguments, self._token)
            identity = read("reminder_identity", {})
            if identity.get("accountId") != account_id or identity.get("listId") != list_id:
                raise PipelineError("限定账户/列表不匹配，不确认分析完成。")
            return read("reminder_read_record", {"taskId": task_id})
        except PipelineError:
            raise
        except ScopedRequestError as error:
            raise PipelineError(str(error)) from None
        except Exception:
            raise PipelineError("限定账户/列表的完整分析无法实时回读；不确认分析完成。") from None


class Pipeline:
    def __init__(self, root=ROOT, api=None, clock=time.time):
        self.root = Path(root).resolve()
        self.base = self.root / "完成"
        self.db_path = self.base / ".pipeline" / "queue.sqlite3"
        self.reports = self.base / "分析报告"
        self.records = self.base / "记录"
        self.journals = self.base / ".pipeline" / "publish"
        self.clock = clock
        self.api = api
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with contextlib.closing(self._connection()) as connection:
            connection.executescript(SCHEMA)
            columns = {row["name"] for row in connection.execute("PRAGMA table_info(tasks)")}
            if "publication_history" not in columns:
                connection.execute("ALTER TABLE tasks ADD COLUMN publication_history TEXT")
                connection.commit()
            for column in ("analysis_completed_at", "analysis_receipt", "analysis_history"):
                if column not in columns:
                    connection.execute("ALTER TABLE tasks ADD COLUMN " + column + " TEXT")
            connection.commit()

    def _connection(self):
        connection = sqlite3.connect(str(self.db_path), timeout=60)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=FULL")
        return connection

    @contextlib.contextmanager
    def _tx(self):
        connection = self._connection()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _site(self):
        if self.api is None:
            self.api = SiteAPI()
        return self.api

    def _row(self, connection, task_id):
        row = connection.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        if row is None:
            raise PipelineError("队列中没有此任务；先 sync。")
        return dict(row)

    def _update(self, connection, task_id, **values):
        current = self._row(connection, task_id)
        if all(current.get(key) == value for key, value in values.items()):
            return current
        values.setdefault("updated_at", stamp(self.clock()))
        connection.execute("UPDATE tasks SET " + ",".join(k + "=?" for k in values) +
                           " WHERE task_id=?", (*values.values(), task_id))
        return self._row(connection, task_id)

    def _legacy(self):
        result = {}
        path = self.base / "学习队列.md"
        if not path.exists():
            return result
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            if not line.startswith("|"):
                continue
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) < 2 or columns[1] in {"task_id", "---", ""}:
                continue
            state = columns[0]
            if ("进行中" in state or "完成" in state or "非学习" in state or
                    "暂停" in state or "跳过" in state):
                result[columns[1]] = state
        return result

    @staticmethod
    def _protection(row):
        reasons = []
        if row["deleted"]:
            reasons.append("网站已删除")
        if row["missing"]:
            reasons.append("本次网站快照未返回")
        if row["site_state"] != 0:
            reasons.append("网站状态 " + str(row["site_state"]))
        if row["legacy_status"]:
            reasons.append("旧队列 " + row["legacy_status"])
        return "；".join(reasons)

    @staticmethod
    def _analysis_is_current(row):
        if (row["phase"] != "analysis_confirmed" or not row.get("analysis_receipt") or
                row["invalidated"] or row["deleted"] or row["missing"]):
            return False
        try:
            receipt = json.loads(row["analysis_receipt"])
        except (ValueError, TypeError):
            return False
        return isinstance(receipt, dict) and receipt.get("source_hash") == row["content_hash"]

    @staticmethod
    def _idle_phase(row):
        if Pipeline._analysis_is_current(row):
            return "analysis_confirmed"
        if row["duplicate_of"]:
            return "needs_review"
        if row["protection"]:
            return "protected"
        if row["invalidated"]:
            return "needs_review"
        if row["kind"] == "learning":
            return "learning_queued"
        if row["kind"] == "non_learning":
            return "classified"
        if row["kind"]:
            return "needs_review"
        return "pending"

    def _phase_label(self, phase):
        if phase == "learning_queued" and self._workflow_policy().get("automatic_full_learning", False):
            return "已分类，待获准执行"
        return PHASE_LABELS.get(phase, phase)

    def _record(self, row):
        journal = self._journal(row["task_id"])
        pending_journal = bool(journal and journal.get("attempted_at") and not journal.get("cancelled_at") and
                               row["phase"] != "synced")
        phase = "publish_pending" if pending_journal and row["phase"] in {"claimed", "learning", "ready"} else row["phase"]
        complete = phase == "synced" and row["kind"] == "learning"
        analysis_complete = self._analysis_is_current(row)
        return {"task_id": row["task_id"], "status": phase, "status_label": self._phase_label(phase),
                "website_state": row["site_state"], "owner": row["owner"],
                "lease_until": stamp(row["lease_until"]) if row["lease_until"] else None,
                "source": json.loads(row["snapshot"]), "source_hash": row["content_hash"],
                "source_urls": json.loads(row["urls"]), "canonical_urls": json.loads(row["canonical_urls"]),
                "protection": row["protection"], "duplicate_of": row["duplicate_of"] or None,
                "classification": {"kind": row["kind"], "reason": row["reason"],
                                   "evidence": json.loads(row["evidence"] or "[]"),
                                   "source_hash": row["classified_hash"]},
                "learning_started": bool(row["learning_started"]), "project_key": row["project_key"],
                "manifest": json.loads(row["manifest"] or "null"),
                "quality_review": json.loads(row["review"] or "null"),
                "artifact_fingerprint": row["artifact_fingerprint"],
                "publish_intent": (journal if journal and not journal.get("cancelled_at") else None) or
                json.loads(row["publish_intent"] or "null"), "publisher": row["publisher"],
                "unresolved_publication": pending_journal,
                "publication_history": json.loads(row["publication_history"] or "[]"),
                "publication_journal": "完成/.pipeline/publish/" + row["task_id"] + ".json"
                if (self.journals / (row["task_id"] + ".json")).exists() else None,
                "report": "完成/分析报告/" + row["task_id"] + ".md",
                "website_synced": phase == "synced", "synced_at": row["synced_at"],
                "completed_at": row["completed_at"] if complete else None,
                "analysis_completed": analysis_complete,
                "analysis_completed_at": row["analysis_completed_at"] if analysis_complete else None,
                "analysis_receipt": json.loads(row["analysis_receipt"] or "null"),
                "analysis_history": json.loads(row["analysis_history"] or "[]"),
                "first_seen": row["first_seen"], "updated_at": row["updated_at"],
                "content_changed": bool(row["invalidated"]), "last_error": row["last_error"]}

    def _save_record(self, row):
        path = self.records / (row["task_id"] + ".json")
        record = self._record(row)
        if path.exists():
            try:
                previous = json.loads(path.read_text(encoding="utf-8"))
                history = previous.get("completion_history", [])
                if previous.get("completed_at") and previous["completed_at"] != record["completed_at"]:
                    entry = {"completed_at": previous["completed_at"],
                             "source_hash": previous.get("source_hash"),
                             "manifest": previous.get("manifest")}
                    if entry not in history:
                        history.append(entry)
                if history:
                    record["completion_history"] = history
            except (OSError, ValueError):
                pass
        atomic_write(path, json.dumps(record, ensure_ascii=False, indent=2) + "\n")

    def _journal(self, task_id):
        path = self.journals / (task_id + ".json")
        if not path.exists():
            return None
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(result, dict):
                raise ValueError
            return result
        except (OSError, ValueError):
            raise PipelineError("发布 journal 无法读取；停止写网站，需协调者核实。") from None

    def _save_journal(self, task_id, intent):
        # 独立于 SQLite 事务持久化：进程在服务端接受写入后退出，意图仍能恢复。
        atomic_write(self.journals / (task_id + ".json"),
                     json.dumps(intent, ensure_ascii=False, indent=2) + "\n")

    def _no_pending_publication(self, row):
        journal = self._journal(row["task_id"])
        if journal and journal.get("attempted_at") and not journal.get("cancelled_at") and row["phase"] != "synced":
            raise PipelineError("存在持久化的待确认网站写入；先 publish 重试确认，不能修改分类或产物。")

    def _source_report(self, row, historical=""):
        snapshot = json.loads(row["snapshot"])
        links = "\n".join("- " + url for url in json.loads(row["urls"])) or "- 原文未提取到完整 HTTP(S) 链接。"
        content = (f"# 拾遗记录分析 · {row['task_id']}\n\n"
                   f"- 首次记录：{row['first_seen']}（Asia/Shanghai）\n"
                   f"- 当前来源快照：{row['updated_at']}\n"
                   f"- 采集时网站状态：{row['site_state']}\n"
                   f"- 来源哈希：`{row['content_hash']}`\n"
                   f"- 保护原因：{row['protection'] or '无'}\n"
                   f"- 重复记录：{row['duplicate_of'] or '未发现相同规范化 URL'}\n\n"
                   "## 原始内容（完整保留）\n\n" + str(snapshot.get("text", "")) + "\n\n"
                   "## 网站摘要（线索，尚未核实）\n\n" + str(snapshot.get("summary") or "无摘要") + "\n\n"
                   "## 原链接\n\n" + links + "\n\n"
                   "## 分析与进度\n\n" + PENDING_MARKER + "\n"
                   "尚未完成内容分析，未执行 learn-project，未完成学习。"
                   "网站进行中/已完成与旧队列状态仅作为保护依据，不能证明本流水线完成学习。\n")
        if historical:
            content += "\n## 历史分析（旧来源快照，须重新核实）\n\n" + historical
        return content

    @staticmethod
    def _tasks(snapshot):
        if isinstance(snapshot, dict):
            snapshot = snapshot.get("tasks")
        if not isinstance(snapshot, list):
            raise PipelineError("快照必须是任务数组或 {tasks: [...]}。")
        ids = set()
        result = []
        for item in snapshot:
            if not isinstance(item, dict) or "id" not in item:
                raise PipelineError("快照中有无 ID 的任务。")
            task = dict(item)
            task["id"] = valid_id(task["id"])
            if task["id"] in ids:
                raise PipelineError("快照包含重复任务 ID。")
            ids.add(task["id"])
            if task.get("state", 0) not in (0, 1, 2, 3):
                raise PipelineError("网站任务状态必须为 0/1/2/3。")
            result.append(task)
        return result

    def sync(self, snapshot=None):
        supplied_snapshot = snapshot is not None
        tasks = self._tasks(snapshot) if snapshot is not None else None
        with self._tx() as connection:
            # 与 publish 使用同一事务锁：下载过程也不得和本流水线发布交错。
            if tasks is None:
                tasks = self._tasks(self._site().download())
            legacy = self._legacy()
            counts = {"new": 0, "changed": 0, "stale": 0, "total": len(tasks)}
            returned_ids = {task["id"] for task in tasks}
            for existing in connection.execute("SELECT task_id FROM tasks").fetchall():
                if existing["task_id"] not in returned_ids:
                    self._update(connection, existing["task_id"], missing=1)
            changed_reports = {}
            for position, task in enumerate(tasks):
                task_id = task["id"]
                old = connection.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
                if old is not None:
                    local_snapshot = json.loads(old["snapshot"])
                    # 文件快照可能早于本地已确认发布；实时下载以当前网站为准，
                    # 即使不合作的外部写者未递增 updatedAt，也不能隐藏网站重开。
                    if supplied_snapshot and self._site_version(task) < self._site_version(local_snapshot):
                        counts["stale"] += 1
                        self._update(connection, task_id, missing=0)
                        continue
                urls = extract_urls(task.get("text", ""))
                canonical = []
                for url in urls:
                    try:
                        value = canonical_url(url)
                    except PipelineError:
                        continue
                    if value not in canonical:
                        canonical.append(value)
                now = stamp(self.clock())
                values = {"snapshot": dumps(task), "content_hash": task_hash(task),
                          "urls": dumps(urls), "canonical_urls": dumps(canonical),
                          "site_state": int(task.get("state", 0)), "deleted": int(bool(task.get("deleted"))),
                          "missing": 0, "position": position, "legacy_status": legacy.get(task_id, "")}
                if old is None:
                    connection.execute("INSERT INTO tasks(task_id,snapshot,content_hash,urls,canonical_urls,"
                                       "site_state,deleted,missing,position,legacy_status,first_seen,updated_at) "
                                       "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                                       (task_id, *values.values(), now, now))
                    changed_reports[task_id] = ""
                    counts["new"] += 1
                else:
                    changed = old["content_hash"] != values["content_hash"]
                    if changed:
                        counts["changed"] += 1
                        report = self.reports / (task_id + ".md")
                        changed_reports[task_id] = report.read_text(encoding="utf-8") if report.exists() else ""
                        values.update(invalidated=int(bool(old["owner"] or old["kind"])),
                                      manifest=None, artifact_fingerprint=None, review=None,
                                      publish_intent=None, last_error="来源原文或摘要变更，原分析须重新核实。")
                        if old["owner"] or old["kind"]:
                            values["phase"] = "needs_review"
                        values.update(self._invalidate_analysis(dict(old), "原文或摘要发生变化"))
                    self._update(connection, task_id, **values)
            # 同 URL 以当前已确认分析优先；其他记录按队列首次插入顺序选锚。
            # 不使用网站 position，避免新记录排在前面而抢走旧成果的来源锚。
            # rowid 保留插入先后，也避免 first_seen 秒级时间相同造成新任务抢锚。
            seen = {}
            anchors = [dict(raw) for raw in connection.execute("SELECT rowid AS ingest_order,* FROM tasks").fetchall()]
            anchors.sort(key=lambda row: (0 if self._analysis_is_current(row) else 1, row["ingest_order"]))
            for row in anchors:
                duplicate = next((seen[url] for url in json.loads(row["canonical_urls"])
                                  if url in seen and seen[url] != row["task_id"]), "")
                if not row["deleted"] and not row["missing"]:
                    for url in json.loads(row["canonical_urls"]):
                        seen.setdefault(url, row["task_id"])
                row["legacy_status"] = legacy.get(row["task_id"], "")
                row["duplicate_of"] = duplicate
                row["protection"] = self._protection(row)
                values = {"duplicate_of": duplicate, "legacy_status": row["legacy_status"],
                          "protection": row["protection"]}
                if row["phase"] != "synced" and not row["owner"]:
                    values["phase"] = self._idle_phase(row)
                target = 3 if row["kind"] == "learning" else 1
                if row["phase"] == "synced" and (row["deleted"] or row["missing"] or row["site_state"] != target):
                    values.update(phase="needs_review", invalidated=1,
                                  last_error="网站已重开、删除或缺失；历史完成保留，当前不能列作确认完成。")
                if row["analysis_receipt"] and (row["deleted"] or row["missing"]):
                    values.update(self._invalidate_analysis(row, "原记录删除或缺失"),
                                  phase="needs_review", invalidated=1,
                                  last_error="原记录删除或缺失；完整分析保留为历史，当前待核实。")
                if row["owner"] and duplicate:
                    values.update(invalidated=1, phase="needs_review", last_error="发现同 URL 记录，须明确核实。")
                updated = self._update(connection, row["task_id"], **values)
                if row["task_id"] in changed_reports:
                    atomic_write(self.reports / (row["task_id"] + ".md"),
                                 self._source_report(updated, changed_reports[row["task_id"]]))
                self._save_record(updated)
        return counts

    def _invalidate_analysis(self, row, reason):
        if not row.get("analysis_receipt"):
            return {}
        history = json.loads(row["analysis_history"] or "[]")
        history.append({"analysis_completed_at": row["analysis_completed_at"],
                        "receipt": json.loads(row["analysis_receipt"]),
                        "manifest": json.loads(row["manifest"] or "null"),
                        "quality_review": json.loads(row["review"] or "null"),
                        "invalidated_at": stamp(self.clock()), "reason": reason})
        return {"analysis_completed_at": None, "analysis_receipt": None, "analysis_history": dumps(history)}

    @staticmethod
    def _site_version(task):
        try:
            return int(task.get("updatedAt") or 0)
        except (TypeError, ValueError):
            return 0

    def _owner_name(self, name):
        if not name or not name.strip() or len(name) > 100 or any(ord(ch) < 32 for ch in name):
            raise PipelineError("owner 必须是简短且稳定的代理名称。")
        return name.strip()

    def _project_key(self, value):
        value = str(value).strip().replace("\\", "/")
        if not value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
            raise PipelineError("project 必须是仓库内的相对项目目录。")
        path = (self.root / value).resolve()
        if path == self.root or not path.is_relative_to(self.root):
            raise PipelineError("project 不能越出仓库或指向仓库根目录。")
        return path.relative_to(self.root).as_posix().casefold()

    def _lock(self, connection, task_id, key):
        old = connection.execute("SELECT task_id FROM resource_locks WHERE resource_key=?", (key,)).fetchone()
        if old and old["task_id"] != task_id:
            raise PipelineError("此 URL 或项目已由另一任务占有；即使租约过期也需先 release。")
        connection.execute("INSERT OR IGNORE INTO resource_locks(resource_key,task_id) VALUES(?,?)", (key, task_id))

    def _owned(self, connection, task_id, owner, allow_expired=False):
        row = self._row(connection, task_id)
        if row["owner"] != owner:
            raise PipelineError("任务未被此 owner 认领。")
        if not row["lease_until"] or (row["lease_until"] <= self.clock() and not allow_expired):
            raise PipelineError("认领租约已到期；不会自动抢活，请原 owner 明确 renew 或 release。")
        if row["invalidated"] or row["claim_hash"] != row["content_hash"]:
            raise PipelineError("来源已变更或认领已失效；请 release 后重新分析。")
        if row["duplicate_of"] or row["deleted"] or row["missing"]:
            raise PipelineError("任务为重复、删除或缺失记录，不能继续发布。")
        legacy = self._legacy().get(task_id, "")
        if legacy and legacy != row["baseline_legacy"]:
            raise PipelineError("旧队列状态发生变化，停止处理以避免相互干扰。")
        keys = ["url:" + url for url in json.loads(row["canonical_urls"])]
        if row["project_key"]:
            keys.append("project:" + row["project_key"])
        for key in keys:
            lock = connection.execute("SELECT task_id FROM resource_locks WHERE resource_key=?", (key,)).fetchone()
            if not lock or lock["task_id"] != task_id:
                raise PipelineError("任务资源锁失效，须协调者核实。")
        return row

    def _claim_row(self, connection, row, owner, lease_seconds, project=None, adopt=False):
        if row["phase"] == "analysis_confirmed":
            raise PipelineError("当前来源的完整分析已确认；不再领取或重复学习，任务完成由用户点击。")
        if not 30 <= lease_seconds <= 86400:
            raise PipelineError("租约秒数范围为 30 至 86400；学习中应及时 renew。")
        if row["owner"]:
            raise PipelineError("任务已有 owner；过期租约也不能自动接管，必须明确 release。")
        journal = self._journal(row["task_id"])
        if journal and journal.get("attempted_at") and not journal.get("confirmed_at") and not journal.get("cancelled_at"):
            raise PipelineError("此任务有崩溃后保留的待确认网站写入；须原 owner 确认，不能另行接管。")
        if row["duplicate_of"] or row["deleted"] or row["missing"]:
            raise PipelineError("重复、删除或缺失记录保留待审，不可认领。")
        legacy = self._legacy().get(row["task_id"], "")
        if row["site_state"] == 3 or "完成" in legacy or "非学习" in legacy or "跳过" in legacy:
            raise PipelineError("已完成或非学习旧记录受保护，不能接管。")
        if not adopt and (row["site_state"] != 0 or legacy or row["protection"]):
            raise PipelineError("网站或旧队列正在使用此任务；只有确认旧代理停止后 adopt --ack-stopped 可接管。")
        if row["invalidated"]:
            # 无 owner 的旧分类失效后，明确按 ID 重新认领才会清除它。
            row = self._update(connection, row["task_id"], invalidated=0, kind=None, reason=None,
                               evidence=None, classified_hash=None, learning_started=0)
        for url in json.loads(row["canonical_urls"]):
            self._lock(connection, row["task_id"], "url:" + url)
        key = self._project_key(project) if project else None
        if key:
            self._lock(connection, row["task_id"], "project:" + key)
        row = self._update(connection, row["task_id"], phase="claimed", owner=owner,
                           lease_until=self.clock() + lease_seconds, claim_hash=row["content_hash"],
                           baseline_state=row["site_state"], baseline_legacy=legacy,
                           adopted=int(adopt), project_key=key, last_error=None)
        self._save_record(row)
        return self._record(row)

    def claim(self, owner, task_id=None, lease_seconds=3600, project=None):
        owner = self._owner_name(owner)
        with self._tx() as connection:
            if task_id:
                row = self._row(connection, task_id)
                if row["phase"] == "synced":
                    raise PipelineError("任务已同步，无需再次认领。")
                return self._claim_row(connection, row, owner, lease_seconds, project)
            candidates = connection.execute("SELECT * FROM tasks WHERE phase='pending' AND owner IS NULL "
                                            "AND kind IS NULL ORDER BY position,first_seen,task_id").fetchall()
            for raw in candidates:
                row = dict(raw)
                # 自动 claim 仅取一个未分类、未受保护任务；学习队列须用户指定 start。
                if (row["site_state"] != 0 or row["protection"] or row["duplicate_of"] or
                        self._legacy().get(row["task_id"])):
                    continue
                if any(connection.execute("SELECT 1 FROM resource_locks WHERE resource_key=?",
                                          ("url:" + url,)).fetchone() for url in json.loads(row["canonical_urls"])):
                    continue
                return self._claim_row(connection, row, owner, lease_seconds, project)
            return {"status": "empty", "message": "没有可自动认领的未分类任务。"}

    def adopt(self, task_id, owner, ack_stopped=False, lease_seconds=3600, project=None):
        if not ack_stopped:
            raise PipelineError("明确确认旧代理已停止后，使用 --ack-stopped 接管。")
        with self._tx() as connection:
            return self._claim_row(connection, self._row(connection, task_id),
                                   self._owner_name(owner), lease_seconds, project, adopt=True)

    def renew(self, task_id, owner, lease_seconds=3600):
        if not 30 <= lease_seconds <= 86400:
            raise PipelineError("租约秒数范围为 30 至 86400。")
        with self._tx() as connection:
            self._owned(connection, task_id, owner, allow_expired=True)
            row = self._update(connection, task_id, lease_until=self.clock() + lease_seconds)
            self._save_record(row)
            return self._record(row)

    def release(self, task_id, owner, reason=""):
        with self._tx() as connection:
            row = self._row(connection, task_id)
            if row["phase"] == "analysis_confirmed" and row["owner"] is None:
                if json.loads(row["analysis_receipt"] or "{}").get("owner") != owner:
                    raise PipelineError("已确认分析仅允许原 owner 幂等释放。")
                return self._record(row)
            if row["owner"] != owner:
                raise PipelineError("只有记录中的 owner 可以 release；可由协调者使用该名称明确释放。")
            journal = self._journal(task_id)
            intent = journal or json.loads(row["publish_intent"] or "null")
            if intent and intent.get("attempted_at") and not intent.get("cancelled_at") and row["phase"] != "synced":
                raise PipelineError("网站写入结果尚未确认：先 renew/publish 重试确认；不能丢弃待确认写入。")
            connection.execute("DELETE FROM resource_locks WHERE task_id=?", (task_id,))
            values = {"owner": None, "lease_until": None, "claim_hash": None,
                      "project_key": None, "learning_started": 0, "adopted": 0,
                      "manifest": None, "artifact_fingerprint": None, "review": None,
                      "publish_intent": None, "last_error": reason or row["last_error"]}
            if row["invalidated"]:
                values.update(invalidated=0, kind=None, reason=None, evidence=None, classified_hash=None)
            row.update(values)
            values["phase"] = self._idle_phase(row)
            row = self._update(connection, task_id, **values)
            self._save_record(row)
            if journal and not journal.get("attempted_at"):
                (self.journals / (task_id + ".json")).unlink(missing_ok=True)
            return self._record(row)

    def bind_project(self, task_id, owner, project):
        key = self._project_key(project)
        with self._tx() as connection:
            row = self._owned(connection, task_id, owner)
            self._no_pending_publication(row)
            if row["project_key"] and row["project_key"] != key:
                raise PipelineError("此认领已绑定其他项目；请 release 后重新规划。")
            self._lock(connection, task_id, "project:" + key)
            row = self._update(connection, task_id, project_key=key)
            self._save_record(row)
            return self._record(row)

    def classify(self, task_id, owner, kind, reason, evidence):
        if kind not in KINDS or not reason or not reason.strip():
            raise PipelineError("分类需明确 kind 和内容分析理由。")
        if not evidence:
            raise PipelineError("分类必须记录至少一个已核实的 HTTP(S) 证据链接。")
        for url in evidence:
            canonical_url(url)
        with self._tx() as connection:
            row = self._owned(connection, task_id, owner)
            self._no_pending_publication(row)
            if row["publish_intent"] and json.loads(row["publish_intent"]).get("attempted_at"):
                raise PipelineError("存在待确认网站写入，须先 publish 核实。")
            phase = "learning" if kind == "learning" and row["learning_started"] else "claimed"
            row = self._update(connection, task_id, kind=kind, reason=reason.strip(), evidence=dumps(evidence),
                               classified_hash=row["content_hash"], manifest=None, review=None,
                               artifact_fingerprint=None, publish_intent=None, phase=phase)
            path = self.reports / (task_id + ".md")
            content = path.read_text(encoding="utf-8") if path.exists() else self._source_report(row)
            content = content.replace(PENDING_MARKER, "<!-- PIPELINE_ANALYSIS_RECORDED -->")
            content = content.replace("尚未完成内容分析，未执行 learn-project，未完成学习。",
                                      "内容分析与证据已记录；学习进度以队列及后续的学习和网站确认记录为准。")
            content += (f"\n## 内容分析 · {stamp(self.clock())}\n\n"
                        f"- 分析者：{owner}\n- 判断：{kind}\n- 本次来源哈希：`{row['content_hash']}`\n\n"
                        + reason.strip() + "\n\n### 证据\n\n" + "\n".join("- " + u for u in evidence) +
                        "\n\n" + self._classification_progress(kind, bool(row["learning_started"])) + "\n")
            atomic_write(path, content)
            self._save_record(row)
            return self._record(row)

    @staticmethod
    def _classification_progress(kind, learning_started):
        if kind == "learning":
            return ("用户已选择开始学习；本次分析不代表学习完成。" if learning_started else
                    "学习主题已进入待用户选择队列；本次分类不代表学习已完成。")
        if kind == "non_learning":
            return "非学习内容分析已记录；若需要标记网站进行中，由协调者统一 publish，不计入学习完成。"
        return {"needs_review": "证据尚不足，保留待核实；不标记为非学习或学习完成。",
                "duplicate": "发现重复主题或来源，保留增补核实；不自动沿用已有成果标记完成。",
                "blocked": "当前处理受阻，保留原因和证据；不标记为非学习或学习完成。"}[kind]

    def start(self, task_id, owner, project, lease_seconds=3600):
        """人工选择入口：只能开始已有证据分类的 learning，不能批量启动。"""
        owner = self._owner_name(owner)
        key = self._project_key(project)
        with self._tx() as connection:
            row = self._row(connection, task_id)
            if row["phase"] == "analysis_confirmed":
                raise PipelineError("当前来源完整分析已确认，不能重新 start；用户任务状态独立。")
            if row["kind"] != "learning" or row["classified_hash"] != row["content_hash"] or row["invalidated"]:
                raise PipelineError("需先对当前来源完成 learning 分类，然后由用户选择 start。")
            if not row["owner"]:
                self._claim_row(connection, row, owner, lease_seconds, project)
                row = self._row(connection, task_id)
            row = self._owned(connection, task_id, owner)
            self._no_pending_publication(row)
            if row["project_key"] and row["project_key"] != key:
                raise PipelineError("认领与学习项目不一致。")
            self._lock(connection, task_id, "project:" + key)
            row = self._update(connection, task_id, learning_started=1, project_key=key, phase="learning")
            self._save_record(row)
            return self._record(row)

    def _path(self, value, is_dir=False):
        if not isinstance(value, str) or not value.strip():
            raise PipelineError("产物清单缺少文件或目录路径。")
        path = Path(value)
        path = (path if path.is_absolute() else self.root / path).resolve()
        if path == self.root or not path.is_relative_to(self.root):
            raise PipelineError("产物路径必须在仓库内部，禁止 ../ 或链接逃逸。")
        if is_dir:
            if not path.is_dir():
                raise PipelineError("产物目录不存在。")
        elif not path.is_file() or path.stat().st_size == 0:
            raise PipelineError("产物文件不存在或为空。")
        return path

    @staticmethod
    def _file_hash(path):
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    def _validate_manifest(self, row, manifest):
        if not isinstance(manifest, dict):
            raise PipelineError("manifest 必须是 JSON 对象。")
        result = dict(manifest)
        result["topic"] = manifest.get("topic") or manifest.get("theme") or manifest.get("主题")
        if not isinstance(result["topic"], str) or not result["topic"].strip():
            raise PipelineError("manifest 需要 topic（主题）。")
        paths = {}
        for name in ("project_dir", "pdf", "html", "exercise_dir", "experiment_log", "vault_note"):
            paths[name] = self._path(manifest.get(name), is_dir=name in ("project_dir", "exercise_dir"))
            result[name] = paths[name].relative_to(self.root).as_posix()
        if self._project_key(result["project_dir"]) != row["project_key"]:
            raise PipelineError("manifest 项目目录必须与开始学习前绑定的项目锁一致。")
        for name in ("pdf", "html", "exercise_dir", "experiment_log"):
            if not paths[name].is_relative_to(paths["project_dir"]):
                raise PipelineError("PDF、HTML、实验与日志必须属于绑定项目目录。")
        if not paths["vault_note"].is_relative_to(self.root / "vault"):
            raise PipelineError("知识笔记必须放入本仓库 vault。")
        with paths["pdf"].open("rb") as stream:
            if stream.read(5) != b"%PDF-":
                raise PipelineError("PDF 头无效，不能用普通文件伪装 PDF。")
        if paths["experiment_log"].stat().st_size < 20:
            raise PipelineError("实验实测日志过短；记录命令、真实输出和限制。")
        report = self._path(manifest.get("report_path", "完成/分析报告/" + row["task_id"] + ".md"))
        if PENDING_MARKER in report.read_text(encoding="utf-8") or report.stat().st_size < 200:
            raise PipelineError("学习分析报告仍是待分析占位或没有填充。")
        result["report_path"] = report.relative_to(self.root).as_posix()
        urls = manifest.get("source_urls")
        if not isinstance(urls, list) or not urls:
            raise PipelineError("manifest 需要非空 source_urls。")
        for url in urls:
            if not isinstance(url, str):
                raise PipelineError("source_urls 只能包含 HTTP(S) 字符串。")
            canonical_url(url)
        # 至少带回原记录或分类证据来源，不能用无关 URL 作为完成证据。
        known = set(json.loads(row["canonical_urls"])) | {canonical_url(u) for u in json.loads(row["evidence"] or "[]")}
        if not known.intersection(canonical_url(u) for u in urls):
            raise PipelineError("source_urls 必须关联当前记录或分类证据。")
        files = [paths[n] for n in ("pdf", "html", "experiment_log", "vault_note")] + [report]
        exercise_files = []
        explicit_files = manifest.get("experiment_files")
        if explicit_files is not None:
            if not isinstance(explicit_files, list) or not explicit_files:
                raise PipelineError("experiment_files 应为非空的仓库相对实验文件列表。")
            for value in explicit_files:
                path = self._path(value)
                if not path.is_relative_to(paths["exercise_dir"]):
                    raise PipelineError("experiment_files 必须属于 exercise_dir。")
                if any(part.casefold() in IGNORED_EXERCISE_DIRS
                       for part in path.relative_to(paths["exercise_dir"]).parts[:-1]):
                    raise PipelineError("依赖缓存不能充当实验产物。")
                exercise_files.append(path)
            result["experiment_files"] = [p.relative_to(self.root).as_posix() for p in exercise_files]
        else:
            total_bytes = 0
            for folder, directories, names in os.walk(paths["exercise_dir"], followlinks=False):
                directories[:] = [name for name in directories if name.casefold() not in IGNORED_EXERCISE_DIRS]
                for name in directories:
                    if not (Path(folder) / name).resolve().is_relative_to(self.root):
                        raise PipelineError("实验目录含仓库外链接。")
                for name in names:
                    path = Path(folder) / name
                    if not path.resolve().is_relative_to(self.root):
                        raise PipelineError("实验目录含仓库外链接。")
                    size = path.stat().st_size
                    if path.is_file() and size:
                        exercise_files.append(path)
                        total_bytes += size
                        if len(exercise_files) > 2000 or total_bytes > 256 * 1024 * 1024:
                            raise PipelineError("实验目录过大；请用 manifest 的 experiment_files 明确列出需要验收的实验文件。")
        if not exercise_files:
            raise PipelineError("exercise_dir 为空；仅有 PDF 不能视为完成学习。")
        # 实验不能只有一份日志，至少另有代码、数据或可运行的操作步骤。
        if not any(path.resolve() != paths["experiment_log"] for path in exercise_files):
            raise PipelineError("实验目录只有日志；需补充实际练习产物。")
        files += exercise_files
        hashes = {p.resolve().relative_to(self.root).as_posix(): self._file_hash(p) for p in files}
        fingerprint = hashlib.sha256(dumps(hashes).encode("utf-8")).hexdigest()
        return result, fingerprint

    def ready(self, task_id, owner, manifest):
        with self._tx() as connection:
            row = self._owned(connection, task_id, owner)
            self._no_pending_publication(row)
            if row["kind"] != "learning" or not row["learning_started"]:
                raise PipelineError("学习需由用户选择 start 后才能 ready；分类排队不能标完成。")
            result, fingerprint = self._validate_manifest(row, manifest)
            row = self._update(connection, task_id, manifest=dumps(result), artifact_fingerprint=fingerprint,
                               review=None, phase="ready", last_error=None)
            self._save_record(row)
            return self._record(row)

    def review(self, task_id, owner, reviewer, notes):
        reviewer = self._owner_name(reviewer)
        if reviewer == owner or not notes or not notes.strip():
            raise PipelineError("学习产物需由不同 reviewer 审核并记录具体意见。")
        with self._tx() as connection:
            row = self._owned(connection, task_id, owner)
            self._no_pending_publication(row)
            if row["kind"] != "learning" or not row["manifest"] or row["phase"] != "ready":
                raise PipelineError("需先 ready 提交完整学习产物。")
            _, fingerprint = self._validate_manifest(row, json.loads(row["manifest"]))
            if fingerprint != row["artifact_fingerprint"]:
                raise PipelineError("产物在 ready 后变更；请重新 ready 并审核。")
            review = {"reviewer": reviewer, "approved": True, "notes": notes.strip(),
                      "reviewed_at": stamp(self.clock()), "artifact_fingerprint": fingerprint}
            row = self._update(connection, task_id, review=dumps(review))
            self._save_record(row)
            return self._record(row)

    def _require_coordinator(self, coordinator):
        try:
            try:
                from . import reminder_coordinator
            except ImportError:
                import reminder_coordinator
            reminder_coordinator.require_owner(self.root, coordinator or "")
        except (RuntimeError, ValueError, ImportError):
            raise PipelineError("确认完整分析需有效的全局协调者租约。") from None

    def _verify_analysis_receipt(self, row, manifest, receipt):
        """核验网站私有备份及其六份真实产物；receipt 本身不作为成功凭据。"""
        if not isinstance(receipt, dict) or receipt.get("schema") != "reminder-analysis-confirmation-v1":
            raise PipelineError("不是已支持的完整分析确认 receipt。")
        for key in ("accountId", "listId", "reportId"):
            valid_id(receipt.get(key, ""))
        if receipt.get("taskId") != row["task_id"] or receipt.get("sourceHash") != row["content_hash"]:
            raise PipelineError("确认 receipt 的任务或来源版本不符。")
        expected_hash = receipt.get("backupSha256", "")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise PipelineError("receipt 缺少严格的备份 SHA256。")
        folder = self.base / ".pipeline" / "dot" / receipt["accountId"] / receipt["listId"]
        bundle_file, handoff_file = self._path(receipt.get("backupBundle")), self._path(receipt.get("handoff"))
        if (bundle_file != (folder / "exports" / (expected_hash + ".json")).resolve() or
                handoff_file != (folder / "handoff.json").resolve()):
            raise PipelineError("receipt 必须指向同账户/列表的既有私有备份与交接账本。")
        if bundle_file.stat().st_size > 512 * 1024 * 1024:
            raise PipelineError("确认备份过大，停止读取。")
        raw = bundle_file.read_bytes()
        checksum = bundle_file.with_suffix(".sha256")
        if (hashlib.sha256(raw).hexdigest() != expected_hash or not checksum.is_file() or
                checksum.read_text(encoding="utf-8").strip() != expected_hash):
            raise PipelineError("备份原件或校验副本损坏，不确认分析完成。")
        try:
            bundle = json.loads(raw)
            handoff = json.loads(handoff_file.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            raise PipelineError("备份或交接账本无法解析。") from None
        if (not isinstance(bundle, dict) or bundle.get("schema") != "reminder-dot-export-v1" or
                bundle.get("accountId") != receipt["accountId"] or
                not isinstance(bundle.get("list"), dict) or bundle["list"].get("id") != receipt["listId"] or
                not isinstance(bundle.get("reports"), list) or
                not isinstance(handoff, dict) or handoff.get("schema") != "reminder-dot-handoff-v1" or
                handoff.get("accountId") != receipt["accountId"] or handoff.get("listId") != receipt["listId"]):
            raise PipelineError("备份或交接账本超出指定账户/列表范围。")
        matches = [r for r in bundle["reports"] if isinstance(r, dict) and r.get("id") == receipt["reportId"]]
        if len(matches) != 1:
            raise PipelineError("备份中必须唯一包含指定完整分析报告。")
        report = matches[0]
        if (report.get("taskId") != row["task_id"] or report.get("sourceHash") != row["content_hash"] or
                report.get("userId") != receipt["accountId"] or report.get("listId") != receipt["listId"] or
                report.get("stale") is not False or not isinstance(report.get("record"), dict) or
                report["record"].get("id") != row["task_id"] or task_hash(report["record"]) != row["content_hash"]):
            raise PipelineError("备份报告已过期或来源/授权范围不符。")
        analysis = report.get("analysis")
        completion = analysis.get("completion") if isinstance(analysis, dict) else None
        if (not isinstance(analysis, dict) or analysis.get("stage") != "full" or analysis.get("kind") != "learning" or
                not isinstance(completion, dict) or not completion.get("reviewer") or
                completion.get("reviewer") == report.get("owner") or
                not all(completion.get(key) is True for key in ("pdfRendered", "experimentChecked", "knowledgeChecked"))):
            raise PipelineError("备份不是经独立审核的完整学习分析。")
        reports = handoff.get("reports")
        item = reports.get(receipt["reportId"]) if isinstance(reports, dict) else None
        if (not isinstance(item, dict) or item.get("taskId") != row["task_id"] or
                item.get("sourceHash") != row["content_hash"] or item.get("analysisStage") != "full" or
                item.get("markdownSha256") != report.get("markdownSha256") or
                not isinstance(item.get("cloud"), dict) or item["cloud"].get("status") != "saved" or
                item["cloud"].get("staleAtExport") is not False or
                not bundle.get("exportedAt") or item["cloud"].get("exportedAt") != bundle["exportedAt"] or
                not isinstance(item.get("local"), dict) or item["local"].get("status") != "verified"):
            raise PipelineError("本次备份交接账本没有匹配的云端保存/本机校验证据。")
        report_base = folder / "reports" / row["task_id"] / receipt["reportId"]
        report_markdown_file = Path(str(report_base) + ".md")
        markdown = report.get("markdown")
        if (not isinstance(markdown, str) or
                hashlib.sha256(markdown.encode("utf-8")).hexdigest() != report.get("markdownSha256") or
                self._file_hash(self._path(str(report_markdown_file))) != report.get("markdownSha256") or
                self._path(str(folder / item["local"].get("report", ""))) != report_markdown_file.resolve() or
                self._path(str(folder / item["local"].get("artifacts", "")), is_dir=True) !=
                Path(str(report_base) + "-files").resolve()):
            raise PipelineError("备份报告正文或本地报告路径校验失败。")
        role_extensions = {"guide_pdf": ".pdf", "guide_html": ".html", "exercise_archive": ".zip",
                           "experiment_log": ".txt", "knowledge_notes": ".md", "review_log": ".md"}
        artifacts = completion.get("artifacts")
        if (not isinstance(artifacts, list) or len(artifacts) != 6 or
                any(not isinstance(a, dict) for a in artifacts) or
                {a.get("role") for a in artifacts} != set(role_extensions)):
            raise PipelineError("完整分析必须有六类真实产物，不能仅凭报告或 PDF 确认。")
        data, total_bytes = {}, 0
        for artifact in artifacts:
            try:
                blob = base64.b64decode(artifact.get("base64", ""), validate=True)
            except (ValueError, TypeError):
                raise PipelineError("备份产物编码损坏。") from None
            role = artifact["role"]
            total_bytes += len(blob)
            backup_file = self._path(str(Path(str(report_base) + "-files") / (role + role_extensions[role])))
            if (len(blob) < 20 or total_bytes > 1000000 or len(blob) != artifact.get("bytes") or
                    hashlib.sha256(blob).hexdigest() != artifact.get("sha256") or
                    self._file_hash(backup_file) != artifact.get("sha256")):
                raise PipelineError("完整分析的实际产物缺失或单文件校验失败。")
            data[role] = blob
        if (not data["guide_pdf"].startswith(b"%PDF-") or b"%%EOF" not in data["guide_pdf"][-1024:] or
                not re.search(rb"<(?:!doctype html|html)\b", data["guide_html"], re.I)):
            raise PipelineError("备份 PDF/HTML 格式无效。")
        for role, key in (("guide_pdf", "pdf"), ("guide_html", "html"), ("experiment_log", "experiment_log")):
            if hashlib.sha256(data[role]).hexdigest() != self._file_hash(self._path(manifest[key])):
                raise PipelineError("网站已保存产物与本地已审核学习产物不一致。")
        knowledge = item.get("knowledge", {})
        if hashlib.sha256(data["knowledge_notes"]).hexdigest() != self._file_hash(self._path(manifest["vault_note"])):
            if (not isinstance(knowledge, dict) or knowledge.get("status") != "merged" or
                    self._path(knowledge.get("note")) != self._path(manifest["vault_note"])):
                raise PipelineError("知识提案变更后缺少对应已审核笔记的协调者合并记录。")
        exercise = self._path(manifest["exercise_dir"], is_dir=True)
        project = self._path(manifest["project_dir"], is_dir=True)
        try:
            with zipfile.ZipFile(io.BytesIO(data["exercise_archive"])) as archive:
                entries = [entry for entry in archive.infolist() if not entry.is_dir()]
                if (not entries or len(entries) > 2000 or
                        sum(entry.file_size for entry in entries) > 64 * 1024 * 1024 or
                        len({entry.filename for entry in entries}) != len(entries)):
                    raise PipelineError("实验归档为空、重复或超过核验范围。")
                # 一些完整 ZIP 用独立的包名包装同一实验目录。仅当所有文件
                # 共用同一层前缀时支持解包后的目录；不能逐文件随意去路径。
                prefixes = {entry.filename.split("/", 1)[0] for entry in entries}
                wrapped = len(prefixes) == 1 and all("/" in entry.filename for entry in entries)
                for entry in entries:
                    name = entry.filename
                    if (name.startswith("/") or "\\" in name or ":" in name or ".." in name.split("/") or
                            any(part.casefold() in IGNORED_EXERCISE_DIRS for part in name.split("/"))):
                        raise PipelineError("实验归档含越界路径或依赖缓存。")
                # 整包必须共享一种布局，不允许各成员混合挑选不同候选路径。
                modes = [(exercise, False), (project, False)]
                if wrapped:
                    modes.append((exercise, True))
                matched = False
                for base, strip_prefix in modes:
                    all_match = True
                    for entry in entries:
                        name = entry.filename.split("/", 1)[1] if strip_prefix else entry.filename
                        local_file = (base / name).resolve()
                        if (not local_file.is_relative_to(exercise) or not local_file.is_file() or
                                hashlib.sha256(archive.read(entry)).hexdigest() != self._file_hash(local_file)):
                            all_match = False
                            break
                    if all_match:
                        matched = True
                        break
                if not matched:
                    raise PipelineError("网站实验归档未匹配本地已审核的实际实验文件。")
        except (zipfile.BadZipFile, RuntimeError, OSError):
            raise PipelineError("实验归档无法核验。") from None
        return report, {"schema": receipt["schema"], "account_id": receipt["accountId"], "list_id": receipt["listId"],
                        "report_id": receipt["reportId"], "source_hash": row["content_hash"],
                        "backup_bundle": bundle_file.relative_to(self.root).as_posix(), "backup_sha256": expected_hash,
                        "handoff": handoff_file.relative_to(self.root).as_posix(),
                        "markdown_sha256": report["markdownSha256"], "exported_at": bundle["exportedAt"]}

    def confirm_analysis(self, task_id, owner, receipt, coordinator):
        """确认分析交付并释放资源；始终只读网站，永不标记用户任务完成。"""
        self._require_coordinator(coordinator)
        with self._tx() as connection:
            row = self._row(connection, task_id)
            previous = json.loads(row["analysis_receipt"] or "null")
            repeat = row["phase"] == "analysis_confirmed" and previous is not None
            if repeat:
                if previous.get("owner") != owner:
                    raise PipelineError("只能由原分析 owner 幂等确认，不能接管已确认分析。")
            else:
                row = self._owned(connection, task_id, owner)
                self._no_pending_publication(row)
                if row["phase"] != "ready":
                    raise PipelineError("确认完整分析前必须 ready 并完成独立 review。")
            if (row["kind"] != "learning" or not row["learning_started"] or not row["manifest"] or
                    not row["review"] or row["invalidated"] or row["classified_hash"] != row["content_hash"]):
                raise PipelineError("当前来源没有有效的完整学习产物及独立审核。")
            manifest, fingerprint = self._validate_manifest(row, json.loads(row["manifest"]))
            review = json.loads(row["review"])
            if (fingerprint != row["artifact_fingerprint"] or not review.get("approved") or
                    review.get("reviewer") == owner or review.get("artifact_fingerprint") != fingerprint):
                raise PipelineError("本地学习产物或独立审核已失效，不能确认完整分析。")
            report, audit = self._verify_analysis_receipt(row, manifest, receipt)
            try:
                remote = self._remote_task(task_id)
                live = self._site().read_analysis(receipt["accountId"], receipt["listId"], task_id)
            except PipelineError as error:
                # 包装层仅传递已脱敏的 PipelineError，不打印原始网络异常/凭据。
                raise PipelineError("当前来源或 scoped full 报告无法真实回读，不确认分析完成。" + str(error)) from None
            except Exception:
                raise PipelineError("当前来源或 scoped full 报告无法真实回读，不确认分析完成。") from None
            live_record = live.get("record") if isinstance(live, dict) else None
            live_report = live.get("report") if isinstance(live, dict) else None
            if (not remote or remote.get("deleted") or task_hash(remote) != row["content_hash"] or
                    not isinstance(live_record, dict) or live_record.get("id") != task_id or
                    live_record.get("sourceHash") != row["content_hash"] or task_hash(live_record) != row["content_hash"] or
                    not isinstance(live_report, dict) or any(live_report.get(key) != report.get(key) for key in
                        ("id", "taskId", "userId", "listId", "sourceHash", "markdownSha256"))):
                raise PipelineError("当前网站来源或 scoped 报告与本次备份版本不符，不确认分析完成。")
            expected_analysis = json.loads(dumps(report["analysis"]))
            for artifact in expected_analysis["completion"]["artifacts"]:
                artifact.pop("base64", None)
            if live_report.get("analysis") != expected_analysis:
                raise PipelineError("当前网站 full 报告或六类产物 metadata 不匹配备份。")
            self._require_coordinator(coordinator)
            if repeat:
                if previous.get("report_id") != audit["report_id"] or previous.get("source_hash") != row["content_hash"]:
                    raise PipelineError("已确认分析不能替换成其他报告；须先核实来源版本。")
                return self._record(row)
            self._owned(connection, task_id, owner)  # 网络核验后再次检查原认领租约。
            now = stamp(self.clock())
            audit.update(owner=owner, coordinator=coordinator, artifact_fingerprint=fingerprint,
                         verified_at=now, task_completion="user_only", observed_task_state=live_record.get("state", 0))
            snapshot = dict(remote)
            snapshot["state"] = live_record.get("state", 0)
            row = self._update(connection, task_id, phase="analysis_confirmed", analysis_completed_at=now,
                               analysis_receipt=dumps(audit), snapshot=dumps(snapshot), site_state=snapshot["state"],
                               owner=None, lease_until=None, claim_hash=None, completed_at=None, last_error=None)
            connection.execute("DELETE FROM resource_locks WHERE task_id=?", (task_id,))
            self._save_record(row)
            return self._record(row)

    def _publish_failed(self, connection, row, message, conflict=False):
        row = self._update(connection, row["task_id"], phase="needs_review" if conflict else "publish_pending",
                           invalidated=int(conflict), last_error=message)
        self._save_record(row)
        return self._record(row)

    def _remote_task(self, task_id):
        tasks = self._tasks(self._site().download())
        return next((t for t in tasks if t["id"] == task_id), None)

    def _workflow_policy(self):
        file = self.root / "tools/reminder_workflow_policy.json"
        if not file.exists():
            return {"automatic_full_learning": False, "task_completion": "legacy_publish"}
        try:
            policy = json.loads(file.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            raise PipelineError("工作流策略不可读取，停止网站状态写入。") from None
        if not isinstance(policy, dict) or policy.get("task_completion") not in {"user_only", "legacy_publish"}:
            raise PipelineError("工作流策略无效，停止网站状态写入。")
        return policy

    def publish(self, task_id, owner):
        """唯一网站状态写入者；持有写事务直至读取确认，以排斥本队列的其他写者。"""
        if self._workflow_policy()["task_completion"] == "user_only":
            raise PipelineError("当前用户要求任务完成由本人点击；请经 reminder_dot_agent 保存分析标签，不调用旧 publish。")
        with self._tx() as connection:
            row = self._row(connection, task_id)
            if row["phase"] == "synced" and row["classified_hash"] == row["content_hash"]:
                # 幂等仍须只读验证网站；手动重开不能继续显示当前已完成。
                try:
                    remote = self._remote_task(task_id)
                except Exception:
                    return self._publish_failed(connection, row, "网站无法核实当前完成状态；历史记录保留，待核实。", True)
                expected_state = 3 if row["kind"] == "learning" else 1
                if (not remote or remote.get("deleted") or task_hash(remote) != row["content_hash"] or
                        remote.get("state", 0) != expected_state):
                    return self._publish_failed(connection, row, "网站已重开、删除或来源变更；历史记录保留，当前待核实。", True)
                return self._record(row)  # 同一发布重试不重复写网站。
            row = self._owned(connection, task_id, owner)
            if row["classified_hash"] != row["content_hash"]:
                raise PipelineError("必须先对当前来源分类。")
            if row["kind"] == "non_learning":
                target = 1
            elif row["kind"] == "learning":
                if not row["learning_started"] or not row["manifest"] or not row["review"]:
                    raise PipelineError("学习完成需 start、完整 ready 产物及独立 review。")
                _, fingerprint = self._validate_manifest(row, json.loads(row["manifest"]))
                review = json.loads(row["review"])
                if (fingerprint != row["artifact_fingerprint"] or not review.get("approved") or
                        review.get("reviewer") == owner or review.get("artifact_fingerprint") != fingerprint):
                    raise PipelineError("产物已变更或审核失效；重新 ready/review。")
                target = 3
            else:
                raise PipelineError("needs_review、duplicate、blocked 禁止写为非学习或完成。")
            journal = self._journal(task_id)
            if journal and journal.get("cancelled_at"):
                history = json.loads(row["publication_history"] or "[]")
                if not any(entry.get("archive") == journal.get("archive_path") for entry in history):
                    raise PipelineError("发布已明确取消，但本地恢复尚未完成；请重新 reconcile，不写网站。")
                journal = None
            intent = journal or json.loads(row["publish_intent"] or "null")
            classification_hash = hashlib.sha256(dumps({"kind": row["kind"], "reason": row["reason"],
                                                       "evidence": row["evidence"]}).encode("utf-8")).hexdigest()
            expected = {"task_id": task_id, "owner": owner, "target_state": target,
                        "source_hash": row["content_hash"], "baseline_state": row["baseline_state"],
                        "artifact_fingerprint": row["artifact_fingerprint"],
                        "classification_hash": classification_hash}
            if intent and any(intent.get(key) != value for key, value in expected.items()):
                raise PipelineError("持久发布意图与认领/来源/产物不一致，需协调者核实；不写网站。")
            if not intent:
                intent = {**expected, "prepared_at": stamp(self.clock()), "attempted_at": None, "confirmed_at": None}
            row = self._update(connection, task_id, phase="publish_pending", publish_intent=dumps(intent))
            self._save_journal(task_id, intent)
            self._save_record(row)  # 先持久化待发布结果，绝不提前写 completed_at。
            try:
                remote = self._remote_task(task_id)
            except Exception:
                return self._publish_failed(connection, row, "网站读取失败；保留待确认发布，可重试。")
            if not remote or remote.get("deleted") or task_hash(remote) != row["content_hash"]:
                return self._publish_failed(connection, row, "网站原文或摘要已变更/缺失；没有写入，须重新分析。", True)
            state = remote.get("state", 0)
            if state == target and intent.get("attempted_at"):
                confirmed = remote  # 上次写入响应丢失，此次读取确认即可。
            elif state != row["baseline_state"]:
                return self._publish_failed(connection, row, "网站状态已由外部改变；没有写入，须核实所有者。", True)
            else:
                if row["lease_until"] <= self.clock():
                    return self._publish_failed(connection, row, "读取期间租约到期；没有写入，先处理租约。")
                intent["attempted_at"] = stamp(self.clock())
                row = self._update(connection, task_id, publish_intent=dumps(intent))
                self._save_journal(task_id, intent)
                self._save_record(row)
                updated = dict(remote)
                updated["state"] = target
                updated["updatedAt"] = int(self.clock() * 1000)
                if target == 1:
                    updated["lastViewedAt"] = updated["updatedAt"]
                try:
                    self._site().upload(updated)
                except Exception:
                    pass  # 超时可能发生于服务端写入之后；必须读取真实状态确认。
                try:
                    confirmed = self._remote_task(task_id)
                except Exception:
                    return self._publish_failed(connection, row, "网站写入结果不确定，读取确认失败；保留待发布，可重试。")
                if (not confirmed or confirmed.get("deleted") or task_hash(confirmed) != row["content_hash"]):
                    return self._publish_failed(connection, row, "写入后网站来源变更/缺失；不能确认本次结果。", True)
                if confirmed.get("state", 0) != target:
                    if confirmed.get("state", 0) != row["baseline_state"]:
                        return self._publish_failed(connection, row, "写入后网站状态冲突；须人工核实。", True)
                    return self._publish_failed(connection, row, "读取未确认目标状态；保留待发布，可重试。")
            now = stamp(self.clock())
            intent["confirmed_at"] = now
            self._save_journal(task_id, intent)
            row = self._update(connection, task_id, phase="synced", site_state=target, snapshot=dumps(confirmed),
                               synced_at=now, completed_at=now if target == 3 else None,
                               owner=None, lease_until=None, publisher=owner, last_error=None,
                               publish_intent=dumps(intent))
            connection.execute("DELETE FROM resource_locks WHERE task_id=?", (task_id,))
            self._save_record(row)
            return self._record(row)

    def reconcile(self, task_id, owner, ack_conflict=False, reason="", coordinator=None):
        """显式取消不确定发布，仅下载网站与归档审计；不宣称学习完成。

        CLI 必须持有全局协调者租约。此动作同时解除原任务资源锁，重新保留待审。
        """
        if not ack_conflict or not reason or not reason.strip():
            raise PipelineError("reconcile 需 --ack-conflict 和详细 --reason，明确接受不确定结果并释放原任务。")
        with self._tx() as connection:
            row = self._row(connection, task_id)
            journal = self._journal(task_id) or json.loads(row["publish_intent"] or "null")
            if not journal or not journal.get("attempted_at") or row["phase"] == "synced":
                raise PipelineError("没有需要人工取消的待确认发布。")
            if row["owner"] != owner and not (row["owner"] is None and journal.get("owner") == owner):
                raise PipelineError("reconcile 的 owner 必须对应原发布认领。")
            try:
                remote = self._remote_task(task_id)
            except Exception:
                raise PipelineError("无法只读确认网站现状态；保留发布意图与资源锁，稍后重试。") from None
            now = stamp(self.clock())
            archive = self.journals / "archive" / task_id / (str(int(self.clock() * 1000000)) + "-" + uuid.uuid4().hex[:8] + ".json")
            audit = {"outcome": "uncertain_cancelled_not_learning_completed", "at": now,
                     "owner": owner, "coordinator": coordinator, "reason": reason.strip(),
                     "observed_site_state": remote.get("state", 0) if remote else None,
                     "observed_deleted": bool(remote.get("deleted")) if remote else None,
                     "observed_source_hash": task_hash(remote) if remote else None,
                     "publish_intent": journal, "archive": archive.relative_to(self.root).as_posix()}
            atomic_write(archive, json.dumps({"audit": audit, "observed_task": remote}, ensure_ascii=False, indent=2) + "\n")
            # 取消证据也先落盘；中途退出仍不允许旧意图继续声称成功。
            self._save_journal(task_id, {**journal, "cancelled_at": now, "archive_path": audit["archive"],
                                         "cancel_reason": reason.strip()})
            history = json.loads(row["publication_history"] or "[]")
            history.append(audit)
            values = {"publication_history": dumps(history), "owner": None, "lease_until": None,
                      "claim_hash": None, "project_key": None, "learning_started": 0, "adopted": 0,
                      "invalidated": 0, "manifest": None, "artifact_fingerprint": None, "review": None,
                      "publish_intent": None, "kind": "needs_review", "classified_hash": None,
                      "reason": "已明确取消待确认发布；须重新分析。" + reason.strip(), "evidence": dumps([]),
                      "last_error": "发布结果已按人工确认归档；没有断言旧学习完成。"}
            if remote:
                urls = extract_urls(remote.get("text", ""))
                canonical = []
                for url in urls:
                    try:
                        canonical.append(canonical_url(url))
                    except PipelineError:
                        pass
                values.update(snapshot=dumps(remote), content_hash=task_hash(remote), urls=dumps(urls),
                              canonical_urls=dumps(sorted(set(canonical))), site_state=int(remote.get("state", 0)),
                              deleted=int(bool(remote.get("deleted"))), missing=0)
            else:
                values["missing"] = 1
            row.update(values)
            row["legacy_status"] = self._legacy().get(task_id, "")
            values["legacy_status"] = row["legacy_status"]
            row["protection"] = values["protection"] = self._protection(row)
            values["phase"] = self._idle_phase(row)
            updated = self._update(connection, task_id, **values)
            connection.execute("DELETE FROM resource_locks WHERE task_id=?", (task_id,))
            report_path = self.reports / (task_id + ".md")
            historical = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
            report = self._source_report(updated, historical)
            report += f"\n## 人工恢复 · {now}\n\n{reason.strip()}\n\n仅只读记录网站现状态并归档不确定发布，没有确认旧学习成果完成。\n"
            atomic_write(report_path, report)
            self._save_record(updated)
            return self._record(updated)

    def status(self, task_id=None):
        with contextlib.closing(self._connection()) as connection:
            if task_id:
                return self._record(self._row(connection, task_id))
            rows = [dict(row) for row in connection.execute("SELECT * FROM tasks ORDER BY position,task_id")]
            records = {row["task_id"]: self._record(row) for row in rows}
            counts = {}
            for row in rows:
                phase = records[row["task_id"]]["status"]
                counts[phase] = counts.get(phase, 0) + 1
            active = [{"task_id": row["task_id"], "owner": row["owner"], "phase": records[row["task_id"]]["status"],
                       "lease_until": stamp(row["lease_until"]),
                       "expired": row["lease_until"] <= self.clock(), "project_key": row["project_key"]}
                      for row in rows if row["owner"]]
            policy = self._workflow_policy()
            return {"total": len(rows), "counts": counts, "active_claims": active,
                    "database": str(self.db_path), "learning_requires_manual_start": not policy.get("automatic_full_learning", False),
                    "task_completion_requires_user_click": policy["task_completion"] == "user_only",
                    "primary_executor": policy.get("primary_executor", "local"),
                    "backup_targets": policy.get("backup_targets", []),
                    "git_scope": policy.get("git_scope", "unspecified")}

    @staticmethod
    def _cell(value):
        return re.sub(r"\s+", " ", "" if value is None else str(value)).replace("|", "\\|")

    def render(self):
        # 同一 SQLite 写事务串行化多个 render；先从数据库修复记录文件再渲染。
        with self._tx() as connection:
            records = []
            for raw in connection.execute("SELECT * FROM tasks ORDER BY position,task_id").fetchall():
                row = dict(raw)
                self._save_record(row)
                records.append(json.loads((self.records / (row["task_id"] + ".json")).read_text(encoding="utf-8")))
            counts = {}
            for record in records:
                counts[record["status"]] = counts.get(record["status"], 0) + 1
            automatic_learning = self._workflow_policy().get("automatic_full_learning", False)
            flow = ("> 默认 Dot 云端分析与完整学习；本机备份后由协调者知识入库并同步学习成果到 Git，任务完成由用户点击。"
                    if automatic_learning else "> 新记录自动建分析台账与分类排队；完整学习必须由用户选择 start。")
            lines = ["# 拾遗记录流水线纲要", "", f"> 生成时间：{stamp(self.clock())}（Asia/Shanghai）",
                     flow, "",
                     "## 状态计数", "", "| 状态 | 数量 |", "|---|---:|"]
            lines += [f"| {self._phase_label(phase)} ({phase}) | {number} |" for phase, number in sorted(counts.items())]
            chosen = [r for r in records if r["classification"]["kind"] == "learning" and
                      not r["learning_started"] and r["status"] != "synced" and not r["content_changed"]]
            lines += ["", "## " + ("已分类学习项（自动执行仍须核对获准列表及来源）" if automatic_learning else "待用户选择学习"), "", "| task_id | 主题线索 | 当前状态 | 分析报告 |",
                      "|---|---|---|---|"]
            for record in chosen:
                values = [record["task_id"], str(record["source"].get("summary") or record["source"].get("text", ""))[:160],
                          record["status_label"], f"[报告](分析报告/{record['task_id']}.md)"]
                lines.append("| " + " | ".join(self._cell(v) for v in values) + " |")
            complete = sorted((r for r in records if r["status"] == "synced" and
                               r["classification"]["kind"] == "learning" and r["completed_at"]),
                              key=lambda r: (r["completed_at"], r["task_id"]))
            analyses = sorted((r for r in records if r["analysis_completed"]),
                              key=lambda r: (r["analysis_completed_at"], r["task_id"]))
            lines += ["", "## 已确认完整分析（独立于用户任务完成）", "",
                      "| 分析完成时间 | 主题 | task_id | 网站任务状态 | 分析报告 |",
                      "|---|---|---|---:|---|"]
            for record in analyses:
                values = [record["analysis_completed_at"], record["manifest"]["topic"], record["task_id"],
                          record["website_state"], f"[报告](分析报告/{record['task_id']}.md)"]
                lines.append("| " + " | ".join(self._cell(v) for v in values) + " |")
            lines += ["", "## 已确认学习完成（按完成时间升序）", "",
                      "| 序号 | 完成时间 | 主题 | task_id | 原链接 | PDF | 分析报告 |",
                      "|---:|---|---|---|---|---|---|"]
            for number, record in enumerate(complete, 1):
                manifest = record["manifest"]
                values = [number, record["completed_at"], manifest["topic"], record["task_id"],
                          " · ".join(record["source_urls"]), manifest["pdf"],
                          f"[报告](分析报告/{record['task_id']}.md)"]
                lines.append("| " + " | ".join(self._cell(v) for v in values) + " |")
            lines += ["", "## 全部分析记录", "",
                      "| task_id | 流水线状态 | 分类 | 网站状态 | 原链接 | 保护/待审原因 | 分析报告 |",
                      "|---|---|---|---:|---|---|---|"]
            priorities = {"learning_queued": 0, "classified": 1, "claimed": 2, "needs_review": 3,
                          "learning": 4, "ready": 5, "publish_pending": 6, "analysis_confirmed": 6,
                          "pending": 7, "protected": 8, "synced": 9}
            records.sort(key=lambda r: (priorities.get(r["status"], 10),
                                       0 if r["classification"]["kind"] else 1, r["first_seen"], r["task_id"]))
            for record in records:
                reason = record["last_error"] or record["protection"]
                if record["duplicate_of"]:
                    reason = "重复来源，待审：" + record["duplicate_of"] + ("；" + reason if reason else "")
                values = [record["task_id"], record["status_label"], record["classification"]["kind"] or "未分析",
                          record["website_state"], " · ".join(record["source_urls"]), reason,
                          f"[报告](分析报告/{record['task_id']}.md)"]
                lines.append("| " + " | ".join(self._cell(v) for v in values) + " |")
            path = self.base / "流水线纲要.md"
            atomic_write(path, "\n".join(lines) + "\n")
            return {"path": str(path), "total": len(records), "confirmed_learning": len(complete),
                    "confirmed_analysis": len(analyses), "counts": counts}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT, help="仓库根目录；默认当前工具所属仓库")
    commands = parser.add_subparsers(dest="command", required=True)
    sync = commands.add_parser("sync", help="下载来源快照，生成未完成分析台账；不改网站")
    sync.add_argument("--input", type=Path, help="使用本地 JSON 快照，避免联网")
    status = commands.add_parser("status", help="查看状态计数/认领，或单条完整记录")
    status.add_argument("--task")
    claim = commands.add_parser("claim", help="事务认领一个分析任务；默认只取未分类条目")
    claim.add_argument("--owner", required=True)
    claim.add_argument("--task", help="明确选择一条任务，仍不自动开始学习")
    claim.add_argument("--project", help="可预先绑定项目相对目录；同项目不能并行")
    claim.add_argument("--lease-seconds", type=int, default=3600)
    adopt = commands.add_parser("adopt", help="旧代理停止后，明确接管网站进行中/暂停的单条任务")
    adopt.add_argument("--task", required=True)
    adopt.add_argument("--owner", required=True)
    adopt.add_argument("--ack-stopped", action="store_true", help="确认先前执行者已停止")
    adopt.add_argument("--project")
    adopt.add_argument("--lease-seconds", type=int, default=3600)
    for name, help_text in (("renew", "续租；到期不会自动接管"),
                            ("release", "明确释放；保留分析分类，学习回到待选择队列"),
                            ("bind-project", "开始写学习产物前锁定项目相对目录"),
                            ("classify", "记录内容分析、判断及证据；不改网站"),
                            ("start", "仅在用户手动选择后开始单条 learning，并锁定项目"),
                            ("ready", "验证完整学习交付清单；还需独立 review"),
                            ("review", "协调者审核已 ready 的产物，reviewer 需不同于 owner"),
                            ("confirm-analysis", "协调者核验私有备份及 scoped full 回读，只确认分析，不更改用户任务状态"),
                            ("reconcile", "协调者明确取消冲突/不确定发布，只读核实并归档，不标学习完成"),
                            ("publish", "唯一网站写入口；非学习→state1，审核完成学习→state3")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--task", required=True)
        command.add_argument("--owner", required=True)
        if name in {"renew", "start"}:
            command.add_argument("--lease-seconds", type=int, default=3600)
        if name == "release":
            command.add_argument("--reason", default="")
        if name in {"bind-project", "start"}:
            command.add_argument("--project", required=True, help="仓库相对项目目录，例如 agent-harness")
        if name == "classify":
            command.add_argument("--kind", required=True, choices=KINDS)
            command.add_argument("--reason", required=True, help="详细内容分析与判断理由")
            command.add_argument("--evidence", required=True, action="append", help="证据 URL；可重复指定")
        if name == "ready":
            command.add_argument("--manifest", required=True, type=Path,
                                 help="JSON: topic/project_dir/pdf/html/exercise_dir/experiment_log/vault_note/source_urls，report_path/experiment_files 可选")
        if name == "review":
            command.add_argument("--reviewer", required=True)
            command.add_argument("--notes", required=True, help="审核实验真实性、报告、PDF排版及知识入库后的意见")
        if name in {"publish", "reconcile", "confirm-analysis"}:
            command.add_argument("--coordinator", required=True, help="已领取有效全局协调者租约的名称")
        if name == "confirm-analysis":
            command.add_argument("--receipt", type=Path, required=True,
                                 help="私有JSON：schema/accountId/listId/taskId/reportId/sourceHash/backupBundle/backupSha256/handoff")
        if name == "reconcile":
            command.add_argument("--ack-conflict", action="store_true", help="明确接受不确定结果并释放原认领锁")
            command.add_argument("--reason", required=True, help="取消待确认发布的详细审计理由")
    commands.add_parser("render", help="从确认记录生成独立 完成/流水线纲要.md；不改旧纲要/学习队列")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        pipeline = Pipeline(args.root)
        command = args.command
        if command == "sync":
            snapshot = json.loads(args.input.read_text(encoding="utf-8-sig")) if args.input else None
            result = pipeline.sync(snapshot)
        elif command == "status":
            result = pipeline.status(args.task)
        elif command == "claim":
            result = pipeline.claim(args.owner, args.task, args.lease_seconds, args.project)
        elif command == "adopt":
            result = pipeline.adopt(args.task, args.owner, args.ack_stopped, args.lease_seconds, args.project)
        elif command == "renew":
            result = pipeline.renew(args.task, args.owner, args.lease_seconds)
        elif command == "release":
            result = pipeline.release(args.task, args.owner, args.reason)
        elif command == "bind-project":
            result = pipeline.bind_project(args.task, args.owner, args.project)
        elif command == "classify":
            result = pipeline.classify(args.task, args.owner, args.kind, args.reason, args.evidence)
        elif command == "start":
            result = pipeline.start(args.task, args.owner, args.project, args.lease_seconds)
        elif command == "ready":
            result = pipeline.ready(args.task, args.owner, json.loads(args.manifest.read_text(encoding="utf-8-sig")))
        elif command == "review":
            result = pipeline.review(args.task, args.owner, args.reviewer, args.notes)
        elif command == "confirm-analysis":
            result = pipeline.confirm_analysis(args.task, args.owner,
                        json.loads(args.receipt.read_text(encoding="utf-8-sig")), args.coordinator)
        elif command in {"publish", "reconcile"}:
            try:
                try:
                    from . import reminder_coordinator
                except ImportError:
                    import reminder_coordinator
                reminder_coordinator.require_owner(args.root, args.coordinator)
            except (RuntimeError, ValueError, ImportError):
                raise PipelineError("发布需有效全局协调者租约；先通过 reminder_coordinator.py 领取/续约。") from None
            result = (pipeline.publish(args.task, args.owner) if command == "publish" else
                      pipeline.reconcile(args.task, args.owner, args.ack_conflict, args.reason, args.coordinator))
        else:
            result = pipeline.render()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if command == "publish" and result.get("status") != "synced" else 0
    except PipelineError as error:
        print("错误：" + str(error), file=sys.stderr)
        return 2
    except (OSError, ValueError, sqlite3.Error):
        print("错误：本地文件或队列操作失败；请检查输入、权限或磁盘，不显示凭据。", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
