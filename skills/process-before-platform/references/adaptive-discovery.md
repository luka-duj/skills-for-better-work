# Adaptive Discovery

Use this reference for the requester conversation. The goal is not to recite a form. It is to collect the smallest sufficient initiative context while making material gaps explicit.

## Conversation posture

- Assume the requester understands the work better than the skill does.
- Challenge the proposed solution without treating the requester as the problem.
- Explain briefly why a question matters when it may feel like resistance.
- Ask one primary question at a time. Use one immediate follow-up only when the answer contains a material ambiguity.
- During discovery rounds, do not output JSON, a draft decision packet, schema fragments, or the full handoff brief.
- Prefer a recent incident, observable workflow, document, or number over a general opinion.
- Accept `I do not know`. Turn it into an evidence task rather than pressing for a guess.
- Track the coverage map in `initiative-intake.md` internally. Do not repeatedly probe one branch while leaving current-state systems, information, knowledge, ownership, scope, value, or dependencies untouched.
- Do not ask for information already supplied. Combine tightly related details into one answerable primary question when that reduces needless rounds.

## Quick triage

Cover these slots adaptively; do not recite them as a questionnaire:

1. **Outcome and people:** Who needs a better outcome, what should improve, who owns it, and what would they notice?
2. **Current work and systems:** What happens from trigger to completion, who acts, which systems and information sources they use, what is manual, and where waiting, rework, or workarounds occur?
3. **Knowledge:** Which policies, procedures, articles, templates, or judgment guide the work; where do they live; and what remains person-held, disputed, stale, or uncodified?
4. **Observed problem:** What shows the process is broken? Capture frequency, volume, delay, error, cost, risk, service, or user consequence only when known.
5. **Proposed solution and scope:** What has been requested, why does it appear attractive, what is in or out of scope, and which assumption says it will solve the problem?
6. **Necessity and initiative fit:** What obligation or useful outcome requires the process, what happens if it stops, and why does this need initiative-level rather than standard-change handling?
7. **Value, priority, and constraints:** What baseline, measures, value hypothesis, saved-time use, reach, urgency, deadline, budget status, strategy link, dependencies, systems, data, security needs, or commitments constrain the decision?

After triage, give a short prose-only diagnosis before asking deeper questions:

- current readiness;
- strongest supported problem statement;
- leading direction or `insufficient-evidence`;
- the next two or three questions most likely to change that direction.

This diagnosis is conversational guidance, not a decision packet. Continue asking one primary question per turn. Produce artifacts only after every material coverage area has been answered, converted into an evidence task, marked not applicable, or explicitly deferred.

## Coverage-driven progression

After triage, choose the next question from the weakest material coverage area. A typical order is:

1. initiative fit, problem, necessity, and owner;
2. current manual workflow;
3. systems, information sources, data flows, and sources of truth;
4. codified and person-held knowledge;
5. scope, target outcome, users, requirements, and adoption;
6. evidence, baseline, measures, value, urgency, budget, and strategy;
7. dependencies, risks, and lifetime ownership;
8. required solution ladder and requester weights.

Change the order when earlier answers make another branch decision-critical. Before asking for scorecard weights, ensure the requester understands the initiative criteria being weighted and that the current workflow, systems, information, and knowledge landscape have been covered or explicitly left pending.

## Process necessity test

Distinguish:

- a legal, contractual, safety, financial-control, or customer obligation;
- a business outcome that remains necessary but could be achieved differently;
- an internal policy that may be changed by an accountable owner;
- a historical habit, workaround, duplicate control, or preference;
- an unknown that requires evidence.

Ask what fails if the whole process disappears. Then ask which steps, approvals, data captures, reports, and variations can disappear independently.

Do not recommend elimination when the obligation is unclear. Record the obligation as an evidence task with the person or source that can confirm it.

## Deeper discovery triggers

### Process redesign

Deepen when definitions conflict, work varies by person, approvals lack policy, exceptions dominate, or no owner can decide the standard. Map:

- trigger and completion condition;
- actors, roles, and decision rights;
- normal path and material exceptions;
- inputs, outputs, systems, and source of truth;
- handoffs, queues, loops, rework, and failure recovery;
- rules that are explicit, undocumented, disputed, or discretionary;
- steps to remove, combine, clarify, standardize, or leave deliberately flexible.

### Technology assessment

Deepen only after the problem and process purpose are legible. Capture:

- capabilities rather than screens or named features;
- required versus preferred behavior;
- data sensitivity and retention;
- identity, access, audit, integration, performance, availability, and support needs;
- scale, geography, language, accessibility, and procurement constraints;
- transition, training, incentives, trust, fallback, and human override.

### Process-and-tool co-evolution

An exception to process-first may be justified when:

- the new process depends on a capability that cannot be simulated credibly by hand;
- real interaction is needed to learn the correct rules or user behavior;
- a legacy constraint prevents meaningful process testing;
- the experiment is bounded and reversible.

Require a named user, one real job, a limited scope, baseline, evidence window, owner, quality/risk guardrails, fallback, and stop/adapt/expand decision.

## Evidence tasks

Each material unknown becomes a task with:

- the question or claim to resolve;
- why it can change the decision;
- the smallest credible action or source;
- owner, if known;
- completion evidence;
- which direction or scorecard criterion it affects.

Examples include observing three recent cases, checking the current policy owner, extracting volume from a system, testing an existing form capability, or asking Security about a named data path. Numbers are examples of task shapes, not universal minimums.
