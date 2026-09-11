# Proof and Output Contract

## Evidence levels

Use five evidence types without blending them:

- `technical`: build, static, unit, integration, browser, or accessibility evidence;
- `synthetic`: predefined fictional scenarios and fixtures;
- `stakeholder-feedback`: direction or critique from a requester, sponsor, or reviewer who did not attempt the target job;
- `user-observation`: a representative person attempting the target job;
- `business-result`: an observed operational outcome over an appropriate window.

A prototype can reach `validated` from user observation without business-result evidence, but the report must say that realized value, sustained adoption, reliability, support burden, and production behavior remain unproved.

## User session

Confirm the participant is representative of the target role and has authority to test with the supplied data. Record a role label, not identity. Ask them to attempt the job and think aloud only if comfortable. Do not steer around confusing UI or incorrect output. Capture observable facts separately from the participant's interpretation and the evaluator's interpretation.

## Output

Write `proof.md` and `proof.json` in the active slice directory. A repeat session adds a timestamped pair or a new evidence session without deleting earlier evidence. When representative-user evidence is missing and the recommendation is `retest`, include a `ready` session plan detailed enough for a facilitator to run without designing the test from scratch.

Start Markdown with **Evidence decision**: status, what was observed, critical failures, evidence limits, recommendation, human owner, and next action. Then include session evidence, criteria, scenarios, downstream usability, the next session plan, privacy handling, unresolved questions, and uncertainties.

The JSON must conform to `../schemas/prototype-evidence.schema.json`. Reference both the shape and build artifacts by exact path and SHA-256 digest. Reuse their criterion and scenario IDs.
