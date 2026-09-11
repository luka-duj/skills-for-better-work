# Synthetic Walkthrough: Approval Portal Request

This example is invented. It is not derived from a real company, customer, system, or project.

## Initial request

> We need a custom approval portal. Four departments submit roughly 20–40 requests each month through email and team chat. A coordinator manually records status in a shared tracker, but approvers still lose track of requests and teams use different templates and routes. Policy pages vary by department, while coordinators and approvers also rely on experience that is not written down. Nobody owns the full process. Our work-management suite may support forms and approvals, but we have not assessed it. We want to see a tool first and decide the process around it.

## Questionnaire behavior

During the questionnaire, the skill asks one primary question per round and uses prose-only checkpoints. It covers:

- the necessary outcome, initiative fit, requester, owner, people, scope, value, and constraints;
- the manual trigger-to-completion process, decisions, handoffs, exceptions, and failure recovery;
- email or chat, the shared tracker, the owned suite, the information taken from each, and manual transfers;
- partly codified policy pages and person-held routing and exception knowledge;
- the required solution ladder, lifecycle ownership, and evidence tasks.

No JSON or draft packet is produced during these rounds.

## Result

The request contains evidence of a cross-functional coordination problem, but not evidence that custom software is the right answer. The final direction is `process-redesign`: define a minimum approval model and accountable owner, then test the owned suite before buying or building.

The completed questionnaire creates two aligned artifacts. The readable brief starts with a plain-language decision snapshot so a stakeholder can see the recommendation, reason, handoff status, next action, and caution before the detail. Because the trigger, completion, actors, ordered steps, systems, handoffs, and material exceptions are mapped, the Markdown embeds the evidence-gated current view. It separately shows the stakeholder-stated ideal and agent-proposed target-process design, each with its own assumptions and evidence basis. JSON stores the exact source of all three views:

- [Ticket-ready Markdown initiative request](initiative-request.md)
- [Vendor-neutral JSON initiative packet](initiative-request.json)

The JSON conforms to [schema version 2.3.0](../../schemas/initiative-request.schema.json). It includes a stable initiative ID and a prototype-shaping handoff for the Better Work Loop. It is ready for another agent to parse or for a later field-mapping step into a known ticket system. It does not create a ticket or prototype. The diagrams are portable and inspectable, but they are not represented as BPMN 2.0 XML.

The earlier [v1 decision packet](decision-packet.json) remains in the repository for alpha traceability but is no longer the active output contract.
