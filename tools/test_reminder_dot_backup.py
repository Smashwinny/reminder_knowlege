import copy
import base64
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from reminder_dot_backup import validate_bundle, restore, integrate
from reminder_pipeline import Pipeline, PipelineError, task_hash

TEST_ROOT = Path(__file__).resolve().parents[1] / "完成/.pipeline/dot-test-tmp"
TEST_ROOT.mkdir(parents=True, exist_ok=True)


def bundle():
    record = {"id": "one", "text": "https://example.com/a", "summary": "原摘要", "state": 0, "createdAt": 1}
    md = "# 云端初步分析\n\n来源核对、判断理由、知识关联与建议下一步。\n"
    return {"schema": "reminder-dot-export-v1", "accountId": "account-1", "list": {"id": "list-1", "name": "Dot 待分析"}, "exportedAt": "2026-10-04T01:00:00Z", "reports": [{
        "id": "report-1", "taskId": "one", "userId": "account-1", "listId": "list-1", "record": record, "sourceHash": task_hash(record),
        "markdown": md, "markdownSha256": hashlib.sha256(md.encode()).hexdigest(), "createdAt": "2026-10-04T00:59:00Z", "stale": False, "activeClaim": False,
        "analysis": {"kind": "learning", "title": "示例", "recordContent": "已核对原文", "reason": "有可复现内容", "knownKnowledge": "等待本机知识查重", "nextStep": "手动选择开始学习", "uncertainties": "未实际运行实验", "sources": [{"url": "https://example.com/a", "status": "read", "facts": "已核对测试原文"}]},
    }]}


class FakeSite:
    def __init__(self, records): self.records = records
    def download(self): return self.records
    def upload(self, task): raise AssertionError("Backup/import must never write site")


class DotBackupTests(unittest.TestCase):
    def test_wrong_account_list_traversal_and_corrupt_checksums_rejected(self):
        good = bundle()
        self.assertIs(validate_bundle(good, "account-1", "list-1"), good)
        with self.assertRaises(PipelineError): validate_bundle(good, "another-account", "list-1")
        with self.assertRaises(PipelineError): validate_bundle(good, "account-1", "another-list")
        for key, value in [("taskId", "../escape"), ("id", "NUL"), ("markdown", "tampered"), ("sourceHash", "0" * 64), ("userId", "other-user")]:
            bad = copy.deepcopy(good); bad["reports"][0][key] = value
            with self.assertRaises(PipelineError): validate_bundle(bad, "account-1", "list-1")

    def test_idempotent_restore_preserves_cloud_and_conflicting_local_files(self):
        good = bundle(); raw = json.dumps(good, ensure_ascii=False).encode()
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as tmp:
            one = restore(tmp, raw, good); two = restore(tmp, raw, good)
            self.assertEqual(one["added"], 1); self.assertEqual(two["added"], 0)
            self.assertFalse(one["cloudDeleted"])
            self.assertEqual(Path(one["archive"]).read_bytes(), raw)
            file = Path(tmp) / "完成/.pipeline/dot/account-1/list-1/reports/one/report-1.md"
            file.write_text("local edit", encoding="utf-8")
            with self.assertRaises(PipelineError): restore(tmp, raw, good)
            self.assertEqual(file.read_text(encoding="utf-8"), "local edit")
            self.assertFalse((Path(tmp) / "完成/.pipeline/dot/account-1/list-1/.restore.lock").exists())

    def test_queue_import_uses_existing_claim_classify_release_and_never_starts(self):
        good = bundle(); site = FakeSite([good["reports"][0]["record"]])
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as tmp:
            p = Pipeline(tmp, api=site)
            with patch("reminder_dot_backup.Pipeline", return_value=p), patch("reminder_dot_backup.download", return_value=(b"", good)):
                first = integrate(tmp, good)
                second = integrate(tmp, good)
            self.assertEqual(first[0]["status"], "classified_imported")
            self.assertEqual(second[0]["status"], "backup_only")
            record = p.status("one")
            self.assertEqual(record["classification"]["kind"], "learning")
            self.assertFalse(record["learning_started"])
            self.assertIsNone(record["owner"])
            self.assertIsNone(record["completed_at"])

    def test_stale_remote_lease_or_other_local_owner_remains_backup_only(self):
        for flag in ("stale", "activeClaim", "local_owner", "source_changed", "missing"):
            good = bundle()
            if flag in ("stale", "activeClaim"): good["reports"][0][flag] = True
            records = [copy.deepcopy(good["reports"][0]["record"])]
            if flag == "source_changed": records[0]["text"] = "new source"
            if flag == "missing": records = []
            with tempfile.TemporaryDirectory(dir=TEST_ROOT) as tmp:
                p = Pipeline(tmp, api=FakeSite(records)); p.sync()
                if flag == "local_owner": p.claim("other-owner", task_id="one")
                with patch("reminder_dot_backup.Pipeline", return_value=p), patch("reminder_dot_backup.download", return_value=(b"", good)): result = integrate(tmp, good)
                self.assertEqual(result[0]["status"], "backup_only")
                if flag == "local_owner": self.assertEqual(p.status("one")["owner"], "other-owner")

    def test_corrupt_report_never_qualifies_as_non_learning_without_read_sources(self):
        good = bundle(); report = good["reports"][0]
        report["analysis"]["kind"] = "non_learning"
        report["analysis"]["sources"][0]["status"] = "403"
        with self.assertRaises(PipelineError): validate_bundle(good, "account-1", "list-1")

    def test_historical_export_does_not_override_current_cloud_claim_or_list_removal(self):
        for mode in ("new_claim", "removed"):
            historical = bundle(); current = copy.deepcopy(historical)
            if mode == "new_claim": current["reports"][0]["activeClaim"] = True
            else: current["reports"] = []
            with tempfile.TemporaryDirectory(dir=TEST_ROOT) as tmp:
                p = Pipeline(tmp, api=FakeSite([historical["reports"][0]["record"]]))
                with patch("reminder_dot_backup.Pipeline", return_value=p), patch("reminder_dot_backup.download", return_value=(b"", current)):
                    result = integrate(tmp, historical)
                self.assertEqual(result[0]["status"], "backup_only")
                self.assertIsNone(p.status("one")["classification"]["kind"])

    def test_full_artifacts_are_checked_restored_once_and_never_mark_task_complete(self):
        good = bundle(); report = good["reports"][0]
        contents = {"guide_pdf": b"%PDF-1.4\n% Synthetic test-only fixture\n%%EOF", "guide_html": b"<!doctype html><html><body>Test-only fixture.</body></html>", "exercise_archive": b"PK\x03\x04" + b"0" * 40, "experiment_log": b"Synthetic test-only experiment log", "knowledge_notes": b"Synthetic test-only knowledge note", "review_log": b"Synthetic test-only independent review"}
        artifacts = [{"role": role, "base64": base64.b64encode(data).decode(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()} for role, data in contents.items()]
        report["owner"] = "learner"
        report["analysis"].update(stage="full", completion={"reviewer": "separate-reviewer", "pdfRendered": True, "experimentChecked": True, "knowledgeChecked": True, "artifacts": artifacts})
        validate_bundle(good, "account-1", "list-1")
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as tmp:
            raw = json.dumps(good).encode()
            first = restore(tmp, raw, good); second = restore(tmp, raw, good)
            files = Path(tmp) / "完成/.pipeline/dot/account-1/list-1/reports/one/report-1-files"
            self.assertEqual(len(list(files.iterdir())), 6)
            self.assertEqual(first["added"], 1); self.assertEqual(second["added"], 0)
            self.assertFalse(first["cloudDeleted"])
            (files / "guide_pdf.pdf").write_bytes(b"local-edited-pdf")
            with self.assertRaises(PipelineError): restore(tmp, raw, good)
        bad = copy.deepcopy(good); bad["reports"][0]["analysis"]["completion"]["artifacts"][0]["base64"] = base64.b64encode(b"tampered").decode()
        with self.assertRaises(PipelineError): validate_bundle(bad, "account-1", "list-1")

    def test_non_link_is_distinct_from_non_learning_and_stays_private_without_fake_evidence(self):
        good = bundle(); report = good["reports"][0]
        report["record"]["text"] = "买书并记下纸上笔记"
        report["sourceHash"] = task_hash(report["record"])
        report["analysis"].update(kind="non_link", sources=[])
        validate_bundle(good, "account-1", "list-1")
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as tmp:
            p = Pipeline(tmp, api=FakeSite([report["record"]]))
            with patch("reminder_dot_backup.Pipeline", return_value=p), patch("reminder_dot_backup.download", return_value=(b"", good)):
                result = integrate(tmp, good)
            self.assertEqual(result[0]["status"], "backup_only")
            self.assertIsNone(p.status("one")["classification"]["kind"])
            self.assertIsNone(p.status("one")["completed_at"])
        report["record"]["text"] += " https://example.com/a"
        report["sourceHash"] = task_hash(report["record"])
        with self.assertRaises(PipelineError): validate_bundle(good, "account-1", "list-1")


if __name__ == "__main__": unittest.main()
