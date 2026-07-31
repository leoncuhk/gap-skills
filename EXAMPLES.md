# A full pass, end to end

One task — "add rate limiting to the public API" — walked through all six moves. Condensed; the mid-task ledger this produces is [examples/GAP.md](examples/GAP.md).

## 1. Open — gap-survey (automatic)

You say: *"Add rate limiting to the public API."*

Survey sweeps the harness (finds `npm test` exists but no PostToolUse hook → wires it; finds "always use the shared Redis" buried in CLAUDE.md → flags it as a misplaced must) and the territory (finds Redis already in the stack, finds `middleware/auth.ts` resolves keys before routing, suspects Stripe webhook bursts are unhandled). It seeds the ledger and ends:

> **GAP: add per-key rate limiting at the middleware seam, reusing the existing Redis** — 3 open, 1 assumed.

Your request, corrected by the territory.

## 2. Close gaps — gap-resolve (automatic)

Facts were looked up already. One decision remains:

> **Question:** Limit per API key, or per account? Keys can share an account.
> **Why it matters:** per-account needs a key→account join on the hot path.
> **Evidence:** `models/api_key.ts:12` — keys carry `account_id`.
> **Recommended:** per-key. Silence = this.

You answer "per-key". The taste item (429 body tone) gets two contrasting drafts; you point at the terse one → criterion sentence lands in Resolved. Burn-down: `0 open, 2 assumed`.

## 3. Compile — /gap-plan

PLAN.md opens with three lines (what / approach / riskiest assumption), leads with the two decisions you might tweak, compresses the mechanical work, and ends:

> **Stop condition:** `npm test` green, `429` returned under 30 req/s on the bench script, terse body per criterion.

## 4. Build — gap-build (automatic)

Mid-build the plan's "one limiter instance" line collides with the worker pool. The session takes the reversible option (per-worker instance + shared Redis window), logs the deviation, updates the plan line, keeps going. No interruption.

## 5. Gate — /gap-gate

Machine gate: tests green. Understanding gate: reconcile finds one unaccounted edit — a drive-by rename in `auth.ts` — you own it into Resolved. Three questions ("what happens to in-flight requests at the window boundary?"), all answerable from the report. Pass.

## 6. Death — and later, /gap-evolve

The why behind "per-worker limiter instances" graduates to `docs/adr/`; GAP.md and PLAN.md are deleted. Two weeks later, evolve notices "forgot bench script before gate" appeared twice across tasks → proposes one hook line; you approve; journal records it.
