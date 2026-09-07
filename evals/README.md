# Behavioral Evaluation

The fixtures in `cases.json` test decisions, safety boundaries, and output invariants. They do not require exact wording.

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

Treat a failure as evidence about the skill. Prefer a narrow correction and add a fixture only when it protects a materially different behavior.

## Review order

Run requester usability tests before reviewer handoff tests. A requester test checks whether the questions and evidence tasks are understandable without PM coaching. A reviewer test checks whether the packet supports evaluation without reconstructing the basic problem.

Never store a real internal request or initiative packet in this repository. Reproduce the behavior with a synthetic case.
