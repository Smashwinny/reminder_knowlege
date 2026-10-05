"""Local synthetic fixtures: no production website or GitHub writes."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import reminder_manual_sync as sync
from reminder_coordinator import acquire, release, status
from reminder_pipeline import PipelineError

TEST_ROOT = Path(__file__).resolve().parents[1] / "完成/.pipeline"
TEST_ROOT.mkdir(parents=True, exist_ok=True)


def command(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8").strip()


class ManualSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=TEST_ROOT)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        command(self.root, "init", "-b", "main")
        command(self.root, "config", "user.name", "Synthetic Test")
        command(self.root, "config", "user.email", "test@example.invalid")
        (self.root / "README.md").write_text("Synthetic test only\n", encoding="utf-8")
        command(self.root, "add", "--", "README.md")
        command(self.root, "commit", "-m", "Synthetic base")
        self.bare = self.root / "test-remote.git"
        command(self.root, "init", "--bare", str(self.bare))
        command(self.root, "remote", "add", "origin", str(self.bare))
        command(self.root, "push", "origin", "main")
        self.base = command(self.root, "rev-parse", "HEAD")
        self.patch_repo = patch.object(sync, "PUBLIC_REPO", str(self.bare))
        self.patch_repo.start()
        self.addCleanup(self.patch_repo.stop)
        self.config = self.root / sync.PRIVATE / "config.json"
        sync.save(self.config, {"accountId": "synthetic-account", "listId": "synthetic-list"})
        self.bundle = {"schema": "reminder-dot-export-v1", "accountId": "synthetic-account",
                       "list": {"id": "synthetic-list"}, "reports": [], "exportedAt": "synthetic-only"}
        sync.restore(self.root, json.dumps(self.bundle).encode(), self.bundle)
        self.file = self.root / "tools/demo.txt"
        self.file.parent.mkdir()
        self.file.write_text("Public synthetic artifact\n", encoding="utf-8")
        self.files_file = self.root / sync.PRIVATE / "files.txt"
        self.files_file.write_text("tools/demo.txt\n", encoding="utf-8")

    def prepare(self):
        return sync.prepare(self.root, self.config, self.files_file, "test: synthetic public artifact",
                            maintenance=True, review_notes="Synthetic content checked; no private data.")

    def run_sync(self, local_only=False):
        with patch.object(sync, "download", return_value=(json.dumps(self.bundle).encode(), self.bundle)):
            return sync.sync(self.root, self.config, local_only)

    def remote_head(self):
        return command(self.bare, "rev-parse", "refs/heads/main")

    def test_publication_and_repeat_are_idempotent_and_preserve_root_edits(self):
        receipt = self.prepare()
        (self.root / "README.md").write_text("Uncommitted user note\n", encoding="utf-8")
        first = self.run_sync()
        commit = self.remote_head()
        self.assertNotEqual(commit, self.base)
        self.assertEqual(first["publishedBatches"], 1)
        self.assertEqual(sync.load(receipt)["status"], "pushed")
        self.assertEqual(command(self.bare, "show", commit + ":tools/demo.txt"), "Public synthetic artifact")
        self.assertEqual(command(self.bare, "log", "-1", "--format=%an <%ae>"), "Synthetic Test <test@example.invalid>")
        second = self.run_sync()
        self.assertEqual(second["publishedBatches"], 0)
        self.assertEqual(self.remote_head(), commit)
        self.assertEqual((self.root / "README.md").read_text(), "Uncommitted user note\n")
        self.assertIsNone(status(self.root)["owner"])

    def test_push_failure_keeps_commit_and_retry_does_not_recommit(self):
        receipt = self.prepare()
        real_git = sync.git
        def fail_push(repo, *args, **kwargs):
            if args[0] == "push":
                raise PipelineError("Synthetic push failure")
            return real_git(repo, *args, **kwargs)
        with patch.object(sync, "git", side_effect=fail_push):
            with self.assertRaisesRegex(PipelineError, "Synthetic push failure"):
                self.run_sync()
        saved = sync.load(receipt)
        self.assertEqual(saved["status"], "committed")
        self.assertEqual(self.remote_head(), self.base)
        self.assertEqual(sync.load(self.root / sync.PRIVATE / "manual-sync-status.json")["local"], "verified")
        self.run_sync()
        self.assertEqual(self.remote_head(), saved["commit"])

    def test_unknown_root_staging_stops_git_without_touching_it(self):
        self.prepare()
        command(self.root, "add", "--", "tools/demo.txt")
        staged_before = command(self.root, "diff", "--cached", "--binary")
        with self.assertRaisesRegex(PipelineError, "主工作区暂存区非空"):
            self.run_sync()
        self.assertEqual(command(self.root, "diff", "--cached", "--binary"), staged_before)
        self.assertEqual(self.remote_head(), self.base)

    def test_unknown_publication_staging_is_preserved(self):
        self.prepare()
        repo = sync.publication_repo(self.root)
        (repo / "foreign.txt").write_text("Other worker's synthetic file\n", encoding="utf-8")
        command(repo, "add", "--", "foreign.txt")
        staged_before = command(repo, "diff", "--cached", "--binary")
        with self.assertRaisesRegex(PipelineError, "暂存区有归属不明"):
            self.run_sync()
        self.assertEqual(command(repo, "diff", "--cached", "--binary"), staged_before)
        self.assertEqual(self.remote_head(), self.base)

    def test_changed_bytes_after_review_cannot_be_uploaded(self):
        receipt = self.prepare()
        self.file.write_text("Changed after review\n", encoding="utf-8")
        with self.assertRaisesRegex(PipelineError, "审阅后有变化"):
            self.run_sync()
        self.assertEqual(self.remote_head(), self.base)
        self.assertEqual(sync.load(receipt)["status"], "prepared")

    def test_private_paths_and_credentials_are_rejected(self):
        for name in ["完成/.pipeline/config.json", "../README.md", "tools/../README.md", "tools",
                     "tools/.shiyi_token", "tools/.env", "tools/repo/file.md", "tools/key.pem"]:
            with self.subTest(path=name), self.assertRaises(PipelineError):
                sync.public_path(self.root, name, set(), True)
        self.file.write_text("synthetic-account private identity\n", encoding="utf-8")
        receipt = self.prepare()
        handoff = sync.load(self.root / sync.PRIVATE / "dot/synthetic-account/synthetic-list/handoff.json")
        with self.assertRaisesRegex(PipelineError, "私有身份"):
            sync.check_publication(self.root, sync.load(receipt), self.bundle, handoff)
        self.assertEqual(self.remote_head(), self.base)

    def test_local_only_leaves_publication_pending(self):
        receipt = self.prepare()
        result = self.run_sync(local_only=True)
        self.assertEqual(result["local"], "verified")
        self.assertEqual(result["git"], "local_only")
        self.assertEqual(self.remote_head(), self.base)
        self.assertEqual(sync.load(receipt)["status"], "prepared")

    def test_network_failure_never_uses_cache_or_runs_git(self):
        self.prepare()
        handoff_file = self.root / sync.PRIVATE / "dot/synthetic-account/synthetic-list/handoff.json"
        original = handoff_file.read_bytes()
        with patch.object(sync, "download", side_effect=PipelineError("Synthetic network failure")):
            with self.assertRaisesRegex(PipelineError, "Synthetic network failure"):
                sync.sync(self.root, self.config)
        self.assertEqual(self.remote_head(), self.base)
        self.assertEqual(handoff_file.read_bytes(), original)
        self.assertEqual(sync.load(self.root / sync.PRIVATE / "manual-sync-status.json")["git"], "not_run")
        self.assertIsNone(status(self.root)["owner"])

    def test_another_coordinator_is_not_reclaimed(self):
        acquire(self.root, "synthetic-other-owner")
        try:
            with self.assertRaisesRegex(RuntimeError, "协调者已由"):
                self.run_sync()
            self.assertEqual(status(self.root)["owner"], "synthetic-other-owner")
        finally:
            release(self.root, "synthetic-other-owner")

    def test_remote_divergence_after_failed_push_is_preserved(self):
        receipt = self.prepare()
        real_git = sync.git
        def fail_push(repo, *args, **kwargs):
            if args[0] == "push":
                raise PipelineError("Synthetic push failure")
            return real_git(repo, *args, **kwargs)
        with patch.object(sync, "git", side_effect=fail_push), self.assertRaises(PipelineError):
            self.run_sync()
        saved_commit = sync.load(receipt)["commit"]
        (self.root / "other.txt").write_text("Separate device synthetic change\n", encoding="utf-8")
        command(self.root, "add", "--", "other.txt")
        command(self.root, "commit", "-m", "Synthetic other device")
        command(self.root, "push", "origin", "main")
        other_commit = self.remote_head()
        with self.assertRaises(PipelineError):
            self.run_sync()
        self.assertEqual(self.remote_head(), other_commit)
        self.assertEqual(sync.load(receipt)["commit"], saved_commit)
        self.assertEqual(command(self.root / sync.PRIVATE / "knowledge-publication", "rev-parse", "HEAD"), saved_commit)

    def test_interrupted_staging_resumes_only_its_own_files(self):
        receipt = self.prepare()
        real_git = sync.git
        def fail_commit(repo, *args, **kwargs):
            if "commit" in args:
                raise PipelineError("Synthetic interruption before commit")
            return real_git(repo, *args, **kwargs)
        with patch.object(sync, "git", side_effect=fail_commit), self.assertRaises(PipelineError):
            self.run_sync()
        self.assertEqual(sync.load(receipt)["status"], "committing")
        self.assertEqual(self.remote_head(), self.base)
        self.run_sync()
        self.assertEqual(sync.load(receipt)["status"], "pushed")

    def test_crash_after_commit_recovers_same_commit(self):
        receipt = self.prepare()
        real_git = sync.git
        def interrupt_after_commit(repo, *args, **kwargs):
            value = real_git(repo, *args, **kwargs)
            if "commit" in args:
                raise PipelineError("Synthetic crash after commit")
            return value
        with patch.object(sync, "git", side_effect=interrupt_after_commit), self.assertRaises(PipelineError):
            self.run_sync()
        repo = self.root / sync.PRIVATE / "knowledge-publication"
        saved_commit = command(repo, "rev-parse", "HEAD")
        self.assertEqual(sync.load(receipt)["status"], "committing")
        self.run_sync()
        self.assertEqual(self.remote_head(), saved_commit)
        self.assertEqual(sync.load(receipt)["commit"], saved_commit)

    def test_foreign_staged_bytes_after_interruption_are_not_overwritten(self):
        receipt = self.prepare()
        real_git = sync.git
        def fail_commit(repo, *args, **kwargs):
            if "commit" in args:
                raise PipelineError("Synthetic interruption")
            return real_git(repo, *args, **kwargs)
        with patch.object(sync, "git", side_effect=fail_commit), self.assertRaises(PipelineError):
            self.run_sync()
        repo = self.root / sync.PRIVATE / "knowledge-publication"
        result = subprocess.run(["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                                input=b"Other worker staged these bytes\n", capture_output=True, check=True)
        command(repo, "update-index", "--cacheinfo", "100644", result.stdout.decode().strip(), "tools/demo.txt")
        staged_before = command(repo, "diff", "--cached", "--binary")
        with self.assertRaisesRegex(PipelineError, "暂存字节发生变化"):
            self.run_sync()
        self.assertEqual(command(repo, "diff", "--cached", "--binary"), staged_before)
        self.assertEqual(sync.load(receipt)["status"], "committing")
        self.assertEqual(self.remote_head(), self.base)

    def test_learning_gate_rejects_pending_owned_or_stale_evidence(self):
        report = {"id": "synthetic-report", "taskId": "synthetic-task", "sourceHash": "hash", "owner": "synthetic-author",
                  "analysis": {"stage": "full"}, "stale": False, "activeClaim": False}
        handoff = {"reports": {report["id"]: {"sourceHash": "hash", "local": {"status": "verified"}, "knowledge": {"status": "merged"}}}}
        row = {"phase": "analysis_confirmed", "owner": None, "invalidated": False, "deleted": False,
               "missing": False, "content_hash": "hash", "analysis_receipt": json.dumps({"report_id": report["id"], "source_hash": "hash"}),
               "review": json.dumps({"approved": True, "reviewer": "synthetic-independent", "artifact_fingerprint": "fingerprint"}),
               "manifest": "{}", "artifact_fingerprint": "fingerprint"}
        with patch.object(sync, "task_row", return_value=row), patch.object(sync.Pipeline, "_validate_manifest", return_value=({"topic": "Synthetic"}, "fingerprint")):
            self.assertEqual(sync.check_learning(self.root, report, handoff), {"topic": "Synthetic"})
        for field, value in [("phase", "ready"), ("owner", "other-owner"), ("invalidated", True),
                             ("content_hash", "changed"), ("review", json.dumps({"approved": False}))]:
            variant = {**row, field: value}
            with self.subTest(field=field), patch.object(sync, "task_row", return_value=variant), self.assertRaises(PipelineError):
                sync.check_learning(self.root, report, handoff)
        for key in ("stale", "activeClaim"):
            with self.subTest(field=key), patch.object(sync, "task_row", return_value=row), self.assertRaises(PipelineError):
                sync.check_learning(self.root, {**report, key: True}, handoff)
        pending = copy.deepcopy(handoff)
        pending["reports"][report["id"]]["knowledge"]["status"] = "pending_coordinator"
        with patch.object(sync, "task_row", return_value=row), self.assertRaises(PipelineError):
            sync.check_learning(self.root, report, pending)


if __name__ == "__main__":
    unittest.main()
