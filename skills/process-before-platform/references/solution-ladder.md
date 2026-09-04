# Solution Ladder and Scorecard

Use this reference after triage. Compare only plausible options, but always consider the process and existing-capability paths before procurement or custom development.

## Direction definitions

- `eliminate-or-stop`: either eliminate an unnecessary process, or stop the proposed change while a necessary process continues. The rationale and handoff must state which disposition applies.
- `process-redesign`: the underlying outcome matters, but avoidable complexity, disputed rules, unstable handoffs, or missing ownership should be addressed before tooling.
- `use-existing-capability`: an owned tool or service may meet the need through current functionality or modest configuration.
- `buy-or-configure`: the capability is sufficiently standard for vendor evaluation and the expected fit may outweigh procurement, configuration, integration, and vendor-lifecycle costs.
- `integrate-or-automate`: stable work can be improved by connecting existing systems or automating bounded steps without creating a new standalone product.
- `custom-build`: the process is necessary and sufficiently understood, the capability is materially differentiated, and an accountable team can own the full software lifecycle.
- `co-evolve-through-experiment`: process and technology must be tested together through a bounded, reversible experiment.
- `insufficient-evidence`: the current information cannot support a responsible direction.

These values express the current leading direction, not an organizational approval.

Treat `no action` as an option within `eliminate-or-stop`: it means stopping the proposed change, not silently eliminating the underlying process. Always record the exact disposition.

## Default option criteria

Use only criteria material to the request:

1. necessary outcome and user value;
2. process fit and exception handling;
3. capability fit;
4. time to operation;
5. one-time effort and cost;
6. lifetime cost and internal capacity;
7. data, security, privacy, legal, and compliance fit;
8. integration and architecture fit;
9. maintainability, support, and operational ownership;
10. adoption, transition, training, fallback, and human impact;
11. reversibility, portability, vendor dependency, and exit cost.

Add or remove criteria only when the request makes them material. Record the reason.

## Weights and scores

Requester importance weight:

- `1`: minor consideration;
- `2`: useful but negotiable;
- `3`: material;
- `4`: highly important;
- `5`: decision-critical.

Option fit score:

- `1`: conflicts with the need or has a serious known failure;
- `2`: major mismatch or burden;
- `3`: mixed fit or important uncertainty;
- `4`: good fit with manageable limits;
- `5`: strong fit supported by relevant evidence;
- `null`: not assessed.

Every score needs a short rationale and confidence of `low`, `medium`, or `high`. A vendor claim alone cannot support `high` confidence for operational fit.

Use:

`weighted score = sum(weight × assessed fit) / sum(weight × 5 for assessed criteria) × 100`

Use:

`evidence completeness = sum(weights for assessed criteria) / sum(weights for all applicable criteria) × 100`

Round displayed percentages to one decimal place. Keep full precision in calculations when possible.

## Human ownership

- The requester supplies draft weights. A missing weight remains `null` with status `unassigned`.
- Mark weight status `requester-draft` until a product or automation reviewer confirms or revises it.
- Preserve both requester and reviewer values when a reviewer changes a weight.
- Do not calculate a weighted score or evidence-completeness percentage until all applicable weights are assigned; keep both aggregates `null`.
- A higher score does not override a failed or unresolved critical condition.
- Withhold a ranked recommendation when missing material evidence could reasonably reverse the order. Return the current direction and evidence tasks instead.

## Critical conditions

Treat a condition as critical only when failure makes an option unsafe, unlawful, infeasible, unsupported, or ownerless. Record:

- criterion;
- status: `pass`, `fail`, or `unresolved`;
- evidence and owner;
- consequence for the option.

Do not use critical gates to disguise a preference as a requirement.
