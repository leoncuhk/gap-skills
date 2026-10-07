# gap-skills

[![validate](https://github.com/leoncuhk/gap-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/leoncuhk/gap-skills/actions/workflows/validate.yml)

**One skill, one adaptive path from intent to verified delivery.**

`gap` helps a coding agent carry work from a requested outcome to a checked result. You own the purpose, value tradeoffs and decisions that require human responsibility. The agent investigates the repository, implements, tests, resumes from actual state and closes the task with evidence. When your judgment is needed, it explains the options and their consequences.

The aim is less correction, repeated checking and handoff work for you. Useful experience should inform later tasks only when its scope and results support it. These are design goals: installing a skill does not prove saved time or enable automatic self-improvement.

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

Normal skill use needs a compatible agent and its project tools. Python 3.10+ is needed only for optional helpers. A browser is needed to use generated HTML; JavaScript enables local feedback export. Node is not a gap runtime dependency. Diagrams need the chosen viewer or host rendering support; no additional skill is required.

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

## Start on another machine

Clone once into a directory you choose. These are POSIX shell commands (macOS/Linux, or a compatible shell):

```sh
git clone https://github.com/leoncuhk/gap-skills.git
cd gap-skills
gap_source="$(pwd)/skills/gap"
printf '%s\n' "$gap_source/SKILL.md"
```

Choose one of these routes. The whole `skills/gap` folder is self-contained; copying only `SKILL.md` loses its references and helpers.

**Install for a project.** From the same shell, set your project's absolute path and choose its host:

```sh
project_dir="/absolute/path/to/your/project"
skill_parent="$project_dir/.agents/skills"   # Codex
# For Claude Code instead: skill_parent="$project_dir/.claude/skills"
if [ -d "$project_dir" ] && [ ! -e "$skill_parent/gap" ] && [ ! -L "$skill_parent/gap" ]; then
  mkdir -p "$skill_parent" && cp -R "$gap_source" "$skill_parent/gap"
else
  printf '%s\n' 'Check the project path and existing gap installation before copying.'
fi
```

Start the agent in that project and invoke `$gap` in Codex or `/gap` in Claude Code. If it is not listed, check the location and your host's skill settings; restart the session if needed. Implicit activation is host/model-dependent. See the official [Codex skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) and [Claude Code skill locations](https://code.claude.com/docs/en/skills#where-skills-live).

**Use without installing.** Copy the absolute path printed above into a normal message in your project's agent session:

```text
Read and follow <absolute-path-to-gap-skills>/skills/gap/SKILL.md.
Goal: <the task and observable success conditions>.
Preserve: <existing behavior, data definitions and scope boundaries>.
Investigate, implement, test, resume from actual state and finish the work.
Bring me the purpose, value tradeoffs and judgments I must own, with options
and consequences. Report the result, actual checks and any remaining boundary.
```

The agent must be able to read that checkout and the relevant project files in its execution environment. A path on your laptop is not automatically accessible to a remote agent. This route does not register `$gap` or `/gap` and does not require them.

To update a clean clone, run `git pull --ff-only` inside it. Direct-path use then reads the updated source; a copied installation stays at its old version until you deliberately replace it after checking for local changes. Use `git rev-parse HEAD` to record or match a version across machines. Existing compatible installers may also use `npx skills add leoncuhk/gap-skills`; that optional route needs Node/npm and was not exercised by our isolated folder checks.

The repository includes both plugin manifests. A Claude plugin installation uses the namespaced command `/gap-skills:gap`; the plain `/gap` examples here assume a skill-folder installation. Host-specific controls remain host-specific.

## Use for real development

State the work and success conditions; you do not need to select internal references or operate the helper yourself. After installation, use the prompts below (`/gap` for a Claude skill-folder install). Without installation, prepend the direct-path instruction above and omit `$gap`.

| Situation | Short request | What to expect |
|---|---|---|
| New feature | `$gap Add team invitations following README.md; preserve existing identity rules and verify the lifecycle.` | Inspect the existing contract, ask only unresolved material choices, implement and test the requested behavior. |
| Fix an existing project | `$gap Fix this reproducible bug: <steps and expected result>. Preserve unrelated behavior and show the failing and passing check.` | Investigate the cause, make a focused repair, verify through the real entry point. |
| Resume another session | `$gap Continue <task> from its existing records and outputs. Preserve the goal; recheck stale claims and avoid repeating completed actions.` | Inspect actual state before continuing; report evidence gaps instead of blindly restarting. |
| Review and hand off | `$gap Review this change against <requirements>. Report actual checks, deviations and decisions still needed. Do not publish.` | Separate correctness from intent fit, identify review independence, and distinguish ready output from pending judgment or external action. |

For a clear, local, reversible fix, Quick means inspect → edit → run the relevant checks → report; no plan, ledger or checkpoint files. Simple edits also need no explicit skill invocation. A checkpoint becomes useful when work spans sessions or a changed input could make a prior passing result misleading. Use the project's existing records first; add a brief only when sources, differences or a real choice need explanation.

On completion, expect usable output and evidence tied to the requested outcome, not just a finished process. The agent should name a real blocker, decision or authorization boundary when one remains, and retain only scoped experience supported by observed results. Check actual correction and review effort over subsequent work before concluding that gap helps more than your existing agent setup.

See [EXAMPLES.md](EXAMPLES.md) for executable feature/review fixtures and the [evidence review example](examples/evidence-review/README.md) for a source-backed handoff. Adopting gap does not require rewriting project configuration; ask for a read-only adoption proposal first if configuration changes are wanted.

## Resume or close a multi-session task

```text
$gap continue this task from the actual artifacts and latest evidence. Preserve the original goal and data definitions; recheck only invalidated claims, then report what is ready and what still needs a decision.
```

Version 0.7.2 includes an optional Python 3.10+ checkpoint helper **inside** the installed skill folder. It binds actual receipts to the purpose, semantic contract and files, preserving revisions and distinguishing run termination from artifact readiness. See [delivery.md](skills/gap/references/delivery.md) for the short CLI procedure. It neither runs an agent nor certifies business truth, external actions or reviewer identity. Quick tasks still create no process files. No global installation is required to test the helper.

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

The [0.7.2 portability check](tests/results/2026-10-07-portable-use.md) covers English guidance, isolated folder installs and actual local usage checks. Historical task inputs, quotations and reports retain their original language and identities.

Repository validation checks packaging, documentation links, references, manifests, invocation metadata, templates, and workflow invariants. Behavioral evaluation includes positive and negative activation cases, executable Quick, Standard-delivery, and standalone-review fixtures, plus declared Governed/adoption/retrospective scenarios. These checks show that the implementation is coherent and that planted review defects are detectable; the Governed scenario and comparative effectiveness still require retained harness and real-work results.

The [0.7.1 final review](tests/results/2026-10-06-gap-final.md) adds one fresh scoped trial, repository cleanup, isolated installation checks and malformed-input handling.

[0.7 source-bound delivery and scoped experience](tests/results/2026-10-06-gap07.md): 57 local regressions and four independently replayed task outcomes. Baseline and enhanced both solve the tasks; enhanced binds original excerpts and stale feedback, while originally producing substantially more artifacts. A separately reviewed presentation reduction retains full on-demand evidence and reduces default text; it is not a new solver comparison. Human understanding and net effort savings remain unmeasured.

Earlier [0.6.1 Matt adoption and three-arm results](tests/results/2026-10-06-matt-adoption.md). All three repaired artifacts pass independent local controls; complete original execution traces and comparative benefit remain unverified. Earlier [0.6.0 feedback-loop results](tests/results/2026-10-06-batch2.md) and [archived synthetic MVP](examples/evidence-review/README.md) retain their browser-QA and human-effort limits.

See [tests/PROTOCOL.md](tests/PROTOCOL.md) for the evaluation contract, [tests/results/2026-08-27.md](tests/results/2026-08-27.md) for the historical baseline, and [NOTICE.md](NOTICE.md) for lineage.

## License

MIT
