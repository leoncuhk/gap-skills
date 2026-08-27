# Changelog

## 0.3.1 — 2026-08-27

- Added evidence-driven repair budgets and explicit blocked outcomes for long or costly loops.
- Added immediate labeled self-review fallback when independent review infrastructure is unavailable.
- Added an executable Standard invitation MVP with a clean fixture, evaluator-held checks, and a known-green reference solution.
- Reorganized behavioral evidence into scalable cases, fixtures, evaluators, reference solutions, and results directories.
- Added a repository map and repository-wide Markdown link validation; clarified which workflow scenarios are executable versus declared.
- Updated project documentation and validation to cover the new runtime boundaries.

## 0.3.0 — 2026-08-27

Rebuilt the package around one user-facing `gap` skill.

- Replaced seven lifecycle skills with one adaptive router and progressively disclosed discovery, planning, problem-solving, delivery, communication, governance, retrospective, and adoption references.
- Added Quick, Standard, and Governed paths so ceremony scales with ambiguity, size, and risk.
- Folded in the useful coverage of unknown discovery, grilling, specs/tickets, debugging, architecture, context handoffs, visual artifacts, plan-conditioned implementation, two-axis review, AI-native SDLC governance, and environment retrospectives without requiring parallel skill suites.
- Made adoption read-only by default and separated guidance, automated checks, and protected external gates.
- Split disposable task state from durable intent/spec/plan/review records and long-lived environment backlog.
- Added current Codex metadata and plugin packaging alongside the Claude plugin.
- Replaced the trigger-only protocol with positive and negative activation cases, workflow fixtures, deterministic contract tests, and a paired real-work pilot design.

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
