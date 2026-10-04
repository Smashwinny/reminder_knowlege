import concurrent.futures
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import reminder_coordinator as guard

TEST_ROOT = Path(__file__).resolve().parents[1] / "完成/.pipeline"
TEST_ROOT.mkdir(parents=True, exist_ok=True)


def temporary_workspace():
    return tempfile.TemporaryDirectory(dir=TEST_ROOT)


class CoordinatorSafetyTests(unittest.TestCase):
    def test_two_processes_cannot_acquire_same_coordinator(self):
        with temporary_workspace() as folder:
            command = str(Path(guard.__file__).resolve())
            def run(owner):
                return subprocess.run([sys.executable, command, "--root", folder,
                                       "acquire", "--owner", owner], capture_output=True)
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(run, ["codex", "claude"]))
            self.assertEqual(sorted(result.returncode for result in results), [0, 2],
                             [result.stderr.decode("utf-8", errors="replace") for result in results])

    def test_expired_coordinator_not_reclaimed_automatically(self):
        with temporary_workspace() as folder:
            guard.acquire(folder, "codex")
            with guard.transaction(folder) as db:
                db.execute("UPDATE coordinator SET lease_until=0")
            with self.assertRaises(RuntimeError):
                guard.require_owner(folder, "codex")
            with self.assertRaises(RuntimeError):
                guard.acquire(folder, "claude")
            guard.renew(folder, "codex")
            guard.require_owner(folder, "codex")

    def test_other_worker_cannot_renew_release_or_write(self):
        with temporary_workspace() as folder:
            guard.acquire(folder, "codex")
            for action in (guard.require_owner, guard.renew, guard.release):
                with self.assertRaises(RuntimeError):
                    action(folder, "claude")
            self.assertEqual(guard.status(folder)["owner"], "codex")
            guard.release(folder, "codex")
            guard.acquire(folder, "claude")
            guard.require_owner(folder, "claude")


if __name__ == "__main__":
    unittest.main()
