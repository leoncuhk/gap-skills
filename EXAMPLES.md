# Examples

## Quick: a local bug fix

Request: “Fix the typo in the validation error and update its snapshot.”

Route: Quick. Inspect the existing error and snapshot convention, make the local change, run the focused test, report evidence. No intent, plan, ledger, or quiz.

## Standard: an ambiguous feature

Request: “Add team invitations.”

Route: Standard. Inspect authentication, membership, email, and existing UI patterns. Ask only material decisions such as invitation expiry and duplicate handling. Record intent and a concise plan, implement end-to-end slices, run checks, then review separately for intent/spec fit and engineering quality.

### Executable Standard MVP

The repository includes a complete invitation-lifecycle case from a user's point of view:

1. Start from `tests/fixtures/standard-invitation`, which contains the request, project rules, existing API, and verification command.
2. Ask: “Use `$gap` to implement the invitation lifecycle described in README.md. Complete the Standard path end to end; do not commit.”
3. Expect one concise intent and plan in the conversation, no process files, a red verifier before implementation, and focused changes to source plus tests.
4. Run the project's visible tests, then run the evaluator-held outcome checks:

   ```bash
   python3 tests/evaluators/standard_invitation.py <candidate-repository> -v
   ```

5. Expect separate intent/spec and engineering review findings. If an independent reviewer is unavailable, the agent labels the self-review instead of waiting or retrying.
6. Completion reports passed checks, their limits, deviations, residual risk, and any exhausted budget or blocker.

The hidden evaluator checks case-insensitive identity, non-extending duplicates, the exact expiry boundary, replacement after expiry, canonical acceptance, and refusal to reinvite an accepted identity. A known-green implementation under `tests/reference-solutions/standard-invitation` proves the evaluator is solvable without exposing it to the implementation session.

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
