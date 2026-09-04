# Synthetic Walkthrough: Approval Portal Request

This example is invented. It is not derived from a real company, customer, system, or project.

## Initial request

> We need a custom approval portal. Requests arrive in email and chat, approvers lose track of status, and people use different templates. We want to see a working tool first, then we can decide the process around it. Four departments submit roughly 20–40 requests each month. Approval paths vary, and nobody currently owns the full process. Our work-management suite may already support forms and approval steps, but we have not assessed it.

## Quick-triage result

- The approval outcome appears necessary, but the exact obligation and approval policy are unclear.
- Inconsistent request definitions, routes, and ownership would be encoded into any portal built now.
- The leading direction is `process-redesign`, not custom development.
- Existing capability should be assessed after the minimum approval model is defined.

## Why the proposed solution changed

The request contains evidence of a coordination problem, but not evidence that custom software is the appropriate answer. A portal cannot decide which requests exist, which approvals are mandatory, which exceptions are legitimate, or who owns changes to those rules.

## Decision and handoff brief

### Current direction

`process-redesign` — medium confidence.

Define the minimum approval model and its owner before selecting software. Assess the existing work-management capability against that model before researching vendors or building a portal.

### Request and desired outcome

The requester wants a custom portal to reduce lost status, inconsistent submissions, and unclear approval routing. The desired outcome is a traceable request-to-decision flow across four departments.

### Process necessity

Some approval outcome appears necessary, but the basis for each approval and variation has not been established. The team should confirm which approvals come from policy or control requirements and which are historical practice.

### What is known

Facts supplied in the synthetic request:

- Requests arrive through email and chat.
- Different templates and approval routes are used.
- Four departments submit an estimated 20–40 requests monthly.
- No owner for the end-to-end process is named.
- An existing work-management suite may offer relevant capabilities but has not been assessed.

Unknowns include the mandatory approval rules, request categories, exception frequency, failure consequences, current-system fit, and future owner.

### Options considered

- **Process redesign:** plausible now. It addresses unstable definitions, routes, and ownership.
- **Use existing capability:** deferred until the minimum process is defined and the current suite is tested against it.
- **Custom build:** rejected for the current stage. The differentiated need, lifecycle owner, and total-cost inputs are missing.

### Scorecard

The requester-draft weights are illustrative and require reviewer confirmation.

| Criterion | Weight | Process redesign | Existing capability | Custom build |
| --- | ---: | ---: | ---: | ---: |
| Necessary outcome and user value | 5 | 4 | 4 | 3 |
| Process fit and exceptions | 5 | 5 | 3 | 2 |
| Time to operation | 3 | 4 | 4 | 2 |
| Lifetime cost and capacity | 4 | 4 | 4 | Not assessed |
| Ownership and support | 4 | 3 | Not assessed | 1 |

- Process redesign: 81.0% weighted fit, 100.0% evidence completeness.
- Existing capability: 74.1% weighted fit, 81.0% evidence completeness.
- Custom build: 41.2% weighted fit, 81.0% evidence completeness.

The ranking is withheld as an organizational decision because the weights are requester drafts and critical ownership and policy questions remain unresolved.

### Lifetime ownership and cost

There are insufficient inputs for a monetary estimate. Product/process ownership, development, security, integration, deployment, monitoring, support, change, upgrades, and retirement are currently unowned for a custom portal.

### Evidence tasks

1. Confirm which approval outcomes and controls are mandatory and who owns the policy.
2. Define the minimum request categories, required information, normal approval path, and legitimate exceptions from recent cases.
3. Test the existing work-management suite against that minimum model.
4. Name the operational owner and support path for any future solution.

### Handoff

The approval outcome appears necessary, but the current process is not stable enough for a responsible custom build decision. Complete the four evidence tasks above. Then compare process-only, existing-capability, integration, buy, and custom paths with reviewer-confirmed priorities.

### What may be missing or uncertain

The supplied volume is an estimate, no policy source was provided, and the existing suite has not been tested. The example therefore does not support procurement, architecture, budget, or delivery approval.

The machine-readable companion is [decision-packet.json](decision-packet.json).
