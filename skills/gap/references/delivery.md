# Delivery

Implement against accepted intent and planning artifacts while keeping feedback tight.

## Build

Read the current source-of-truth artifacts before editing. Work in the smallest slice that can be verified. Prefer the smallest design that satisfies accepted behavior: every changed line supports that behavior or cleans up something this change made obsolete; preserve unrelated code and local conventions. Add abstraction or configuration only for a present requirement or an established seam.

For changed behavior, prefer a failing test or other observable red signal before the fix when the repository supports it. Run focused checks during the build and the full relevant verification before review.

When reality contradicts the plan:

- take the most reversible safe option;
- record what the plan said, what changed, why, and the cost to revisit;
- update the plan when it is durable;
- continue only if the deviation does not change architecture, security, data, cost, scope, or the user's promise.

Material deviations stop at a coherent checkpoint for a user decision. Do not hide a scope change inside implementation judgment.

## Verification evidence

Use the project's real commands and observable behavior. Report:

- command or check;
- result;
- behavior or risk it supports;
- what it does not establish.

Treat modifications to tests, fixtures, CI, hooks, evaluators, and acceptance thresholds as verifier changes. They require explicit ownership in the plan or deviation record and separate scrutiny; a green result after weakening the judge is not evidence of success.

## Bounded repair loop

When verification fails, feed the exact command, observed failure, and supported conclusion into the next repair. Each retry must use new evidence, a changed hypothesis, or a meaningfully different action; never repeat an unchanged attempt. A repair iteration begins after a failed verification; if a budget should include the initial implementation, say "total attempts" instead.

For long-running, costly, flaky, or externally limited work, set a proportional time, iteration, or tool-cost budget before looping. Stop when the objective passes, the budget is exhausted, no defensible new path remains, or user input is required. A stopped loop reports attempted paths, evidence, blocker, and the input that would unlock progress; budget exhaustion is not completion.

## Review handoff

Before closing Standard or Governed delivery, read [reviewing-changes.md](reviewing-changes.md). Review the accepted intent, fixed diff, verification evidence, and verifier changes. Fix blocking findings only within the user's authorized scope, rerun affected checks, and review the resulting diff again.

## Human understanding

For large solo-maintained or high-risk changes, summarize how behavior interacts with existing paths, then ask a few prediction questions about the consequences most likely to surprise a maintainer. This is a learning and risk check, not a universal ceremony or a substitute for independent approval.

## Close

Reconcile intent, plan, deviations, diff, and evidence. Promote durable decisions and unresolved environment gaps. Delete only disposable working state; retain artifacts required by the project's review, audit, or future maintenance.

## Resume from actual state

Read the latest purpose, accepted semantics and remaining criteria. Inspect the actual outputs, source versions, worktree and receipts before deciding what to run next. A process that ended, a saved file, a passed local check, a separate acceptance verdict and a pending human decision are different facts. Reuse still-valid work; recheck only affected claims. Never overwrite an original with a processed copy or repeat an external action merely because a previous session stopped.

When file freshness is a concrete risk, [checkpoint.py](../scripts/checkpoint.py) provides a local Python 3.10+ standard-library helper. It ships inside the skill and has no repository imports. It does not run jobs, interpret business truth, authenticate reviewers or grant permission. File hashes and resolved targets only show continuity of the paths the agent actually declared; repointing a symlink invalidates its evidence. Use one checkpoint writer at a time. Include all inputs that could invalidate a claim and inspect semantic fit yourself.

Use an existing task directory and checkpoint location. Create a contract JSON with `purpose`, `source` (user decision/source pointer), `semantics` (list), `inputs` (root-relative files), and `criteria` (nonempty list of `{ "id": "report", "claim": "requested observable result", "kind": "artifact" }`). Kinds are `artifact`, `check`, `external`, `human`, `review`. Set `"independent": true` on a review criterion when a genuinely separate review is required. Include `review` only when required; a substantive human decision has its own criterion. Do not add permission gates that the user has already resolved.

```sh
# Set TASK to the actual task directory, GAP to the installed gap skill folder.
python3 "$GAP/scripts/checkpoint.py" --root "$TASK" --state "$TASK/state.json" init --contract "$TASK/contract.json"
# After a real check: retain its actual log, then bind it and the observed output.
python3 "$GAP/scripts/checkpoint.py" --root "$TASK" --state "$TASK/state.json" record --criterion report --kind artifact --result pass --by current-session --receipt verification.txt --file report.csv --note 'Compared the generated report with the requested definition; no external delivery claimed.'
python3 "$GAP/scripts/checkpoint.py" --root "$TASK" --state "$TASK/state.json" check
```

`check` is read-only: exit 0 means every declared criterion has current recorded passing evidence, 1 means missing/failed/stale evidence, 2 means invalid input. It is not an independent acceptance gate. Read the returned dimensions, not just the exit code. `end --reason ...` records termination without satisfying criteria. `revise --contract ... --authority ... --reason ...` preserves old contracts/input fingerprints and invalidates old receipts; use it after inspecting changed goals or inputs, even when the wording is unchanged. Direct edits to the stored contract are rejected. Evidence files must be inside the task root; use a local, authorized receipt/export for external observations. No synthetic success logs.

Record each check's actual failing or passing result; never capture an old log against new files as though the check was rerun. For a separate review, use kind `review`, `--by` with its real context/identity, and `--independent` only if it actually was independent; the review also binds earlier evidence. A self-declared name is not proof. In the final report distinguish run ended, artifact ready, independent acceptance (or its absence), and waiting for a named human judgment. Missing external-action receipts remain incomplete even when a list or draft exists.
