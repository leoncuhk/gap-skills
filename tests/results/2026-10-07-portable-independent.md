# 0.7.2 English guidance and portability: independent scoped review

Verdict: **Pass within the requested diff; no blocking finding.** Baseline is `f7c8df393f7034ca9f2a7788e23e6886ff6f3725`. Reviewed the current working-tree README, SKILL introduction, two renderer files, adjusted assertion, manifests/changelog and current example guide. No repository edits, new solver, network, browser or global installation were performed.

The practical guide now supplies a usable division of responsibility, two explicit local-use routes, four ordinary development requests, update/version behavior and completion expectations. It distinguishes a registered skill from asking an agent to read a checkout, and warns that a laptop path is not automatically visible to a remote agent. Copied installations do not silently track updates. It does not promise saved time, automatic learning, a general diagram engine or host-independent runtime.

The README correctly distinguishes Codex `$gap`, Claude skill-folder `/gap` and Claude plugin `/gap-skills:gap`. The manifests remain one `gap` skill and both declare 0.7.2. This review establishes folder layout and manifest validity; it did not launch a model to verify discovery or slash-command registration, nor fetch the linked official pages. Natural activation remains host/model-dependent as the README states.

## Actual checks

- Copied the current working tree to `package/` (not an archive of the older HEAD).
- Repository validator passed: 1 skill, 9 references, 7 assets, 2 manifests.
- Ran only affected test modules: `test_brief.py` 8/8 and `test_review_view.py` 9/9. The complete 58-test suite was not repeated.
- `claude plugin validate <copied-package>` passed.
- Executed the README's POSIX installation block for both `.agents/skills/gap` and `.claude/skills/gap` in project paths containing spaces. Each installed folder matched all 22 source files. Second execution preserved the existing installation; dangling destination symlinks were also refused without replacement.
- Both copied folders actually executed `init`, expected-incomplete `check`, HTML `view` and detailed-text `view` without repository imports. All 21 internal Markdown links remain within the installed folder and exist.
- 18 actual commands satisfied their expected exit codes. Full command arguments/stdout/stderr are in `result.json`; compact evidence is in `receipt.json`.

## Translation and scope

The changed strings preserve the original meanings: stale sources require rechecking; source facts, inference and proposal remain distinct; before/after/differences and owner/deferral are not collapsed; feedback still neither approves nor executes an action. Original task text is interpolated unchanged and remains escaped in HTML. The test keeps its Chinese source fixture and changes only the expected built-in stale warning.

Verified byte identity against HEAD for checkpoint.py and experience.py. Verified unchanged ASTs for brief `_text`/`load_brief` and view `evidence_index`/`render_html`/`validate_feedback`. Therefore the changed code is confined to intended presentation labels; state, citations, observation binding, feedback validation, HTML structure/JavaScript and experience rules are unchanged. Source-rendering behavior is also covered by the 17 affected tests. This is not a claim that output bytes are identical: labels intentionally changed.

The existing `review.html`, `review.txt`, `review-details.txt` and `provenance.json` presentation snapshots remain byte-identical to HEAD. Their English README explicitly identifies them as old Chinese snapshots, distinguishes the public demo builder from the ignored original experiment bundle, and retains browser/human-comprehension limits.

At inspection, `tests/results/2026-10-06-portable-use.md` explicitly remained a draft awaiting execution receipts. Fill that section with actual smoke results before publication; do not turn this review into evidence for browser QA, actual natural activation, external documentation verification or comparative benefit. Push authorization, remote concurrency and sensitive-file scanning remain the main thread's separate release work.

## Evidence identities

- 22-file skill manifest SHA256: `d959c1e4f611686d0bbdee198fad1153b776b2f496f3f05aa16fcb380109273b`. Algorithm: SHA256 of path-sorted `{path, sha256, bytes}` rows, serialized with `json.dumps(rows, sort_keys=True, separators=(',', ':'))`.
- `manifest.json` SHA256: `33f61baf455929e93e8e02ac9e70d77eca18822c7b65fe29898449c9625abf92`.
- `result.json` SHA256: `0792aa66650e1388569c532572829dd22ed0ffb73ef0606c66f675815488320d`.
- `receipt.json` SHA256: `4f88911bc3b99dcee42bf0e3aba28d35e7779d1d583c30d855227350d83329a6`.

Independent intent-fit verdict: pass for practical English usage guidance with explicit boundaries. Independent engineering verdict: pass for this presentation/documentation diff and the exercised local entry points. No browser, model, network or global host setup result is implied.
