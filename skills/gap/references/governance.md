# Governance

Governance controls consequential handoffs; it does not prescribe ceremony for ordinary development.

## Name the source of truth

For intent, spec, plan, review, approval, release, and incident records, choose exactly one authority:

- repository artifacts;
- the existing tracker/change system;
- a linked transition where each side carries the other's stable identifier.

Working copies are not competing authorities.

## Enforcement levels

Classify every important rule:

| Level | Suitable for | Examples |
|---|---|---|
| Guidance | Judgment and local conventions | design principles, review heuristics |
| Automated check | Deterministic, repeatable facts | tests, lint, schema checks, secret scanning |
| Protected gate | Actions that must resist bypass | protected CI, branch rules, managed permissions, deployment service authorization |

Local hooks improve feedback but are not protected gates unless the platform prevents users and agents from disabling them. Maintain a rule-to-enforcement table for governed projects; an alleged hard rule with only prose is an acknowledged control gap.

## Approval gates

Name the owner and evidence required at each applicable transition:

- intent accepted before design;
- spec accepted before governed implementation planning;
- plan accepted before governed implementation;
- independent review and CI before merge;
- explicit release authorization before production or irreversible external action.

In a solo project, a pause/checklist may still help, but it is not separation of duties. Record that limitation instead of calling self-approval independent governance.

## Deployment

The agent may prepare a release, verification evidence, rollback plan, and exact proposed operation. It does not perform a production, migration, destructive, financial, or externally visible action without fresh explicit authorization.

Enforce production authorization at the real deployment interface or protected CI/service boundary. Do not treat shell-command substring matching as a security boundary.

## Continuous evaluation

Separate:

- deterministic product checks;
- agent-configuration evaluations for instructions, skills, and tools;
- human or validated-judge evaluations for qualities that cannot be reduced to exit codes.

Report each dimension independently. Add real failures as regression cases. A combined pass rate must not hide a failing high-risk dimension.

## Maintain

Monitoring or an incident starts with deterministic detection and read-only diagnosis. Record evidence, confidence, affected users, mitigation, and the decision owner. Material fixes re-enter the workflow as a new intent; small safe fixes still pass the applicable review and release gate.
