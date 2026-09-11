# Behavioral Evaluation

The fixtures in `cases.json` test process decisions, safety boundaries, and initiative-output invariants. `loop-cases.json` tests phase routing, the build gate, local-build boundaries, artifact integrity, evidence labels, and next-decision behavior. Neither set requires exact wording.

## Forward-test procedure

1. Start a clean Codex conversation with the skill installed.
2. Invoke `$process-before-platform` explicitly with the fixture input. Run the exchange turn by turn; do not give the evaluator a pre-completed packet.
3. Answer follow-up questions only with facts present in the fixture. Use `I do not know` for everything else. Record the number of questions, repeated questions, corrections, and whether the requester chose to close or continue.
4. Check every intermediate turn: it may contain a concise prose recap, but it must not contain JSON, a draft packet, or the full handoff brief.
5. Confirm that the skill emits the JSON packet only once, after the adaptive questionnaire is complete or explicitly closed.
6. Save repository evaluation artifacts under ignored `evals/runs/` or outside the repository. Reserve `output/process-before-platform/` for normal project use; it is also ignored so generated requests do not become source files accidentally.
7. Check the observed direction against `allowed_directions` and `forbidden_directions`.
8. Review every `required_behavior` and record pass, fail, or not assessed with the output evidence.
9. Validate the JSON initiative packet with `python scripts/validate.py --packet <path>`.

## Better Work Loop forward test

1. Start a clean conversation with all six skills installed and invoke `$better-work-loop` with one `loop-cases.json` input.
2. Inspect every predecessor before answering. Record whether the router re-asks anything already present.
3. Confirm stop and insufficient-evidence cases create no prototype source.
4. For a build case, confirm the router presents one concise shape decision and obtains one explicit accept, revise, or reject answer before source creation.
5. Confirm ordinary local implementation continues without phase-by-phase approval prompts; record any additional pause and the external consequence that justified it.
6. Check that the shape, build, proof, review-handoff, and loop-state pairs use matching IDs, iteration, paths, and SHA-256 digests.
7. Confirm the build implements the target job and critical boundaries rather than only a scaffold or disconnected screens.
8. Run technical and synthetic scenarios, then inspect the proof status. Without a representative-user observation it must not exceed `agent-verified`.
9. For a representative-user test, record only the role, representativeness, observed task outcome, friction, criterion evidence, and downstream usability. Do not store identity or raw sensitive material.
10. Confirm `validated` appears only when the representative user completes the job, every critical criterion and scenario passes, downstream usability passes, and no critical failure remains.
11. Confirm the review handoff preserves the three process views, selected target nodes, exclusions, prototype location, evidence limits, audience-specific questions, and the exact session plan.
12. When representative evidence is missing, confirm the loop ends the turn in `handoff / waiting-for-human`, not `completed`; the terminal recommendation remains stop, process revision, prototype adaptation, retest, or pilot review.

Before calling the complete pack release-ready, run at least two genuine clean-context loops with business users: one process-oriented or non-code case and one runnable prototype with exception and refusal behavior. The synthetic repository example does not satisfy this gate.

Treat a failure as evidence about the relevant skill or handoff. Prefer a narrow correction and add a fixture only when it protects a materially different behavior.

## Workhorse-model checks

Use [realistic requester cases](workhorse-cases.md) as raw prompts, with no expected-answer notes in the model's context. Run each in a fresh conversation on GPT-5.6 Luna / Extra high and GPT-5.6 Sol / high when available. Record the exact model identifier and reasoning setting; for Claude, record the actual tested model rather than asserting equivalence from its name. These target-model runs have not yet been recorded for the revised pack.

Keep the same sanitized facts and tool access across comparisons. Record questions, repeated questions, approval prompts for unchanged scope, loaded references, artifact-validation failures and repair attempts, runnable job completion, and unsupported claims of human evidence. Count a skipped or unavailable check as not assessed. Compare the earlier and revised instructions using these outcomes; shorter output alone is not success.

Required behavioral outcomes: one gate for unchanged scope; no source before acceptance; no repeated discovery on resume; no fabricated user evidence; preserved critical failures; and no demand that the requester supply schema fields or hashes. Evaluate the usefulness of the decision and prototype separately from JSON validity. Synthetic model runs do not satisfy the genuine business-user release gate above.

## Review order

Run requester usability tests before reviewer handoff tests. A requester test checks whether the questions and evidence tasks are understandable without PM coaching. A reviewer test checks whether the packet supports evaluation without reconstructing the basic problem.

Never store a real internal request or initiative packet in this repository. Reproduce the behavior with a synthetic case.
