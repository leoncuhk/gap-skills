---
name: gap
description: Guide ambiguous, multi-step, risky, or governed software changes from intent through planning, implementation, verification, review, release, and retrospective. Use for requirements discovery, prototypes, specs, plans, multi-session delivery, evidence-backed review, production gates, incidents, or agent-environment improvement. Skip simple well-scoped edits and questions answerable with one lookup.
---

# Gap

Run one adaptive software-delivery workflow. Use the smallest path that makes the change trustworthy; do not make the user choose among separate process skills.

## Operating contract

- Inspect the repository and available evidence before asking questions. Facts come from the environment; decisions come from the user.
- Start read-only. Changing project instructions, hooks, permissions, CI, dependencies, or repository structure requires the user's request or explicit approval of a concrete proposal.
- Treat fluent claims as unverified until supported by a file, command, observation, source, or clearly labeled judgment.
- Put a rule at the weakest layer that safely controls its failure: guidance for judgment, automated checks for repeatable facts, protected external gates for actions that must not be bypassed.
- Keep working state separate from durable evidence. Temporary notes may die; accepted intent, specifications, plans, approvals, incidents, and lasting environment gaps remain in the project's chosen source of truth.
- Preserve the project's existing tracker, documentation layout, commands, and delivery system. Add a parallel system only when the user explicitly wants migration.

## Route the task

Inspect the request and repository, then assess three dimensions:

1. **Ambiguity**: Are outcome, behavior, constraints, and important choices settled?
2. **Scale**: Is the work local and single-session, or cross-cutting, multi-session, or parallel?
3. **Risk**: Could it affect production, security, privacy, money, data, compatibility, compliance, or an irreversible external action?

Choose the highest path required by any dimension:

| Path | Use when | Required shape |
|---|---|---|
| **Quick** | Clear, local, reversible, low-risk | Inspect, implement, run the project's checks, report evidence. Create no process files. |
| **Standard** | Material ambiguity, several interacting changes, a material standalone review, or a handoff/multi-session build | Clarify intent as needed, record a concise plan for implementation work, complete only the requested stages, run relevant checks, review. |
| **Governed** | Production, migration, sensitive data, external side effects, regulated work, or required organizational approval | Durable intent → spec → plan → implementation evidence → independent review → named approval → release/incident loop. |

For Standard or Governed work, state the selected path and the reason in one sentence. If the task changes shape, reroute upward; moving downward requires evidence that the original risk is gone.

The path controls rigor, not scope. A request to plan, diagnose, review, adopt, or run a retrospective stops after that requested outcome; it does not silently continue into implementation, release, or environment changes.

## Load only the branch you need

- Unclear intent, unfamiliar territory, hidden constraints, user taste, or “like this” references: read [references/discovery.md](references/discovery.md).
- A written plan, specification, task graph, handoff, or multi-session build: read [references/planning.md](references/planning.md).
- A hard bug, flaky failure, incoming issue backlog, architecture improvement, domain-language problem, merge conflict, or long investigation: read [references/problem-solving.md](references/problem-solving.md).
- Any code or configuration change on Standard or Governed paths: read [references/delivery.md](references/delivery.md).
- A standalone PR/diff review, or the closing review for Standard or Governed delivery: read [references/reviewing-changes.md](references/reviewing-changes.md).
- A plan, comparison, architecture explanation, review, demo, or status report whose relationships are hard to scan in prose: read [references/communication.md](references/communication.md).
- Production, approvals, policy enforcement, deployment, monitoring, or incidents: read [references/governance.md](references/governance.md).
- A retrospective, repeated failure, or proposed change to agent instructions/tools: read [references/retrospective.md](references/retrospective.md).
- Installing or adapting this workflow to a project: read [references/adoption.md](references/adoption.md) first and alone; load another reference only if the inspected project presents that branch's concrete risk.

Quick work needs no reference unless one of these branches actually applies.

## Artifact policy

Use the project's existing issue tracker or documentation convention as the source of truth. When none exists:

- Temporary Standard/Governed working state when a real handoff needs it: `.gap/work/<change-id>/state.md` from [assets/state.md](assets/state.md).
- Durable governed change records: `docs/changes/<change-id>/` using [intent.md](assets/intent.md), [spec.md](assets/spec.md), [plan.md](assets/plan.md), and [review.md](assets/review.md).
- Durable environment work: `docs/agent/harness-backlog.md` and `docs/agent/evolution-log.md` using the supplied assets.

Standard work may keep intent and plan in the issue/PR instead of adding files. Governed work names one durable source of truth and records approvals there. Never maintain two authoritative copies.

Before deleting temporary state, promote every unresolved environment problem, important deviation, and hard-to-reverse decision to its durable home. A plan required for review or audit remains durable.

## Completion

Completion means the selected path's promises are satisfied:

- **Quick**: requested behavior exists and relevant project checks were run.
- **Standard**: intent, plan, implementation, and verification agree; material deviations are explained; review finds no unresolved blocking issue.
- **Governed**: durable artifacts and evidence agree, required independent reviews passed, and every requested authorized action was executed and verified. Awaiting authorization is not completion; report it as the remaining boundary.

For a partial workflow, completion means its requested artifact or decision is evidence-backed, its limits are explicit, and no unrequested downstream action was taken.

Report what was verified, what was not verified, and any remaining risk. Never call the workflow effective or optimal from self-assessment alone; that conclusion comes from retained task results and comparison over time.
