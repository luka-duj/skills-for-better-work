---
name: better-work-loop
description: Coordinate a business-led internal-workflow loop from a sanitized request through current and proposed process design, one testable slice, prototype or rehearsal, evidence, and a review-ready handoff. Use only when the user explicitly invokes $better-work-loop and wants the complete pack rather than one specialist phase. Do not use for production deployment or approval.
license: Apache-2.0
metadata:
  author: "Luka Dujmovic"
  version: "0.4.0-alpha"
  compatibility: "Agent Skills format; built and evaluated natively in Codex; requires the other Better Work Loop skills, referenced-file access, and local filesystem access. Behavior may vary by client."
---

# Better Work Loop

Move a sanitized internal process, automation, or internal-tool request through the lightest responsible path to a tested prototype, a process rehearsal, or an earlier stop decision. Keep the business requester in control, preserve the evidence trail, and finish with a package another reviewer can understand without reconstructing the work.

## Start

1. Warn the user not to share confidential business data, personal data, credentials, private architecture, contracts, or non-public vendor material.
2. Read [routing and state](references/routing-and-state.md).
3. Inspect supplied artifacts before asking for information already recorded.
4. Resolve the current project root and create loop artifacts under `output/better-work-loop/`. If no writable project root is clear, ask for a destination before writing.

## Route

1. **Decide and map.** Invoke or apply `$process-before-platform` unless a compatible initiative packet is supplied. Preserve three distinct views when applicable: evidence-gated current state, stakeholder-stated ideal, and agent-proposed target process. Stop on `eliminate-or-stop`. Stay in decision discovery on `insufficient-evidence`.
2. **Choose the first learning boundary.** Before shaping, identify the earliest material handoff, decision, or uncertainty that can change the direction. Distinguish requester, primary user, downstream user, and accountable owner. Do not equate accountability with primary-user status.
3. **Shape.** Use `$shape-the-slice` for a plausible process redesign, existing-capability test, configuration test, integration, automation, custom build, or co-evolution experiment. Require one primary user job and one independently testable uncertainty; split broader journeys before the build gate.
4. **Build gate.** Shaping owns the single approval question. Reuse an explicit acceptance of that exact slice, boundaries, and evidence plan; do not ask again at the router. If still pending, present the shape decision and wait for accept, revise, or reject. Record phase `shape`, status `waiting-for-human`, and current decision `decide-build-gate`. Silence is not acceptance.
5. **Rehearse or build.** After acceptance, use `$build-the-slice`. Honor the selected fidelity: a workflow simulation starts with a role-and-decision rehearsal, and code needs a recorded interaction or logic reason. Do not add ordinary phase-by-phase approval prompts. Pause again only for a new external consequence, cost, sensitive-data boundary, live-system change, deployment, or materially expanded scope.
6. **Prove.** Use `$prove-before-pilot`. Technical and synthetic checks may establish `agent-verified`; only representative-user evidence can establish `validated`. Keep stakeholder direction separate from observed user-task evidence.
7. **Prepare the handoff.** Use `$prepare-review-handoff` after proof, including when the recommendation is `retest`. Package the process views, slice boundary, prototype or rehearsal, evidence, session plan, unresolved decisions, and audience-specific review notes.
8. **Decide next.** End with one human-owned recommendation: `stop`, `revise-process`, `adapt-prototype`, `retest`, or `prepare-pilot-review`.

## Interaction rules

- Use the requester's language and show the practical decision before controlled status labels.
- Ask only questions that can change routing, the slice, a critical boundary, or the evidence decision.
- Never make the requester reconstruct context already present in a predecessor artifact.
- Apply one specialist at a time by reading its `SKILL.md` and only the references needed for that phase. Routing means following those instructions in this conversation; it does not require a subagent, new task, or a callable skill tool. If a required skill is missing, explain which one and preserve the completed work.
- Give a short progress update at a phase boundary: what was learned and what happens next. Keep paths, hashes, and schema fields out of business questions.
- Keep one active slice per iteration. A material hypothesis change starts a new iteration; it does not silently rewrite prior evidence.
- When representative-user evidence is missing and the recommendation is `retest`, keep the loop `waiting-for-human` with current decision `seek-user-evidence`; do not label the loop completed.
- Do not call a local prototype production-ready or treat deployment, usage, or a polished demo as validation.

## Deliver

Maintain the Markdown and JSON loop-state pair defined in [routing and state](references/routing-and-state.md). Link the current readable state, review handoff, and latest specialist artifacts in the final response. Do not paste full JSON unless requested.

## Boundaries

- The loop can create local prototype files when the user requested the loop and accepted the build gate.
- It cannot approve or perform procurement, production deployment, live integration, pilot access, budget, architecture, security, legal, or compliance decisions without a separate explicit request and the relevant human owner.
- Prefer synthetic or sanitized data and simulated adapters. Do not put secrets in generated files.
- This skill creates prototypes for the requester's workflow. It does not authorize building the companion application discussed in the repository's app evidence gate.
