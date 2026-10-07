# -*- coding: utf-8 -*-
"""运行：python -m unittest tools.test_reminder_pipeline -v（不访问真实网站）。"""
from copy import deepcopy
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
from unittest.mock import patch
from types import SimpleNamespace
import zipfile

from tools import reminder_dot_http as scoped_http
from tools.reminder_pipeline import Pipeline, PipelineError, ROOT, SiteAPI, canonical_url, task_hash


def task(task_id="a", state=0, url=None):
    return {"id": task_id, "text": "完整原始记录，后续文字不能截断 " +
            (url or "https://example.com/" + task_id), "summary": "待核实的摘要",
            "state": state, "deleted": False, "createdAt": 123000,
            "updatedAt": 123000, "attachmentUri": "", "viewCount": 0}


class FakeAPI:
    def __init__(self, tasks):
        self.tasks = deepcopy(tasks)
        self.fail_downloads = 0
        self.fail_uploads = 0
        self.apply_then_fail = False
        self.fail_confirmation = False
        self.crash_after_apply = False
        self.upload_count = 0
        self.download_count = 0
        self.analysis_report = None
        self.analysis_scope = None
        self.scoped_reads = 0

    def read_analysis(self, account_id, list_id, task_id):
        self.scoped_reads += 1
        if (account_id, list_id) != self.analysis_scope or self.analysis_report is None:
            raise RuntimeError("scope not granted; token=secret must not be printed")
        record = deepcopy(next(t for t in self.tasks if t["id"] == task_id))
        record["sourceHash"] = task_hash(record)
        report = deepcopy(self.analysis_report)
        for artifact in report["analysis"]["completion"]["artifacts"]:
            artifact.pop("base64", None)
        return {"record": record, "report": report, "learningAttempts": [], "contentIsUntrustedData": True}

    def download(self):
        self.download_count += 1
        if self.fail_downloads:
            self.fail_downloads -= 1
            raise RuntimeError("不应泄漏的 token=secret")
        return deepcopy(self.tasks)

    def upload(self, updated):
        self.upload_count += 1
        if self.fail_uploads:
            self.fail_uploads -= 1
            raise RuntimeError("不应泄漏的 token=secret")
        for index, old in enumerate(self.tasks):
            if old["id"] == updated["id"]:
                self.tasks[index] = deepcopy(updated)
        if self.crash_after_apply:
            raise SystemExit("模拟进程在服务器接受后崩溃，SQLite事务回滚")
        if self.fail_confirmation:
            self.fail_downloads += 1
        if self.apply_then_fail:
            raise RuntimeError("响应丢失 token=secret")
        return {"success": True}


class PipelineTests(unittest.TestCase):
    def setUp(self):
        # Windows 沙箱的系统 temp 目录不可可靠写子目录，限定在工作区运行目录。
        runtime = ROOT / "完成" / ".pipeline"
        runtime.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="test-pipeline-", dir=runtime)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        self.now = [time.time()]
        self.api = FakeAPI([task()])
        self.pipeline = Pipeline(self.root, self.api, clock=lambda: self.now[0])
        self.pipeline.sync(self.api.tasks)

    def tearDown(self):
        self.temporary.cleanup()

    def classify(self, kind="learning", task_id="a", owner="worker"):
        return self.pipeline.classify(task_id, owner, kind,
            "核实官方原文及项目文档：该链接提供可实践的实现与明确的技术主题。"
            "实验将对真实代码运行记录输出，不能把摘要或单一 PDF 当作完成依据。",
            ["https://example.com/" + task_id])

    def make_manifest(self):
        project = self.root / "demo"
        exercise = project / "exercise"
        exercise.mkdir(parents=True, exist_ok=True)
        (project / "guide.pdf").write_bytes(b"%PDF-1.7\nminimal fixture for structural checks\n%%EOF\n")
        (project / "guide.html").write_text("<!doctype html><html><body>guide fixture</body></html>", encoding="utf-8")
        (exercise / "run.py").write_text("print(1 + 1)\n", encoding="utf-8")
        (exercise / "experiment.log").write_text("$ python run.py\n2\nExit code: 0\nFixture run recorded for validation.\n", encoding="utf-8")
        (self.root / "vault").mkdir(exist_ok=True)
        (self.root / "vault" / "demo.md").write_text("# 项目笔记\n实验、概念及知识关联的测试占位。", encoding="utf-8")
        return {"topic": "测试项目", "project_dir": "demo", "pdf": "demo/guide.pdf",
                "html": "demo/guide.html", "exercise_dir": "demo/exercise",
                "experiment_log": "demo/exercise/experiment.log", "vault_note": "vault/demo.md",
                "source_urls": ["https://example.com/a"]}

    def learning_ready(self, review=True):
        self.pipeline.claim("worker", "a")
        self.classify()
        self.pipeline.start("a", "worker", "demo")
        manifest = self.make_manifest()
        self.pipeline.ready("a", "worker", manifest)
        if review:
            self.pipeline.review("a", "worker", "coordinator", "核对完整报告、PDF、实验命令真实输出与知识关联。")
        return manifest

    def analysis_receipt(self):
        self.learning_ready()
        from tools import reminder_coordinator
        reminder_coordinator.acquire(self.root, "coordinator")
        record = self.pipeline.status("a")
        manifest = record["manifest"]
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as stream:
            # 验证云端以项目为基准的 exercise/... 及本地工具无前缀两种布局。
            for path in sorted((self.root / "demo" / "exercise").iterdir()):
                stream.writestr("exercise/" + path.name, path.read_bytes())
        data = {role: (self.root / manifest[key]).read_bytes() for role, key in
                (("guide_pdf", "pdf"), ("guide_html", "html"), ("experiment_log", "experiment_log"),
                 ("knowledge_notes", "vault_note"))}
        data["exercise_archive"] = archive.getvalue()
        data["review_log"] = json.dumps(record["quality_review"], ensure_ascii=False).encode("utf-8")
        markdown = "# Fixture full analysis\n\nPrivate fixture only, not evidence of live learning.\n"
        report = {"id": "full-a", "taskId": "a", "userId": "account-a", "listId": "list-a", "owner": "cloud-worker",
                  "sourceHash": record["source_hash"], "record": deepcopy(self.api.tasks[0]), "stale": False,
                  "activeClaim": False, "markdown": markdown,
                  "markdownSha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
                  "analysis": {"kind": "learning", "stage": "full", "title": "Fixture", "completion": {
                      "project": "demo", "reviewer": "cloud-independent-reviewer", "pdfRendered": True,
                      "experimentChecked": True, "knowledgeChecked": True,
                      "artifacts": [{"role": role, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest(),
                                     "base64": base64.b64encode(blob).decode("ascii")} for role, blob in data.items()]}}}
        bundle = {"schema": "reminder-dot-export-v1", "accountId": "account-a", "list": {"id": "list-a"},
                  "exportedAt": "2026-10-05T00:00:00Z", "reports": [report]}
        raw = json.dumps(bundle, ensure_ascii=False, indent=2).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        folder = self.root / "完成/.pipeline/dot/account-a/list-a"
        export = folder / "exports" / (digest + ".json")
        export.parent.mkdir(parents=True)
        export.write_bytes(raw)
        export.with_suffix(".sha256").write_text(digest + "\n", encoding="utf-8")
        report_base = folder / "reports/a/full-a"
        report_base.parent.mkdir(parents=True)
        Path(str(report_base) + ".md").write_text(markdown, encoding="utf-8", newline="\n")
        files = Path(str(report_base) + "-files")
        files.mkdir()
        extensions = {"guide_pdf": ".pdf", "guide_html": ".html", "exercise_archive": ".zip",
                      "experiment_log": ".txt", "knowledge_notes": ".md", "review_log": ".md"}
        for role, blob in data.items():
            (files / (role + extensions[role])).write_bytes(blob)
        handoff = {"schema": "reminder-dot-handoff-v1", "accountId": "account-a", "listId": "list-a",
                   "reports": {"full-a": {"taskId": "a", "sourceHash": record["source_hash"], "analysisStage": "full",
                    "markdownSha256": report["markdownSha256"],
                    "cloud": {"status": "saved", "staleAtExport": False, "exportedAt": bundle["exportedAt"]},
                    "local": {"status": "verified", "report": "reports/a/full-a.md", "artifacts": "reports/a/full-a-files"},
                    "knowledge": {"status": "merged", "note": "vault/demo.md"}, "git": {"status": "pending_coordinator"}}}}
        (folder / "handoff.json").write_text(json.dumps(handoff), encoding="utf-8")
        self.api.analysis_report = report
        self.api.analysis_scope = ("account-a", "list-a")
        return {"schema": "reminder-analysis-confirmation-v1", "accountId": "account-a", "listId": "list-a",
                "taskId": "a", "reportId": "full-a", "sourceHash": record["source_hash"],
                "backupBundle": export.relative_to(self.root).as_posix(), "backupSha256": digest,
                "handoff": (folder / "handoff.json").relative_to(self.root).as_posix()}

    def replace_archive(self, receipt, members):
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as stream:
            for name, data in members.items():
                stream.writestr(name, data)
        blob = archive.getvalue()
        def mutation(bundle):
            artifacts = bundle["reports"][0]["analysis"]["completion"]["artifacts"]
            item = next(a for a in artifacts if a["role"] == "exercise_archive")
            item.update(bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(),
                        base64=base64.b64encode(blob).decode("ascii"))
            self.api.analysis_report = deepcopy(bundle["reports"][0])
        result = self.rewrite_receipt_bundle(receipt, mutation)
        (self.root / "完成/.pipeline/dot/account-a/list-a/reports/a/full-a-files/exercise_archive.zip").write_bytes(blob)
        return result

    def confirm(self, receipt):
        return self.pipeline.confirm_analysis("a", "worker", receipt, "coordinator")

    def rewrite_receipt_bundle(self, receipt, mutation):
        original = self.root / receipt["backupBundle"]
        bundle = json.loads(original.read_text(encoding="utf-8"))
        mutation(bundle)
        raw = json.dumps(bundle, ensure_ascii=False, indent=2).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        new_file = original.parent / (digest + ".json")
        new_file.write_bytes(raw)
        new_file.with_suffix(".sha256").write_text(digest, encoding="utf-8")
        return {**receipt, "backupBundle": new_file.relative_to(self.root).as_posix(), "backupSha256": digest}

    def test_two_processes_only_one_claim(self):
        gate = self.root / "go"
        code = ("import sys,time; from pathlib import Path; from tools.reminder_pipeline import Pipeline,PipelineError; "
                "root=Path(sys.argv[1]); gate=Path(sys.argv[3]);\n"
                "while not gate.exists(): time.sleep(.01)\n"
                "try:\n p=Pipeline(root); p.claim(sys.argv[2], 'a'); print('CLAIMED')\n"
                "except PipelineError:\n print('REFUSED')\n")
        processes = [subprocess.Popen([sys.executable, "-c", code, str(self.root), owner, str(gate)],
                                     cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                     for owner in ("claude", "codex")]
        try:
            gate.write_text("go", encoding="utf-8")
            outputs = [process.communicate(timeout=30) for process in processes]
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                    process.wait()
        self.assertEqual([p.returncode for p in processes], [0, 0], outputs)
        self.assertEqual(sum("CLAIMED" in out for out, _ in outputs), 1, outputs)
        self.assertEqual(sum("REFUSED" in out for out, _ in outputs), 1, outputs)
        self.assertEqual(len(self.pipeline.status()["active_claims"]), 1)

    def test_website_and_legacy_are_protected(self):
        legacy = self.root / "完成" / "学习队列.md"
        legacy.write_text("| 状态 | task_id |\n|---|---|\n| 进行中 | legacy-run |\n"
                          "| 已完成 | legacy-done |\n| 跳过(非学习) | legacy-skip |\n"
                          "| 待处理 | untouched |\n", encoding="utf-8")
        data = [task("site-run", 1), task("site-pause", 2), task("site-done", 3),
                task("legacy-run"), task("legacy-done"), task("legacy-skip"), task("untouched")]
        self.pipeline.sync(data)
        for protected in ("site-run", "site-pause", "site-done", "legacy-run", "legacy-done", "legacy-skip"):
            self.assertEqual(self.pipeline.status(protected)["status"], "protected")
            with self.assertRaises(PipelineError):
                self.pipeline.claim("worker", protected)
        self.assertEqual(self.pipeline.claim("worker")["task_id"], "untouched")
        self.assertEqual(legacy.read_text(encoding="utf-8").count("legacy-run"), 1)

    def test_adopt_requires_ack_and_cannot_take_completed(self):
        self.pipeline.sync([task("run", 1), task("done", 3)])
        with self.assertRaises(PipelineError):
            self.pipeline.adopt("run", "worker")
        self.assertEqual(self.pipeline.adopt("run", "worker", True)["owner"], "worker")
        with self.assertRaises(PipelineError):
            self.pipeline.adopt("done", "worker", True)

    def test_expired_lease_is_not_stolen(self):
        self.pipeline.claim("claude", "a", lease_seconds=30)
        self.now[0] += 31
        with self.assertRaises(PipelineError):
            self.pipeline.claim("codex", "a")
        self.assertTrue(self.pipeline.status()["active_claims"][0]["expired"])
        self.pipeline.release("a", "claude")
        self.assertEqual(self.pipeline.claim("codex", "a")["owner"], "codex")

    def test_same_owner_can_explicitly_renew_expired_claim(self):
        self.pipeline.claim("worker", "a", lease_seconds=30)
        self.now[0] += 31
        self.pipeline.renew("a", "worker")
        self.assertFalse(self.pipeline.status()["active_claims"][0]["expired"])

    def test_project_mutex_rolls_back_partial_claim(self):
        self.pipeline.sync([task("a"), task("b")])
        self.pipeline.claim("claude", "a", project="demo")
        with self.assertRaises(PipelineError):
            self.pipeline.claim("codex", "b", project="demo")
        self.assertIsNone(self.pipeline.status("b")["owner"])
        self.pipeline.release("a", "claude")
        self.assertEqual(self.pipeline.claim("codex", "b", project="demo")["owner"], "codex")

    def test_duplicate_urls_are_pending_review_not_complete(self):
        data = [task("a", url="https://x.com/user/status/123?s=20&utm_source=a"),
                task("b", url="https://twitter.com/user/status/123#section")]
        self.pipeline.sync(data)
        duplicate = self.pipeline.status("b")
        self.assertEqual(duplicate["duplicate_of"], "a")
        self.assertEqual(duplicate["status"], "needs_review")
        self.assertIsNone(duplicate["completed_at"])
        with self.assertRaises(PipelineError):
            self.pipeline.claim("worker", "b")
        self.assertEqual(canonical_url(data[0]["text"].split()[-1]), canonical_url(data[1]["text"].split()[-1]))

    def test_original_text_and_all_links_preserved(self):
        original = "开头 https://example.com/a 这是后半段，另有 https://example.com/b?x=1 完整结尾"
        data = [dict(task(), text=original)]
        self.pipeline.sync(data)
        record = self.pipeline.status("a")
        self.assertEqual(record["source"]["text"], original)
        self.assertEqual(record["source_urls"], ["https://example.com/a", "https://example.com/b?x=1"])
        report = (self.root / "完成" / "分析报告" / "a.md").read_text(encoding="utf-8")
        self.assertIn(original, report)
        self.assertIn("未完成学习", report)

    def test_sync_and_render_keep_handwritten_report(self):
        report = self.root / "完成" / "分析报告" / "a.md"
        report.write_text("人工核验的原文、报告与详细判断。", encoding="utf-8")
        self.pipeline.sync(self.api.tasks)
        self.pipeline.render()
        self.assertEqual(report.read_text(encoding="utf-8"), "人工核验的原文、报告与详细判断。")

    def test_same_snapshot_sync_is_content_idempotent(self):
        path = self.root / "完成" / "记录" / "a.json"
        original = path.read_bytes()
        self.now[0] += 1000
        result = self.pipeline.sync(self.api.tasks)
        self.assertEqual(result["changed"], 0)
        self.assertEqual(path.read_bytes(), original)

    def test_learning_classification_queues_but_does_not_start(self):
        self.pipeline.claim("worker", "a")
        self.classify()
        with self.assertRaises(PipelineError):
            self.pipeline.ready("a", "worker", self.make_manifest())
        self.pipeline.release("a", "worker")
        self.assertEqual(self.pipeline.status("a")["status"], "learning_queued")
        self.assertEqual(self.pipeline.claim("classifier")["status"], "empty")
        self.pipeline.start("a", "chosen-worker", "demo")
        self.assertTrue(self.pipeline.status("a")["learning_started"])

    def test_manifest_path_escape_rejected(self):
        self.pipeline.claim("worker", "a")
        self.classify()
        self.pipeline.start("a", "worker", "demo")
        manifest = self.make_manifest()
        outside = self.root.parent / "outside.pdf"
        outside.write_bytes(b"%PDF-1.7\noutside\n")
        manifest["pdf"] = "../outside.pdf"
        with self.assertRaises(PipelineError):
            self.pipeline.ready("a", "worker", manifest)
        self.assertEqual(self.pipeline.status("a")["status"], "learning")

    def test_only_pdf_and_forged_pdf_cannot_be_ready(self):
        self.pipeline.claim("worker", "a")
        self.classify()
        self.pipeline.start("a", "worker", "demo")
        manifest = self.make_manifest()
        minimal = {"topic": "假完成", "pdf": manifest["pdf"]}
        with self.assertRaises(PipelineError):
            self.pipeline.ready("a", "worker", minimal)
        (self.root / manifest["pdf"]).write_text("This is not a PDF", encoding="utf-8")
        with self.assertRaises(PipelineError):
            self.pipeline.ready("a", "worker", manifest)

    def test_experiment_and_evidence_are_required(self):
        self.pipeline.claim("worker", "a")
        with self.assertRaises(PipelineError):
            self.pipeline.classify("a", "worker", "learning", "理由", [])
        self.classify()
        self.pipeline.start("a", "worker", "demo")
        manifest = self.make_manifest()
        (self.root / "demo" / "exercise" / "run.py").unlink()
        with self.assertRaises(PipelineError):
            self.pipeline.ready("a", "worker", manifest)
        with self.assertRaises(PipelineError):
            self.pipeline.classify("a", "worker", "learning", "理由", ["file:///secret"])

    def test_dependency_cache_is_excluded_from_experiment(self):
        self.pipeline.claim("worker", "a")
        self.classify()
        self.pipeline.start("a", "worker", "demo")
        manifest = self.make_manifest()
        cache = self.root / "demo" / "exercise" / "node_modules"
        cache.mkdir()
        (cache / "library.js").write_text("cached dependency", encoding="utf-8")
        (self.root / "demo" / "exercise" / "run.py").unlink()
        with self.assertRaises(PipelineError):
            self.pipeline.ready("a", "worker", manifest)
        (self.root / "demo" / "exercise" / "run.py").write_text("print(2)\n", encoding="utf-8")
        self.pipeline.ready("a", "worker", manifest)
        self.pipeline.review("a", "worker", "coordinator", "核对真实实验记录。")
        (cache / "library.js").write_text("changed cache", encoding="utf-8")
        self.assertEqual(self.pipeline.publish("a", "worker")["status"], "synced")

    def test_explicit_experiment_file_list(self):
        self.pipeline.claim("worker", "a")
        self.classify()
        self.pipeline.start("a", "worker", "demo")
        manifest = self.make_manifest()
        manifest["experiment_files"] = ["demo/exercise/run.py"]
        result = self.pipeline.ready("a", "worker", manifest)
        self.assertEqual(result["manifest"]["experiment_files"], manifest["experiment_files"])
        manifest["experiment_files"] = ["vault/demo.md"]
        with self.assertRaises(PipelineError):
            self.pipeline.ready("a", "worker", manifest)

    def test_requires_separate_review_and_rechecks_artifacts(self):
        self.learning_ready(review=False)
        with self.assertRaises(PipelineError):
            self.pipeline.publish("a", "worker")
        with self.assertRaises(PipelineError):
            self.pipeline.review("a", "worker", "worker", "自己审核")
        self.pipeline.review("a", "worker", "coordinator", "已核对实验真实输出及交付。")
        (self.root / "demo" / "exercise" / "run.py").write_text("print(3)\n", encoding="utf-8")
        with self.assertRaises(PipelineError):
            self.pipeline.publish("a", "worker")
        self.assertEqual(self.api.upload_count, 0)

    def test_sync_changed_claim_cannot_publish(self):
        self.learning_ready()
        updated = deepcopy(self.api.tasks)
        updated[0]["summary"] = "新摘要"
        self.pipeline.sync(updated)
        self.assertTrue(self.pipeline.status("a")["content_changed"])
        with self.assertRaises(PipelineError):
            self.pipeline.publish("a", "worker")
        self.assertEqual(self.api.upload_count, 0)
        self.assertIsNone(self.pipeline.status("a")["completed_at"])

    def test_latest_site_change_prevents_publish(self):
        self.learning_ready()
        self.api.tasks[0]["text"] += " 外部变更"
        result = self.pipeline.publish("a", "worker")
        self.assertEqual(result["status"], "needs_review")
        self.assertIsNone(result["completed_at"])
        self.assertEqual(self.api.upload_count, 0)

    def test_external_site_state_cannot_be_mistaken_for_own_success(self):
        self.learning_ready()
        self.api.tasks[0]["state"] = 3
        result = self.pipeline.publish("a", "worker")
        self.assertEqual(result["status"], "needs_review")
        self.assertFalse(result["website_synced"])
        self.assertEqual(self.api.upload_count, 0)

    def test_api_failure_does_not_show_completion(self):
        self.learning_ready()
        self.api.fail_uploads = 1
        result = self.pipeline.publish("a", "worker")
        self.assertEqual(result["status"], "publish_pending")
        self.assertIsNone(result["completed_at"])
        self.assertNotIn("secret", json.dumps(result))
        self.assertEqual(self.pipeline.render()["confirmed_learning"], 0)
        record = json.loads((self.root / "完成" / "记录" / "a.json").read_text(encoding="utf-8"))
        self.assertFalse(record["website_synced"])
        self.assertIsNone(record["completed_at"])

    def test_lost_upload_response_and_retry_are_idempotent(self):
        self.learning_ready()
        self.api.apply_then_fail = True
        self.api.fail_confirmation = True
        initial = self.pipeline.publish("a", "worker")
        self.assertEqual(initial["status"], "publish_pending")
        self.assertIsNone(initial["completed_at"])
        self.api.fail_confirmation = False
        result = self.pipeline.publish("a", "worker")
        self.assertEqual(result["status"], "synced")
        self.assertTrue(result["completed_at"].endswith("+08:00"))
        self.assertEqual(self.api.upload_count, 1)
        self.assertEqual(self.pipeline.publish("a", "worker")["completed_at"], result["completed_at"])
        self.assertEqual(self.api.upload_count, 1)
        self.assertEqual(self.pipeline.render()["confirmed_learning"], 1)

    def test_process_crash_journal_survives_sqlite_rollback(self):
        self.learning_ready()
        self.api.crash_after_apply = True
        with self.assertRaises(SystemExit):
            self.pipeline.publish("a", "worker")
        record = self.pipeline.status("a")
        self.assertEqual(record["status"], "publish_pending")
        self.assertTrue(record["publish_intent"]["attempted_at"])
        self.assertIsNone(record["completed_at"])
        with self.assertRaises(PipelineError):
            self.pipeline.release("a", "worker")
        self.api.crash_after_apply = False
        result = self.pipeline.publish("a", "worker")
        self.assertEqual(result["status"], "synced")
        self.assertEqual(self.api.upload_count, 1)

    def test_unknown_publish_content_change_can_be_reconciled_without_false_completion(self):
        self.learning_ready()
        self.api.fail_uploads = 1
        self.pipeline.publish("a", "worker")
        self.api.tasks[0]["summary"] = "来源后来发生实质变化"
        self.api.tasks[0]["updatedAt"] += 1
        self.pipeline.sync(self.api.tasks)
        with self.assertRaises(PipelineError):
            self.pipeline.renew("a", "worker")
        with self.assertRaises(PipelineError):
            self.pipeline.release("a", "worker")
        with self.assertRaises(PipelineError):
            self.pipeline.reconcile("a", "worker", False, "来源发生变化，人工取消旧待发布结果。")
        uploads_before = self.api.upload_count
        result = self.pipeline.reconcile("a", "worker", True,
                                         "来源发生变化且旧代理已停止，取消旧意图，待重新核实。", "coordinator")
        self.assertEqual(self.api.upload_count, uploads_before)
        self.assertFalse(result["unresolved_publication"])
        self.assertIsNone(result["completed_at"])
        self.assertIsNone(result["owner"])
        self.assertTrue(result["publication_history"])
        self.assertEqual(self.pipeline.render()["confirmed_learning"], 0)
        self.assertEqual(self.pipeline.claim("new-worker", "a")["owner"], "new-worker")
        self.classify("learning", owner="new-worker")
        self.pipeline.start("a", "new-worker", "demo")
        self.pipeline.ready("a", "new-worker", self.make_manifest())
        self.pipeline.review("a", "new-worker", "coordinator", "重分析并重新审核真实产物。")
        self.assertEqual(self.pipeline.publish("a", "new-worker")["status"], "synced")

    def test_reconcile_accepted_but_unconfirmed_write_does_not_claim_learning_complete(self):
        self.learning_ready()
        self.api.fail_confirmation = True
        result = self.pipeline.publish("a", "worker")
        self.assertEqual(result["status"], "publish_pending")
        self.api.fail_confirmation = False
        result = self.pipeline.reconcile("a", "worker", True, "人工保留不确定结果，只归档与释放，后续另行验收。")
        self.assertEqual(result["website_state"], 3)
        self.assertEqual(result["status"], "protected")
        self.assertIsNone(result["completed_at"])
        self.assertEqual(self.pipeline.render()["confirmed_learning"], 0)

    def test_manual_website_reopen_invalidates_current_completion_but_keeps_history(self):
        self.learning_ready()
        completed = self.pipeline.publish("a", "worker")["completed_at"]
        self.api.tasks[0]["state"] = 0
        self.api.tasks[0]["updatedAt"] += 1
        self.pipeline.sync(self.api.tasks)
        record = self.pipeline.status("a")
        self.assertEqual(record["status"], "needs_review")
        self.assertFalse(record["website_synced"])
        self.assertIsNone(record["completed_at"])
        rendered = self.pipeline.render()
        self.assertEqual(rendered["confirmed_learning"], 0)
        persistent = json.loads((self.root / "完成" / "记录" / "a.json").read_text(encoding="utf-8"))
        self.assertEqual(persistent["completion_history"][0]["completed_at"], completed)

    def test_stale_snapshot_cannot_overwrite_successful_publish(self):
        original = deepcopy(self.api.tasks)
        self.learning_ready()
        self.pipeline.publish("a", "worker")
        result = self.pipeline.sync(original)
        self.assertEqual(result["stale"], 1)
        self.assertEqual(self.pipeline.status("a")["website_state"], 3)
        self.assertEqual(self.pipeline.render()["confirmed_learning"], 1)

    def test_synced_publish_retry_checks_website_reopen(self):
        self.learning_ready()
        self.pipeline.publish("a", "worker")
        self.api.tasks[0]["state"] = 0
        result = self.pipeline.publish("a", "worker")
        self.assertEqual(result["status"], "needs_review")
        self.assertFalse(result["website_synced"])
        self.assertEqual(self.api.upload_count, 1)

    def test_zero_site_state_is_rendered_and_classification_report_is_not_pending(self):
        self.pipeline.claim("worker", "a")
        self.classify("non_learning")
        self.pipeline.release("a", "worker")
        report = (self.root / "完成" / "分析报告" / "a.md").read_text(encoding="utf-8")
        self.assertNotIn("尚未完成内容分析", report)
        self.assertNotIn("学习仅进入待选择队列", report)
        self.pipeline.render()
        outline = (self.root / "完成" / "流水线纲要.md").read_text(encoding="utf-8")
        self.assertIn("| 0 |", outline)

    def test_pending_publish_lease_recovery_is_explicit(self):
        self.learning_ready()
        self.api.fail_uploads = 1
        self.pipeline.publish("a", "worker")
        self.now[0] += 4000
        with self.assertRaises(PipelineError):
            self.pipeline.claim("other", "a")
        with self.assertRaises(PipelineError):
            self.pipeline.release("a", "worker")
        self.pipeline.renew("a", "worker")
        self.assertEqual(self.pipeline.publish("a", "worker")["status"], "synced")

    def test_non_learning_never_lists_as_learning_complete(self):
        self.pipeline.claim("worker", "a")
        self.classify("non_learning")
        result = self.pipeline.publish("a", "worker")
        self.assertEqual(result["website_state"], 1)
        self.assertEqual(result["status"], "synced")
        self.assertIsNone(result["completed_at"])
        self.assertEqual(self.pipeline.render()["confirmed_learning"], 0)
        self.assertTrue((self.root / "完成" / "分析报告" / "a.md").stat().st_size)

    def test_uncertain_kinds_cannot_publish_as_non_learning(self):
        for kind in ("needs_review", "duplicate", "blocked"):
            with self.subTest(kind=kind):
                if not self.pipeline.status("a")["owner"]:
                    self.pipeline.claim("worker", "a")
                self.classify(kind)
                with self.assertRaises(PipelineError):
                    self.pipeline.publish("a", "worker")
                self.pipeline.release("a", "worker")
                self.assertEqual(self.pipeline.status("a")["status"], "needs_review")
        self.assertEqual(self.api.upload_count, 0)

    def test_cli_help_and_publish_coordinator_requirement(self):
        script = ROOT / "tools" / "reminder_pipeline.py"
        help_result = subprocess.run([sys.executable, str(script), "--help"], cwd=ROOT,
                                     capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("start", help_result.stdout)
        result = subprocess.run([sys.executable, str(script), "--root", str(self.root), "publish",
                                 "--task", "a", "--owner", "worker", "--coordinator", "unclaimed"],
                                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(result.returncode, 2)
        self.assertIn("协调者", result.stderr)

    def test_confirm_analysis_preserves_review_and_does_not_complete_task(self):
        receipt = self.analysis_receipt()
        before = self.pipeline.status("a")
        result = self.confirm(receipt)
        self.assertEqual(result["status"], "analysis_confirmed")
        self.assertTrue(result["analysis_completed"])
        self.assertTrue(result["analysis_completed_at"].endswith("+08:00"))
        self.assertIsNone(result["completed_at"])
        self.assertFalse(result["website_synced"])
        self.assertEqual(result["website_state"], 0)
        self.assertEqual(result["manifest"], before["manifest"])
        self.assertEqual(result["quality_review"], before["quality_review"])
        self.assertIsNone(result["owner"])
        self.assertEqual(self.api.upload_count, 0)
        self.assertEqual(self.api.tasks[0]["state"], 0)
        self.assertEqual(self.api.scoped_reads, 1)
        self.assertEqual(self.pipeline.release("a", "worker")["status"], "analysis_confirmed")
        self.assertEqual(self.confirm(receipt)["analysis_completed_at"], result["analysis_completed_at"])
        for operation in (lambda: self.pipeline.claim("worker", "a"),
                          lambda: self.pipeline.adopt("a", "worker", True),
                          lambda: self.pipeline.start("a", "worker", "demo")):
            with self.assertRaises(PipelineError):
                operation()
        self.assertEqual(self.pipeline.claim("classifier")["status"], "empty")
        summary = self.pipeline.render()
        self.assertEqual(summary["confirmed_analysis"], 1)
        self.assertEqual(summary["confirmed_learning"], 0)

    def test_confirmation_accepts_single_shared_wrapper_directory(self):
        receipt = self.analysis_receipt()
        exercise = self.root / "demo/exercise"
        receipt = self.replace_archive(receipt, {"delivery-package/" + p.name: p.read_bytes()
                                               for p in exercise.iterdir() if p.is_file()})
        self.assertEqual(self.confirm(receipt)["status"], "analysis_confirmed")
        self.assertEqual(self.api.upload_count, 0)

    def test_confirmation_rejects_mixed_wrapper_directories(self):
        receipt = self.analysis_receipt()
        exercise = self.root / "demo/exercise"
        receipt = self.replace_archive(receipt, {
            "one/run.py": (exercise / "run.py").read_bytes(),
            "two/experiment.log": (exercise / "experiment.log").read_bytes()})
        with self.assertRaisesRegex(PipelineError, "实验归档未匹配"):
            self.confirm(receipt)
        self.assertFalse(self.pipeline.status("a")["analysis_completed"])

    def test_confirmation_rejects_mixed_mapping_even_with_common_wrapper(self):
        receipt = self.analysis_receipt()
        exercise = self.root / "demo/exercise"
        content = (exercise / "run.py").read_bytes()
        (exercise / "pkg").mkdir()
        (exercise / "run.py").rename(exercise / "pkg/run.py")
        manifest = self.pipeline.status("a")["manifest"]
        self.pipeline.ready("a", "worker", manifest)
        self.pipeline.review("a", "worker", "independent",
                             "实际审阅混合布局的回归夹具，不是学习交付证据。")
        receipt = self.replace_archive(receipt, {
            "pkg/run.py": content, "pkg/experiment.log": (exercise / "experiment.log").read_bytes()})
        with self.assertRaisesRegex(PipelineError, "实验归档未匹配"):
            self.confirm(receipt)

    def test_confirmation_rejects_wrapper_path_traversal(self):
        receipt = self.analysis_receipt()
        data = (self.root / "demo/exercise/run.py").read_bytes()
        receipt = self.replace_archive(receipt, {"pkg/../run.py": data})
        with self.assertRaisesRegex(PipelineError, "越界路径"):
            self.confirm(receipt)

    def test_confirmation_needs_original_owner_and_real_coordinator(self):
        receipt = self.analysis_receipt()
        for owner, coordinator in (("other-worker", "coordinator"), ("worker", "other-coordinator")):
            with self.subTest(owner=owner, coordinator=coordinator), self.assertRaises(PipelineError):
                self.pipeline.confirm_analysis("a", owner, receipt, coordinator)
        self.assertFalse(self.pipeline.status("a")["analysis_completed"])
        self.assertEqual(self.api.scoped_reads, 0)
        self.assertEqual(self.api.upload_count, 0)

    def test_confirmation_rejects_forged_receipt_and_wrong_hash(self):
        receipt = self.analysis_receipt()
        for wrong in ({**receipt, "schema": "trust-me"}, {**receipt, "backupSha256": "0" * 64},
                      {**receipt, "sourceHash": "0" * 64}, {**receipt, "taskId": "other"},
                      {**receipt, "reportId": "other-report"}):
            with self.subTest(wrong=wrong), self.assertRaises(PipelineError):
                self.confirm(wrong)
        self.assertFalse(self.pipeline.status("a")["analysis_completed"])
        self.assertEqual(self.api.upload_count, 0)

    def test_confirmation_checks_each_real_backup_artifact(self):
        receipt = self.analysis_receipt()
        folder = self.root / "完成/.pipeline/dot/account-a/list-a/reports/a/full-a-files"
        for path in folder.iterdir():
            original = path.read_bytes()
            with self.subTest(role=path.name):
                path.write_bytes(b"single file damaged")
                with self.assertRaises(PipelineError):
                    self.confirm(receipt)
                self.assertFalse(self.pipeline.status("a")["analysis_completed"])
                path.write_bytes(original)
        self.assertEqual(self.api.upload_count, 0)

    def test_confirmation_rejects_stale_and_preliminary_backup(self):
        receipt = self.analysis_receipt()
        stale = self.rewrite_receipt_bundle(receipt, lambda b: b["reports"][0].update(stale=True))
        preliminary = self.rewrite_receipt_bundle(receipt,
                            lambda b: b["reports"][0]["analysis"].update(stage="preliminary"))
        for bad in (stale, preliminary):
            with self.assertRaises(PipelineError):
                self.confirm(bad)
        self.assertFalse(self.pipeline.status("a")["analysis_completed"])

    def test_confirmation_rechecks_local_review_and_fingerprint(self):
        receipt = self.analysis_receipt()
        manifest = self.pipeline.status("a")["manifest"]
        self.pipeline.ready("a", "worker", manifest)
        with self.assertRaises(PipelineError):
            self.confirm(receipt)
        self.pipeline.review("a", "worker", "coordinator", "Fixture reviewed again")
        (self.root / "demo/exercise/run.py").write_text("print(999)\n", encoding="utf-8")
        with self.assertRaises(PipelineError):
            self.confirm(receipt)
        self.assertEqual(self.api.scoped_reads, 0)

    def test_confirmation_reads_current_source_and_scoped_full_report(self):
        receipt = self.analysis_receipt()
        self.api.tasks[0]["summary"] = "website now has another source version"
        with self.assertRaises(PipelineError):
            self.confirm(receipt)
        self.api.tasks[0]["summary"] = "待核实的摘要"
        self.api.analysis_report["id"] = "different-current-report"
        with self.assertRaises(PipelineError):
            self.confirm(receipt)
        self.api.analysis_report["id"] = "full-a"
        self.api.analysis_report["analysis"]["stage"] = "preliminary"
        with self.assertRaises(PipelineError):
            self.confirm(receipt)
        self.assertFalse(self.pipeline.status("a")["analysis_completed"])
        self.assertGreaterEqual(self.api.scoped_reads, 3)
        self.assertEqual(self.api.upload_count, 0)

    def test_confirmed_analysis_survives_task_state_changes_but_not_source_changes(self):
        receipt = self.analysis_receipt()
        confirmed = self.confirm(receipt)
        self.api.tasks[0]["state"] = 3  # 用户点击完成；分析状态不借此声称任务完成时间。
        self.api.tasks[0]["updatedAt"] += 1
        self.pipeline.sync(self.api.tasks)
        self.assertTrue(self.pipeline.status("a")["analysis_completed"])
        self.assertIsNone(self.pipeline.status("a")["completed_at"])
        self.api.tasks[0]["summary"] += " source changed"
        self.api.tasks[0]["updatedAt"] += 1
        self.pipeline.sync(self.api.tasks)
        result = self.pipeline.status("a")
        self.assertFalse(result["analysis_completed"])
        self.assertIsNone(result["analysis_completed_at"])
        self.assertEqual(result["analysis_history"][0]["analysis_completed_at"], confirmed["analysis_completed_at"])
        self.assertIsNone(result["analysis_receipt"])
        self.assertEqual(self.pipeline.render()["confirmed_analysis"], 0)

    def test_merged_knowledge_note_requires_matching_handoff_and_new_review(self):
        receipt = self.analysis_receipt()
        manifest = self.pipeline.status("a")["manifest"]
        (self.root / "vault/demo.md").write_text("# Final merged note\nCoordinator merged fixture concepts and links.\n", encoding="utf-8")
        self.pipeline.ready("a", "worker", manifest)
        self.pipeline.review("a", "worker", "coordinator", "Merged fixture note and unchanged experiments reviewed")
        handoff_file = self.root / receipt["handoff"]
        handoff = json.loads(handoff_file.read_text(encoding="utf-8"))
        handoff["reports"]["full-a"]["knowledge"]["status"] = "pending_coordinator"
        handoff_file.write_text(json.dumps(handoff), encoding="utf-8")
        with self.assertRaises(PipelineError):
            self.confirm(receipt)
        handoff["reports"]["full-a"]["knowledge"]["status"] = "merged"
        handoff_file.write_text(json.dumps(handoff), encoding="utf-8")
        self.assertTrue(self.confirm(receipt)["analysis_completed"])

    def test_scope_read_failure_never_uses_backup_as_current_site_proof(self):
        receipt = self.analysis_receipt()
        self.api.analysis_scope = ("not-this-account", "not-this-list")
        with self.assertRaises(PipelineError) as caught:
            self.confirm(receipt)
        self.assertNotIn("secret", str(caught.exception))
        self.assertFalse(self.pipeline.status("a")["analysis_completed"])
        self.assertEqual(self.api.upload_count, 0)

    def test_confirmation_preserves_sanitized_scoped_http_status(self):
        receipt = self.analysis_receipt()
        with patch.object(self.api, "read_analysis", side_effect=PipelineError(
                "网站标签接口拒绝请求 HTTP 403；未把本地缓存当本次网站结果。")):
            with self.assertRaisesRegex(PipelineError, "HTTP 403"):
                self.confirm(receipt)
        self.assertFalse(self.pipeline.status("a")["analysis_completed"])
        self.assertEqual(self.api.upload_count, 0)

    def test_new_same_url_before_confirmed_record_is_duplicate_regardless_of_website_order(self):
        receipt = self.analysis_receipt()
        self.confirm(receipt)
        original = deepcopy(self.api.tasks[0])
        # 原文/摘要都不同，不能因为这是一条新记录而自动重复完整学习。
        newer = task("00-new", url="https://example.com/a?utm_source=new")
        newer["text"] = "不同的新分享文字 " + "https://example.com/a?utm_source=new"
        newer["summary"] = "另一段摘要，可能只需增补核实"
        newer["createdAt"] += 1000
        for snapshot in ([newer, original], [original, newer], [newer, original]):
            self.api.tasks = deepcopy(snapshot)
            self.pipeline.sync(snapshot)
            old_record = self.pipeline.status("a")
            new_record = self.pipeline.status("00-new")
            self.assertTrue(old_record["analysis_completed"])
            self.assertIsNone(old_record["duplicate_of"])
            self.assertEqual(new_record["duplicate_of"], "a")
            self.assertEqual(new_record["status"], "needs_review")
            self.assertIsNone(new_record["analysis_completed_at"])
            with self.assertRaises(PipelineError):
                self.pipeline.claim("new-worker", "00-new")
            with self.assertRaises(PipelineError):
                self.pipeline.start("00-new", "new-worker", "demo")
        self.assertEqual(self.api.upload_count, 0)

    def test_task_state_changes_do_not_move_confirmed_same_url_anchor(self):
        receipt = self.analysis_receipt()
        self.confirm(receipt)
        original = deepcopy(self.api.tasks[0])
        newer = task("00-new", url="https://example.com/a")
        for state in (1, 2, 3, 0):
            original["state"] = state
            original["updatedAt"] += 1
            self.api.tasks = deepcopy([newer, original])
            self.pipeline.sync(self.api.tasks)
            self.assertTrue(self.pipeline.status("a")["analysis_completed"])
            self.assertIsNone(self.pipeline.status("a")["duplicate_of"])
            self.assertEqual(self.pipeline.status("00-new")["duplicate_of"], "a")
            self.assertIsNone(self.pipeline.status("a")["completed_at"])

    def test_changed_confirmed_source_can_be_reanalyzed_without_new_same_url_task_stealing_anchor(self):
        receipt = self.analysis_receipt()
        self.confirm(receipt)
        original = deepcopy(self.api.tasks[0])
        original["summary"] += " 原来源版本发生变化"
        original["updatedAt"] += 1
        newer = task("00-new", url="https://example.com/a")
        self.api.tasks = deepcopy([newer, original])
        self.pipeline.sync(self.api.tasks)
        current = self.pipeline.status("a")
        self.assertFalse(current["analysis_completed"])
        self.assertIsNone(current["analysis_receipt"])
        self.assertIsNone(current["duplicate_of"])
        self.assertTrue(current["analysis_history"])
        self.assertEqual(self.pipeline.status("00-new")["duplicate_of"], "a")
        self.assertEqual(self.pipeline.claim("reanalyst", "a")["owner"], "reanalyst")
        with self.assertRaises(PipelineError):
            self.pipeline.claim("other", "00-new")
        with self.assertRaises(PipelineError):
            self.pipeline.confirm_analysis("a", "reanalyst", receipt, "coordinator")
        self.assertEqual(self.pipeline.render()["confirmed_analysis"], 0)

    def test_changed_original_url_releases_old_duplicate_for_fresh_analysis(self):
        receipt = self.analysis_receipt()
        self.confirm(receipt)
        original = deepcopy(self.api.tasks[0])
        newer = task("00-new", url="https://example.com/a")
        self.pipeline.sync([newer, original])
        self.assertEqual(self.pipeline.status("00-new")["duplicate_of"], "a")
        original["text"] = "修改到另一份来源 https://example.com/changed-source"
        original["updatedAt"] += 1
        self.api.tasks = deepcopy([newer, original])
        self.pipeline.sync(self.api.tasks)
        current = self.pipeline.status("00-new")
        self.assertIsNone(current["duplicate_of"])
        self.assertEqual(current["status"], "pending")
        self.assertEqual(self.pipeline.claim("new-worker", "00-new")["owner"], "new-worker")
        self.assertFalse(self.pipeline.status("a")["analysis_completed"])
        self.assertFalse(self.pipeline.status("00-new")["analysis_completed"])

    def test_unconfirmed_same_url_anchor_is_stable_when_first_seen_timestamp_ties(self):
        original = deepcopy(self.api.tasks[0])
        newer = task("00-new", url="https://example.com/a")
        self.pipeline.sync([newer, original])
        self.assertEqual(self.pipeline.status("a")["first_seen"], self.pipeline.status("00-new")["first_seen"])
        for snapshot in ([newer, original], [original, newer]):
            self.pipeline.sync(snapshot)
            self.assertIsNone(self.pipeline.status("a")["duplicate_of"])
            self.assertEqual(self.pipeline.status("00-new")["duplicate_of"], "a")


class ScopedReadClientTests(unittest.TestCase):
    @staticmethod
    def site():
        site = SiteAPI.__new__(SiteAPI)
        site._token = "test-secret"
        return site

    @staticmethod
    def response(value):
        return io.BytesIO(json.dumps(value).encode("utf-8"))

    def test_identity_then_record_use_shared_transport_read_only(self):
        calls = []
        def open_request(request, timeout):
            self.assertEqual(request.full_url, scoped_http.SITE + "/api/dot/agent")
            self.assertEqual(request.get_method(), "POST")
            self.assertEqual(request.get_header("User-agent"), scoped_http.HTTP_USER_AGENT)
            self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
            self.assertEqual(timeout, 45)
            payload = json.loads(request.data)
            calls.append((payload["listId"], payload["tool"], payload["arguments"]))
            if payload["tool"] == "reminder_identity":
                return self.response({"accountId": "account", "listId": "list"})
            return self.response({"record": {"id": "task"}, "report": {"analysis": {"stage": "full"}}})
        with patch.object(scoped_http.urllib.request, "build_opener",
                          return_value=SimpleNamespace(open=open_request)) as opener:
            result = self.site().read_analysis("account", "list", "task")
        self.assertEqual(opener.call_count, 2)
        self.assertTrue(all(call.args == (scoped_http.NoRedirect,) for call in opener.call_args_list))
        self.assertEqual(result["record"]["id"], "task")
        self.assertEqual(calls, [("list", "reminder_identity", {}),
                                 ("list", "reminder_read_record", {"taskId": "task"})])

    def test_mismatched_identity_stops_before_record_read(self):
        for identity in ({"accountId": "other", "listId": "list"},
                         {"accountId": "account", "listId": "other"}):
            calls = []
            def open_request(request, timeout):
                calls.append(json.loads(request.data)["tool"])
                return self.response(identity)
            with patch.object(scoped_http.urllib.request, "build_opener",
                              return_value=SimpleNamespace(open=open_request)):
                with self.assertRaisesRegex(PipelineError, "账户/列表不匹配"):
                    self.site().read_analysis("account", "list", "task")
            self.assertEqual(calls, ["reminder_identity"])

    def test_scoped_client_keeps_sanitized_http_status(self):
        error = urllib.error.HTTPError("https://test-secret.invalid", 403, "secret", {}, None)
        with patch.object(scoped_http.urllib.request, "build_opener",
                          side_effect=error):
            with self.assertRaisesRegex(PipelineError, "HTTP 403") as caught:
                self.site().read_analysis("account", "list", "task")
        self.assertNotIn("secret", str(caught.exception))

    def test_unexpected_client_exception_never_exposes_token(self):
        with patch.object(scoped_http.urllib.request, "build_opener",
                          side_effect=RuntimeError("token=secret must not escape")):
            with self.assertRaises(PipelineError) as caught:
                self.site().read_analysis("account", "list", "task")
        self.assertNotIn("secret", str(caught.exception))

    def test_network_failure_is_not_report_absence(self):
        with patch.object(scoped_http.urllib.request, "build_opener",
                          side_effect=urllib.error.URLError("token=secret")):
            with self.assertRaisesRegex(PipelineError, "网络读取失败") as caught:
                self.site().read_analysis("account", "list", "task")
        self.assertNotIn("secret", str(caught.exception))

    def test_redirect_rejected_without_following_location(self):
        self.assertIsNone(scoped_http.NoRedirect().redirect_request(
            None, None, 302, "redirect", {}, "https://test-secret.invalid"))
        with patch.object(scoped_http.urllib.request, "build_opener",
                          side_effect=urllib.error.HTTPError(
                              "https://test-secret.invalid", 302, "secret", {}, None)) as opener:
            with self.assertRaisesRegex(PipelineError, "HTTP 302") as caught:
                self.site().read_analysis("account", "list", "task")
        self.assertEqual(opener.call_count, 1)
        self.assertNotIn("secret", str(caught.exception))

    def test_response_read_is_bounded_and_oversize_is_rejected(self):
        reads = []
        class Response(io.BytesIO):
            def read(self, size=-1):
                reads.append(size)
                return super().read(size)
        def open_request(*args, **kwargs):
            return Response(b"123456789secret")
        with patch.object(scoped_http, "MAX_BUNDLE_BYTES", 8), patch.object(
                scoped_http.urllib.request, "build_opener",
                return_value=SimpleNamespace(open=open_request)):
            with self.assertRaisesRegex(PipelineError, "响应过大") as caught:
                self.site().read_analysis("account", "list", "task")
        self.assertEqual(reads, [9])
        self.assertNotIn("secret", str(caught.exception))

    def test_malformed_or_non_object_json_is_rejected_safely(self):
        for raw in (b"not JSON secret", b"[]", b"null", b"\xffsecret"):
            with patch.object(scoped_http.urllib.request, "build_opener",
                              return_value=SimpleNamespace(open=lambda *a, **kw: io.BytesIO(raw))):
                with self.assertRaisesRegex(PipelineError, "JSON") as caught:
                    self.site().read_analysis("account", "list", "task")
            self.assertNotIn("secret", str(caught.exception))

    def test_actual_package_agent_uses_same_transport_and_error_class(self):
        from tools import reminder_dot_agent, reminder_dot_backup, shiyi_sync
        self.assertIs(reminder_dot_agent.PipelineError, PipelineError)
        self.assertIs(reminder_dot_backup.PipelineError, PipelineError)
        self.assertIs(reminder_dot_agent.scoped_request, scoped_http.scoped_request)
        self.assertEqual(reminder_dot_backup.MAX_BUNDLE_BYTES, scoped_http.MAX_BUNDLE_BYTES)
        payloads = []
        def open_request(request, timeout):
            payloads.append(json.loads(request.data))
            return self.response({"saved": True})
        with patch.object(shiyi_sync, "get_token", return_value="test-secret"), patch.object(
                scoped_http.urllib.request, "build_opener",
                return_value=SimpleNamespace(open=open_request)):
            self.assertTrue(reminder_dot_agent.post("list", "reminder_save_analysis", {"taskId": "task"})["saved"])
        self.assertEqual(payloads, [{"listId": "list", "tool": "reminder_save_analysis",
                                     "arguments": {"taskId": "task"}}])
        with patch.object(shiyi_sync, "get_token", return_value="test-secret"), patch.object(
                scoped_http.urllib.request, "build_opener",
                side_effect=urllib.error.HTTPError("secret", 403, "secret", {}, None)):
            with self.assertRaisesRegex(PipelineError, "HTTP 403"):
                reminder_dot_agent.post("list", "reminder_identity", {})

    def test_script_and_package_imports_resolve_without_alias_injection(self):
        scripts = ["tools/reminder_pipeline.py", "tools/reminder_dot_agent.py", "tools/reminder_dot_backup.py"]
        for script in scripts:
            for arguments in ([script, "--help"], ["-m", script[:-3].replace("/", "."), "--help"]):
                result = subprocess.run([sys.executable, *arguments], cwd=ROOT,
                                        capture_output=True, text=True, encoding="utf-8", timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
