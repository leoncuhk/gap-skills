# gap-skills

[![validate](https://github.com/leoncuhk/gap-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/leoncuhk/gap-skills/actions/workflows/validate.yml)

**One skill, one adaptive path from intent to verified delivery.**

`gap` combines the useful mechanisms behind unknown discovery, structured interviewing, specification, work slicing, plan-conditioned implementation, evidence-backed review, human approval gates, incident feedback, and agent-environment retrospectives. Developers install and invoke one skill; the skill loads only the branch the current task needs.

It does not force every task through a full lifecycle. It routes work by ambiguity, scale, and risk:

| Path | Typical work | Process cost |
|---|---|---|
| **Quick** | Clear, local, reversible edit | Inspect → implement → verify. No process files. |
| **Standard** | Ambiguous, multi-part, multi-session, or standalone change review | Clarify as needed → plan/build as requested → verify → two-axis review. |
| **Governed** | Production, migration, sensitive, regulated, or externally consequential work | Durable intent → spec → plan → evidence → independent review → named approval → release/incident loop. |

## What the single skill covers

- **Discover intent:** facts from the repository, decisions from the user, contrasting prototypes for tacit taste, blind-spot inspection, references read as behavioral specifications.
- **Plan at the right depth:** no artifact for trivial work, a concise plan for ordinary changes, durable intent/spec/plan and tracer-bullet tickets for large or governed changes.
- **Deliver against the plan:** verifiable slices, bounded evidence-driven repair loops, explicit deviations, and special scrutiny when tests or evaluators change.
- **Solve hard engineering problems:** red-first debugging loops, evidence-based issue triage, deep-module architecture, domain-language repair, safe context handoffs, and intent-aware merge resolution.
- **Review on two independent axes:** whether the fixed diff solves the requested problem and whether it is sound engineering; review-only requests stay read-only.
- **Communicate complex work:** concise Markdown by default, with self-contained HTML only when comparison, spatial layout, diagrams, or interaction materially improve understanding.
- **Govern consequential actions:** one source of truth, rule-to-enforcement mapping, named approvals, protected production boundaries, and incident-to-intent feedback.
- **Improve the environment:** turn repeated observed failures into one tested, reversible change to guidance, checks, tools, or protected controls.

## Why one skill

The user should not memorize or coordinate a collection of overlapping process skills. `gap` is the only entry point. Its `SKILL.md` holds routing and shared invariants; focused references are loaded only when their branch applies. This keeps the installed skill list small without forcing every task to carry the entire workflow in context.

## Repository map

| Path | Responsibility |
|---|---|
| [`skills/gap/SKILL.md`](skills/gap/SKILL.md) | The only user-facing skill and route selector. |
| `skills/gap/references/` | Guidance loaded only for the selected discovery, planning, delivery, review, problem-solving, communication, governance, retrospective, or adoption branch. |
| `skills/gap/assets/` | Optional templates copied into projects when durable artifacts are justified. |
| [`tests/PROTOCOL.md`](tests/PROTOCOL.md) | Evaluation levels, pass criteria, independence rules, and known limits. |
| `tests/cases/` | Versioned activation and workflow task definitions. |
| `tests/fixtures/` | Clean disposable repositories visible to an agent under test. |
| `tests/patches/` | Candidate changes applied after fixture initialization so review baselines stay reproducible. |
| `tests/evaluators/` | Outcome checks withheld from implementation sessions. |
| `tests/reference-solutions/` | Known-green implementations proving evaluators are solvable. |
| `tests/results/` | Retained harness runs, measurements, and limitations. |
| [`scripts/validate.py`](scripts/validate.py) | Deterministic package, documentation, and evaluation-contract validation. |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json), [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | Platform-specific manifests for the same `gap` skill. |

## Install

Install from the repository with a compatible skill installer:

```bash
npx skills add leoncuhk/gap-skills
```

Or install the single folder directly:

- Claude Code: place `skills/gap` in the supported project or user skill location.
- Codex repository scope: copy or symlink `skills/gap` to `.agents/skills/gap`.
- Codex user scope: copy or symlink `skills/gap` to `$HOME/.agents/skills/gap`.

The repository also includes Claude and Codex plugin manifests. Platform-specific settings and enforcement remain platform-specific; the shared workflow does not pretend one harness's hooks control another.

## Use

State the development task normally. `gap` may activate for ambiguous, multi-step, risky, governed, review, incident, or environment-improvement work. It deliberately skips simple well-scoped edits and one-lookup questions.

Invoke it explicitly when desired. Codex uses `$gap`; Claude Code uses `/gap`:

```text
Codex:       $gap assess and deliver this change using the smallest trustworthy path
Claude Code: /gap assess and deliver this change using the smallest trustworthy path
```

Ordinary natural-language requests can also activate the skill when the harness supports implicit discovery. You never call separate planning, debugging, implementation, or review skills; `gap` loads those internal references only when the task needs them.

To adopt it in an existing project:

```text
$gap inspect this repository and propose a minimal adoption plan; do not change configuration yet
```

The adoption pass is read-only until the user approves exact project changes.

See [EXAMPLES.md](EXAMPLES.md) for Quick, Standard, Governed, review, adoption, and retrospective examples, including executable Standard and review MVPs.

## Execution budgets

A budget is a stop condition for a costly or uncertain repair loop, not a quota for ordinary development and not permission to stop before success. Set one only when retries are long-running, flaky, externally rate-limited, or expensive, for example `max repair iterations: 5` or `max elapsed time: 30 minutes`. A repair iteration starts after verification fails; use `total attempts` when the initial implementation must count. Passing ends the loop early. Exhaustion produces a blocked report with attempts, evidence, and required input; it never counts as completion.

## Artifacts

Existing trackers and documentation conventions win. Defaults are provided only when a project has none:

- disposable working state: `.gap/work/<change-id>/state.md`;
- durable governed records: `docs/changes/<change-id>/`;
- durable environment work: `docs/agent/harness-backlog.md` and `docs/agent/evolution-log.md`.

Temporary state is removed only after unresolved environment problems, meaningful deviations, and durable decisions have been promoted. Accepted plans and approvals needed for review or audit are retained.

## Evidence and limits

Repository validation checks packaging, documentation links, references, manifests, invocation metadata, templates, and workflow invariants. Behavioral evaluation includes positive and negative activation cases, executable Quick, Standard-delivery, and standalone-review fixtures, plus declared Governed/adoption/retrospective scenarios. These checks show that the implementation is coherent and that planted review defects are detectable; the Governed scenario and comparative effectiveness still require retained harness and real-work results.

See [tests/PROTOCOL.md](tests/PROTOCOL.md) for the evaluation contract, [tests/results/2026-08-27.md](tests/results/2026-08-27.md) for current evidence, and [NOTICE.md](NOTICE.md) for lineage.

## License

MIT
