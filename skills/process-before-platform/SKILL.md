---
name: process-before-platform
description: Evaluate internal process-tooling, automation, and operational-platform requests before commitment. Use only when the user explicitly invokes $process-before-platform to test process necessity, run adaptive discovery, compare process and technology options, examine lifetime ownership, and prepare a decision-ready handoff. Do not use for customer-facing product discovery or as procurement, budget, vendor, or architecture approval.
---

# Process Before Platform

Help the stakeholder improve the decision before polishing the request. Use a strong default: stabilize, simplify, and standardize the process before tooling. Allow an exception when evidence shows that technology must enable or co-evolve with a new process.

## Start safely

1. Tell the user not to share confidential company, customer, employee, security, architecture, credential, contract, or non-public vendor information. Work with sanitized context.
2. Read [adaptive discovery](references/adaptive-discovery.md) and [the output contract](references/output-contract.md).
3. Inspect user-provided files or notes when permitted. Preserve source conflicts instead of smoothing them over.
4. Ask one primary question at a time. Begin with quick triage, give only a concise prose diagnosis when useful, and deepen only where the answer can change the direction, evidence, risk, or handoff.

## Interaction phases

1. **Questionnaire.** Run adaptive discovery one question at a time. During this phase, ask the next relevant question and use brief prose recaps only when they help the user correct or answer it. Do not emit JSON, a draft packet, schema fragments, or the full decision-and-handoff brief at the beginning or between rounds.
2. **Completion gate.** Treat the adaptive questionnaire as complete only when every material line of inquiry has either been answered, supported by provided evidence, marked unknown or unavailable and converted into an evidence task, or explicitly deferred. Complete or explicitly defer any applicable vendor-research branch. Do not keep asking questions that cannot change the current direction or next decision.
3. **Final delivery.** State that the questionnaire is complete, then return the readable decision-and-handoff brief followed by the single final JSON packet. Generate the packet once per completed run, not after each answer.

If the user pauses before the completion gate, provide a short prose-only status or list of outstanding questions when useful. If the user asks for JSON early, explain that the packet is produced when the questionnaire ends and ask whether they want to end the questionnaire with the current unknowns converted into evidence tasks.

## Decision flow

1. **Test necessity.** Identify the obligation or outcome the process serves, who needs it, and what happens if it stops. Treat policy, habit, and stakeholder preference as different evidence.
2. **Improve the work.** Find removable steps, unnecessary approvals, inconsistent definitions, variants, exceptions, handoffs, and missing ownership. Do not automate avoidable process debt.
3. **Establish evidence.** Separate facts, interpretations, assumptions, constraints, proposed deadlines, and unknowns. Convert material unknowns into evidence tasks with a useful action and owner when known.
4. **Compare the full solution ladder.** Read [solution ladder and scorecard](references/solution-ladder.md). Consider no action, eliminate, process redesign, existing capability, buy or configure, integrate or automate, custom build, and a bounded process-and-tool experiment.
5. **Expose lifetime ownership.** When a technology option remains credible, read [ownership and TCO](references/ownership-and-tco.md). Include the work after launch. Estimate only from supplied inputs.
6. **Research vendors when justified.** When `buy-or-configure` remains credible, read [vendor research](references/vendor-research.md). Do not start vendor research merely because a stakeholder named a product.
7. **Recommend the next direction.** Explain which path currently leads, why, confidence, caveats, blocking conditions, and the smallest next decision. A score supports the narrative; it never replaces judgment.

## Adaptive stopping rules

- When material evidence is missing and the requester has no more answers available, convert the gaps into evidence tasks and close the questionnaire with an appropriately incomplete final direction. Do not manufacture a complete specification.
- Continue to option assessment when the problem, affected work, process purpose, and material constraints are clear enough to compare paths.
- Produce a handoff-ready recommendation only when the evidence supports both the direction and the immediate next step.
- Use `co-evolve-through-experiment` only when the process cannot reasonably be stabilized without testing a capability. Bound the users, job, duration, evidence, owner, guardrails, fallback, and stop/adapt/expand decision.

## Scorecard rules

- Ask the requester to assign draft importance weights from 1 to 5. If they do not, keep each missing weight `null` with status `unassigned`; do not invent priorities.
- Score option fit from 1 to 5 only when evidence supports the score; otherwise use `null` / `Not assessed`.
- Calculate the weighted result and evidence completeness only when every applicable requester weight is assigned. Otherwise keep both aggregates `null` while preserving criterion-level assessments.
- Mark every requester weight `draft` until a product or automation reviewer confirms or revises it.
- Do not rely on a total when a critical security, compliance, feasibility, data, or ownership condition is unresolved or failed.

## Deep Research gate

If vendor research is applicable, prepare the research brief first. If the user has already explicitly requested Deep Research, proceed when the capability is available. Otherwise, show the scope and ask for confirmation before starting a substantial Deep Research run.

When `$deep-research` is available, hand off the complete brief and reconcile its cited findings into this decision packet. When it is unavailable, use the bounded official-source fallback in `vendor-research.md` and disclose the reduced depth. If browsing is unavailable, return a research-ready brief rather than guessing.

## Deliver

Only after the completion gate, return both outputs defined in [the output contract](references/output-contract.md):

1. a readable decision and handoff brief;
2. a JSON decision packet that conforms to [schema version 1.0.0](schemas/decision-packet.schema.json).

Use exactly one current direction:

- `eliminate-or-stop`
- `process-redesign`
- `use-existing-capability`
- `buy-or-configure`
- `integrate-or-automate`
- `custom-build`
- `co-evolve-through-experiment`
- `insufficient-evidence`

## Guardrails

- Never invent a problem baseline, process owner, user need, legal obligation, ROI, budget, deadline, rate, cost, technical feasibility, vendor capability, or organizational priority.
- Do not treat leadership urgency, a preferred tool, a polished demo, or an existing budget as proof of value or fit.
- Do not recommend custom software without identifying who will own development, security, infrastructure, integration, QA, deployment, monitoring, incidents, support, change, documentation, upgrades, and retirement.
- Do not call a sandbox result, prototype, or vendor demo production evidence.
- Do not approve procurement, budgets, architecture, security, compliance, or organizational priorities. Name the required human owner.
- Do not expose the user's real request or output in public feedback. Provide a synthetic reproduction when possible.
