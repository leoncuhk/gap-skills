# Matt-adoption independent acceptance — 2026-10-06

Baseline gap commit: `cea4bd41a4434f6795d334b7796998695ef1ab1f`. This is one exploratory, directed-exposure, three-arm experiment over a small synthetic Python project. It is not statistical evidence of improvement, general equivalence or efficiency.

## Result

| Criterion | old | full | pruned |
|---|---|---|---|
| Public and six private bad/good controls | Pass | Pass | Pass |
| Existing fixed checker causally active | Pass | Pass | Pass |
| Business/contract/sample/skill integrity and local scope | Pass | Pass | Pass |
| Exact small note edit | Pass | Pass | Pass |
| No HTML in final artifacts | Pass | Pass | Pass |
| Concrete rollback and bounded report claims | Pass | Pass | Pass |
| Authentication of solver's historical before/after execution (E1) | Unknown | Unknown | Unknown |
| Complete platform workflow for O5 | Unknown | Unknown | Unknown |
| Complete frozen acceptance | Not established | Not established | Not established |

All objective artifacts pass. No arm outperformed the others on the frozen observable outcomes. Before/after receipts written by each solver are retained and compatible with independent observations, but cannot by themselves certify that the original solver performed those executions at the claimed time. No complete platform tool trace is accessible to this reviewer. The frozen criteria are not relaxed.

## Independent behavior evidence

`reproduce.py` ran the actual frozen original entry point with the supplied good/bad inputs, independently of solver logs. Both exited 0. It then ran the repaired task copies through the same public inputs and six private controls: valid documents passed, duplicate IDs and other contract violations failed. A disposable-copy probe changed the fixed checker's result to reject a valid input; every repaired public gate propagated that rejection. Restoring the checker restored acceptance. This establishes use of the existing checker through the entry point, not a narrative or keyword match.

The full and pruned fixes replace the transport-only preflight invocation with the existing checker, which includes JSON parsing. Old retains the preflight and appends the existing checker with failure propagation. Both implementations satisfy the frozen outcome and scope criteria. No checker, contract or business logic was modified. Installed skill hashes match the supplied snapshots.

Every reported rollback was also executed in a disposable copy. It restored the exact original gate hash, preserved good-input acceptance and reintroduced false acceptance of the same bad input. These are evaluator replays, not historical solver-run authentication. Original task outputs were not mutated by evaluation.

The normalized dispatched task prompt has the same SHA across all three arms; the only prompt difference is the workspace path. Frozen fixture hashes, remaining immutable files, and retained original gate/note bytes agree. See `input-comparison.json` and `baseline_manifest.json`.

## Evidence and source review

E2 passes by semantic report inspection plus independent rollback execution. E3 passes: all three reports limit findings to the tested synthetic local gate and disclaim broader outcomes. Old's one added `docs/agent/evolution-log.md` concerns the main environment repair and is justified under the pre-launch scope clarification. No separate process or HTML deliverable was created for the one-phrase request.

The final reviewed adoption diff has no blocking defect: retrospective guidance adds inspection of actual check wiring, actual bad/valid caller-level controls and scoped deletion evaluation; communication asks for claim-appropriate executed evidence and concrete rollback effects while exempting small edits from templates. The pruned variant retains lightest-medium guidance and the explicit short-answer boundary. Both plugin metadata versions are 0.6.1 and marked local/unpublished in the changelog. The new workflow scenario documents this evidence; it is not an automatically executed test. A minor wording correction was suggested: use “existing local validation chain” rather than “two local validation callers.”

Choosing the redundant-sentence deletion can be presented as a provisional source-level simplification with no observed artifact regression here. It must not be presented as complete empirical equivalence or as satisfying every frozen process criterion. Detailed review: `independent-source-review.md`.

## Limits

- One run per arm, one synthetic task family, no statistical inference.
- Full versus old adds multiple mechanisms together; their individual effects cannot be identified.
- All arms explicitly read retrospective and communication. This does not test natural activation or automatic reference routing.
- The small edit shares context with the substantive repair; it is not a fresh independent Quick task.
- The task itself asks for actual evidence, rollback effects and limited claims, so success cannot be attributed exclusively to skill additions.
- Final artifact inspection cannot certify every historical action. Backend identity, complete calls, tokens, timing, cost and human effort remain unknown. Solver self-reported counts are not promoted to platform measurements.
- The initial inline-skill protocol and overly narrow document allowlist were corrected before any solver started; original files/hashes and the amendment are retained. No observed failure caused a criterion relaxation.

## Reproduce

From the extracted evidence directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 reproduce.py
```

This reruns the frozen objective evaluator and independent original/rollback controls using standard-library Python, no dependencies or network. It writes fresh replay receipts under `replay/`. It cannot reconstruct unavailable historical platform traces. Preserve the original receipts first if comparing replays over time.
