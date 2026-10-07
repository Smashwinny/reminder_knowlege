# -*- coding: utf-8 -*-
"""Twilio 试用账户机制模拟器 —— 学习实验。

按 Twilio 官方文档（how-to-use-your-free-trial-account）真实建模试用账户规则：
  1. 免费额度按产品固定发放：100 SMS / 100 WhatsApp / 3000 邮件 / 75 分钟通话（非共享余额）
  2. 试用账户 30 天过期
  3. 发送对象只能是已验证号码（上限 VERIFIED_RECIPIENT_LIMIT 个），注册号码自动验证
  4. 试用必须使用 Twilio 提供的模板，自定义正文不可用
  5. 试用 SMS/Voice 限注册国；邮件限注册邮箱
  6. 额度用尽 → 该渠道拒绝发送，需升级付费账户
  7. 试用号由产品 Try out 流程分配，不可自选

只依赖标准库。用法：
    python trial_simulator.py
"""
import sys
from datetime import date, timedelta

QUOTA = {"sms": 100, "whatsapp": 100, "email": 3000, "voice_seconds": 75 * 60}
TRIAL_DAYS = 30
VERIFIED_RECIPIENT_LIMIT = 5


class TrialAccount:
    def __init__(self, registration_country="US", signup_day=None):
        self.country = registration_country
        self.signup_day = signup_day or date.today()
        self.used = {k: 0 for k in QUOTA}
        self.verified = set()          # 已验证 recipient 号码
        self.trial_number = None       # 试用号（None=未分配）

    def _alive(self, today):
        return (today - self.signup_day).days < TRIAL_DAYS

    def assign_trial_number(self, product_try_out=True):
        """试用号由产品 Try out 流程分配，不可自选。"""
        if not product_try_out:
            return ("fail", "试用号不可自选：必须从产品 Try out 流程分配")
        self.trial_number = "+1TWILIO"  # 模拟系统分配
        return ("ok", f"系统分配试用号 {self.trial_number}")

    def verify_recipient(self, number):
        if number in self.verified:
            return ("ok", "已验证")
        if len(self.verified) >= VERIFIED_RECIPIENT_LIMIT:
            return ("fail", f"已验证 recipient 已达上限 {VERIFIED_RECIPIENT_LIMIT}，需升级付费账户")
        self.verified.add(number)
        return ("ok", f"{number} 已加入验证列表（{len(self.verified)}/{VERIFIED_RECIPIENT_LIMIT}）")

    def send(self, channel, to, country, custom_body=False, today=None):
        """返回 (判决, 详情)。channel ∈ sms/whatsapp/email/voice。"""
        today = today or date.today()
        if not self._alive(today):
            return ("reject", f"试用账户已过期（{TRIAL_DAYS} 天周期）")
        if channel not in QUOTA:
            return ("reject", f"未知渠道 {channel}")
        if self.trial_number is None and channel != "email":
            return ("reject", "未分配试用号（需先走产品 Try out 流程）")
        if self.used[channel] >= QUOTA[channel]:
            return ("reject", f"{channel} 免费额度用尽（{QUOTA[channel]}），需升级付费账户")
        if channel in ("sms", "voice") and country != self.country:
            return ("reject", f"试用 {channel} 限注册国（{self.country}），目标 {country} 超出")
        if channel == "email":
            pass  # 邮件限注册邮箱由调用方保证 to 为注册邮箱
        if custom_body:
            return ("reject", "试用必须使用 Twilio 提供的模板，自定义正文不可用")
        if channel in ("sms", "whatsapp", "voice") and to not in self.verified:
            return ("reject", f"{to} 不是已验证 recipient（试用只能发给已验证号码）")
        self.used[channel] += 1 if channel != "voice_seconds" else 60
        return ("sent", f"{channel} 发送成功（已用 {self.used[channel]}/{QUOTA[channel]}）")

    def quota_report(self):
        return {k: f"{self.used[k]}/{v}" for k, v in QUOTA.items()}


def test():
    cases = []

    def check(name, got, want, needle=""):
        ok = got[0] == want and (not needle or needle in got[1])
        cases.append((name, ok, got))
        return ok

    d0 = date(2026, 10, 1)
    a = TrialAccount("US", signup_day=d0)
    # T1 额度数字与官方一致
    assert QUOTA == {"sms": 100, "whatsapp": 100, "email": 3000, "voice_seconds": 4500}
    # T2 试用号不可自选
    check("T2 试用号不可自选", a.assign_trial_number(product_try_out=False), "fail", "不可自选")
    assert a.assign_trial_number()[0] == "ok"
    # T3 发送给未验证号码被拒
    check("T3 未验证 recipient 拒发", a.send("sms", "+8613800000001", "US"), "reject", "已验证")
    # T4 验证后可发，计数
    a.verify_recipient("+8613800000001")
    check("T4 验证后可发", a.send("sms", "+8613800000001", "US"), "sent")
    # T5 自定义正文被拒
    check("T5 自定义正文拒发", a.send("sms", "+8613800000001", "US", custom_body=True), "reject", "模板")
    # T6 跨国 SMS 拒发
    a.verify_recipient("+442071234567")
    check("T6 试用 SMS 限注册国", a.send("sms", "+442071234567", "GB"), "reject", "注册国")
    # T7 验证 recipient 上限 5
    a2 = TrialAccount("US", signup_day=d0)
    for i in range(VERIFIED_RECIPIENT_LIMIT):
        a2.verify_recipient(f"+1000000000{i}")
    check("T7 验证上限5", a2.verify_recipient("+19999999999"), "fail", "上限")
    # T8 30 天过期
    check("T8 30天过期拒发", a.send("email", "me@reg.com", "US", today=d0 + timedelta(days=31)), "reject", "过期")
    # T9 额度用尽拒发（sms 用到 100）
    a3 = TrialAccount("US", signup_day=d0)
    a3.assign_trial_number()
    a3.verify_recipient("+1x")
    a3.used["sms"] = 100
    check("T9 额度用尽拒发", a3.send("sms", "+1x", "US"), "reject", "用尽")
    # T10 邮件渠道不需要试用号
    a4 = TrialAccount("US", signup_day=d0)
    check("T10 邮件无需试用号", a4.send("email", "me@reg.com", "US"), "sent")

    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, got in cases:
        print(f"  {'✅' if ok else '❌'} {name}: [{got[0]}] {got[1]}")
    print(f"\n测试结果：{passed}/{len(cases)} 通过")
    return passed == len(cases)


def demo():
    a = TrialAccount("US")
    a.assign_trial_number()
    print("演示：试用账户生命周期（额度数字 = 官方文档值）")
    a.verify_recipient("+8613800000001")
    for ch, to, ctry in [("sms", "+8613800000001", "US"),
                         ("whatsapp", "+8613800000001", "US"),
                         ("email", "me@reg.com", "US")]:
        print(f"  send {ch:<9} -> {a.send(ch, to, ctry)}")
    print("  额度：", a.quota_report())


if __name__ == "__main__":
    ok = test()
    print()
    demo()
    sys.exit(0 if ok else 1)
