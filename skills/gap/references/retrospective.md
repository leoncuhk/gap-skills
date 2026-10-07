# Retrospective

Improve the agent environment from observed failures, not from speculative completeness.

## Evidence

Read the actual session/task record, review findings, incidents, reverted changes, CI failures, user corrections, and the previous evolution entry. Judge the last environment change before proposing another: keep it only if the expected behavior appeared without disproportionate friction.

Look for repeated mechanisms across tasks:

- navigation or missing context pointers;
- missing or ineffective automated checks: trace the existing command through its callers and retained results before adding another; distinguish an absent check from one that is unwired, skipped, or whose failure is swallowed;
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

For a check or its wiring, exercise the actual entry point with a known-bad case and a valid control. The bad case must fail for the intended reason and propagate failure to its caller; the valid case must still pass. Reuse the project's check before introducing a new rule or tool. Local execution does not prove remote CI ran or branch protection is active.

For exact duplicates or obsolete references, inspect the retained meaning and dependencies and run the relevant local checks. When an instruction’s behavioral effect is uncertain and the comparison cost is justified, compare otherwise identical skill variants with and without that instruction on the same task, model configuration and budget. Freeze success criteria first; retain failures, extra calls and user corrections (unknown if unmeasured). Test the branch the instruction governs and a small task that should stay light. Change one instruction at a time; a multi-change comparison cannot identify its individual effect. Remove it only within the tested scope when required behavior survives; one passing pair is provisional, not general equivalence. Keep authorization, user-purpose and evidence boundaries intact. If a needed reference was missed, test a clearer trigger before inlining its contents or adding another skill.

Retrospection is complete when one change is accepted with a test and rollback, or explicitly rejected with a reason. More rules are not success; fewer repeated failures at acceptable cost are.

## Experience is scoped evidence, not a new universal rule

Keep an observation or suspected cause as a **candidate** until a comparable task validates the proposed correction. A severe single failure can justify a precaution, but does not prove its explanation. Mark an experience **validated** only with its scope, independent observations, regression/forward result, limits and reversal condition. Validation for one task family is not global validity.

At the start of a relevant later task, consult only the matching entries in the project's existing evolution log. Check whether their sources, versions and task conditions still apply; record the selected entry and why it is applied, trialed or rejected. At closure attach the observed outcome and cost/extra user intervention (unknown if not measured). Reading an entry alone is not evidence that it helped.

If using the delivery checkpoint, `use --file <local-experience-file> --status candidate --decision trial --reason <applicability>` keeps legacy Markdown usable as a candidate. Its result stays `unverified` until the same task records its actual outcome. A `validated` command-line label cannot promote Markdown or a candidate JSON entry. No automatic promotion or global installation. Apply an environment change already authorized by the current request without asking again; otherwise present the concrete proposal.

### File-bound experience and adoption

Use structured JSON only when the additional evidence is useful. Keep it beside the project's existing evolution log, not in a global rule registry. Version 1 has these fields:

```text
{
  version: 1, id: "bounded-experience-id", status: "candidate" | "validated",
  sources: [{task_id, failure, receipt: REF}],
  scope: {applies_to: [condition], excludes: [condition]},
  correction: {action, expected_result, check},
  validations: [{
    task_id, kind: "regression" | "forward", scope: [condition],
    before: REF, after: REF, before_result: "fail", after_result: "pass",
    observed, review: {by, independent: true, receipt: REF}
  }]
}
REF = {path: "root-relative/file", sha256: "64 lowercase hex digits", target: "resolved/root-relative/file"}
```

All text is nonempty; conditions, exclusions and failure sources are nonempty lists. A candidate may have no validations. A validated entry needs at least two distinct validation tasks, separate from failure-source tasks, including a forward task. Each validation covers the exact bounded scope, has distinct before/after files and a separate semantic-review receipt. Reusing the same after-receipt target or bytes under another task label cannot count twice. One severe incident may justify a candidate precaution, not a validated claim. Exact scope labels prevent accidental structural broadening; they cannot prove the labels describe reality.

For structured `trial` or `apply`, add `--scope <task-scope.json>`:

```text
{task_id, experience_id, matched_scope: [condition],
 excluded_conditions_checked: [condition], basis: [REF], reason}
```

The scope file must identify this experience, match all its conditions, check every exclusion, and retain actual task evidence. The helper snapshots the experience, all source/validation/review files, the scope file and its basis together. Changed bytes, missing files or a repointed symlink make the adoption stale even when the experience JSON is unchanged. Paths must remain inside the task root. A stale entry cannot be applied or trialed; rejection may retain stale references for audit. Legacy Markdown remains candidate-only and may retain its reason without a structured scope file.

For every trial/application, capture a new result receipt at task closure and attach it through `use-result --use-id <id> --receipt <result.json> --outcome pass|fail|unknown`:

```text
{use_id, task_id, experience_id, outcome: "pass" | "fail" | "unknown",
 observed, cost, user_intervention, checks: [REF]}
```

Copy the use and task identifiers from the recorded adoption. `checks` must bind new actual check files for this task, not recycled validation evidence. Write `unknown` for unmeasured cost or intervention. The receipt must match this particular adoption and outcome; another task's success cannot close it. Missing or unknown outcomes remain `unverified`; pass/fail means an outcome was recorded, not that improvement was certified. Retries append results so a later pass does not erase failure history. Inspect both failed and successful outcomes before judging the experience.

Hashes check integrity and freshness only. Review independence and actor identity are declarations, not authenticated facts; matching scope labels, a passing receipt and saved files do not establish semantic fit or causal improvement. Independent semantic review must still inspect the underlying evidence and limits. Reading is not use; use is not improvement.
