---
name: terra-plan
description: Compile a burned-down ledger into PLAN.md ordered by decision volatility, ending in a verifiable stop condition a loop can mount.
disable-model-invocation: true
---

# Terra Plan

A plan's job is to put the expensive-to-change decisions in front of the user while changing them is still free — and to compile the goal into a stop condition something else can verify.

Open gaps block the plan: run their listed resolvers first. Only low-risk residue converts to a labeled `[A]`. The plan cites only `Resolved` and `Assumed` items.

Order by volatility:

1. **Decisions you may want to tweak** — data model, interfaces, user-facing behavior. Each: the choice, one alternative considered (or "no real alternative" for territory findings), what changing it later costs. (From `Resolved`.)
2. **Assumptions standing** — the `[A]` batch: one line each, veto window, and the pivot signal — what observation during build forces revisiting it.
3. **Mechanical work** — compressed. The user trusts you here; reviewing it wastes their attention.

End with two things:

- The **2–4 yes/no items** needed before starting.
- The **stop condition** — the checkable state that means done: tests X green, artifact Y exists, criterion Z met. This line is what `/goal` or any loop mounts; a stop condition that isn't mechanically checkable goes back to the ledger as a gap.

Write `PLAN.md` beside the ledger (`PLAN-<task-slug>.md` if slugged). Under ~400 words — a plan too long to read gets skimmed. `TERRA.md` + `PLAN.md` are the launch packet.
