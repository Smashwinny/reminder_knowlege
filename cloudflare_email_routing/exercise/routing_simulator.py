# -*- coding: utf-8 -*-
"""Cloudflare Email Routing 路由规则模拟器 —— 学习实验。

按 Cloudflare 官方文档（email-service/configuration/email-routing-addresses 等）
真实建模入站邮件的匹配逻辑：
  1. 完整 local part 精确匹配优先（含 +tag 字面规则）
  2. RFC 5233 subaddressing：user+tag@ 回退匹配 user@ 规则，+tag 保留供 Worker 检查
  3. catch-all（local='*'）兜底，处理拼错的 local part
  4. 相同 pattern 的多条规则：仅列表第一条生效（dashboard 列表序）
  5. destination address 未验证 → 使用该地址的规则保持禁用（跳过）
  6. action 三种：forward(verified destination) / worker / drop（删除不路由）
  7. 入站消息大小上限 25 MiB，超限拒收

只依赖标准库。用法：
    python routing_simulator.py        # 运行内置测试 + 演示场景
"""
import sys

MiB = 1024 * 1024
INBOUND_LIMIT = 25 * MiB  # 官方：inbound (Routing) message size 25 MiB


class Rule:
    _seq = 0

    def __init__(self, local, domain, action, destination=None, verified=True):
        self.local = local          # local part；'*' 表示 catch-all
        self.domain = domain.lower()
        self.action = action        # 'forward' | 'worker' | 'drop'
        self.destination = destination
        self.verified = verified    # destination 是否已验证
        self.seq = Rule._seq        # dashboard 列表顺序（创建先后）
        Rule._seq += 1

    def __repr__(self):
        d = f" -> {self.destination}{'' if self.verified else '(未验证)'}"
        return f"<Rule {self.local}@{self.domain} {self.action}{d if self.action=='forward' else ''}>"


class Router:
    def __init__(self, domain, rules):
        self.domain = domain.lower()
        self.rules = sorted(rules, key=lambda r: r.seq)

    def route(self, rcpt, size_bytes=0):
        """返回 (判决, 详情)。判决 ∈ {'deliver','worker','drop','reject'}。"""
        local, _, domain = rcpt.partition("@")
        domain = domain.lower()
        if domain != self.domain:
            return ("reject", f"非本域名 {domain}")
        if size_bytes > INBOUND_LIMIT:
            return ("reject", f"超过入站 25MiB 上限（{size_bytes/MiB:.1f} MiB）")

        base, plus, tag = local.partition("+")
        candidates = []
        for r in self.rules:
            if r.domain != domain:
                continue
            if r.local == local:                 # 1. 完整精确匹配（含 +tag 字面量）
                candidates.append((0, r))
            elif plus and r.local == base:       # 2. RFC 5233 回退匹配
                candidates.append((1, r))
            elif r.local == "*":                 # 3. catch-all 兜底
                candidates.append((2, r))
        if not candidates:
            return ("reject", "无匹配规则且未开 catch-all")

        candidates.sort(key=lambda t: (t[0], t[1].seq))
        rank, rule = candidates[0]
        note = f"规则[{rule.local}@{rule.domain}]"
        if rank == 1:
            note += f"（subaddressing 回退，+{tag} 保留）"
        if rule.action == "forward":
            if not rule.verified:
                # 5. 未验证 destination：规则禁用，继续看次优候选
                rest = [c for c in candidates if c[1] is not rule]
                if rest:
                    _, r2 = sorted(rest, key=lambda t: (t[0], t[1].seq))[0]
                    sub = Router(self.domain, [r for r in self.rules if r is not rule])
                    verdict, detail = sub.route(rcpt, size_bytes)
                    return (verdict, f"{note} 因目标未验证被禁用；" + detail)
                return ("reject", f"{note} 目标地址未验证，规则禁用且无兜底")
            return ("deliver", f"{note} 转发到 {rule.destination}")
        if rule.action == "worker":
            return ("worker", f"{note} 交给 Worker 处理（message.to 含完整 rcpt）")
        return ("drop", f"{note} drop：删除不路由")


# ---------------- 内置测试：逐条对应官方文档行为 ----------------
def test():
    D = "example.com"
    cases = []

    def check(name, got, want_verdict, needle=""):
        ok = got[0] == want_verdict and (not needle or needle in got[1])
        cases.append((name, ok, got))
        return ok

    # T1 精确匹配优先于 catch-all
    r = Router(D, [Rule("*", D, "forward", "backup@gmail.com"),
                   Rule("support", D, "forward", "me@gmail.com")])
    check("T1 精确规则优先于 catch-all", r.route("support@example.com"), "deliver", "me@gmail.com")

    # T2 无匹配且无 catch-all → 拒收
    r = Router(D, [Rule("support", D, "forward", "me@gmail.com")])
    check("T2 无匹配拒收", r.route("nobody@example.com"), "reject", "无匹配")

    # T3 catch-all 接住拼错的 local part
    r = Router(D, [Rule("*", D, "forward", "backup@gmail.com")])
    check("T3 catch-all 接拼错地址", r.route("ifno@example.com"), "deliver", "backup@gmail.com")

    # T4 RFC 5233：user+tag 回退匹配 user 规则
    r = Router(D, [Rule("me", D, "forward", "me@gmail.com")])
    check("T4 subaddressing 回退", r.route("me+shopping@example.com"), "deliver", "回退")

    # T5 user+tag 有字面规则时，字面规则优先于回退
    r = Router(D, [Rule("me", D, "forward", "me@gmail.com"),
                   Rule("me+shopping", D, "drop")])
    check("T5 +tag 字面规则优先", r.route("me+shopping@example.com"), "drop")

    # T6 相同 pattern 重复规则：仅列表第一条生效
    r = Router(D, [Rule("a", D, "forward", "first@gmail.com"),
                   Rule("a", D, "forward", "second@gmail.com")])
    check("T6 同 pattern 首条生效", r.route("a@example.com"), "deliver", "first@gmail.com")

    # T7 未验证 destination → 规则禁用
    r = Router(D, [Rule("support", D, "forward", "pending@gmail.com", verified=False)])
    check("T7 未验证目标规则禁用", r.route("support@example.com"), "reject", "未验证")

    # T8 未验证规则禁用后 catch-all 兜底
    r = Router(D, [Rule("support", D, "forward", "pending@gmail.com", verified=False),
                   Rule("*", D, "forward", "backup@gmail.com")])
    check("T8 禁用后 catch-all 兜底", r.route("support@example.com"), "deliver", "backup@gmail.com")

    # T9 drop 动作：删除不路由
    r = Router(D, [Rule("spam", D, "drop"), Rule("*", D, "forward", "backup@gmail.com")])
    check("T9 drop 优先于 catch-all", r.route("spam@example.com"), "drop")

    # T10 入站 25MiB 上限
    r = Router(D, [Rule("*", D, "forward", "backup@gmail.com")])
    check("T10 26MiB 拒收", r.route("x@example.com", 26 * MiB), "reject", "25MiB")
    check("T11 25MiB 边界放行", r.route("x@example.com", 25 * MiB), "deliver")

    # T12 worker 动作
    r = Router(D, [Rule("hook", D, "worker")])
    check("T12 worker 接管", r.route("hook@example.com"), "worker")

    # T13 其他域名拒收
    check("T13 非本域名拒收", r.route("hook@other.com"), "reject", "非本域名")

    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, got in cases:
        print(f"  {'✅' if ok else '❌'} {name}: [{got[0]}] {got[1]}")
    print(f"\n测试结果：{passed}/{len(cases)} 通过")
    return passed == len(cases)


def demo():
    """演示场景：复刻原帖用法 —— .com 域名 + catch-all + 少量自定义别名。"""
    D = "mydomain.com"
    rules = [
        Rule("hi", D, "drop"),                            # 常见扫描地址直接丢
        Rule("support", D, "forward", "me@outlook.com"),  # 客服邮件转主邮箱
        Rule("register", D, "forward", "me@outlook.com"),
        Rule("billing", D, "forward", "me@outlook.com"),
        Rule("*", D, "forward", "archive@outlook.com"),   # catch-all：一切漏网邮件归档
    ]
    router = Router(D, rules)
    print("演示场景：mydomain.com 5 条规则（2 显式 + catch-all + drop）")
    for rcpt in ["support@mydomain.com", "register@mydomain.com",
                 "anything+tag123@mydomain.com", "ifno@mydomain.com",
                 "hi@mydomain.com"]:
        v, d = router.route(rcpt)
        print(f"  {rcpt:<34} -> [{v}] {d}")


if __name__ == "__main__":
    ok = test()
    print()
    demo()
    sys.exit(0 if ok else 1)
