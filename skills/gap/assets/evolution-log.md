# Agent environment evolution log

## <date>: <change>

- Pattern and evidence: <at least two occurrences, or one severe event>
- Change: <one bounded edit>
- Expected behavior: <observable result>
- Regression test: <task/check>
- Risk and rollback: <risk and reversal>
- Owner decision: accepted | rejected — <reason>
- Next review: <date or trigger>

## Evidence scope and later use

- Status: candidate | validated within <task conditions> | rejected
- Observations and validation: <distinct task/source pointers; regression and forward result>
- Limits / reversal signal: <what would invalidate this experience>
- Later task: <pointer> — decision: apply | trial | reject — reason: <fit>
- Actual outcome / extra cost / user intervention: <evidence or unknown>

- Bounded experience JSON: <path; candidate or evidence-backed validated; see references/retrospective.md>
- Adoption scope evidence: <task ID, experience ID, matching conditions, checked exclusions, file/hash/target references>
- Checkpoint use ID / result receipt: <one use ID and same-task observed result; missing means unverified>
- Result history: <retain failures and retries; pass/fail/unknown; cost/intervention or unknown>
- Semantic review: <separate reviewer receipt and limits; identity/independence declared, not authenticated>

A saved record is not evidence of improvement. Two independent validation tasks including forward evidence support only the stated scope; each later application needs its own outcome checks. A changed underlying receipt or scope basis invalidates freshness even if this log and the experience file are unchanged.
