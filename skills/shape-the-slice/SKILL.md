---
name: shape-the-slice
description: Turn a supported internal-workflow direction into one smallest useful prototype slice with a risky assumption, representative user job, fidelity choice, boundaries, acceptance criteria, and evidence plan. Use only when the user explicitly invokes $shape-the-slice or the Better Work Loop routes to shaping. Do not build the prototype or approve production.
license: Apache-2.0
metadata:
  author: "Luka Dujmovic"
  version: "0.4.0-alpha"
  compatibility: "Agent Skills format; built and evaluated natively in Codex; requires referenced-file and local filesystem access. Can consume Better Work Loop initiative packets. Behavior may vary by client."
---

# Shape the Slice

Choose the smallest prototype that can change the next decision. Narrow what must be proved now without turning possible future scope into current scope.

## Start

1. Read [shape and output contract](references/shape-and-output.md).
2. Inspect the supplied initiative packet or plain-language context. Reuse recorded facts, assumptions, process steps, risks, and owners.
3. If the input direction is `eliminate-or-stop` or `insufficient-evidence`, do not create a build-ready slice. Return the request to the Better Work Loop decision phase.
4. Ask only for missing information that can change the hypothesis, fidelity, critical boundary, or evidence decision.

## Shape

1. State the single decision the prototype must inform and the riskiest assumption behind it. Reference the source pain point, handoff, decision, or evidence task rather than relying on thematic similarity.
2. Separate the business requester, primary user, downstream user, and accountable owner. Select one primary user and one real job from trigger to useful outcome; accountability alone does not make someone the primary user.
3. Name the selected handoff or decision and explain why it is the earliest material uncertainty worth testing.
4. Choose the lowest sufficient fidelity:
   - workflow simulation when sequence, roles, rules, or handoffs are uncertain;
   - clickable prototype when comprehension, navigation, trust, or interaction is uncertain;
   - runnable vertical slice when logic, data transformation, tool use, or downstream usability is uncertain;
   - configuration sandbox when an owned or vendor capability must be tested.
5. Run the split assessment twice: record whether the source request `must-split`, including its reasons, then test whether the selected slice itself fits one slice. Preserve the source decision after narrowing. A selected slice that still combines independently testable jobs, unrelated failure modes, or different representative roles cannot pass the build gate. Supporting downstream review may remain only when it tests the same handoff.
6. Define only the capabilities necessary to test the hypothesis. Record non-goals and possible-later scope explicitly. Map the slice to target-process node IDs when a target design exists.
7. Derive scenario coverage from the live workflow: normal, exception, missing information, contradiction, refusal or human-control boundary, and downstream use where applicable.
8. Define observable acceptance criteria and evidence collection. Do not use a polished screen, deployment, or completion of code as success evidence.
9. Record sanitized-data, privacy, security, access, cost, fallback, and external-effect constraints.

## Build gate

Present a short decision snapshot covering the hypothesis, user/job, fidelity, slice, exclusions, critical boundaries, evidence, and important cautions. This skill owns the one build-gate question, including when routed by Better Work Loop. Ask the business owner to accept, revise, or reject only if the exact proposed scope and evidence plan have not already been explicitly accepted. Set the gate to `accepted` only from that answer; a general request to run the loop is not acceptance of an as-yet unseen slice.

Write the completed shape pair with a `pending` gate before waiting so the user can inspect it and resume later. On acceptance, create a new timestamped pair recording the owner and decision time, then point the loop to it. Preserve the pending pair. Do not ask for acceptance again merely because the phase or conversation changed.

## Deliver

After the shape is complete, create `shape.md` and `shape.json` as defined in [shape and output contract](references/shape-and-output.md). Keep Markdown and JSON aligned and link both. Do not create prototype source in this skill.

## Guardrails

- Do not force software when a rehearsal or workflow simulation can answer the question. Record whether code is required and why.
- Do not choose a technology before the fidelity and test need are clear.
- Do not invent a baseline, user need, owner, deadline, value, target, or acceptance threshold.
- Do not broaden one slice into a roadmap, full PRD, architecture, or production plan.
