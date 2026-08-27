# Gap behavioral validation protocol

The objective is not to prove universal superiority. It is to detect packaging failures, wrong routing, missed high-cost behavior, and unnecessary ceremony before real adoption.

## Test layers

### L0: deterministic repository contract

`python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v` verify:

- exactly one installed skill named `gap`;
- all disclosed references and assets exist;
- Claude and Codex manifests describe the same base version and single skill;
- Codex invocation metadata is present;
- legacy skill entry points are absent;
- the three routes, read-only adoption boundary, artifact lifetimes, separate review axes, protected production gate, and evidence limits remain represented.

Failure verdict: fix before release.

### L1: activation precision and recall

Run the cases in `tests/activation-cases.json` in fresh Claude and Codex sessions without naming `gap`.

- Positive recall target: at least 8/10 complex/risky cases invoke the skill.
- Negative precision target: at least 9/10 simple cases remain on the normal path.
- No case may mutate repository configuration merely because the skill activated.

Record model, harness version, skill commit, result, and evidence. A trigger result is harness/model-specific, not a permanent property of the text.

Failure verdict: low recall → sharpen the description; low precision → narrow it. Do not add body text to solve a description-level routing failure.

### L2: workflow behavior

Run the fixtures in `tests/workflow-cases.json` in disposable repositories. A fresh evaluator grades observable actions and artifacts, not preferred wording.

- Quick must finish without process files.
- Standard must resolve material uncertainty, preserve assumptions, verify, and review both axes.
- Governed must create durable linked artifacts and stop before the irreversible action without named approval.
- Adoption must inspect before proposing and must not mutate unapproved harness files.
- Retrospective must use observed repeated evidence and propose at most one reversible change.

Failure verdict: any critical invariant missed → fix and rerun that case plus the nearest negative case.

### L3: paired real-work pilot

Alternate comparable real tasks with and without `gap`. Pre-register:

- task success against acceptance criteria;
- rework after first completion;
- material surprises found before implementation, before merge, and after merge;
- elapsed time and tool cost;
- user interventions;
- false ceremony;
- component retention after 10–20 changes.

Report dimensions separately. Do not combine them into one score that hides a serious failure.

Failure verdict: if the workflow does not reduce costly misses enough to repay its friction, narrow or remove the failing branch. Retention is evidence, not the only score.

## Evaluator independence

The implementation session does not grade its own behavioral run. Use a fresh context, another supported harness/model, or a user-held checklist. Keep planted constraints out of the implementation prompt when the test is meant to measure discovery.
