import unittest

from src.invitations import invitation_key


class InvitationTests(unittest.TestCase):
    def test_identity_is_case_insensitive(self):
        self.assertEqual(
            invitation_key("team-1", " Person@Example.com "),
            ("team-1", "person@example.com"),
        )


if __name__ == "__main__":
    unittest.main()
