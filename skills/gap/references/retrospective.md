# Retrospective

Improve the agent environment from observed failures, not from speculative completeness.

## Evidence

Read the actual session/task record, review findings, incidents, reverted changes, CI failures, user corrections, and the previous evolution entry. Judge the last environment change before proposing another: keep it only if the expected behavior appeared without disproportionate friction.

Look for repeated mechanisms across tasks:

- navigation or missing context pointers;
- absent automated checks;
- review standards that missed a real issue;
- bloated or ineffective AGENTS.md/CLAUDE.md instructions;
- expensive or unreliable tools;
- unavailable information or observability;
- workflow steps repeatedly bypassed because their cost exceeds their value.

## Promotion rule

A pattern normally needs two independent occurrences, unless one occurrence exposes a severe safety or data risk. Propose one bounded change per retrospective:

- deterministic failure → automated check or protected control;
- repeated review judgment → review standard or focused skill guidance;
- missing discoverability → a concise context pointer;
- stale/no-op instruction → remove or narrow it.

State the observed pattern, evidence, proposed change, expected behavior, possible regression, and rollback. The user approves environment changes; the agent does not silently self-modify its future rules.

## Validation

Add or identify a regression task that would fail before the change and pass after it. Re-evaluate on the next retrospective. Record accepted and rejected proposals in the project's durable evolution log.

Retrospection is complete when one change is accepted with a test and rollback, or explicitly rejected with a reason. More rules are not success; fewer repeated failures at acceptable cost are.

## Experience is scoped evidence, not a new universal rule

Keep an observation or suspected cause as a **candidate** until a comparable task validates the proposed correction. A severe single failure can justify a precaution, but does not prove its explanation. Mark an experience **validated** only with its scope, independent observations, regression/forward result, limits and reversal condition. Validation for one task family is not global validity.

At the start of a relevant later task, consult only the matching entries in the project's existing evolution log. Check whether their sources, versions and task conditions still apply; record the selected entry and why it is applied, trialed or rejected. At closure attach the observed outcome and cost/extra user intervention (unknown if not measured). Reading an entry alone is not evidence that it helped.

If using the delivery checkpoint, `use --file <local-experience-file> --status candidate --decision trial --reason <applicability>` records the exact experience file consulted. A candidate cannot be recorded as a validated application. The helper retains declared status and freshness; it cannot certify the experience's validity. Use `validated`/`apply` only after inspecting the underlying validation evidence. No automatic promotion or global installation. Apply an environment change already authorized by the current request without asking again; otherwise present the concrete proposal.
