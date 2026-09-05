---
name: process-before-platform
description: Guide structured initial discovery for internal process, tooling, automation, and operational-platform requests before they enter an initiative queue. Use only when the user explicitly invokes $process-before-platform to test initiative fit and process necessity, document current work, systems, information and knowledge sources, compare the required solution ladder including buy versus build, expose lifetime ownership, and create portable ticket-ready Markdown and JSON artifacts. Do not use for customer-facing product discovery or as procurement, budget, vendor, architecture, or initiative approval.
---

# Process Before Platform

Help the requester do enough structured initial discovery that an initiative, product, automation, or business-analysis team can understand and route the request without reconstructing its basic context. Use a strong default: stabilize, simplify, and standardize the process before tooling. Allow an exception when evidence shows that technology must enable or co-evolve with a new process.

## Start safely

1. Tell the user not to share confidential company, customer, employee, security, architecture, credential, contract, or non-public vendor information. Work with sanitized context.
2. Read [adaptive discovery](references/adaptive-discovery.md), [initiative intake coverage](references/initiative-intake.md), and [the output contract](references/output-contract.md).
3. Inspect user-provided files or notes when permitted. Preserve source conflicts instead of smoothing them over.
4. Ask one primary question at a time. Begin with quick triage, give only a concise prose diagnosis when useful, and deepen only where the answer can change the direction, evidence, risk, or handoff.

## Interaction phases

1. **Questionnaire.** Run adaptive discovery one question at a time. During this phase, ask the next relevant question and use brief prose recaps only when they help the user correct or answer it. Do not emit JSON, a draft packet, schema fragments, or the full decision-and-handoff brief at the beginning or between rounds.
2. **Completion gate.** Use the coverage and readiness rules in `initiative-intake.md`. Treat the adaptive questionnaire as complete only when every material line of inquiry has either been answered, supported by provided evidence, marked unknown or unavailable and converted into an evidence task, or explicitly deferred. Complete or explicitly defer any applicable vendor-research branch. Do not keep asking questions that cannot change initiative routing, the solution direction, or the next decision.
3. **Final delivery.** State that the questionnaire is complete, then create one ticket-ready Markdown file and one semantically aligned JSON file. Generate them once per completed run, not after each answer. Link both files in the response; do not paste the full JSON unless the user asks.

If the user pauses before the completion gate, provide a short prose-only status or list of outstanding questions when useful. If the user asks for JSON early, explain that the packet is produced when the questionnaire ends and ask whether they want to end the questionnaire with the current unknowns converted into evidence tasks.

## Decision flow

1. **Test initiative fit.** Decide whether this is an initiative candidate, standard change, duplicate or already solved request, discovery-needed request, reframe, or do-not-pursue case. Do not inflate narrow work into an initiative.
2. **Test necessity.** Identify the obligation or outcome the process serves, who needs it, and what happens if it stops. Treat policy, habit, and stakeholder preference as different evidence.
3. **Map the current state.** Capture the manual process from trigger to completion, actors, decisions, exceptions, handoffs, workarounds, and failure recovery. Inventory existing systems, what each is used for, information collected or retrieved from each, transfers and integrations, ownership, and sources of truth. Inventory codified, partially codified, conflicting, stale, inaccessible, and person-held knowledge. When the process map meets the evidence gate in `initiative-intake.md`, generate a BPMN-style Mermaid swimlane diagram; otherwise record why a trustworthy diagram cannot yet be produced.
4. **Improve the work.** Find removable steps, unnecessary approvals, inconsistent definitions, variants, exceptions, handoffs, and missing ownership. Do not automate avoidable process debt.
5. **Establish evidence and value.** Separate facts, interpretations, assumptions, constraints, proposed deadlines, and unknowns. Capture users, scope, outcomes, baseline, measures, reach, strategy linkage, urgency, budget status, dependencies, risks, adoption, and saved-time use only when supported. Convert material unknowns into evidence tasks with a useful action and owner when known.
6. **Compare the full solution ladder.** This step is required. Read [solution ladder and scorecard](references/solution-ladder.md). Consider no action, eliminate, process redesign, existing capability, buy or configure, integrate or automate, custom build, and a bounded process-and-tool experiment.
7. **Expose lifetime ownership.** When a technology option remains credible, read [ownership and TCO](references/ownership-and-tco.md). Include the work after launch. Estimate only from supplied inputs.
8. **Research vendors when justified.** When `buy-or-configure` remains credible, read [vendor research](references/vendor-research.md). Do not start vendor research merely because a stakeholder named a product.
9. **Recommend and route.** Explain the leading direction, confidence, caveats, blocking conditions, initiative-fit classification, submission readiness, smallest next decision, and suggested downstream workflow. A score supports the narrative; it never replaces judgment.

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

When `$deep-research` is available, hand off the complete brief and reconcile its cited findings into the initiative packet. When it is unavailable, use the bounded official-source fallback in `vendor-research.md` and disclose the reduced depth. If browsing is unavailable, preserve a research-ready brief in the final artifacts rather than guessing.

## Deliver

Only after the completion gate, create both outputs defined in [the output contract](references/output-contract.md):

1. a ticket-ready Markdown initiative request;
2. a vendor-neutral JSON initiative packet that conforms to [schema version 2.1.0](schemas/initiative-request.schema.json).

Embed a BPMN-style Mermaid diagram in the Markdown and store the exact source in `process_diagram.source` when the current process is mapped successfully. Do not claim BPMN 2.0 conformance or generate a diagram from guessed steps.

Default to sibling files under `<current-project>/output/process-before-platform/` named `<YYYY-MM-DD>-<initiative-slug>.md` and `<YYYY-MM-DD>-<initiative-slug>.json`. If there is no clear writable project root, ask for a destination near the end. Never overwrite an existing artifact; add a time suffix when needed. Never create or modify a ticket, project, or remote system unless the user separately requests it.

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
