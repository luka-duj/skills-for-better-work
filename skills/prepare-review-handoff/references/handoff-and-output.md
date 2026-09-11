# Handoff and Output Contract

## Inputs

Use one initiative packet, accepted shape, build, proof, and loop-state from the same loop and iteration. Verify each predecessor before packaging it. A deliberate stop before build remains reviewable through the decision and shape artifacts; this handoff contract begins after proof and must not invent a missing chain.

## Readable package

Write `review-handoff.md` beside the active slice artifacts. Begin with **Review decision** covering the evidence status, recommendation, requested human decision, owner, resume action, and cautions.

Then include:

1. business problem, outcome, baseline, and current direction;
2. current-state, stated-ideal, and proposed-target BPMN-style Mermaid views, or their explicit evidence gaps;
3. slice overlay: source problem, selected handoff, roles, included target nodes, exclusions, and later work;
4. prototype or rehearsal entrypoint and exact run instructions;
5. evidence matrix with critical failures and not-assessed items visible;
6. business review, PM/PO review, and delivery review notes;
7. session plan when the next recommendation requires representative-user evidence;
8. unresolved decisions, dependencies, ownership gaps, and non-authorizations;
9. what may be missing or uncertain.

## Structured package

Write `review-handoff.json` conforming to `../schemas/review-handoff.schema.json`. Reference each predecessor by exact path and SHA-256 digest. Copy process Mermaid sources exactly from the initiative packet. Reuse the shape's source problem references, role chain, selected handoff, target-node coverage, and exclusions. Reuse the proof status, recommendation, evidence limits, and session plan without upgrading them.

The package status is:

- `waiting-for-human` when representative-user evidence or another named human decision is next;
- `ready-for-review` when reviewers can make the requested non-pilot decision now;
- `closed` after a deliberate stop;
- `blocked` when the chain cannot support a responsible handoff.

The Markdown and JSON are immutable phase artifacts. A later retest creates a timestamped replacement and preserves this version.
