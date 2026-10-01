import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from services.password_analyzer import PasswordAnalyzer

class TestPasswordAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PasswordAnalyzer()

    def test_empty_password(self):
        res = self.analyzer.analyze("")
        self.assertEqual(res["score"], 0)
        self.assertEqual(res["classification"], "VERY WEAK")

    def test_common_password(self):
        res = self.analyzer.analyze("password")
        self.assertIn("Password matches a known common or leaked password pattern.", res["findings"])

    def test_sequence_detection(self):
        res = self.analyzer.analyze("Test1234!")
        any_seq = any("sequential pattern" in f for f in res["findings"])
        self.assertTrue(any_seq)

    def test_keyboard_pattern(self):
        res = self.analyzer.analyze("qwerty99!")
        any_kb = any("keyboard walk" in f for f in res["findings"])
        self.assertTrue(any_kb)

    def test_strong_password(self):
        res = self.analyzer.analyze("X#9mP$2vK!qL8w$z7RtA")
        self.assertGreaterEqual(res["score"], 80)
        self.assertEqual(res["classification"], "VERY STRONG")

if __name__ == "__main__":
    unittest.main()
