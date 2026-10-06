# Independent implementation review — pre-solver

Scope: installed-review-1, copied from current skills/gap after CLI integration; per-file SHA-256 in installed-review-1-manifest.json. Reviewed against frozen/criteria.md. No repository writes.

## Intent axis
22 independent API/CLI assertions pass against installed copy. Both renderers display the same actual source excerpts, before/after diff and option costs/consequences/tradeoffs/owner/deferral. Full-file changes including uncited lines and equal-content symlink target changes are stale. Current review feedback has applied=false and authorization=false; state bytes do not change. Old brief/source feedback, and omission of previously-bound brief, fail. Candidate use requires scope and current task ID; actual result receipt preserves candidate status. Out-of-scope rejection does not require invented matching scope. No blocking intent finding currently open.

## Engineering axis
Found and reproduced one schema inconsistency: experience version true and 1.0 were accepted as version 1. Reported to implementer and fixed; same external test now passes. No blocking engineering finding in inspected seams. HTML is inspected as generated text; no browser run. Source-authentic rendering and content freshness do not prove semantic correctness of summary, option text or scope declarations.

## Evidence and limitations
reports/api-second.txt preserves the original version-type failure (15 pass / 1 fail). reports/cli-second.txt preserves installed-copy 22/22 pass. api-first.txt and cli-first.txt additionally preserve verifier-construction mistakes (unresolved /tmp alias; treating plain-text stdout as JSON), corrected only in external acceptance scripts, not product.

Domain evaluator qualifies on 2 known-solvable mechanical positive controls and 8 meaningful negative controls; full structured results are compared, not just totals/keywords. This does not yet evaluate actual solver artifacts or establish human comprehension, broad workflow efficacy, all-platform trace completeness, model cost or authentication of reviewer identity.

## Follow-up source review and corrective revalidation

Two blocking identity/freshness defects were reproduced before any solver run: (1) when both briefs were already contract inputs, selecting a different brief left the same observation hash, allowing feedback from another explanation; (2) a changed contract input absent from experience scope basis left current_result_status=recorded. Reports/cli-gaps.txt preserves 22 pass / 2 fail. Implementer added explicit selected_brief identity to observation and stale_basis to experience freshness. Installed-review-2 differs only in scripts/checkpoint.py; independent CLI suite now passes 24/24 (cli-review2.txt). Old envelopes are archived as runs/dev-unrun-freeze1 and were never run. Freeze2 manifest SHA-256: d086ecaf8a82b2b192d8db608f48f078b3d6427aa0fe8c241cc24c45377a5481. No blocking finding remains in these reviewed seams.
