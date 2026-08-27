def normalize_email(email: str) -> str:
    """Return the canonical identity form used by memberships."""
    return email.strip().lower()


def invitation_key(team_id: str, email: str) -> tuple[str, str]:
    return team_id, normalize_email(email)
