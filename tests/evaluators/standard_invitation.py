#!/usr/bin/env python3
"""Hidden outcome checks for the Standard invitation MVP fixture."""

from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
    CANDIDATE = Path(sys.argv.pop(1)).resolve()
else:
    CANDIDATE = Path.cwd()

sys.path.insert(0, str(CANDIDATE))

from src.invitations import InvitationStore  # noqa: E402


class HiddenInvitationContractTests(unittest.TestCase):
    def setUp(self):
        self.store = InvitationStore()
        self.start = datetime(2026, 8, 1, tzinfo=timezone.utc)

    def test_duplicate_is_case_insensitive_and_does_not_extend_expiry(self):
        original = self.store.create("team-1", "Person@Example.com", self.start)
        duplicate = self.store.create(
            "team-1", " person@example.COM ", self.start + timedelta(days=2)
        )
        self.assertEqual(duplicate, original)
        self.assertEqual(original.expires_at, self.start + timedelta(days=7))

    def test_exact_expiry_is_rejected_and_then_replaceable(self):
        original = self.store.create("team-1", "person@example.com", self.start)
        with self.assertRaisesRegex(Exception, "expired"):
            self.store.accept("team-1", "person@example.com", original.expires_at)

        replacement = self.store.create(
            "team-1", "person@example.com", original.expires_at
        )
        self.assertNotEqual(replacement.created_at, original.created_at)

    def test_accept_returns_canonical_membership_key(self):
        self.store.create("team-1", " Person@Example.com ", self.start)
        self.assertEqual(
            self.store.accept(
                "team-1", "person@example.COM", self.start + timedelta(days=1)
            ),
            ("team-1", "person@example.com"),
        )

    def test_accepted_identity_cannot_be_invited_again(self):
        self.store.create("team-1", "person@example.com", self.start)
        self.store.accept("team-1", "person@example.com", self.start)
        with self.assertRaisesRegex(Exception, "already accepted"):
            self.store.create(
                "team-1", "PERSON@example.com", self.start + timedelta(days=1)
            )


if __name__ == "__main__":
    unittest.main()
