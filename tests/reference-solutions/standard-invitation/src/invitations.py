from dataclasses import dataclass
from datetime import datetime, timedelta


INVITATION_LIFETIME = timedelta(days=7)


def normalize_email(email: str) -> str:
    """Return the canonical identity form used by memberships."""
    return email.strip().lower()


def invitation_key(team_id: str, email: str) -> tuple[str, str]:
    return team_id, normalize_email(email)


@dataclass(frozen=True)
class Invitation:
    team_id: str
    email: str
    created_at: datetime
    expires_at: datetime


class InvitationError(Exception):
    """Base class for invitation lifecycle failures."""


class InvitationNotFoundError(InvitationError):
    """Raised when an invitation does not exist."""


class InvitationExpiredError(InvitationError):
    """Raised when a pending invitation has expired."""


class InvitationAlreadyAcceptedError(InvitationError):
    """Raised when an invitation has already been accepted."""


class InvitationStore:
    """Keep team invitations and their acceptance state in memory."""

    def __init__(self) -> None:
        self._invitations: dict[tuple[str, str], Invitation] = {}
        self._accepted: set[tuple[str, str]] = set()

    def create(self, team_id: str, email: str, now: datetime) -> Invitation:
        key = invitation_key(team_id, email)
        existing = self._invitations.get(key)

        if existing is not None:
            if key in self._accepted:
                raise InvitationAlreadyAcceptedError(
                    f"invitation already accepted for team {team_id!r} "
                    f"and email {key[1]!r}"
                )
            if now < existing.expires_at:
                return existing

        invitation = Invitation(
            team_id=team_id,
            email=key[1],
            created_at=now,
            expires_at=now + INVITATION_LIFETIME,
        )
        self._invitations[key] = invitation
        return invitation

    def accept(
        self, team_id: str, email: str, now: datetime
    ) -> tuple[str, str]:
        key = invitation_key(team_id, email)
        invitation = self._invitations.get(key)

        if invitation is None:
            raise InvitationNotFoundError(
                f"invitation not found for team {team_id!r} and email {key[1]!r}"
            )
        if key in self._accepted:
            raise InvitationAlreadyAcceptedError(
                f"invitation already accepted for team {team_id!r} and email {key[1]!r}"
            )
        if now >= invitation.expires_at:
            raise InvitationExpiredError(
                f"invitation expired for team {team_id!r} and email {key[1]!r}"
            )

        self._accepted.add(key)
        return key
