---
name: gap-build
description: Execute against the plan — every action conditioned on the launch packet, deviations logged instead of improvised, guards before dangerous ground. Use whenever implementing with a GAP.md or PLAN.md present.
---

# Gap Build

First act: read `GAP.md` and `PLAN.md` if present, announce the open count — a launch packet only works if the receiving session opens it.

Every step is conditioned on the plan, not just the local context. Drift from the objective is a structural failure mode of the model, not bad luck — the plan is the anchor, re-read it when direction feels obvious.

When the territory contradicts the map: take the most reversible option, log the deviation, update the plan line it invalidates, and keep going — do not block on the user. Log under `## Deviations` (create on first write): what the plan said, what was done instead, why, what revisiting costs — 2–3 lines each.

Stop and ask only for: architecture, data migration, security, cost, or anything that changes what the user was promised — even if the response shape looks the same. Stop at a coherent checkpoint (stub, don't half-build); unrelated work may continue while you wait.

Feeling certain is not evidence of safety. Before touching a running service, shared resource, or config other components depend on — re-read the ledger's constraints and deviations; straightforward-sounding steps are where sessions do silent damage.

New gaps discovered mid-build go to `Gaps` with resolvers, even if resolved seconds later. An unlogged deviation is worse than none — the ledger claims completeness.
