# Behavioral Evaluation

The fixtures in `cases.json` test decisions, safety boundaries, and output invariants. They do not require exact wording.

## Forward-test procedure

1. Start a clean Codex conversation with the skill installed.
2. Invoke `$process-before-platform` explicitly with the fixture input.
3. Answer follow-up questions only with facts present in the fixture. Use `I do not know` for everything else.
4. Save the final readable brief and JSON outside the repository or under ignored `evals/runs/`.
5. Check the observed direction against `allowed_directions` and `forbidden_directions`.
6. Review every `required_behavior` and record pass, fail, or not assessed with the output evidence.
7. Validate the JSON decision packet with `python scripts/validate.py --packet <path>`.

Treat a failure as evidence about the skill. Prefer a narrow correction and add a fixture only when it protects a materially different behavior.

## Review order

Run requester usability tests before reviewer handoff tests. A requester test checks whether the questions and evidence tasks are understandable without PM coaching. A reviewer test checks whether the packet supports evaluation without reconstructing the basic problem.

Never store a real internal request or decision packet in this repository. Reproduce the behavior with a synthetic case.
