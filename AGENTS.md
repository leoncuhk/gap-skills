# Project: gap-skills

## Purpose
One cross-harness `gap` skill that routes software work through the smallest trustworthy delivery path.

## Commands
- verify: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate.py && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`

## Structure
- `skills/gap/SKILL.md`: the only skill entry point and shared contract.
- `skills/gap/references/`: branch-specific procedures loaded on demand.
- `skills/gap/assets/`: optional output templates, never project policy.
- `tests/cases/`: activation and workflow contracts.
- `tests/fixtures/`: clean repositories given to agents.
- `tests/evaluators/`: hidden outcome checks kept outside agent fixtures.
- `tests/reference-solutions/`: known-green baselines proving evaluators are solvable.
- `tests/results/`: retained harness evidence and limits.

## Conventions
- Preserve one user-facing skill; add a reference, asset, or deterministic script only when a real branch needs it.
- Default project inspection is read-only. Mutating another project's harness requires explicit user scope or approval.
- Keep temporary working state separate from durable delivery evidence and environment backlog.
- Claude and Codex packaging must both validate; platform-specific controls stay separate.

## Verification
Run the verify command after every change. Structure checks do not prove behavioral value; update behavioral cases when routing or completion behavior changes.
