# TERRA: add rate limiting to public API

A worked example of a ledger mid-task — after a survey pass and two interview questions, before planning.

## Gaps
- [KU] Limit per API key or per account (keys can share an account)? → ask
- [UK] 429 response body tone — terse or explanatory? user will know on sight → show
- [H] No PostToolUse verification wired — repo has `npm test` but no hook → wire

## Assumed
- [A] Sliding window over fixed window — cost to revisit: one module, no schema impact
- [A] Limits configured in env, not DB — cost to revisit: config loader change; revisit when a customer needs per-plan limits

## Resolved
- [x] Redis already in the stack; reuse it, no new infra (territory, 2026-07-23) — found in docker-compose and the session store
- [x] Existing `middleware/auth.ts` resolves the API key before routing (territory, 2026-07-23) — limiter can sit right after it
- [x] Burst allowance required (user, 2026-07-23) — mobile clients batch requests on reconnect; hard cutoffs would break sync
