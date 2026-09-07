# Initiative Intake Coverage

Use this reference throughout discovery to make the final request useful to an initiative queue. This is a coverage map, not a form to recite. Ask only questions whose answers can improve routing, evidence, scope, solution choice, ownership, or the next decision.

## Initiative fit

Classify the request as one of:

- `initiative-candidate`: significant non-standard change needing discovery, cross-functional work, investment, prioritization, or approval;
- `standard-change`: narrow work that fits an existing operational or delivery path;
- `duplicate-or-solved`: an existing process, system, initiative, or capability already addresses the need;
- `discovery-needed`: the problem may be material, but the evidence or ownership is not yet sufficient;
- `reframe`: the request is solution-first or combines separate problems;
- `do-not-pursue`: the process or change is unnecessary, unsupported, ownerless, or currently unacceptable.

The classification routes the request; it does not approve or reject organizational work.

When `reframe` and `discovery-needed` both appear applicable, classify the immediate routing need:

- use `reframe` when the proposed solution, scope, or combination of problems must be restated or separated before useful assessment;
- use `discovery-needed` when the problem and desired outcome are usable, but evidence, ownership, or current-state understanding is insufficient.

Record the secondary concern in the rationale. Do not use initiative fit as a substitute for `readiness`; they answer different questions.

## Coverage map

### Request identity and governance

Capture a concise initiative name, summary, requester, business owner, business areas, affected people, reach, initiative type, related initiatives or standard request paths, decision authority, and lifecycle context. Mark missing values explicitly.

### Problem, necessity, and evidence

Capture who has to do what, the resulting time, cost, risk, service, or human consequence, and the evidence source. Test what happens if the process stops or is radically reduced. Preserve baselines as supplied; never infer a metric from importance or urgency.

### Current manual process

Map the process from trigger to completion at enough depth for another person to follow it:

- sequence, actor, action, decision or rule;
- system or channel used at each step;
- information and knowledge consulted;
- manual entry, copying, checking, judgment, or approval;
- handoffs, queues, loops, rework, exceptions, escalation, and recovery;
- output, completion condition, current owner, and pain or failure at each material step.

Do not summarize a multi-system workflow as merely `manual`.

### Process diagram evidence gate

Treat the current process as successfully mapped for diagramming only when all of the following are known from supplied evidence:

- a trigger and completion condition;
- at least two ordered steps with an actor and action;
- every system referenced by a step is present in the systems inventory;
- the material handoffs and exceptions have been captured, including an explicit empty set when none apply.

When the gate passes, create a portable BPMN-style Mermaid swimlane diagram:

- use `flowchart LR`, start and end events, one labeled `subgraph` per actor, task rectangles, and diamonds for material decisions;
- give process steps stable node IDs `S1`, `S2`, and so on, matching `current_state.steps[].sequence`;
- show the normal path and supported material exception or rework loops without inventing undocumented branches;
- when a known decision or condition changes the next step, show that branch rather than drawing conditional work as if it always happens;
- when an exception or recovery path is known to exist but its steps are not known, leave it unmapped and state what must be confirmed;
- include the system or channel in each task label when known;
- keep confidential record content and sensitive data values out of labels;
- describe it as BPMN-style, not as standards-compliant BPMN 2.0 XML.

When the gate does not pass, do not infer the missing flow. Set the diagram status to `insufficient-evidence`, leave the source empty, list the unmapped elements, and create evidence tasks for material gaps. Use `not-applicable` only when there is no current process to map, such as a supported eliminate-or-stop case.

### Existing systems and information

For every material system, tool, spreadsheet, inbox, document store, database, or shadow tool, record:

- name or sanitized label, category, purpose, users, and owner;
- what enters it, what leaves it, and what information is collected or retrieved;
- which facts or records it is authoritative for;
- integrations, manual transfers, exports, access constraints, and current limitations.

Also map material information flows between systems. Distinguish a system of engagement from a source of truth.

### Knowledge landscape

For every material policy, procedure, article set, template, rule, decision guide, or expert practice, record:

- where it lives and what it is used for;
- whether it is `codified`, `partially-codified`, `tribal`, or `unclear`;
- owner, contributors, intended users, access, freshness, and review practice when known;
- contradictions, gaps, obsolete content, or reliance on individual memory.

Person-held knowledge is a discovery finding, not an instruction to scrape or publish private information.

### Scope and target state

Separate the desired outcome from the proposed solution. Record in-scope and out-of-scope work, required capabilities, functional requirements, non-functional constraints, human controls, transition, training, support, fallback, and adoption conditions. Do not turn initial discovery into detailed architecture or a full PRD.

### Value, priority, and measurement

Capture supported value levers, outcome narrative, saved-time use, current baseline, success measures, evidence window, urgency rationale, hard deadline, budget status, strategy linkage, and reach. Keep unsupported monetary value, ROI, targets, dates, and priority claims pending.

### Dependencies, risks, and ownership

Name system, data, team, security, privacy, legal, compliance, procurement, funding, release, adoption, vendor, and operational dependencies when material. Distinguish a known dependency from an unresolved risk. Include the full lifecycle ownership map for any technology path.

### Required solution assessment

Complete the solution ladder even when the requester proposes a specific tool. The final request must show which options are plausible, deferred, or rejected and why. Buying, configuring, integrating, automating, and custom building all carry implementation, transition, support, change, upgrade, and retirement work.

## Completion and submission readiness

The questionnaire is complete when every material coverage area is either supported, explicitly not applicable, or represented by an evidence task. Completion does not imply submission readiness.

`handoff.submission_ready` means there is enough information to send or route the request now. It does not mean every later discovery, assessment, or delivery task is complete.

Set it to `true` only when the receiving team can understand:

- the problem and necessary outcome;
- current workflow, systems, information, and knowledge landscape;
- affected people, owner, scope, evidence, value hypothesis, and constraints;
- required solution assessment and leading direction;
- dependencies, risks, lifecycle ownership, and the next decision.

When required organizational fields are unknown, the artifact can still be ready for a `discovery` ticket if the gaps and owners are explicit. Do not label it ready for initiative approval or implementation.

When `submission_ready` is `true`, keep `missing_for_submission` empty. Put work that happens after submission in evidence tasks or blocking conditions. When it is `false`, use `missing_for_submission` only for information needed before the request can be sent or routed. A `do-not-submit` disposition always has `submission_ready = false`; record the stop decision instead of preparing a ticket for submission.

## Portable ticket mapping

The JSON is vendor-neutral. Use `handoff.target_system` only when the destination and its field names are known:

- preserve the portable source path for every mapped value;
- use exact target field names and option values only from supplied or live metadata;
- leave mapping status `not-requested` or `pending` when the destination is unknown;
- never invent a project key, issue type, dropdown value, user ID, or custom-field ID;
- never create the ticket without a separate explicit request.
