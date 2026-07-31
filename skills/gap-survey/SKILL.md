---
name: gap-survey
description: Open a task by surveying both the harness (missing verification, hooks, conventions) and the territory (unknown unknowns, landmines, constraints). Use at task start, when entering unfamiliar ground, or when a ledger item is tagged → survey.
---

# Gap-skills Survey

Two sweeps, one report, one seeded ledger. A new project is a survey with empty findings — same procedure as a mature one.

## Sweep 1 — the harness

Detect, don't assume: git state; real verify commands (read package.json / pyproject.toml / Makefile / CI config — don't guess); `.claude/settings[.local].json` permissions and hooks; CLAUDE.md (length? "musts" hiding in prose?); `docs/adr/` or the project's own convention. Each finding: **present / missing / misplaced**.

Close the mechanical `[H]` gaps immediately:

- Wire PostToolUse verification to the project's **own** commands (start from `templates/settings-template.json`). Never invent a test framework for an existing project — no verify command means the top `[H]` gap is recorded, not fabricated.
- Deny-list irreversible commands.
- Shared or public repo → install to `.claude/settings.local.json` (a committed rig imposes hooks on every clone); solo project → `settings.json`.
- CLAUDE.md: missing → ≤30 lines from `templates/CLAUDE-template.md`; present → edit surgically: add missing sections, move misplaced "musts" down into hooks, change nothing else.
- Confirm a home for durable decisions (`docs/adr/` or the project's own convention); create it if absent.
- New project (empty sweep): `git init`, a minimal test setup, a first verify command — physics needs something to wire to.

## Sweep 2 — the territory

Read-only — record, never repair. Ranked by how much each would change the plan:

- **Landmines** — mistakes a newcomer here typically makes.
- **Hidden constraints** — decisions already made that bound the work; invariants that must hold.
- **What good looks like** — 2–3 concrete examples to calibrate against.
- **Questions an expert would ask** — with your best-guess answer for each.

## Output

Write findings to the ledger (`gap` skill): territory facts → `Resolved` with why; defaults → `Assumed`; open questions → `Gaps` with resolvers; remaining harness gaps → `[H]`. Confirmed-safe areas are dropped unless a later step would act differently knowing them.

End with the survey manifest: what was wired, what was skipped and why, the top remaining `[H]` gap — then rewrite the task request as the territory shows it should read; it becomes the ledger's `# GAP:` title. Announce burn-down. Done when every "must" found lives in a hook or permission (or stands as a recorded `[H]` gap) and the manifest is announced. "No significant gaps here" is a valid, valuable report.
