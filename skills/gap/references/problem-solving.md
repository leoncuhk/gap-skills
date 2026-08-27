# Problem solving

Use the relevant branch only. These are working methods inside the same `gap` workflow, not separate user-facing processes.

## Hard bugs and flaky failures

Build a tight feedback loop before constructing theories. The loop is one agent-runnable command or action that has already exposed the specific symptom, is as deterministic and fast as practical, and would go red again if the bug returned.

Improve weak reproduction by pinning time and randomness, isolating filesystem/network state, replaying a trace, comparing known-good behavior, or increasing a flake's reproduction rate. A useful 50% reproduction loop beats an unactionable 1% anecdote.

After the loop exists:

1. generate 3–5 ranked, falsifiable hypotheses;
2. state the observation each predicts;
3. change one variable per probe;
4. fix the proven mechanism, not the nearest symptom;
5. retain the loop as a regression check;
6. remove temporary instrumentation.

If the code offers no seam where the behavior can be observed or controlled, record that architectural limitation as a finding.

## Incoming issue triage

Triage raw reports; do not re-triage tickets already produced from an accepted spec. Establish expected versus actual behavior, reproduction evidence, severity/impact, duplicates, missing information, and whether the request is a bug, feature, support question, or policy decision. Turn accepted work into an agent-ready issue with observable acceptance criteria and relevant constraints.

Do not let classification become implementation. The output is a trustworthy decision and prepared work item.

## Architecture and domain language

Prefer deep modules: a small interface that hides substantial behavior and decisions. Evaluate a proposed module with:

- **Deletion test**: if removed, does its complexity disappear or reappear at every caller?
- **Leverage**: how much behavior does each unit of interface knowledge unlock?
- **Locality**: are related decisions and changes kept together?
- **Real seam**: do at least two implementations or consumers actually vary across it? One adapter alone may be a speculative boundary.

Use the project's domain terms consistently. When one word carries several meanings, or several words mean the same thing, resolve the model with the user and record hard-to-reverse decisions in the project's durable convention.

Make the change easy, then make the easy change. Prefactoring is justified when it reduces the target change's risk and remains independently verifiable; it is not permission for unrelated cleanup.

## Large investigations and context boundaries

Keep discovery, decisions, and specification in one coherent context while they still depend on each other. Once work is split into self-contained tickets, use a fresh context per ticket so implementation pressure does not carry irrelevant history.

Use a handoff only when crossing a real boundary: another person, harness, repository, worktree, or context that cannot inherit the needed state. A handoff names the objective, decisions, evidence, current state, next action, and unresolved risks; it is not a transcript dump.

For efforts too uncertain to specify in one session, maintain a map of decision questions. Resolve one decision at a time until the destination can be expressed as a spec, then switch to planning and delivery.

## Merge conflicts

Treat a conflict as two sets of intent, not competing text hunks. Recover each side's purpose from commits, tests, and surrounding code; choose or synthesize behavior that preserves accepted intent; run the nearest tests and the full relevant checks. Never resolve mechanically when both sides changed behavior.
