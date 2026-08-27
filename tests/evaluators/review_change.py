#!/usr/bin/env python3
"""Outcome checks proving the review fixture contains real specification defects."""

from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path


if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
    CANDIDATE = Path(sys.argv.pop(1)).resolve()
else:
    CANDIDATE = Path.cwd()

sys.path.insert(0, str(CANDIDATE))

from src.pricing import final_total  # noqa: E402


class ReviewFixtureContractTests(unittest.TestCase):
    def test_public_signature_is_unchanged(self):
        self.assertEqual(list(inspect.signature(final_total).parameters), [
            "subtotal_cents",
            "is_member",
        ])

    def test_negative_subtotal_is_rejected(self):
        with self.assertRaises(ValueError):
            final_total(-1, False)

    def test_member_discount_uses_exact_integer_policy(self):
        self.assertEqual(final_total(101, True), 90)


if __name__ == "__main__":
    unittest.main()
