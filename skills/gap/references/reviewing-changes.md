# Reviewing changes

Review a fixed change against its accepted intent and engineering constraints. A review request is read-only unless the user also asks for fixes.

A material standalone review is Standard unless its production, data, security, compliance, or external-action risk requires Governed. State the selected path once. Treat the repository root as the instruction-discovery boundary; do not search parent or sibling directories.

## Establish the comparison

Resolve the fixed point before judging code:

1. use the commit, branch, tag, merge-base, PR, or working-tree scope named by the user;
2. when none is named, infer the narrowest defensible comparison from the repository and state it;
3. verify that the reference resolves and the diff is non-empty;
4. record the commits and changed files included.

Find the intent/spec from an explicit user reference, linked issue or commit, branch-matched project document, or the accepted conversation. Find engineering constraints in repository instructions, contribution/coding standards, architecture decisions, tests, and operational policy. If a source is missing, label that axis limited instead of inventing it.

Review the selected diff, not the whole repository. Report a pre-existing problem only when the change introduces, worsens, or relies on it.

## Keep two axes independent

### Intent/spec

Look for required behavior that is missing or partial, behavior implemented incorrectly, unrequested behavior or public-surface change, and violated constraints or non-goals. Cite the controlling requirement for each finding.

### Engineering

Look for correctness, security/privacy, compatibility, data and operational risk; inadequate or weakened verification; unnecessary scope, abstraction, or configuration; and maintainability problems at changed seams. Repository rules override general heuristics. Skip style or facts already enforced reliably by tools.

Do not merge or rerank the axes. A sound implementation of the wrong requirement and a faithful implementation that damages the codebase are different failures.

## Independence and action

For material work, use separate reviewer contexts for the two axes when available and give both the same fixed diff and relevant sources. Attempt unavailable reviewer infrastructure once. Then:

- Standard may continue with an explicitly labeled self-review and an independence limitation;
- Governed work that requires independent review remains incomplete until that review exists.

Review-only work does not modify files, post comments, approve, merge, or release unless the user requested that action. In delivery work, repair authorized blocking findings, rerun affected verification, and review the new diff; suggestions do not expand scope.

## Findings and completion

Each finding names its axis, impact, exact location, source/evidence, and concrete correction. Use blocking only when the accepted outcome, safety, compatibility, or required policy would fail; keep judgment calls labeled as such.

If an axis has no findings, state what sources and checks were reviewed and what they cannot establish. Review is complete when both axes have a separate verdict, blocking findings are resolved or explicitly owned, verification limits are visible, and the independence status is truthful.
