---
name: prove-before-pilot
description: Evaluate an internal-workflow prototype against its approved hypothesis, acceptance criteria, failure scenarios, downstream usability, and representative-user evidence, then recommend stop, process revision, prototype adaptation, retest, or pilot review. Use only when explicitly invoked as $prove-before-pilot or routed by Better Work Loop. Do not approve a pilot or production use.
license: Apache-2.0
metadata:
  author: "Luka Dujmovic"
  version: "0.4.0-alpha"
  compatibility: "Agent Skills format; built and evaluated natively in Codex; requires referenced-file and local filesystem access plus a representative-user session for validated status. Behavior may vary by client."
---

# Prove Before Pilot

Determine what the prototype actually demonstrates. Keep technical verification, synthetic evaluation, user observation, and business decisions distinct.

## Start

1. Read [proof and output contract](references/proof-and-output.md).
2. Load the shape and build artifacts. Verify their IDs, iteration, paths, and SHA-256 digests.
3. Reconstruct the hypothesis, target job, criteria, scenarios, boundaries, and decision rule from the approved shape—not from what the prototype happens to implement.
4. If the prototype cannot run or a critical technical check failed, record the evidence and recommend adaptation or retest without claiming user validation.

## Evaluate

1. Review technical and synthetic results. Label them `technical` or `synthetic`; never relabel them as user evidence. Record advice from a requester or sponsor who did not attempt the target job as `stakeholder-feedback`.
2. When a representative user is available, guide them through the target job without coaching them around defects. The requester may qualify when they genuinely perform that job. If nobody is available, finish the technical/synthetic report, leave user-dependent results `not-assessed`, and create a runnable session plan with participant roles, fixed sanitized tasks, facilitator limits, observations, critical stops, an agreed or null timebox, and an exact resume instruction. Do not wait indefinitely or role-play a human observation.
3. Record role, representativeness, task outcome, observable friction, errors, workarounds, confidence, and whether the output was usable by the next person or system. Do not store identity, raw transcripts, screenshots, or sensitive input by default.
4. Exercise applicable normal, exception, missing-information, contradiction, refusal, fallback, human-override, and downstream-use scenarios.
5. Map every acceptance criterion to observed evidence. Preserve disagreements and missing evidence.
   Copy criterion and scenario IDs and critical flags from the approved shape. Never downgrade a critical item to make the result pass.
6. Identify critical failures before considering aggregate success. A critical safety, privacy, refusal, human-control, or downstream-usability failure prevents `validated`.

## Classify

- `technically-verified`: technical checks passed; no representative-user observation exists.
- `agent-verified`: technical plus synthetic or agent review passed; no representative-user observation exists.
- `user-observed`: representative use was observed, but evidence is incomplete or mixed.
- `validated`: a representative user completed the target job, every critical criterion passed, downstream usability passed, and no critical failure remains.
- `invalidated`: observed evidence contradicts the hypothesis or exposes a critical failure.
- `inconclusive`: the test could not distinguish success from failure.

## Decide

Recommend exactly one: `stop`, `revise-process`, `adapt-prototype`, `retest`, or `prepare-pilot-review`. Name the human owner and explain the evidence. `prepare-pilot-review` means the bounded prototype has enough evidence for accountable review; it is not pilot approval or production readiness.

## Deliver

Create `proof.md` and `proof.json` using [proof and output contract](references/proof-and-output.md). Lead with the evidence decision, include the session plan when further user evidence is needed, and link both files. Do not hide failed or unrun tests in an overall score.

## Guardrails

- Do not invent user observations, task completion, satisfaction, adoption, value, or business impact.
- Do not require a fixed participant count; state how narrow the evidence is.
- Do not conduct live-system tests, deployment, or pilot access without a separate explicit request and required approvals.
- Stop the test if it would expose sensitive data, perform an unapproved consequential action, or remove the safe fallback.
