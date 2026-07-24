---
name: terra
description: Core spec for the terra environment system — the gap ledger, strength hierarchy, and task lifecycle. Use when a task has unresolved gaps or unverified constraints, when the user mentions the terra ledger, or when another terra-* skill needs the shared rules.
---

# Terra

The map (prompt, plan, config) never matches the territory (codebase, APIs, real constraints, taste) at the start. Every mismatch is a **gap**. Terra makes gaps explicit in one ledger, closes each with its cheapest resolver, enforces every "must" as physics, and evolves the environment from its own traces.

## The ledger

One per task: `TERRA.md`, next to the work. Second task in a directory: rename the existing ledger to `TERRA-<task-slug>.md` first, also slugged.

```markdown
# TERRA: <task, corrected as surveyed>

## Gaps
- [KU] <fact to verify> → lookup
- [KU] <decision the user must make> → ask
- [UK] <taste recognized only on sight> → show
- [UU?] <suspected constraint nobody checked> → survey
- [H] <harness gap: missing verification, guard, or convention> → wire

## Assumed
- [A] <default taken> — cost to revisit: <cost>

## Resolved
- [x] <decision or finding> (<who: user | territory>, <date>) — <why>

## Deviations            <!-- add on first deviation; never keep empty -->
- <plan said / did instead / why / cost to revisit>
```

`territory` covers anything verified against the real system, including your own experiments.

## Gap types and resolvers

| Tag | Gap | Resolver |
|---|---|---|
| — | Known known | Not a gap. Straight into the plan. |
| `KU` fact | The territory can answer it | `→ lookup` — never ask what code or docs can answer |
| `KU` decision | The user must choose | `→ ask` (`terra-resolve`) |
| `UK` | Taste, recognized on sight | `→ show` (`terra-resolve`) |
| `UU?` | Suspected unknown unknown | `→ survey` (`terra-survey`) |
| `H` | Environment lacks a verification, guard, or convention | `→ wire` (`terra-survey`), or accept as `[A]` |
| `A` | Low-risk residue | Most reversible default, labeled, veto-able |

## Strength hierarchy

A rule lives at the level its **failure cost** demands, not the level its topic suggests:

1. **Physics** — hooks, permissions, CI. What MUST happen. The agent cannot bypass it.
2. **Structure** — terra skills: budgets, gates, checkable completion criteria.
3. **Prose** — CLAUDE.md, ≤30 lines, judgment calls only. A "must" found in prose is a misplaced `[H]` gap.

## Rules

- **Every open gap carries its resolver.** The ledger is a work queue, not a diary.
- **Burn-down is visible.** Announce `<n> open, <m> assumed` after every ledger write.
- **Triggers bind only to observable events** — a gate passing, the user declaring done. Never to states the agent can't perceive (session end, a merge happening elsewhere).
- **Verdicts are external.** Environment feedback, tests, or the user decide; self-assessment is a signal, never the gate.
- **Resolved keeps its why** — a finding shaped the plan only if a later step would act differently knowing it; the rest is dropped.
- **Terra stands down for trivial work.** A task that is mechanical, has unambiguous acceptance criteria, or whose open questions one tool call can answer needs no ledger — ceremony must never exceed the fog it manages.

## Lifecycle

`SURVEY → RESOLVE → PLAN → BUILD → GATE`, with `EVOLVE` running across tasks.

- **Birth:** any terra-* skill that would write to a missing ledger (or section) creates it first.
- **Handoff:** `TERRA.md` + `PLAN.md` are the launch packet — any fresh session resumes from them at zero loss. Sessions are cattle, not pets.
- **Death:** when `terra-gate` passes or the user declares the task done — graduate the whys that are hard to reverse or surprising without context into `docs/adr/` or the commit message, then delete the ledger. Working memory, not documentation.
