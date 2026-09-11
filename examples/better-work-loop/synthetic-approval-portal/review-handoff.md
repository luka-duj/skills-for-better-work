# Review handoff: synthetic approval portal, iteration 1

## Decision snapshot

The contained prototype is technically and synthetically verified, but no representative coordinator or approver has attempted the target job. The recommendation is `retest`; this iteration is waiting for human evidence, not complete.

## Process-design basis

### Current state — observed and evidence-gated

```mermaid
flowchart LR
  start((Start))
  subgraph requester_lane["Requester"]
    S1["1. Submit approval request<br/>Email or team chat"]
  end
  subgraph coordinator_lane["Approval coordinator"]
    S2["2. Interpret, route, and record status<br/>Shared tracker"]
    G1{"Required information complete?"}
    S4["4. Record outcome and close<br/>Shared tracker"]
  end
  subgraph approver_lane["Approver"]
    S3["3. Review and decide<br/>Email or team chat"]
  end
  finish((End))
  start --> S1 --> S2 --> G1
  G1 -- Yes --> S3 --> S4 --> finish
  G1 -- No --> S1
  S3 -- More information needed --> S1
```

### Stated ideal — stakeholder aspiration

```mermaid
flowchart LR
  ideal_start((Start))
  subgraph requester_lane["Requester"]
    I1["I1. Submit one complete request"]
  end
  subgraph system_lane["Shared workflow"]
    I2["I2. Route and show status"]
  end
  subgraph approver_lane["Approver"]
    I3["I3. Review and decide"]
  end
  ideal_end((End))
  ideal_start --> I1 --> I2 --> I3 --> ideal_end
```

### Proposed target — design hypothesis

```mermaid
flowchart LR
  target_start((Start))
  subgraph requester_lane["Requester"]
    T1["T1. Enter minimum request details"]
    T2["T2. Complete flagged gaps"]
  end
  subgraph coordinator_lane["Approval coordinator"]
    T3{"T3. Complete and routeable?"}
    T4["T4. Prepare reviewer summary"]
  end
  subgraph approver_lane["Approver"]
    T5["T5. Review and decide"]
  end
  target_end((End))
  target_start --> T1 --> T3
  T3 -- No --> T2 --> T3
  T3 -- Yes --> T4 --> T5 --> target_end
```

The original portal request `must-split` because it combines requester intake, coordinator routing, approval, status tracking, and audit concerns with different users and failure modes. The selected slice is only T1–T4: requester-to-coordinator completeness and reviewer-summary preparation, and it `fits-one-slice`. Approval, policy authoring, later status tracking, audit, and production integration are excluded.

## Prototype and evidence

Open `prototype/index.html` and attempt SCN-1, SCN-2, and SCN-5. Code was justified because the accepted uncertainty required field-level feedback, routing, refusal, and a copyable handoff. Technical and synthetic checks passed; representative-user usability and business outcomes remain unproven.

## Review tracks

- Business: confirm that intake is the earliest material failure, validate human control and exception handling, and nominate a coordinator and approver.
- PM/PO: review problem traceability, role separation, slice boundaries, and whether the evidence plan is sufficient.
- Delivery: assess existing-capability fit and dependencies only after the process and slice are accepted.

## Ready-to-run user session

Timebox: 30 minutes. Ask a coordinator to prepare a summary from a complete request, resolve an incomplete request, and hand the result to an approver. Do not explain fields or routing before the attempt. Record completion without coaching, wrong routes, hesitation, and missing reviewer context. Stop if the prototype appears to approve, sensitive data is entered, or the summary cannot start a review.

Resume the loop by appending sanitized representative `user-observation` sessions to the proof, rerunning validation, and choosing `stop`, `adapt-prototype`, `retest`, or `prepare-pilot-review` from the evidence.

## What may be missing or uncertain

No representative user has attempted the job. Final category rules, exception escalation, process ownership, system-of-record choice, access constraints, and existing-tool fit remain unresolved.
