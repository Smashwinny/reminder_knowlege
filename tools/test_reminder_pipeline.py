# -*- coding: utf-8 -*-
"""运行：python -m unittest tools.test_reminder_pipeline -v（不访问真实网站）。"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

from tools.reminder_pipeline import Pipeline, PipelineError, ROOT, canonical_url


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


if __name__ == "__main__":
    unittest.main()
