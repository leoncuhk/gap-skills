# Examples

Use normal language and let `gap` route automatically, or invoke the single entry point explicitly with `$gap` in Codex and `/gap` in Claude Code. The user does not select internal planning, debugging, delivery, or review modules.

## Quick: a local bug fix

Request: “Fix the typo in the validation error and update its snapshot.”

Route: Quick. Inspect the existing error and snapshot convention, make the local change, run the focused test, report evidence. No intent, plan, ledger, or quiz.

## Standard: an ambiguous feature

Request: “Add team invitations.”

Route: Standard. Inspect authentication, membership, email, and existing UI patterns. Ask only material decisions such as invitation expiry and duplicate handling. Record intent and a concise plan, implement end-to-end slices, run checks, then review separately for intent/spec fit and engineering quality.

### Full user-flow MVP

```text
User:
$gap Implement the invitation lifecycle described in README.md. Use repository
facts and take only reversible defaults where the contract is silent. Do not commit.

Agent:
Standard path: the behavior spans invitation creation and acceptance and contains
material policy choices, but has no production or irreversible action.

I found the repository verification command, case-insensitive identity convention,
and existing membership rules. One material decision is still unspecified: should
an accepted identity be invitable again? I recommend no, because membership is the
terminal state and this preserves the existing invariant.

User:
Accepted identities cannot be invited again.

Agent:
Intent: add a seven-day invitation lifecycle without changing existing membership
identity rules. Plan: add red tests for creation, duplicate, expiry, acceptance, and
accepted-identity rejection; implement the smallest state transition changes; run
the declared suite; reconcile the diff; review intent/spec and engineering axes.

... agent records the failing tests, implements, and validates ...

Agent final:
Implemented the invitation lifecycle in the existing source and tests only.
- Verification: project suite 9/9 passed; evaluator-held outcomes 4/4 passed.
- Intent/spec review: pass; all accepted behaviors are represented.
- Engineering review: pass; no blocking finding after final diff review.
- Independence: self-review only; an independent reviewer was unavailable.
- Deviations: none. Process files: none. Remaining limit: no external email delivery
  was requested or tested.
```

The exchange shape is stable; exact wording is not. The important behavior is that repository facts are discovered, only material decisions reach the user, success becomes executable, verification evidence drives repairs, and the two review axes remain separate.

### Reproduce the executable Standard case

The repository includes a complete invitation-lifecycle case from a user's point of view:

1. Start from `tests/fixtures/standard-invitation`, which contains the request, project rules, existing API, and verification command.
2. Ask: “Use `$gap` to implement the invitation lifecycle described in README.md. Complete the Standard path end to end; do not commit.” Use `/gap` in Claude Code.
3. Expect one concise intent and plan in the conversation, no process files, a red verifier before implementation, and focused changes to source plus tests.
4. Run the project's visible tests, then run the evaluator-held outcome checks:

   ```bash
   python3 tests/evaluators/standard_invitation.py <candidate-repository> -v
   ```

5. Expect separate intent/spec and engineering review findings. If an independent reviewer is unavailable, the agent labels the self-review instead of waiting or retrying.
6. Completion reports passed checks, their limits, deviations, residual risk, and any exhausted budget or blocker.

The hidden evaluator checks case-insensitive identity, non-extending duplicates, the exact expiry boundary, replacement after expiry, canonical acceptance, and refusal to reinvite an accepted identity. A known-green implementation under `tests/reference-solutions/standard-invitation` proves the evaluator is solvable without exposing it to the implementation session.

The declared `5 repair iterations / 30 minutes` budget applies only after a verification failure. It prevents an expensive unchanged loop; it does not shorten a successful run or turn an unfinished task into a pass.

## Standard: standalone code review

Request: “`$gap` review `main...HEAD` against `SPEC.md` and repository standards. Read only.”

Route: Standard, review branch only. Resolve the fixed point, record changed files, read the controlling specification and repository rules, inspect only the selected diff, and report separate intent/spec and engineering verdicts. Do not edit, approve, merge, or create process artifacts. If no independent reviewer is available, report self-review and the limitation rather than claiming independence.

The executable fixture in `tests/fixtures/review-change` keeps visible tests green while `tests/patches/review-change.patch` plants four review concerns: missing negative-input rejection, a changed public signature, binary floating-point money, and missing changed-behavior tests. `tests/evaluators/review_change.py` confirms the first two as outcome failures, while the specification and repository rules provide evidence for all four. The reference implementation under `tests/reference-solutions/review-change` passes the evaluator.

## Standard: taste discovered by showing

Request: “Make the dashboard feel calmer.”

Route: Standard with discovery. Find existing references or show contrasting disposable variants along one axis. Convert the reaction into an explicit criterion, plan the accepted direction, and keep prototypes out of production unless separately approved.

## Governed: production data migration

Request: “Merge customer identities and deploy the migration.”

Route: Governed. Create durable intent/spec/plan, name the data owner and release approver, define dry-run evidence and rollback, independently review the migration and verifier changes, and stop before production until the real deployment boundary receives fresh authorization.

## Adoption

Request: “Use gap in this repository.”

Read the repository instructions, commands, CI, tracker, review, deploy path, and risks. Return a minimal proposal first. Do not initialize git, install dependencies, rewrite instructions, or add hooks until those exact changes are approved.

## Retrospective

Observation: two separate changes silently weakened fixtures to make tests pass.

Propose one change: add an independent review check for verifier modifications, define a regression fixture, state the possible false-positive cost, and wait for approval. Do not add unrelated rules in the same retrospective.
