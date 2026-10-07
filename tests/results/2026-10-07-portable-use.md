# 0.7.2: portable use and English guidance

Work started 2026-10-06; release preparation 2026-10-07. Baseline: `f7c8df3`. The first normal fetch found remote `main` at `01d0a10`, with no divergent commits. Scope: practical development guidance, portable access and English built-in presentation. No new runtime, model experiment, global install or browser access.

## What changed

README now explains what the agent owns, which judgments stay with the user, and what completion must report. It supplies one clone step and two routes: copy the full skill into a project host directory, or explicitly ask an agent to read the checkout. New feature, focused repair, session resumption and review/handoff each have a short request and observable expectation. Quick creates no process files; a checkpoint is justified by resumption or stale-evidence risk. Python 3.10+ is optional-helper support, Node/npm only applies to the optional third-party installer, and HTML needs browser support.

The SKILL introduction expresses these responsibilities as actions. Built-in brief/text labels are English. Source data and quoted text remain untouched and escaped. The old three presentation snapshots/provenance and historical task evidence retain their language and bytes; their English guide explains their historical status and the availability of a public demo builder. No historical success, failure or scope is rewritten.

## Actual local validation

- Full repository validator and 58/58 regressions passed. These include the existing planted failures and known-green controls; no tests were added merely to count documentation changes.
- Main-thread smoke executed 18 commands against existing fixtures. Both README folder-install commands worked in paths containing spaces: 22 files and 21 internal links per host, preserving an existing installation on a repeated attempt. These are isolated copies, not global installs or host activation tests.
- Quick: the existing typo fixture changed only README; its declared tests passed and no process files were created.
- Feature: the existing invitation baseline failed the outcome evaluator; its existing reference solution passed. This is a deterministic replay, not a new agent implementation or independent generalization result.
- Resume/handoff: the shipped demo produced a real stale receipt. The installed helper detected it. After an actual byte comparison and targeted repair/revision, artifact readiness passed while the owner decision remained pending. The check correctly stayed at exit 1; no judgment was manufactured to make the task green.
- Three English views from the same brief shared observation `489f02157fd6dd7c8ade95267d8e45fc855fba74d35626a48f41dfbf6544ea7c`. Valid synthetic feedback neither mutated state nor authorized action; changing the source caused intake rejection.
- Claude manifest validation passed; both manifests declare 0.7.2. Codex registration itself was not exercised.

[Independent scoped review](2026-10-07-portable-independent.md) passed 17 affected tests and 18 separate actual commands. It additionally checked dangling-symlink refusal, both installed helpers, unchanged state/experience code and unchanged binding/feedback/JavaScript logic. Its source snapshot was taken before the final report/date/navigation wording; product files remained unchanged afterward.

Official [Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) was checked for `.agents/skills` and explicit `$` invocation. Official [Claude documentation](https://code.claude.com/docs/en/skills#where-skills-live) was checked for `.claude/skills`, folder `/gap` and plugin `/gap-skills:gap`. This source check was performed by the main thread, not attributed to the offline independent reviewer.

## Retained evidence and limits

Local ignored archive: `tests/results/2026-10-07-portable-use-evidence.tar.gz`, 22596 bytes, SHA256 `75644ec06169518a8f180d0a89b3dbfdcb08c45c5a2fef199f23fdd2d13bf41d`. It contains the actual main and independent command outputs, scripts and manifests; all nine archived files were extracted into a new directory and byte-checked. It is not distributed in GitHub and is not a portable runtime. The public tests and demo builder can be run from a normal checkout; the scripts in the archive retain their original audit paths.

No browser tool, alternate browser route, model API, natural skill activation or real human-effort measurement was used. A working folder and CLI prove local package availability, not automatic discovery, better task outcomes than a baseline, or saved review time. Existing independent task outcomes retain their original limits. Publishing and CI are checked separately against the final commit; use that commit's GitHub Actions result rather than treating these local checks as remote CI.
