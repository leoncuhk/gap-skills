# Changelog

## 0.2.1 — 2026-07-31

Line-by-line review pass: legacy vocabulary purged (fog, rig), skill headings unified, LICENSE holder corrected, knowns/unknowns quadrant table added to README, GitHub About + topics set. Fixed a real installability bug: templates now live inside the skills that reference them (`gap-survey/templates/`, `gap-gate/templates/`) — root-level `templates/` never reached `npx skills add` installs.

## 0.2.0 — 2026-07-31

Renamed: terra → **gap-skills**. The primitive is the name: repo, skill prefix (`gap-*`), and ledger (`GAP.md`) now all say the same word. GitHub redirects the old URLs.

## 0.1.1 — 2026-07-24

Lineage deep-audit round: mechanisms recovered or adopted from source-by-source comparison.

- **From finding-unknowns-skills**: decision checkpointing with conflict flagging; economic stop rule; source-as-spec reference reading; three-line plan opening.
- **From grill-for-unknowns**: stand-down rule for trivial work (negative triggers); criterion-sentence-as-gate-question for untestable quality; quiz fairness (answerable from the report); calibration against over-specified plans.
- **From EurekAgent (arXiv 2606.13662)**: verifier-integrity clause — changes to tests/CI/hooks are highest-severity in gate reconciliation.
- Restored clauses dropped in the defog/rig merge (silence definition, artifact-form guidance, survey manifest, CLAUDE.md surgery, verbatim-quiz rule).
- Added `tests/PROTOCOL.md`: pre-registered validation protocol with planted-defect scenarios and falsification criteria.

## 0.1.0 — 2026-07-24

Initial release: one gap ledger, six moves. Unifies the unknowns ledger (defog lineage) and audit-first environment assembly (rig lineage) under a single primitive — the gap — with the strength hierarchy, dual merge gate, and gated evolution.
