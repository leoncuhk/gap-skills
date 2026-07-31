# Project: terra

## Stack
Markdown agent skills (SKILL.md format) + a Python validator. No build step.

## Commands
- verify: `python3 scripts/validate.py` — also wired as a PostToolUse hook; the hook is authoritative

## Conventions
- Skill prose follows writing-great-skills: pruned, leading words, checkable completion criteria.
- Any rule that MUST hold goes into `scripts/validate.py` or a hook, never prose.
- Every mechanism adapted from elsewhere gets a NOTICE.md line — the attribution chain never breaks.

## Boundaries
- Surgical changes: every changed line traces to the request.
- Domain is cognition + environment assembly only. Engineering discipline (TDD, code review, debugging) stays out — reference it, never absorb it.
- Ceremony must never exceed the fog it manages — when in doubt, cut.

## State
- Task working memory: TERRA.md ledgers, deleted after merge.
- Durable decisions: CHANGELOG.md (what changed) + NOTICE.md (where ideas came from).
