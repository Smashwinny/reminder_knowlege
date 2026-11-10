import unittest
from src.calc import add


class TestCalc(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative(self):
        self.assertEqual(add(-2, 3), 1)

    def test_zero(self):
        self.assertEqual(add(0, 0), 0)
