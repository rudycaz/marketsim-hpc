import unittest

from marketsim import SUPPORTED_RANGES, normalize_range, run_simulation


class MarketSimTests(unittest.TestCase):
    def test_supported_ranges_are_normalized(self):
        self.assertEqual(normalize_range("week"), "week")
        self.assertEqual(normalize_range("month"), "month")
        self.assertEqual(normalize_range("year"), "year")
        self.assertEqual(normalize_range("5+ years"), "5+ years")
        self.assertEqual(normalize_range("5y"), "5+ years")

    def test_invalid_range_raises_value_error(self):
        with self.assertRaises(ValueError):
            normalize_range("day")

    def test_run_simulation_returns_expected_shape(self):
        result = run_simulation("aapl", "month")
        self.assertEqual(result["ticker"], "AAPL")
        self.assertEqual(result["range"], "month")
        self.assertEqual(result["trading_days"], SUPPORTED_RANGES["month"])
        self.assertIn(result["predicted_trend"], {"upward", "downward", "sideways"})
        self.assertGreaterEqual(result["confidence"], 0.5)
        self.assertLessEqual(result["confidence"], 0.95)


if __name__ == "__main__":
    unittest.main()
