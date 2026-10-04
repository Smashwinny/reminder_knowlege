import base64
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock
import zipfile

from reminder_dot_agent import owned, attach_reviewed_artifacts
from reminder_pipeline import Pipeline, PipelineError

TEST_ROOT = Path(__file__).resolve().parents[1] / '完成/.pipeline/dot-test-tmp'
TEST_ROOT.mkdir(parents=True, exist_ok=True)


class LocalAgentTests(unittest.TestCase):
    def test_current_policy_blocks_legacy_publish_before_any_site_write(self):
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as tmp:
            root = Path(tmp)
            (root / 'tools').mkdir()
            (root / 'tools/reminder_workflow_policy.json').write_text('{"automatic_full_learning":true,"task_completion":"user_only"}')
            pipeline = Pipeline(root=root)
            with self.assertRaisesRegex(PipelineError, '本人点击'): pipeline.publish('one', 'worker')
            self.assertFalse(pipeline.status()['learning_requires_manual_start'])
            self.assertTrue(pipeline.status()['task_completion_requires_user_click'])

    def test_other_owner_or_unresolved_publication_cannot_cross_local_queue(self):
        pipeline = MagicMock()
        for record in [{'owner': 'other', 'unresolved_publication': False}, {'owner': 'mine', 'unresolved_publication': True}]:
            pipeline.status.return_value = record
            with self.assertRaises(PipelineError): owned(pipeline, 'one', 'mine')

    def test_no_review_or_changed_artifacts_cannot_be_packaged_as_complete(self):
        pipeline = MagicMock()
        record = {'task_id': 'one', 'owner': 'worker', 'learning_started': True, 'manifest': {'project_dir':'project'}, 'quality_review': None, 'artifact_fingerprint': 'original'}
        with self.assertRaises(PipelineError): attach_reviewed_artifacts(pipeline, record, {})
        record['quality_review'] = {'approved': True, 'reviewer': 'reviewer', 'artifact_fingerprint': 'original'}
        pipeline._connection.return_value.execute.return_value.fetchone.return_value = {'task_id':'one'}
        pipeline._validate_manifest.return_value = ({}, 'changed')
        with self.assertRaises(PipelineError): attach_reviewed_artifacts(pipeline, record, {})

    def test_actual_reviewed_files_replace_any_caller_supplied_artifact_payload(self):
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as tmp:
            root = Path(tmp)
            contents = {'project/guide.pdf': b'%PDF-1.4\n% Fixture only\n%%EOF', 'project/guide.html': b'<!doctype html><html><body>Fixture</body></html>', 'project/exercise/log.txt': b'Fixture command and real file contents for packaging test.', 'project/exercise/main.py': b'print("fixture")\n', 'vault/project.md': b'Fixture reviewed knowledge note'}
            for name, data in contents.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            manifest = {'project_dir':'project', 'pdf':'project/guide.pdf', 'html':'project/guide.html', 'experiment_log':'project/exercise/log.txt', 'exercise_dir':'project/exercise', 'experiment_files':['project/exercise/main.py'], 'vault_note':'vault/project.md'}
            record = {'task_id':'one', 'owner':'worker', 'learning_started':True, 'manifest':manifest, 'quality_review':{'approved':True, 'reviewer':'reviewer', 'notes':'Fixture-only independent review', 'artifact_fingerprint':'checked'}, 'artifact_fingerprint':'checked'}
            pipeline = MagicMock()
            pipeline.root = root
            pipeline._connection.return_value.execute.return_value.fetchone.return_value = {'task_id':'one'}
            pipeline._validate_manifest.return_value = (manifest, 'checked')
            pipeline._path.side_effect = lambda name, **kwargs: root / name
            result = attach_reviewed_artifacts(pipeline, record, {'completion':{'artifacts':[{'role':'guide_pdf','base64':'injected'}]}})
            files = {a['role']:base64.b64decode(a['base64']) for a in result['completion']['artifacts']}
            self.assertEqual(files['guide_pdf'], contents['project/guide.pdf'])
            self.assertEqual(result['completion']['reviewer'], 'reviewer')
            with zipfile.ZipFile(io.BytesIO(files['exercise_archive'])) as archive:
                self.assertEqual(archive.namelist(), ['main.py'])
                self.assertEqual(archive.read('main.py'), contents['project/exercise/main.py'])


if __name__ == '__main__': unittest.main()
