# gap-skills

[![validate](https://github.com/leoncuhk/gap-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/leoncuhk/gap-skills/actions/workflows/validate.yml)

**One skill, one adaptive path from intent to verified delivery.**

项目愿景：

> 人主要负责目的、价值取舍和必须由人承担的判断。AI应该承担查证、实施、测试、状态接续和收尾的大部分劳动，并把需要人介入的部分讲清楚。真正实现人机协作方式：让人与AI组成一个能把真实工作持续做得更好的协作系统，并把有效经验留下来，让下一次更好。

这是设计目标；持续改善真实工作及减少人力负担仍需实际任务证据验证。

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

## Capability boundaries

| Capability | What the single installed folder supplies | What still depends on the host or task |
|---|---|---|
| Workflow | One entry, nine focused references, seven optional templates | An agent that reads the skill and has authorized project tools; this is no autonomous runtime |
| Resumption and evidence | Four Python standard-library helpers; source-bound receipts, briefs and scoped experience use | Python 3.10+ for optional helpers; truthful external evidence and actual reviewer identity |
| HTML feedback | Offline checkpoint HTML, source disclosures, local JSON export and freshness-checked intake | Browser behavior and human comprehension need real testing; no HTTP receiver or automatic conversation return |
| Diagrams and other HTML | Guidance for choosing a source-backed form | Agent-authored SVG/Mermaid/HTML per task; no bundled generic diagram renderer, editor, hosting or visual QA |
| Prior methods | Selected Matt and Thariq mechanisms with [lineage](NOTICE.md) | No claim to include their full suites; no identified Karpathy source mapping in this package |

Isolated folder/manifest/helper checks establish package self-containment. They do not establish natural activation in Codex/Claude, and no global installation was performed. See the [final review and reference assessment](tests/results/2026-10-06-gap-final.md).

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

The verified 0.7.1 changes are local and unpublished. To use this exact version, copy the local `skills/gap` folder or ask the agent to read its `SKILL.md`. The remote installer below uses the published repository, which may differ.

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

Without installation, ask the agent to read this repository’s `skills/gap/SKILL.md` and complete the task using it. `$gap` and `/gap` require the corresponding installation; local package validation does not establish installation or automatic activation.

Ordinary natural-language requests can also activate the skill when the harness supports implicit discovery. You never call separate planning, debugging, implementation, or review skills; `gap` loads those internal references only when the task needs them.

To adopt it in an existing project:

```text
$gap inspect this repository and propose a minimal adoption plan; do not change configuration yet
```

The adoption pass is read-only until the user approves exact project changes.

See [EXAMPLES.md](EXAMPLES.md) for Quick, Standard, Governed, review, adoption, and retrospective examples, including executable Standard and review MVPs.

## Resume or close a multi-session task

```text
$gap continue this task from the actual artifacts and latest evidence. Preserve the original goal and data definitions; recheck only invalidated claims, then report what is ready and what still needs a decision.
```

Version 0.7.1 includes an optional Python 3.10+ checkpoint helper **inside** the installed skill folder. It binds actual receipts to the purpose, semantic contract and files, preserving revisions and distinguishing run termination from artifact readiness. See [delivery.md](skills/gap/references/delivery.md) for the short CLI procedure. It neither runs an agent nor certifies business truth, external actions or reviewer identity. Quick tasks still create no process files. No global installation is required to test the helper.

Use `view` for a concise text checkpoint or `view --format html --output <new-file>` for an offline evidence/feedback surface. Returned feedback is bound to current file identity and is never an approval. See [communication.md](skills/gap/references/communication.md). Text is the default; diagrams show relationships, HTML supports inspection, and video needs a real motion/procedure requirement.

For substantive handoff, optional `view --brief brief.json` puts original excerpts, actual differences, impacts and pending choices ahead of technical receipts. Use the same `--brief` on feedback intake. Default text is concise; add `--details` for full originals and deduplicated receipts. HTML exposes the same evidence through expandable source links.

Experience remains candidate or validated within a stated scope; later tasks record apply/trial/reject and observed results through `use-result`. Structured validated application requires source failures, at least two distinct validation tasks including a forward task, and current-task scope evidence. No automatic self-promotion. Comparative human-effort savings are not established by the synthetic tests.

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

The [0.7.1 final review](tests/results/2026-10-06-gap-final.md) adds one fresh scoped trial, repository cleanup, isolated installation checks and malformed-input handling.

[0.7 source-bound delivery and scoped experience](tests/results/2026-10-06-gap07.md): 57 local regressions and four independently replayed task outcomes. Baseline and enhanced both solve the tasks; enhanced binds original excerpts and stale feedback, while originally producing substantially more artifacts. A separately reviewed presentation reduction retains full on-demand evidence and reduces default text; it is not a new solver comparison. Human understanding and net effort savings remain unmeasured.

Earlier [0.6.1 Matt adoption and three-arm results](tests/results/2026-10-06-matt-adoption.md). All three repaired artifacts pass independent local controls; complete original execution traces and comparative benefit remain unverified. Earlier [0.6.0 feedback-loop results](tests/results/2026-10-06-batch2.md) and [archived synthetic MVP](examples/evidence-review/README.md) retain their browser-QA and human-effort limits.

See [tests/PROTOCOL.md](tests/PROTOCOL.md) for the evaluation contract, [tests/results/2026-08-27.md](tests/results/2026-08-27.md) for the historical baseline, and [NOTICE.md](NOTICE.md) for lineage.

## License

MIT
