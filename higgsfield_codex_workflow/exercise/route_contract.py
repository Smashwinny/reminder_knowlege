#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""本地通路/预算/通用异步契约实验，不连接 Higgsfield。

通用五态借自已学 PixStag，不表示 Higgsfield 使用这些状态值。
"""
import copy

ROUTES = {
    "CLI": {"actor": "coding agent", "evidence": "命令与任务回执"},
    "MCP": {"actor": "chat agent", "evidence": "工具调用与生成回执"},
    "GUI": {"actor": "computer use", "evidence": "逐步界面截图"},
}
TERMINAL = {"succeeded", "failed", "cancelled"}
TRANSITIONS = {"queued": {"running", "failed", "cancelled"}, "running": TERMINAL}


def validate_route(name, unlimited=False):
    if name not in ROUTES:
        raise ValueError("未知通路")
    if unlimited:
        raise ValueError("CLI/MCP 不得按 Unlimited 或免费生成估算")
    return copy.deepcopy(ROUTES[name])


class BudgetGuard:
    def __init__(self, balance):
        if balance < 0:
            raise ValueError("余额不能为负")
        self.balance = balance

    def reserve(self, estimate):
        if estimate <= 0:
            raise ValueError("估算成本必须大于零")
        if estimate > self.balance:
            return False
        self.balance -= estimate
        return True


class GenericTask:
    def __init__(self):
        self.state = "queued"
        self.assets_reviewed = False

    def advance(self, new_state):
        if new_state not in TRANSITIONS.get(self.state, set()):
            raise ValueError(f"非法状态迁移 {self.state}→{new_state}")
        self.state = new_state

    def review_assets(self):
        if self.state != "succeeded":
            raise ValueError("只有 succeeded 才能验收 Assets")
        self.assets_reviewed = True


def main():
    for route in ROUTES:
        print(route, validate_route(route))
    guard = BudgetGuard(500)
    assert guard.reserve(120) and guard.reserve(120)
    assert not guard.reserve(300) and guard.balance == 260
    task = GenericTask()
    task.advance("running")
    task.advance("succeeded")
    task.review_assets()
    assert task.assets_reviewed
    print("PASS：三通路校验；预算500→260后拒绝300；通用终态才验收Assets")
    print("边界：五态是本地通用模型，Higgsfield具体状态值未文档化")


if __name__ == "__main__":
    main()
