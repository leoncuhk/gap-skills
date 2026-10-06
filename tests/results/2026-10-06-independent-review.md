# Independent acceptance report — 2026-10-06

Engineering review passes for repaired commit `5bd5fe68cb939c1ebd41056485a2fd434e68cb29`. The planned held-out paired protocol fails; neither comparative effectiveness nor lower human effort is established.

## Fixed review scope

Baseline `c7a2fabd2f00f1ed9b29cf809a0bf70bf4af23f1`; first frozen implementation `b8ab8e7f02f974fcff33990b2521381daf20a6b8`; one repair round `5bd5fe68cb939c1ebd41056485a2fd434e68cb29`. Independent reviewer read the fixed diffs and frozen iteration plan, inspected actual helper logic and verifier changes, ran probes and the required validator/tests on a separately archived fixed tree. No repository files were edited by acceptance.

## Intent/contract axis

Pass for the implemented local capability: existing skill remains the only entry point; helper is optional and standard-library-only; Quick retains no process files. Guidance preserves purpose, source authority and semantic invariants, distinguishes process termination/local artifacts/separate acceptance/human decisions, and makes experience candidate versus validated scope explicit. No runtime, external execution, identity authentication, global install or publication was added. Scope expansion to analysis/local artifacts is consistent with the frozen plan. Guidance does not treat hashes or a self-declared reviewer label as content truth or authenticated independent acceptance.

The broader task's frozen criterion 7 remains FAILED: the actual first solver envelopes paraphrased frozen task/agreement wording, and the acceptance coordinator then launched three corrective contexts beyond the two-pair budget before the parent stopped them. Criteria were not changed. These failures cannot be converted into a compliant comparative pass by the successful local outputs.

## Engineering axis

Pass at the repaired commit, with no remaining blocking finding in this bounded review.

1. **Independent finding, fixed (P2): source alias changes could falsely preserve evidence.** In first implementation `checkpoint.py:30-35`, snapshot keys were resolved targets. Repointing a declared source symlink from v1 to v2 left the old target unchanged; `check` returned exit 0 and all criteria evidenced while output still represented v1. Repair retains declared path plus target fingerprint and resolves safely on recheck. The independent probe now returns stale/exit 1. The new test also covers equal-byte target changes.
2. **Developer-disclosed finding, independently reproduced and fixed (P2): retired output blocked fresh reviews.** Old review recording merged every historical non-review receipt, including retired artifacts from earlier contracts. After authorized revision and removal of an obsolete output, fresh valid review stayed stale. Repair binds latest evidence for current criteria/current revision. Independent probe now passes; historical receipts remain retained.

Evidence: `review/independent-probes.json` records actual CLI results for both first and repaired versions, including failing-before and passing-after controls. `review/fixed-verification.json` records fixed-tree validator and 21 passing tests. The copied installed helper remains self-contained. Existing standard/review evaluators were not weakened; `scripts/validate.py` only added a helper-existence check. New development collaboration evaluator is clearly labeled synthetic and verifies original preservation, message semantics, unobserved external status and no-duplicate resumption. It is not independent effectiveness evidence.

## Held-out outcomes, separately from protocol compliance

Four first arms requested `gpt-6-astra/high` through the spawn API. Actual backend identity is not exposed. Each used a fresh context, the same fixture bytes and local-only budget; enhanced arms read a copied installed skill from the first frozen commit. Task wording was semantically matched but not byte-identical, so the strict prompt criterion failed. First-arm artifacts are under `outcomes/` in the curated export and `preliminary-runs/` in the retained working evidence. Old final-response links point at original launch paths; use the relocated paths in the export.

| Task / arm | Machine + manual local outcome | Tool calls | Observed first-to-last tool span |
|---|---|---:|---:|
| Data semantics / baseline | Pass | 4 | 59.80 s |
| Data semantics / enhanced | Pass | 4 | 49.82 s |
| Interrupted artifact / baseline | Pass | 5 | 39.89 s |
| Interrupted artifact / enhanced | Pass | 5 | 48.31 s |

These times include inter-tool reasoning but exclude final-response generation and are not user-time measurements. Concurrent execution, four small synthetic tasks, and the protocol failures preclude comparative efficiency conclusions. Tokens, monetary cost, backend identity and real-user timing are null.

All four preserved source meaning and public interfaces, ran actual local checks, and reported no independent acceptance or successful external publication. Both report implementations produced 4 eligible customers, 2 converted, 0.5 conversion and $24.99 revenue and passed altered-input checks. Both briefing edits retained the original navigation, presenter notes, source links and visual CSS, replaced the obsolete policy/trial goal, and correctly explained the current cancellation policy. Both resumed from inspected artifact/source/handoff and rejected stale prior acceptance. No agent edited fixture tests or created process files. No real customer usefulness study or rendered visual QA occurred. Neither enhanced arm used the optional helper, so the pilot does not establish its behavioral uptake or incremental contribution.

Experience ideas stayed candidates with no invented adoption evidence. The briefing layout used before/after-window organization, but this only shows an implementation choice; there is no observed validated-experience transfer or customer benefit.

## Protocol and budget failure accounting

The coordinator noticed prompt paraphrasing and attempted a correction without approval for more solver contexts. Three extra contexts launched; all were interrupted on the parent's stop. Actual observed additional tool invocations were 3, 2 and 0 (five total); extra observed spans were 8.24 s, 4.79 s and unknown. Fourth corrective arm was never launched. Their partial outputs are excluded from task grades. Additional token/monetary costs are unknown, not zero. `spawn-envelopes.json` retains actual requested messages and model settings; `metrics.json` retains the failures and measured values. This is an acceptance-execution failure, not a reason to weaken the frozen criteria.

## Remaining limits

Quick friction is supported by unchanged Quick guidance, contract tests and zero process-file additions in the four completed tasks. There was no fresh held-out Quick activation trial, so activation precision and actual trivial-task overhead are unproven. Candidate-versus-validated rules and helper constraints are tested, but longitudinal use/rejection/outcome evidence remains absent. Human-effort reduction requires a newly authorized properly controlled real-work pilot; none is claimed here.
