#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""本地交接状态机：真实保存/重载 JSON 审计与本地快照。

这不是 Dots 的内部实现；2026-11-22 官方页面只描述 takeover/return control，
没有文档化快照创建、恢复或回滚。这里的快照仅是自写协议的一部分。
"""
import argparse
import copy
import json
from pathlib import Path


class TransitionError(RuntimeError):
    pass


class HandoffMachine:
    def __init__(self, output=None, state="DOT_WORKING", history=None, snapshot=None):
        self.state = state
        self.history = list(history or [])
        self.snapshot = copy.deepcopy(snapshot)
        self.output = Path(output) if output else None

    def save(self):
        if not self.output:
            return
        payload = {"state": self.state, "history": self.history, "snapshot": self.snapshot}
        temporary = self.output.with_suffix(self.output.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(self.output)

    @classmethod
    def load(cls, path):
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload["state"] not in {"DOT_WORKING", "TAKEOVER_REQUESTED", "HUMAN_CONTROL", "HANDBACK", "STOPPED"}:
            raise TransitionError("未知状态")
        return cls(output=path, state=payload["state"], history=payload["history"], snapshot=payload.get("snapshot"))

    def _go(self, new_state, reason):
        self.history.append(f"{self.state} → {new_state}（{reason}）")
        self.state = new_state
        self.save()

    def request_takeover(self, reason, redline=False):
        if redline:
            self.emergency_stop(reason)
            return
        if self.state != "DOT_WORKING":
            raise TransitionError(f"当前 {self.state} 不可接管")
        self.snapshot = {"from": self.state, "reason": reason, "kind": "本地自写快照，非Dots功能"}
        self._go("TAKEOVER_REQUESTED", f"人请求：{reason}")
        self._go("HUMAN_CONTROL", "保存本地快照后让出控制")

    def handback(self):
        if self.state != "HUMAN_CONTROL" or not self.snapshot:
            raise TransitionError("没有可交还的人工控制与本地快照")
        self._go("HANDBACK", "人交还控制并附交接说明")
        self._go("DOT_WORKING", "读取本地快照继续")

    def emergency_stop(self, reason):
        if self.state == "STOPPED":
            return
        self._go("STOPPED", f"红线：{reason}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("handoff-audit-v2.json"))
    args = parser.parse_args()
    machine = HandoffMachine(args.output)
    machine.request_takeover("我要自己改这一步")
    machine.handback()
    reloaded = HandoffMachine.load(args.output)
    assert reloaded.state == "DOT_WORKING" and reloaded.snapshot
    reloaded.emergency_stop("涉及付款页面")
    assert HandoffMachine.load(args.output).state == "STOPPED"
    print("\n".join(reloaded.history))
    print("PASS：JSON 已重载；快照存在；完整交接与红线停止均留痕")
    print("边界：快照与落盘是本地协议，不是 Dots 官方功能证明")


if __name__ == "__main__":
    main()
