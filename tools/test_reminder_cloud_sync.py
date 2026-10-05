"""Real local Git objects, synthetic reports; no production writes or networking."""
import base64
import copy
import json
from pathlib import Path
import subprocess
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import reminder_cloud_sync as cloud
import reminder_manual_sync as manual
from reminder_coordinator import acquire, release
from reminder_dot_backup import restore
from reminder_pipeline import PipelineError, task_hash
from test_reminder_dot_backup import bundle

TMP = Path(__file__).resolve().parents[1] / "完成/.pipeline"


def command(path, *args):
    result = subprocess.run(["git", "-C", str(path), *args], capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr.decode(errors="replace"))
    return result.stdout.decode().strip()


class CloudSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        command(self.root, "init", "-b", "main")
        command(self.root, "config", "user.name", "Synthetic Test")
        command(self.root, "config", "user.email", "test@example.invalid")
        (self.root / "vault").mkdir()
        (self.root / "vault/00-总览.md").write_bytes(b"# Synthetic base\n")
        command(self.root, "add", "--", "vault/00-总览.md")
        command(self.root, "commit", "-m", "Synthetic base")
        self.base = command(self.root, "rev-parse", "HEAD")
        self.source = self.root / "source"
        command(self.root, "clone", "--", str(self.root), str(self.source))
        command(self.source, "config", "user.name", "Synthetic Test")
        command(self.source, "config", "user.email", "test@example.invalid")
        self.bundle = bundle()
        self.report = self.bundle["reports"][0]
        self.report["owner"] = "synthetic-learner"
        roles = {"guide_pdf": b"%PDF-1.4\nSynthetic fixture only\n%%EOF", "guide_html": b"<!doctype html><html>Synthetic fixture only</html>",
                 "exercise_archive": b"PK\x03\x04" + b"0"*40, "experiment_log": b"Synthetic experiment fixture only", "knowledge_notes": b"Synthetic knowledge fixture only", "review_log": b"Synthetic independent review fixture"}
        self.report["analysis"].update(stage="full", completion={"project":"demo", "reviewer":"synthetic-reviewer", "pdfRendered":True, "experimentChecked":True, "knowledgeChecked":True,
            "artifacts":[{"role":k,"base64":base64.b64encode(v).decode(),"bytes":len(v),"sha256":cloud.sha(v)} for k,v in roles.items()]})
        self.files = {"demo/demo-小白指南.pdf":roles["guide_pdf"],"demo/guide.html":roles["guide_html"],"demo/experiment_log.txt":roles["experiment_log"],
                      "demo/exercise/demo.py":b"print('Synthetic fixture')\n", "vault/00-总览.md":b"# Synthetic merged MOC\n", "vault/项目笔记/demo.md":b"# Synthetic project note\n"}
        for name,data in self.files.items():
            file = self.source / name; file.parent.mkdir(parents=True,exist_ok=True); file.write_bytes(data)
            command(self.source,"add","--",name)
        command(self.source,"commit","-m","Synthetic cloud publication")
        self.commit = command(self.source,"rev-parse","HEAD")
        self.report["cloudDelivery"] = {"id":"delivery-1","state":"pushed","receipt":{
            "schema":"reminder-cloud-publication-v1","repository":cloud.REPOSITORY,"branch":"main","reportId":self.report["id"],"sourceHash":self.report["sourceHash"],
            "commit":self.commit,"baseCommit":self.base,"fingerprint":"1"*64,"reviewer":"synthetic-reviewer","pushedAt":"2026-10-05T00:00:00Z",
            "files":[{"path":name,"sha256":cloud.sha(data),"baseSha256":cloud.sha(b"# Synthetic base\n") if name=="vault/00-总览.md" else None} for name,data in self.files.items()]}}
        self.mirror = object.__new__(cloud.PublicMirror); self.mirror.path = self.source / ".git"
        command(self.source,"update-ref","refs/remotes/origin/main",self.commit)
        self.restore()
        self.owner="synthetic-coordinator"; acquire(self.root,self.owner)
        self.addCleanup(release,self.root,self.owner)

    def restore(self):
        return restore(self.root,json.dumps(self.bundle,ensure_ascii=False).encode(),self.bundle)

    def run_copy(self):
        return cloud.apply_cloud_receipts(self.root,self.bundle,self.owner,lambda root:self.mirror)

    def handoff(self):
        return json.loads((self.root/"完成/.pipeline/dot/account-1/list-1/handoff.json").read_text(encoding="utf-8"))["reports"][self.report["id"]]

    def test_copy_verified_objects_and_repeat_preserves_receipts_and_root_head(self):
        self.assertEqual(self.run_copy()["localKnowledgeSynced"],1)
        for name,data in self.files.items(): self.assertEqual((self.root/name).read_bytes(),data)
        self.restore(); self.run_copy()
        self.assertEqual(self.handoff()["git"]["commit"],self.commit)
        self.assertEqual(self.handoff()["localKnowledge"]["status"],"synced")
        self.assertEqual(command(self.root,"rev-parse","HEAD"),self.base)

    def test_user_edits_preserved_and_git_success_separate_from_local_conflict(self):
        (self.root/"vault/00-总览.md").write_bytes(b"My own unsynced note\n")
        result=self.run_copy()
        self.assertEqual(len(result["conflicts"]),1)
        self.assertEqual((self.root/"vault/00-总览.md").read_bytes(),b"My own unsynced note\n")
        self.assertEqual(self.handoff()["git"]["status"],"pushed")
        self.assertEqual(self.handoff()["knowledge"]["status"],"merged")
        self.assertEqual(self.handoff()["localKnowledge"]["status"],"conflict")
        self.assertFalse((self.root/"demo/guide.html").exists())

    def test_wrong_actual_hash_base_or_binding_cannot_copy(self):
        original=copy.deepcopy(self.report["cloudDelivery"])
        for key in ("sha256","baseSha256"):
            self.report["cloudDelivery"]=copy.deepcopy(original)
            self.report["cloudDelivery"]["receipt"]["files"][0][key]="f"*64
            with self.assertRaises(PipelineError): self.run_copy()
            self.assertFalse((self.root/"demo/guide.html").exists())
        self.report["cloudDelivery"]=original
        self.report["analysis"]["completion"]["artifacts"][0]["sha256"]="e"*64
        with self.assertRaises(PipelineError): self.run_copy()

    def test_stale_claimed_or_unpublished_receipts_are_backup_only(self):
        for flag in ("stale","activeClaim"):
            self.report[flag]=True
            self.assertEqual(self.run_copy()["cloudPublished"],0)
            self.report[flag]=False
        self.report["cloudDelivery"]["state"]="publishing"
        self.assertEqual(self.run_copy()["cloudPublished"],0)

    def test_nonempty_staging_stops_copy_without_touching_it(self):
        (self.root/"user.txt").write_text("user staging",encoding="utf-8")
        command(self.root,"add","--","user.txt")
        before=command(self.root,"diff","--cached","--binary")
        with self.assertRaises(PipelineError): self.run_copy()
        self.assertEqual(command(self.root,"diff","--cached","--binary"),before)

    def test_old_local_owner_is_preserved_and_blocks_project_overwrite(self):
        connection=sqlite3.connect(self.root/"完成/.pipeline/queue.sqlite3")
        connection.execute('CREATE TABLE tasks(task_id TEXT, project_key TEXT, owner TEXT)')
        connection.execute('INSERT INTO tasks VALUES(?,?,?)',(self.report['taskId'],'demo','original-owner'))
        connection.commit();connection.close()
        result=self.run_copy()
        self.assertEqual(result['conflicts'][0]['paths'],['demo/'])
        self.assertFalse((self.root/'demo/guide.html').exists())
        self.assertEqual(self.handoff()['git']['status'],'pushed')
        connection=sqlite3.connect(self.root/"完成/.pipeline/queue.sqlite3")
        self.assertEqual(connection.execute('SELECT owner FROM tasks').fetchone()[0],'original-owner')
        connection.close()

    def test_two_cloud_merges_copy_latest_moc_from_original_base_without_rollback(self):
        other=copy.deepcopy(self.report)
        other.update(id="report-2",taskId="two",createdAt="2026-10-05T01:00:00Z")
        other["record"]["id"]="two";other["sourceHash"]=task_hash(other["record"])
        other["analysis"]["completion"]["project"]="demo2"
        files={name.replace("demo/","demo2/",1).replace("demo-小白","demo2-小白"):data for name,data in self.files.items() if name.startswith("demo/")}
        files.update({"vault/00-总览.md":b"# Synthetic latest MOC\n","vault/项目笔记/demo2.md":b"# Second synthetic project\n"})
        for name,data in files.items():
            target=self.source/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            command(self.source,"add","--",name)
        command(self.source,"commit","-m","Synthetic second cloud publication")
        second=command(self.source,"rev-parse","HEAD")
        value=other["cloudDelivery"]["receipt"]
        value.update(reportId=other["id"],sourceHash=other["sourceHash"],baseCommit=self.commit,commit=second,pushedAt="2026-10-05T01:00:00Z",files=[
            {"path":name,"sha256":cloud.sha(data),"baseSha256":cloud.sha(self.files[name]) if name in self.files else None} for name,data in files.items()])
        command(self.source,"update-ref","refs/remotes/origin/main",second)
        self.bundle["reports"].append(other);self.restore()
        self.assertEqual(self.run_copy()["localKnowledgeSynced"],2)
        self.assertEqual((self.root/"vault/00-总览.md").read_bytes(),files["vault/00-总览.md"])
        self.restore();self.run_copy()
        self.assertEqual((self.root/"vault/00-总览.md").read_bytes(),files["vault/00-总览.md"])

    def test_paths_remote_commit_and_malformed_receipts_rejected(self):
        for name in ["../escape.md","demo/.env","vault/../key.md","demo/NUL.md","vault/new.md"]:
            with self.assertRaises(PipelineError): cloud.public_path(self.root,name,"demo")
        with patch.object(Path,'is_symlink',return_value=True), self.assertRaises(PipelineError):
            cloud.public_path(self.root,'demo/guide.html','demo')
        with self.assertRaises(PipelineError): self.mirror.verify_commit("f"*40)
        self.report["cloudDelivery"]="malformed"
        with self.assertRaises(PipelineError): cloud.receipt(self.report)

    def direct_fixture(self, mutate=None, extra_file=None):
        """Publish real synthetic Git objects without a server delivery receipt."""
        self.report.pop("cloudDelivery", None)
        base = command(self.source, "rev-parse", "HEAD")
        # Model a Windows vault already at the publication's known Git baseline.
        (self.root / "vault/00-总览.md").write_bytes((self.source / "vault/00-总览.md").read_bytes())
        artifacts = self.report["analysis"]["completion"]["artifacts"]
        extensions = {"guide_pdf": ".pdf", "guide_html": ".html", "exercise_archive": ".zip",
                      "experiment_log": ".txt", "knowledge_notes": ".md", "review_log": ".md"}
        entries, files = [], {}
        for original in artifacts:
            role = original["role"]
            name = "demo/delivery/" + role + extensions[role]
            data = base64.b64decode(original["base64"])
            if role == "experiment_log":
                data = b"Redacted public synthetic log; this is no real learning evidence.\n"
            files[name] = data
            entries.append({"path": name, "sha256": cloud.sha(data), "baseSha256": None,
                            "artifactRole": role, "sourceSha256": original["sha256"]})
        for name, data in {"vault/00-总览.md": b"# Synthetic direct merged MOC\n",
                           "vault/项目笔记/demo.md": b"# Synthetic direct project note\n"}.items():
            before = (self.source / name).read_bytes()
            files[name] = data
            entries.append({"path": name, "sha256": cloud.sha(data), "baseSha256": cloud.sha(before)})
        manifest = {"schema": "reminder-learning-publication-v1", "repository": cloud.REPOSITORY,
                    "branch": "main", "project": "demo", "baseCommit": base,
                    "reviewPath": "demo/delivery/review_log.md", "files": entries}
        if mutate:
            mutate(manifest)
        files["demo/delivery/publication-manifest.json"] = json.dumps(manifest, ensure_ascii=False).encode()
        if extra_file:
            files[extra_file] = b"Synthetic unrelated file\n"
        for name, data in files.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            command(self.source, "add", "--", name)
        command(self.source, "commit", "-m", "Synthetic Dot direct publication")
        direct_commit = command(self.source, "rev-parse", "HEAD")
        command(self.source, "update-ref", "refs/remotes/origin/main", direct_commit)
        self.restore()
        return direct_commit, files

    def test_direct_git_without_server_receipt_copies_redacted_files_and_zip(self):
        commit, files = self.direct_fixture()
        result = self.run_copy()
        self.assertEqual(result["cloudPublished"], 1)
        self.assertEqual(result["localKnowledgeSynced"], 1)
        for name, data in files.items():
            self.assertEqual((self.root / name).read_bytes(), data)
        self.assertNotEqual(self.handoff().get("cloudDelivery", {}).get("status"), "verified")
        self.assertEqual(self.handoff()["dotDirectGit"]["status"], "verified")
        self.assertEqual(self.handoff()["git"]["commit"], commit)
        self.assertEqual(command(self.root, "rev-parse", "HEAD"), self.base)
        # Direct Git never calls a website tool that is not deployed.
        with patch("reminder_dot_agent.post", side_effect=AssertionError("No server delivery tool")):
            self.assertEqual(cloud.acknowledge_local_backups(self.root, self.bundle, self.owner, self.restore()["archive"]),
                             {"acknowledged": 0, "pending": 0})
        self.assertEqual(self.run_copy()["localKnowledgeSynced"], 1)
        self.restore()
        self.assertEqual(self.handoff()["dotDirectGit"]["receipt"]["commit"], commit)

    def test_direct_publication_other_originals_remain_pending(self):
        self.direct_fixture(lambda m: m["files"][0].update(sourceSha256="f" * 64))
        self.assertEqual(self.run_copy()["cloudPublished"], 0)
        self.assertFalse((self.root / "demo/delivery/guide_pdf.pdf").exists())

    def test_direct_publication_wrong_hash_cannot_copy(self):
        self.direct_fixture(lambda m: m["files"][0].update(sha256="f" * 64))
        with self.assertRaises(PipelineError):
            self.run_copy()
        self.assertFalse((self.root / "demo/delivery/guide_pdf.pdf").exists())

    def test_direct_publication_unlisted_commit_files_cannot_copy(self):
        self.direct_fixture(extra_file="tools/unrelated.json")
        with self.assertRaises(PipelineError):
            self.run_copy()
        self.assertFalse((self.root / "demo/delivery/guide_pdf.pdf").exists())

    def test_direct_publication_private_metadata_is_rejected(self):
        self.direct_fixture(lambda m: m.update(taskId="synthetic-private-task"))
        with self.assertRaises(PipelineError):
            self.run_copy()

    def test_direct_publication_duplicate_roles_or_missing_review_rejected(self):
        self.direct_fixture(lambda m: m["files"][1].update(artifactRole="guide_pdf"))
        with self.assertRaises(PipelineError):
            self.run_copy()

    def test_direct_publication_missing_review_rejected(self):
        self.direct_fixture(lambda m: m.update(reviewPath="demo/delivery/missing.md"))
        with self.assertRaises(PipelineError):
            self.run_copy()

    def test_direct_publication_wrong_parent_base_rejected(self):
        self.direct_fixture(lambda m: m.update(baseCommit=self.base))
        with self.assertRaises(PipelineError):
            self.run_copy()

    def test_project_cannot_overlap_vault_or_tools(self):
        for project in ("vault", "tools", "reminder-dot", "../demo"):
            with self.assertRaises(PipelineError):
                cloud.public_path(self.root, "vault/_templates/private.md", project)

    def test_local_acknowledgement_binds_actual_originals_and_network_failure_stays_pending(self):
        self.run_copy(); archived=self.restore()["archive"]
        seen=[]
        def post(list_id,name,args):
            seen.append(args)
            return {"acknowledged":True,"reportId":self.report["id"],"localBackup":{"commit":self.commit}}
        result=cloud.acknowledge_local_backups(self.root,self.bundle,self.owner,archived,post)
        self.assertEqual(result["acknowledged"],1)
        self.assertEqual(seen[0]["backupBundleSha256"],cloud.sha(Path(archived).read_bytes()))
        def failed(*args): raise PipelineError("Synthetic failure")
        result=cloud.acknowledge_local_backups(self.root,self.bundle,self.owner,archived,failed)
        self.assertEqual(result["pending"],1)
        self.assertEqual(self.handoff()["git"]["status"],"pushed")
        file=self.root/"完成/.pipeline/dot/account-1/list-1/reports/one/report-1-files/guide_pdf.pdf"
        file.write_bytes(b"Local tamper")
        with self.assertRaises(PipelineError): cloud.acknowledge_local_backups(self.root,self.bundle,self.owner,archived,post)

    def test_cloud_only_entry_never_calls_local_publisher(self):
        config=self.root/"完成/.pipeline/config.json"
        manual.save(config,{"accountId":"account-1","listId":"list-1"})
        # Caller has its own lease; release only our synthetic fixture lease.
        release(self.root,self.owner)
        with patch.object(manual,"download",return_value=(json.dumps(self.bundle).encode(),self.bundle)), \
             patch.object(cloud,"PublicMirror",return_value=self.mirror), \
             patch.object(manual,"apply_cloud_receipts",side_effect=lambda root,bundle,owner: cloud.apply_cloud_receipts(root,bundle,owner,lambda root:self.mirror)), \
             patch.object(manual,"acknowledge_local_backups",return_value={"acknowledged":0,"pending":1}), \
             patch.object(manual,"publication_repo",side_effect=AssertionError("No local publisher")):
            result=manual.sync(self.root,config)
        self.assertEqual(result["publishedBatches"],0)
        self.assertEqual(result["cloudPublished"],1)
        self.assertEqual(result["localKnowledgeSynced"],1)


if __name__=="__main__": unittest.main()
