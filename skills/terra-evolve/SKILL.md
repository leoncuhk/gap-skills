---
name: terra-evolve
description: Mine deviation traces across tasks for repeated failure mechanisms and promote one bounded fix into the environment — hard patterns to hooks, soft patterns to CLAUDE.md.
disable-model-invocation: true
---

# Terra Evolve

The environment is not static config; it evolves from its own traces. Run periodically, or after a task that hurt.

## 1. Audit the last edit

Open `.terra/journal.md` and judge the previous entry first: did it help? No observable effect, or new friction → revert it and log the verdict. An edit that survives two runs is part of the environment.

## 2. Mine

Evidence: every `TERRA*.md` Deviations section, graduated ADRs, `.terra/journal.md`, git history since the last entry. Cluster failures by **mechanism, not by task** — "missing final artifact", "retried identical command", "touched running service unchecked".

## 3. Propose

Only patterns seen ≥2 times qualify. For the single highest-cost pattern, propose one bounded edit:

- deterministic check possible → a hook or permission rule (strongest — prefer this)
- genuine judgment call → one line in CLAUDE.md (weakest, and say so)

State what behavior it changes and what regression it risks. **One edit per run — never batch.**

## 4. Gate

The user approves; you never self-adopt. On approval, apply the edit and log it in `.terra/journal.md`: date, pattern, edit, expected effect.

Done when one edit is adopted-and-logged or explicitly rejected, and the previous edit has its verdict.
