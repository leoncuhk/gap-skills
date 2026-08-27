# Discovery

Use discovery to remove consequential uncertainty before implementation, not to turn every request into an interview.

## Build the decision frontier

First read the request, relevant repository instructions, nearby code, history, tests, and prior decisions. Separate:

- **Facts** the environment can answer: inspect them yourself.
- **Decisions** whose alternatives materially change the result: ask the user.
- **Taste** the user can recognize more easily than describe: show contrasting artifacts.
- **Suspected blind spots**: inspect landmines, hidden constraints, prior art, and what competent work looks like here.

Map decisions by dependency. Ask the whole current frontier in one concise round: only independent questions whose prerequisites are settled. Give options, the consequence of each, and a recommended default. Prefer at most five blocking decisions per round; when the user delegates a choice, take the most reversible reasonable default and record it as an assumption.

Stop asking when the remaining uncertainty is cheaper and safe to discover during implementation. High-risk, irreversible, security, data, cost, and user-promise decisions never silently become assumptions.

## Taste and prototypes

Ask first whether a suitable reference already exists. If not, create 3–5 cheap variations that differ on one meaningful axis while holding the rest stable. Make each variation test a different belief, not a cosmetic shade of the same idea.

The output is the decision learned from the reaction, for example: “The user rejected dense dashboards; scanability outranks information density.” Prototypes are disposable unless the user separately approves production use.

## References as specifications

When the user says “like this,” inspect the reference and summarize:

- behavior and guarantees;
- deliberate versus incidental choices;
- edge cases and failure modes;
- what must change for the target stack;
- licensing limits on copying.

Have the user confirm the semantics when a misreading would materially change the build. Reimplement behavior using the target project's conventions; do not transliterate syntax.

## Intent output

For Standard or Governed work, capture:

- problem and affected users;
- desired observable outcome;
- constraints and non-goals;
- decisions and their reasons;
- assumptions with reversal cost and pivot signals;
- open questions, owner, and next resolver;
- evidence consulted.

Use the existing tracker when it is authoritative. Otherwise use [the intent asset](../assets/intent.md). Discovery is complete when the remaining uncertainty is explicitly owned and the next step can proceed without inventing a consequential answer.
