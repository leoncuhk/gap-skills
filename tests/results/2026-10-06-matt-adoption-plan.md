# Matt adoption: bounded validation plan

Frozen before solver dispatch, 2026-10-06. Baseline gap: `cea4bd41a4434f6795d334b7796998695ef1ab1f`. Reference upstream: `mattpocock/skills@4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d`.

## Purpose and scope

Make existing checks effective, make change evidence easier to verify, and test a small instruction deletion. Modify existing gap references only; retain one entry point, nine references, seven assets and existing helpers. No coordinator, parallel runtime, automatic schedules, global installation, production action, external dependency or publication.

Absorb three mechanisms: diagnose existing check wiring before inventing new checks; use claim-appropriate before/after receipts plus concrete rollback effects when helpful; validate a suspected no-op with controlled deletion rather than a writing preference. The upstream retro was promoted without a body change; writing-for-agents was already present. These are re-examined mechanisms, not all new upstream features.

## Frozen comparison

- `old`: installed skill from the baseline commit.
- `full`: two reference edits, before deletion.
- `pruned`: identical to full except removal of the sentence “HTML earns its cost only when interaction or layout materially improves understanding.” Adjacent medium-selection conditions and the short-answer boundary remain intact.
- Skill manifests under `/tmp/gap-matt-adoption-snapshots-20261006/manifest.json` bind every installed file.
- Independent acceptance owner creates synthetic raw project inputs, prompt, negative/positive controls and outcome criteria before dispatch. Same files/prompt/budget in all arms; only workspace path and skill variant differ. No answer hints sent to solvers.
- Main owns dispatch. At most three solver contexts and one independent acceptance/review context; no solver delegation, paid API/CLI experiment or extra trial without a new concrete reason and recorded budget revision. Each solver requests `gpt-6-astra/high`, at most 16 tool calls / 10 minutes. Actual backend identity, complete platform call stream, tokens, cost and human minutes may remain unknown.
- One substantive repair and a separate small request may share each solver context. This is a scoped exploratory comparison, not fresh-context Quick generalization or a statistical efficacy claim.

## Acceptance and stopping

1. Existing safe project checks fail on the actual negative control for the intended reason and still pass valid input after repair; original check/business semantics are preserved.
2. Actual evidence supports the before/after claim and rollback scope; no fabricated execution, remote-CI or human-efficiency assertion.
3. No unnecessary framework, new dependency, HTML or process-file ceremony for the small request.
4. Full/pruned comparison preserves required behavior. A passing pair supports only provisional deletion of this redundant sentence; no conclusion that all guidance is unnecessary.
5. Independent source review checks authorization boundaries, evidence limits and accidental universal rules; repair supported defects and rerun affected checks.
6. Package validator and complete existing unittest suite pass; behavior evidence remains distinct from structure tests.

Stop when these scoped checks pass, budget expires, or a real blocker remains. Preserve failure and do not weaken criteria. Repository checks and one task family cannot establish saved human work. Rollback is reversing the local adoption commit; no global installs are changed.

## Pre-dispatch protocol clarification

Before any solver started, the main reviewer rejected an envelope that inlined every skill file. The final protocol installs each frozen skill under the task's `.agents/skills/gap`, reads its real entry point and explicitly exposes retrospective/communication in all three arms. This tests those mechanisms under controlled exposure, not automatic reference routing. The independent owner also corrected an over-broad new-file prohibition to allow justified gap evolution/backlog records, which the task had not forbidden. Original protocol hashes and these clarifications remain in the evidence bundle; no observed solver result motivated either change.
