# gap-skills

[![skills.sh](https://skills.sh/b/leoncuhk/gap-skills)](https://skills.sh/leoncuhk/gap-skills) [![validate](https://github.com/leoncuhk/gap-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/leoncuhk/gap-skills/actions/workflows/validate.yml)

**One ledger, six moves: a complete environment system that keeps the map true to the territory — and the territory safe under the map.**

Gap-skills is a working, installable implementation of **environment engineering** — the emerging discipline (harness engineering, agent environment engineering, AX) of designing everything around a fixed-capability model that determines how much of that capability you actually get.

Your prompt, plan, and config are a map. The codebase, APIs, real constraints, and your own taste are the territory. Every mismatch between them is a **gap**, and with strong models, output quality is bottlenecked by gaps, not capability: goal gaps (the request is wrong), harness gaps (nothing enforces what must hold), understanding gaps (shipped ≠ understood), environment gaps (the same failure keeps repeating). Gap-skills tracks all four kinds in one ledger with one grammar, closes each with its cheapest resolver, and evolves the environment from its own traces.

## The primitive

One entry type — the gap, tagged and carrying its cheapest resolver. The tags follow the classic knowns/unknowns quadrants, extended by one:

| Tag | Quadrant | What it is | Cheapest resolver |
|---|---|---|---|
| — | Known known | Already stated or proven | straight into the plan |
| `KU` | Known unknown — fact | The codebase or docs can answer it | `→ lookup`: never ask a human what the territory can answer |
| `KU` | Known unknown — decision | Only the user can choose | `→ ask`: budgeted, evidence-priced interview |
| `UK` | Unknown known | Taste the user recognizes on sight but can't verbalize | `→ show`: contrasting throwaway artifacts |
| `UU?` | Unknown unknown — suspected | A constraint nobody has checked yet | `→ survey`: blindspot sweep of the territory |
| `[H]` | Harness gap | The environment lacks a verification, guard, or convention | `→ wire`: hooks and permissions |
| `[A]` | Assumption | Low-risk residue | most reversible default, labeled, veto-able |

One file per task: `GAP.md`. Cognitive gaps (`KU`/`UK`/`UU?`) and harness gaps (`[H]`) live in the same ledger because they are the same thing: a difference between the current state and the ready state.

## The skills

| Skill | Phase | One move |
|---|---|---|
| [`gap`](skills/gap/SKILL.md) | always | The spec: ledger format, gap types, strength hierarchy, lifecycle |
| [`gap-survey`](skills/gap-survey/SKILL.md) | open | Sweep harness and territory in one pass; wire what's mechanical; seed the ledger; rewrite the request |
| [`gap-resolve`](skills/gap-resolve/SKILL.md) | before | Facts by lookup, decisions by budgeted evidence-priced interview, taste by contrasting artifacts |
| [`gap-plan`](skills/gap-plan/SKILL.md) | gate | Volatility-ordered PLAN.md ending in a mechanically checkable stop condition |
| [`gap-build`](skills/gap-build/SKILL.md) | during | Every action conditioned on the launch packet; deviations logged, never improvised; guards before dangerous ground |
| [`gap-gate`](skills/gap-gate/SKILL.md) | close | Dual gate: machine green + understanding quiz reconciled against the diff; then the death rite |
| [`gap-evolve`](skills/gap-evolve/SKILL.md) | across tasks | Mine repeated failure mechanisms; promote one bounded, gated, revertible fix per run |

Lifecycle: `SURVEY → RESOLVE → PLAN → BUILD → GATE`, with `EVOLVE` across tasks.

## What gap-skills deliberately does NOT build

Gap-skills is the **process tier**. The physics tier — hooks, permissions, CI, sandboxes — already exists in your harness; gap-survey wires to it, never replaces it. On Claude Code that means `.claude/settings[.local].json`; the same ledger and lifecycle run unchanged on any harness that reads SKILL.md (pi included) — only the physics wiring is harness-specific. Loops (`/goal`, schedulers) are also native: gap-plan's stop condition is what you mount on them, and only after the chain has run clean by hand.

## Design rules

- **Musts are physics.** Anything that must happen lives in a hook or permission. A "must" in prose is a recorded `[H]` gap.
- **Verdicts are external.** Tests, environment feedback, or the user decide; self-assessment is a signal, never the gate.
- **Triggers bind to observable events only** — never to states the agent can't perceive.
- **Brownfield first.** A new project is a survey with empty findings; wire to what exists, report gaps instead of fabricating fixes.
- **Budgets over relentlessness.** Interviews are capped and priced; ceremony scales to the risk it guards.
- **Retention is the score.** A component that goes unused is a negative asset — delete it.

## Install

```bash
npx skills add leoncuhk/gap-skills
```

Or copy any `skills/<name>` folder into `~/.claude/skills/` (Claude Code), or anywhere your agent reads the SKILL.md format.

## Use

You do three things; everything else fires on its own:

1. **State your task normally.** `gap-survey` opens it — audits the harness, scouts the territory, seeds `GAP.md`, and hands back your request rewritten by what it found. Trivial tasks: gap-skills stands down, no ceremony.
2. **`/gap-plan` when gaps are burned down** — a one-page plan, volatile decisions first, ending in a checkable stop condition. Answer the 2–4 yes/no items and let it build. Deviations get logged, not asked about.
3. **`/gap-gate` before merge** — tests must be green, the diff must reconcile against the ledger, and you pass a short quiz on what actually shipped. Then the ledger dies and its whys graduate to `docs/adr/`.

Every two weeks: `/gap-evolve` — it mines your deviation history and proposes one bounded improvement to your hooks or CLAUDE.md; nothing lands without your approval.

Fresh session mid-task? Say "continue — read GAP.md and PLAN.md". Nothing is lost.

A complete worked pass: [EXAMPLES.md](EXAMPLES.md). Validation methodology: [tests/PROTOCOL.md](tests/PROTOCOL.md). History: [CHANGELOG.md](CHANGELOG.md).

## Lineage

Gap-skills is the unified successor to the author's [defog](https://github.com/leoncuhk/defog) (unknowns ledger, quadrants, budgeted asking, quiz gate — now archived) and rig (audit-first assembly, strength hierarchy, gated evolution). It also adapts, with gratitude: Matt Pocock's [skills](https://github.com/mattpocock/skills) (grilling discipline, skill-writing principles) and the documented failure modes of its wayfinder (#450, #484); Thariq Shihipar's map/territory frame; Neeeophytee's [finding-unknowns-skills](https://github.com/Neeeophytee/finding-unknowns-skills) (belief-labeled probes, criterion sentence, blast-radius ordering); Nico Bailon's [grill-for-unknowns](https://github.com/nicobailon/grill-for-unknowns) (ledger concept, question budget, fatigue valve, question gates); the verification-density principle (Jason Wei's Verifier's Law); plan-conditioned execution (StraTA, arXiv 2605.06642); and trace-driven, regression-gated environment evolution (Self-Harness, arXiv 2606.09498). See [NOTICE.md](NOTICE.md).

## License

MIT
