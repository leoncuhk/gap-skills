# Adoption

Use this branch only when the user asks to install, configure, or assess the workflow for a project.

## Inspect first

Read-only inventory:

- repository instructions and skill/plugin locations;
- build, test, lint, typecheck, and run commands from their real configuration;
- CI, branch protection evidence, review ownership, deployment path, and monitoring;
- current issue/spec/ADR conventions and source-of-truth systems;
- secrets, production, data, migration, and compliance exposure;
- recurring agent failures already documented.

Do not create a test framework, initialize git, rewrite project instructions, or install hooks during inspection.

## Propose the project profile

Return a compact adoption report:

1. default task path: Quick, Standard, or Governed;
2. existing capabilities to reuse;
3. missing checks or controls, ranked by failure cost;
4. exact files/settings that would change;
5. verification and rollback for each proposed change;
6. components deliberately not installed.

Apply only the approved items.

## Minimal useful adoption

Prefer this order:

1. one reliable project verification command;
2. concise repository guidance containing only non-discoverable conventions and navigation pointers;
3. one repository-scoped installation of this `gap` skill;
4. a review rule that compares change evidence with intent;
5. durable artifacts and approvals only for risks that require them;
6. agent-configuration evals after real tasks exist to turn into cases.

Fast local feedback may use hooks. Full checks belong before completion and in CI. Protected actions belong at external service or CI boundaries.

## Claude and Codex packaging

The workflow is shared; installation and controls are platform-specific:

- Claude Code discovers its supported skill/plugin locations and uses Claude settings/hooks.
- Codex discovers repository skills under `.agents/skills` and user skills under `$HOME/.agents/skills`; `agents/openai.yaml` controls optional UI metadata and implicit invocation.

Never copy a Claude settings file into Codex or claim equivalent enforcement without testing the target harness.

## Adoption verification

Test both discovery directions:

- positive cases where complex/risky work should invoke `gap`;
- negative cases where a simple edit or one-lookup question should not.

Then run at least one realistic Quick, Standard, and Governed scenario against a disposable fixture. Measure task success, caught issues, false ceremony, time/tool cost, and retained use. Structure validation alone does not establish workflow value.
