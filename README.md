# terra

**One ledger, six moves: a complete environment system that keeps the map true to the territory — and the territory safe under the map.**

Terra is a working, installable implementation of **environment engineering** — the emerging discipline (harness engineering, agent environment engineering, AX) of designing everything around a fixed-capability model that determines how much of that capability you actually get.

Your prompt, plan, and config are a map. The codebase, APIs, real constraints, and your own taste are the territory. Every mismatch between them is a **gap**, and with strong models, output quality is bottlenecked by gaps, not capability: goal gaps (the request is wrong), harness gaps (nothing enforces what must hold), understanding gaps (shipped ≠ understood), environment gaps (the same failure keeps repeating). Terra tracks all four kinds in one ledger with one grammar, closes each with its cheapest resolver, and evolves the environment from its own traces.

## The primitive

One entry type — the gap, tagged and carrying its resolver. One file per task: `TERRA.md`. Cognitive gaps (`KU`/`UK`/`UU?`) and harness gaps (`[H]`) live in the same ledger because they are the same thing: a difference between the current state and the ready state.

## The skills

| Skill | Phase | One move |
|---|---|---|
| [`terra`](skills/terra/SKILL.md) | always | The spec: ledger format, gap types, strength hierarchy, lifecycle |
| [`terra-survey`](skills/terra-survey/SKILL.md) | open | Sweep harness and territory in one pass; wire what's mechanical; seed the ledger; rewrite the request |
| [`terra-resolve`](skills/terra-resolve/SKILL.md) | before | Facts by lookup, decisions by budgeted evidence-priced interview, taste by contrasting artifacts |
| [`terra-plan`](skills/terra-plan/SKILL.md) | gate | Volatility-ordered PLAN.md ending in a mechanically checkable stop condition |
| [`terra-build`](skills/terra-build/SKILL.md) | during | Every action conditioned on the launch packet; deviations logged, never improvised; guards before dangerous ground |
| [`terra-gate`](skills/terra-gate/SKILL.md) | close | Dual gate: machine green + understanding quiz reconciled against the diff; then the death rite |
| [`terra-evolve`](skills/terra-evolve/SKILL.md) | across tasks | Mine repeated failure mechanisms; promote one bounded, gated, revertible fix per run |

Lifecycle: `SURVEY → RESOLVE → PLAN → BUILD → GATE`, with `EVOLVE` across tasks.

## What terra deliberately does NOT build

Terra is the **process tier**. The physics tier — hooks, permissions, CI, sandboxes — already exists in your harness; terra-survey wires to it, never replaces it. On Claude Code that means `.claude/settings[.local].json`; the same ledger and lifecycle run unchanged on any harness that reads SKILL.md (pi included) — only the physics wiring is harness-specific. Loops (`/goal`, schedulers) are also native: terra-plan's stop condition is what you mount on them, and only after the chain has run clean by hand.

## Design rules

- **Musts are physics.** Anything that must happen lives in a hook or permission. A "must" in prose is a recorded `[H]` gap.
- **Verdicts are external.** Tests, environment feedback, or the user decide; self-assessment is a signal, never the gate.
- **Triggers bind to observable events only** — never to states the agent can't perceive.
- **Brownfield first.** A new project is a survey with empty findings; wire to what exists, report gaps instead of fabricating fixes.
- **Budgets over relentlessness.** Interviews are capped and priced; ceremony scales to the risk it guards.
- **Retention is the score.** A component that goes unused is a negative asset — delete it.

## Install

```bash
npx skills add leoncuhk/terra
```

Or copy any `skills/<name>` folder into `~/.claude/skills/` (Claude Code), or anywhere your agent reads the SKILL.md format. Then in any project, start any task — `terra-survey` opens it.

## Lineage

Terra is the unified successor to the author's [defog](https://github.com/leoncuhk/defog) (unknowns ledger, quadrants, budgeted asking, quiz gate — now archived) and rig (audit-first assembly, strength hierarchy, gated evolution). It also adapts, with gratitude: Matt Pocock's [skills](https://github.com/mattpocock/skills) (grilling discipline, skill-writing principles) and the documented failure modes of its wayfinder (#450, #484); Thariq Shihipar's map/territory frame; Neeeophytee's [finding-unknowns-skills](https://github.com/Neeeophytee/finding-unknowns-skills) (belief-labeled probes, criterion sentence, blast-radius ordering); Nico Bailon's [grill-for-unknowns](https://github.com/nicobailon/grill-for-unknowns) (ledger concept, question budget, fatigue valve, question gates); the verification-density principle (Jason Wei's Verifier's Law); plan-conditioned execution (StraTA, arXiv 2605.06642); and trace-driven, regression-gated environment evolution (Self-Harness, arXiv 2606.09498). See [NOTICE.md](NOTICE.md).

## License

MIT
