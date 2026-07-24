# Terra Validation Protocol

Pre-registered before any test run (2026-07-24). Metrics and thresholds below are fixed; running the tests may not move them retroactively.

## Principles

1. **Grader ≠ generator.** All behavioral tests use planted defects; the score is recall of the plants — counted, not felt. Grading is done by a fresh session without the implementation context, or by the user against the checklist.
2. **Boundary difficulty.** Each scenario is calibrated so an agent without the skill would plausibly miss the plant; trivial and impossible scenarios both measure nothing.
3. **n=1 honesty.** Personal-scale testing yields evidence, not proof. The objective signals: plant recall, trigger rate, longitudinal retention, and documented counterfactuals (recorded at the moment of the catch, never reconstructed later).
4. **Falsifiable.** Every level carries a failure verdict written in advance.

## L1 — Behavioral (planted-defect scenarios)

| # | Scenario | Plants | Pass criterion |
|---|---|---|---|
| 1 | survey on a prepared repo | test command with no hook; 2 "musts" hiding in CLAUDE.md; 1 hidden constraint in code | 3/3 recalled; mechanical gap wired; request rewritten as title |
| 2 | resolve-ask with role-played user | user gives a "just pick" reply at question 4 | fatigue valve fires; remainder → [A] batch for veto; ≤5 questions total |
| 3 | resolve-show with hidden-taste persona | persona held by grader, not shown | asks for a reference first; delivers a criterion sentence matching the persona |
| 4 | build against a poisoned plan | one PLAN.md line contradicts the codebase; one step touches a "running service" config | deviation logged + plan line updated without blocking; ledger constraints re-read before the config step |
| 5 | gate on a salted diff | 1 unlogged drive-by change; 1 test-file modification | reconcile catches both; verifier change flagged highest-severity |
| 6 | evolve on synthetic archives | 3 TERRA files sharing one failure mechanism ×2; journal has an unaudited prior entry | prior entry audited first; exactly one bounded edit proposed |
| 7 | **trigger test** | 5 fresh task openings, terra never mentioned | survey self-fires ≥4/5 |

Failure verdict: any scenario <pass → fix the skill text, rerun that scenario. Trigger <4/5 → fix descriptions before anything else; the lifecycle has no entrance without it.

## L2 — Paired comparison (signal, not proof)

Pairs of similar tasks, alternating with/without terra. Pre-registered metrics: time to genuinely-done; rework count after first "done"; surprises surfacing later; friction (1–5 self-report). No statistical claim at this n; direction only.

## L3 — Mileage (checkpoint 2026-08-07)

Counted from real work: TERRA.md files created · deviations later actually consulted · unlogged changes caught by gate · component retention.

Failure verdicts (any one → delete the component; all four → archive the system, which is also a valid result):
- zero ledgers created → survey never fires or gets bypassed
- ledgers exist but Deviations stay empty → logging discipline is theater
- gate never catches an unlogged change → reconcile is ceremony
- user routinely works bare because terra feels like friction → retention law (28→4) has spoken

## L4 — External

- Natural installs from the published repo; any third-party report outranks all self-testing.
- Cross-model test: run scenarios 1, 4, 5 with a non-Claude model — skill text may be overfit to one model's habits (failure modes are model-specific; Self-Harness, arXiv 2606.09498).
