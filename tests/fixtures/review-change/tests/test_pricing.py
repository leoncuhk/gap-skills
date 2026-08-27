import unittest

from src.pricing import final_total


class PricingTests(unittest.TestCase):
    def test_non_member_total_is_unchanged(self):
        self.assertEqual(final_total(1_000, False), 1_000)


if __name__ == "__main__":
    unittest.main()
