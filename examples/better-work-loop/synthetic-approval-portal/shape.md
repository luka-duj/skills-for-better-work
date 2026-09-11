# Shape the Slice — Synthetic approval portal

## Shape decision

- **Test now:** whether a structured intake helps an operations coordinator prepare a complete, correctly routed request without making the approval decision.
- **Fidelity:** a contained runnable vertical slice is enough to test completeness, routing feedback, refusal to approve, and downstream summary usability.
- **Primary user:** operations coordinator; the requester, approver, and accountable process owner are distinct roles.
- **Selected handoff:** requester-to-coordinator intake completeness and route preparation, corresponding to proposed target nodes T1–T4.
- **Split assessment:** the source portal request `must-split` because it spans several user jobs and failure modes; the selected T1–T4 intake-to-handoff slice itself `fits-one-slice`. Approval, policy authoring, status tracking, audit, and production integration remain adjacent jobs.
- **Excluded:** accounts, storage, integrations, ticket creation, audit history, and production infrastructure.
- **Build gate:** accepted by the fictional example owner for demonstration only.
- **Next:** build the local slice and verify the five scenarios before seeking representative-user evidence.

## Target job and hypothesis

An operations coordinator needs to turn an incoming approval request into a complete summary that the correct human reviewer can use.

The hypothesis is: A structured intake that exposes missing information and separates standard from exception review will let a coordinator prepare a usable review summary without email clarification or accidental approval.

Code is justified for this slice because the uncertainty requires an exercisable interaction: field-level feedback, routing, refusal to approve, and a copyable handoff. This is not a default expectation for workflow simulations.

## Critical evidence

The prototype must handle a complete request, missing information, an exception route, refusal to approve, and a usable downstream summary. It can be called validated only after a representative coordinator completes the job and a reviewer can use the result.

## Boundaries

Use fictional data only. The prototype does not store or send information, authenticate users, call external services, or approve anything. The manual process remains the fallback.

## What may be missing or uncertain

The minimum fields and acceptance gate are synthetic. Real coordinators and reviewers have not confirmed that the summary is sufficient.
