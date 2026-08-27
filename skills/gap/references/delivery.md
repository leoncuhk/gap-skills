# Delivery

Implement against accepted intent and planning artifacts while keeping feedback tight.

## Build

Read the current source-of-truth artifacts before editing. Work in the smallest slice that can be verified. For changed behavior, prefer a failing test or other observable red signal before the fix when the repository supports it. Run focused checks during the build and the full relevant verification before review.

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

When verification fails, feed the exact command, observed failure, and supported conclusion into the next repair. Each retry must use new evidence, a changed hypothesis, or a meaningfully different action; never repeat an unchanged attempt.

For long-running, costly, flaky, or externally limited work, set a proportional time, iteration, or tool-cost budget before looping. Stop when the objective passes, the budget is exhausted, no defensible new path remains, or user input is required. A stopped loop reports attempted paths, evidence, blocker, and the input that would unlock progress; budget exhaustion is not completion.

## Two-axis review

Review the change independently on two axes and keep the findings separate:

1. **Intent/spec**: missing behavior, wrong behavior, unrequested behavior, unresolved constraints.
2. **Engineering**: correctness, security, maintainability, repository conventions, tests, operational risk.

Use a separate reviewer/context when available for material work so implementation assumptions do not silently become review assumptions. Attempt unavailable review infrastructure once, then continue with an explicit self-review and report that independence was not achieved; do not wait or retry unchanged. Every blocking finding cites concrete evidence and a location. Skip issues already enforced reliably by tools.

Do not collapse the axes into one score. A change can follow engineering standards while solving the wrong problem, or match the spec while damaging the codebase.

## Human understanding

For large solo-maintained or high-risk changes, summarize how behavior interacts with existing paths, then ask a few prediction questions about the consequences most likely to surprise a maintainer. This is a learning and risk check, not a universal ceremony or a substitute for independent approval.

## Close

Reconcile intent, plan, deviations, diff, and evidence. Promote durable decisions and unresolved environment gaps. Delete only disposable working state; retain artifacts required by the project's review, audit, or future maintenance.
