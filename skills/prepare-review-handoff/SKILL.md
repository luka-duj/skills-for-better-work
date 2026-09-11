---
name: prepare-review-handoff
description: Package a completed Better Work Loop iteration for business, PM/PO, and delivery review with process views, slice scope, prototype evidence, unresolved decisions, and a runnable next test. Use only when explicitly invoked as $prepare-review-handoff or routed after Prove Before Pilot. Do not invent architecture, approve a pilot, or claim production readiness.
license: Apache-2.0
metadata:
  author: "Luka Dujmovic"
  version: "0.4.0-alpha"
  compatibility: "Agent Skills format; built and evaluated natively in Codex; requires Better Work Loop artifacts, referenced-file access, and local filesystem access. Behavior may vary by client."
---

# Prepare Review Handoff

Turn the loop's fragmented artifacts into one reviewable decision package. Preserve evidence limits and give each audience the information needed to decide without reconstructing the work.

## Start

1. Read [handoff and output contract](references/handoff-and-output.md).
2. Load the initiative, shape, build, proof, and loop-state artifacts. Verify recorded paths, IDs, iterations, and SHA-256 digests.
3. Use the current-state, stated-ideal, and proposed-target process views from the initiative packet. Do not relabel a proposed or incomplete view as observed reality.
4. Reuse the proof recommendation and session plan. This skill packages evidence; it does not raise the evidence level.

## Package

1. Lead with the decision, evidence level, next human action, and important cautions.
2. Include all three process views or the explicit reason each is unavailable. Highlight the target-process nodes included in the slice and the adjacent jobs excluded.
3. Separate business, PM/PO, and delivery review notes:
   - business: outcome, process choice, ownership, effort requested, and next decision;
   - PM/PO: hypothesis, users, scope, evidence, adoption, risks, and decision rule;
   - delivery: behavior, boundaries, inputs and outputs, scenarios, source-of-truth gaps, and unapproved technical decisions.
4. Link the exercisable prototype or rehearsal and give exact run instructions.
5. Carry forward failed, not-assessed, and disputed evidence. Include the runnable session plan when more user evidence is required.
6. State what the handoff does not authorize: implementation commitment, architecture, procurement, pilot, deployment, or production use.

## Deliver

Create `review-handoff.md` and `review-handoff.json` beside the active slice artifacts using the contract. Update loop state to reference the handoff. When proof recommends `retest` because representative-user evidence is missing, leave the loop `waiting-for-human` with decision `seek-user-evidence` and an exact resume instruction.

## Guardrails

- Do not fill evidence gaps with inferred current-state steps, system authority, rules, costs, or owners.
- Do not expand the accepted slice or turn possible-later work into committed scope.
- Do not produce a technical architecture unless separately requested and supported by the relevant owners.
- Do not call a handoff, prototype, or recommendation pilot approval or production readiness.
