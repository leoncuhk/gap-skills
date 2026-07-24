---
name: terra-gate
description: The dual merge gate — machine verification green, then an understanding quiz reconciled against the diff. Use before merge, delivery, or sign-off.
disable-model-invocation: true
---

# Terra Gate

Two gates, both required. Machine green means the code passed; it doesn't mean anyone understands what shipped — and for a solo developer there is no reviewer behind you.

## Gate 1 — machine

Run the project's verify commands (the same ones the hooks enforce). Red → back to build. No verify command exists → say so plainly and record the `[H]` gap; this gate never passes silently.

## Gate 2 — understanding

First **reconcile ledger against diff**: scan the changes for anything no plan step, resolved item, or deviation accounts for. Unaccounted changes are unlogged deviations — the highest-risk items in the room. Each is dispositioned before any question is asked: the user owns it (→ `Resolved` with a why), or it is reverted or split into its own change.

Then a report, grouped by intent: what changed, how it interacts with existing code paths, and the 2–3 mental-model updates the user should walk away with.

Then the quiz, scaled to the risk it guards: no unlogged deviations and fewer than ~4 ledger entries → one round of 2–3 questions; otherwise 5–8, asked and graded one at a time, mixing recall ("what happens to in-flight jobs during deploy now?") with prediction ("someone calls X with a stale token — what do they see?"), weighted toward what would bite an unaware maintainer.

Grade honestly. A miss is either a gap in the user's model or a change too clever — say which. Never pass out of politeness. After a failed round: walk the missed entries, then a second round of variant questions on the missed ground. Two failed rounds → recommend splitting or simplifying the change, not a third quiz.

## Death rite

Both gates pass → graduate the whys that are hard to reverse or surprising without context into `docs/adr/` or the commit message, then delete `TERRA.md` and `PLAN.md`. Working memory, not documentation.
