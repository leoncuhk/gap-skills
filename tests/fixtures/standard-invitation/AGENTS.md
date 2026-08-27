# Sample project

- Verify with `python3 -m unittest discover -s tests -v`.
- Email identity comparisons are case-insensitive.
- Pending invitations expire after seven days. At the exact expiry time they are expired.
- Creating a duplicate pending invitation returns the original invitation without extending its expiry.
- An expired invitation may be replaced by a new invitation.
- Creating another invitation after acceptance raises a clear already-accepted domain error.
- Production releases use an external release service; local scripts only prepare artifacts.
