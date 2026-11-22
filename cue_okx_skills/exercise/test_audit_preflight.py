import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("audit_preflight.py")
SPEC = importlib.util.spec_from_file_location("audit_preflight", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PreflightTests(unittest.TestCase):
    def test_not_logged_in_global_is_placeholder(self):
        self.assertIsNone(MODULE.selected_site({}, {"status": "not_logged_in", "site": "global"}))

    def test_logged_in_site_is_selected(self):
        self.assertEqual(MODULE.selected_site({}, {"status": "logged_in", "site": "eea"}), "eea")

    def test_profile_site_is_selected(self):
        config = {"profiles": [{"name": "p", "site": "us"}]}
        self.assertEqual(MODULE.selected_site(config, {"status": "not_logged_in"}), "us")

    def test_api_key_precedes_oauth(self):
        config = {"profiles": [{"name": "synthetic", "api_key": "not-real"}]}
        result = MODULE.detect_auth(config, {"status": "logged_in"})
        self.assertEqual(result["action"], "use_api_key_no_oauth")

    def test_oauth_default_is_live(self):
        self.assertEqual(MODULE.oauth_trading_mode(), "live")
        self.assertEqual(MODULE.oauth_trading_mode(True), "demo")

    def test_pending_does_not_start_new_login(self):
        self.assertEqual(MODULE.detect_auth({}, {"status": "pending"})["action"], "wait_no_new_login")

    def test_no_auth_loads_auth_skill(self):
        self.assertEqual(MODULE.detect_auth({}, {"status": "not_logged_in"})["action"], "load_auth_skill")

    def test_order_requires_core_parameters(self):
        with self.assertRaises(ValueError):
            MODULE.validate_order({"instId": "BTC-USDT"})

    def test_usdt_order_requires_explicit_mode(self):
        order = {"instId": "BTC-USDT", "side": "buy", "ordType": "market", "sz": "10", "ccy": "USDT"}
        with self.assertRaises(ValueError):
            MODULE.validate_order(order)
        order["order_mode"] = "quote_ccy"
        self.assertTrue(MODULE.validate_order(order))


if __name__ == "__main__":
    unittest.main()
