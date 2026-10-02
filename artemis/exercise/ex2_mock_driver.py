# -*- coding: utf-8 -*-
"""ex2: 无真机亲手驱动 ARTEMIS 的 MockDeviceDriver。

ARTEMIS 把"设备"抽象成 BaseDeviceDriver（20 个 async 方法），
MockDeviceDriver 是它的内存假实现——不用插手机也能验证
"Agent 下发的每个动作都会被设备层如实记录"。

运行（在 repo 目录下）：
    uv run python ../exercise/ex2_mock_driver.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "repo"))

from artemis.drivers.mock.mock_driver import MockDeviceDriver  # noqa: E402


async def main() -> None:
    # 1. 造一台 1080x2400 的"假手机"，开机即停在 Settings
    phone = MockDeviceDriver(device_id="ex2-mock-phone", width=1080, height=2400)
    await phone.connect()
    print(f"[1] 连接设备: id={phone.device_id}  屏幕={phone.screen_size}")

    # 2. 看一眼屏幕（截图+UI树）
    screen = await phone.get_screen_data()
    print(f"[2] 截图 {len(screen.screenshot_bytes)} 字节(PNG)  "
          f"UI树含元素: {[e['text'] for e in screen.ui_elements]}")
    assert screen.width == 1080 and screen.height == 2400

    # 3. 模拟 Agent 的一串动作：点击 → 输入 → 滑动 → 按键 → 启动 App
    ok_tap = await phone.tap(540, 1200)
    ok_input = await phone.input_text("hello artemis", clear_existing=True)
    ok_swipe = await phone.swipe(540, 1800, 540, 600, duration_ms=300)
    ok_key = await phone.press_key("BACK")
    ok_app = await phone.launch_app("com.android.settings")
    print(f"[3] 动作回执 tap={ok_tap} input={ok_input} swipe={ok_swipe} "
          f"key={ok_key} launch={ok_app}")

    # 4. 验证：驱动把每个动作都记进了流水账 action_history
    print("[4] 动作流水账（Agent 的'手'留下的每一步）:")
    for i, act in enumerate(phone.action_history, 1):
        print(f"    #{i} {act['action']:<12} {dict((k, v) for k, v in act.items() if k != 'action')}")

    # 5. 断言流水账内容与下发动作一一对应
    kinds = [a["action"] for a in phone.action_history]
    assert kinds[:5] == ["tap", "input_text", "swipe", "press_key", "launch_app"], kinds
    current_pkg = await phone.get_current_package()
    assert current_pkg == "com.android.settings", current_pkg
    await phone.disconnect()
    print("[5] ✅ 全部断言通过：假手机如实记录了 Agent 的每一步动作")


if __name__ == "__main__":
    asyncio.run(main())
