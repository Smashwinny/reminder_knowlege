import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("handoff_state_machine.py")
SPEC = importlib.util.spec_from_file_location("handoff_state_machine", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
HandoffMachine = MODULE.HandoffMachine
TransitionError = MODULE.TransitionError


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.audit = Path(self.temporary.name) / "audit.json"

    def tearDown(self):
        self.temporary.cleanup()

    def test_complete_handoff_has_four_transitions(self):
        machine = HandoffMachine(self.audit)
        machine.request_takeover("修改合成草稿")
        machine.handback()
        self.assertEqual(machine.state, "DOT_WORKING")
        self.assertEqual(len(machine.history), 4)

    def test_snapshot_is_real_data(self):
        machine = HandoffMachine(self.audit)
        machine.request_takeover("保存合成状态")
        self.assertEqual(machine.snapshot["from"], "DOT_WORKING")
        self.assertIn("非Dots功能", machine.snapshot["kind"])

    def test_json_audit_can_be_reloaded(self):
        machine = HandoffMachine(self.audit)
        machine.request_takeover("修改合成草稿")
        machine.handback()
        loaded = HandoffMachine.load(self.audit)
        self.assertEqual(loaded.history, machine.history)
        self.assertEqual(loaded.snapshot, machine.snapshot)

    def test_redline_from_human_control_is_persistent(self):
        machine = HandoffMachine(self.audit)
        machine.request_takeover("修改合成草稿")
        machine.emergency_stop("付款")
        self.assertEqual(HandoffMachine.load(self.audit).state, "STOPPED")

    def test_redline_takeover_never_enters_human_control(self):
        machine = HandoffMachine(self.audit)
        machine.request_takeover("删除文件", redline=True)
        self.assertEqual(machine.state, "STOPPED")
        self.assertNotIn("HUMAN_CONTROL", "\n".join(machine.history))

    def test_invalid_takeover_fails_closed(self):
        machine = HandoffMachine(self.audit)
        machine.request_takeover("修改合成草稿")
        with self.assertRaises(TransitionError):
            machine.request_takeover("重复接管")

    def test_handback_without_snapshot_fails_closed(self):
        machine = HandoffMachine(self.audit, state="HUMAN_CONTROL")
        with self.assertRaises(TransitionError):
            machine.handback()

    def test_unknown_saved_state_rejected(self):
        self.audit.write_text(json.dumps({"state": "RESUMED_MAGIC", "history": []}), encoding="utf-8")
        with self.assertRaises(TransitionError):
            HandoffMachine.load(self.audit)


if __name__ == "__main__":
    unittest.main()
