#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OKX 文档预检规则的合成输入实验；不运行 CLI、不连接账户或交易。"""
import argparse
import json
from pathlib import Path

COMMIT = "0ea4378645dfc212e9d58df9fc4ca4446398c9e3"


def selected_site(config, auth):
    for profile in config.get("profiles", []):
        if profile.get("site"):
            return profile["site"]
    if auth.get("status") in {"logged_in", "pending"} and auth.get("site"):
        return auth["site"]
    return None


def detect_auth(config, auth):
    for profile in config.get("profiles", []):
        if profile.get("api_key"):
            return {"mode": "api_key", "profile": profile.get("name"), "action": "use_api_key_no_oauth"}
    status = auth.get("status")
    if status == "logged_in":
        return {"mode": "oauth", "action": "use_oauth"}
    if status == "pending":
        return {"mode": "oauth", "action": "wait_no_new_login"}
    return {"mode": "none", "action": "load_auth_skill"}


def oauth_trading_mode(demo=False):
    return "demo" if demo else "live"


def validate_order(order):
    required = ["instId", "side", "ordType", "sz"]
    missing = [key for key in required if not order.get(key)]
    if order.get("ccy") == "USDT" and order.get("order_mode") not in {"quote_ccy", "margin"}:
        missing.append("order_mode(quote_ccy/margin)")
    if missing:
        raise ValueError("缺少逐项确认：" + ", ".join(missing))
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("preflight-audit-v2.json"))
    args = parser.parse_args()
    placeholder = selected_site({}, {"status": "not_logged_in", "site": "global"})
    assert placeholder is None
    assert detect_auth({}, {"status": "not_logged_in"})["action"] == "load_auth_skill"
    assert detect_auth({"profiles": [{"name": "broken", "api_key": "synthetic"}]},
                       {"status": "logged_in"})["action"] == "use_api_key_no_oauth"
    assert oauth_trading_mode() == "live" and oauth_trading_mode(True) == "demo"
    result = {"commit": COMMIT, "placeholder_site": placeholder,
              "oauth_default": oauth_trading_mode(), "synthetic_only": True,
              "scope": "文档规则模型；未运行CLI、未连接账户、未证明底层硬门或链路原子性"}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PASS：未登录 global 占位符视为未选择；API key 优先；OAuth 默认 live；--demo 才 demo")
    print("输出：", args.output)


if __name__ == "__main__":
    main()
