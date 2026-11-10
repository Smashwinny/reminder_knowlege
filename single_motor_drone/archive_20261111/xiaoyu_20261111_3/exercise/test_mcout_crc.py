#!/usr/bin/env python3
"""Unit checks for the published MCOUT CRC and lag-pitch kinematics."""
import unittest

from ex_cyclic_hinge_sim import (
    crc16_xmodem,
    pack_mcout,
    parse_mcout,
    lag_to_pitch,
    MCOUT_FLAG_MOTORS_ARMED,
    MCOUT_FLAG_SOFT_ARMED,
    MCOUT_FLAG_INTERLOCK,
    MCOUT_FLAG_OUTPUT_ENABLED,
    MCOUT_FLAG_ESTOP,
)
import math


class TestCrcAndKinematics(unittest.TestCase):
    def test_xmodem_vector(self):
        self.assertEqual(crc16_xmodem(b"123456789"), 0x31C3)

    def test_pack_roundtrip_and_safety(self):
        flags = (
            MCOUT_FLAG_MOTORS_ARMED
            | MCOUT_FLAG_SOFT_ARMED
            | MCOUT_FLAG_INTERLOCK
            | MCOUT_FLAG_OUTPUT_ENABLED
        )
        pkt = pack_mcout(1, 0, flags, 3, 2, 0.1, -0.2, 0.3, 0.4)
        self.assertEqual(len(pkt), 84)
        d = parse_mcout(pkt)
        self.assertTrue(d["crc_ok"] and d["output_allowed"])
        self.assertAlmostEqual(d["pitch"], -0.2, places=5)

        bad = bytearray(pkt)
        bad[22] ^= 1
        self.assertFalse(parse_mcout(bytes(bad))["crc_ok"])

        estop = pack_mcout(2, 0, flags | MCOUT_FLAG_ESTOP, 3, 2, 0.1, -0.2, 0.3, 0.4)
        self.assertFalse(parse_mcout(estop)["output_allowed"])

    def test_forty_five_degree_is_one_to_one(self):
        z = math.radians(7.5)
        self.assertAlmostEqual(lag_to_pitch(z, 45.0), z, places=12)
        self.assertAlmostEqual(lag_to_pitch(z, 30.0), z * math.tan(math.radians(30)), places=12)


if __name__ == "__main__":
    unittest.main()
