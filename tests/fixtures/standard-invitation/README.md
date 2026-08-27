# Sample invitations

This fixture keeps team invitations separate from active memberships.

## Invitation lifecycle

Add an in-memory `InvitationStore` in `src/invitations.py`:

- `create(team_id, email, now)` returns an `Invitation` containing canonical email, creation time, and expiry time.
- `accept(team_id, email, now)` returns the canonical membership key for a pending invitation.
- Accepting a missing, expired, or already accepted invitation raises a clear domain exception.
- Preserve the existing `invitation_key` API and use only the Python standard library.
