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
