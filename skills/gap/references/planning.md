# Planning

Choose the smallest planning artifact that survives the required handoffs.

## Artifact choice

- **Quick**: a short in-conversation approach, if any.
- **Standard, single session**: a concise plan in the issue, PR, or `plan.md`.
- **Standard, multi-session**: accepted intent plus a durable plan and independently verifiable work slices.
- **Governed**: durable intent, spec, plan, verification expectations, owners, and approval points.

Intent says why and what outcome matters. A spec defines stable behavior and constraints. A plan explains how this repository will implement and verify it. Do not repeat the same content across them.

## Specification

A spec covers behavior, actors, interfaces, invariants, failure modes, compatibility, security/privacy constraints, observability, acceptance criteria, and non-scope. It avoids volatile file paths and code snippets unless a prototype encodes a decision more precisely than prose.

Use [the specification asset](../assets/spec.md) only when the task needs a durable spec. Small changes do not.

## Plan

Open with the outcome, chosen approach, and riskiest assumption. Then record:

1. decisions expensive to change later, with alternatives and tradeoffs;
2. assumptions, reversal cost, and pivot signals;
3. affected seams/files and implementation order;
4. proof for each meaningful behavior;
5. risks, rollback or recovery where relevant;
6. machine-checkable checks and human judgment checks as separate lists.

Machine-verifiable claims use commands or observable assertions. Experience, product fit, visual quality, and risk acceptance use a named human judgment check; do not pretend they are mechanically decidable.

## Work slicing

For work too large for one fresh context, create tracer-bullet tickets. Each ticket delivers a narrow end-to-end behavior, is independently demonstrable, fits one session, and declares blocking edges.

Wide mechanical refactors are the exception. Use expand–migrate–contract: introduce the new form beside the old, migrate callers in green batches, then remove the old form after all migrations complete.

## Approval

Standard work needs user confirmation only for unresolved material choices or when the user requested plan approval. Governed work requires explicit acceptance of intent, spec, and plan by the named owner before the next irreversible stage.

Planning is complete when the next implementer can act without guessing at consequential choices and every acceptance check has an owner.
