# Output Contract

Return a readable brief followed by JSON conforming to `../schemas/decision-packet.schema.json`. Keep the two outputs semantically aligned.

## Readable brief

Use these sections when applicable:

1. **Current direction** — one allowed direction, confidence, and a plain-language explanation.
2. **Request and desired outcome** — describe the request without strengthening it.
3. **Process necessity** — required outcome or obligation, evidence, what may be removed, and what remains unclear.
4. **What is known** — facts, interpretations, assumptions, constraints, and contradictions kept separate.
5. **Current process** — actors, normal path, exceptions, handoffs, rules, systems, and ownership at the depth supported by evidence.
6. **Options considered** — plausible, deferred, and rejected paths with reasons.
7. **Scorecard** — requester weights, reviewer status, fit scores, rationales, weighted results, evidence completeness, and critical conditions.
8. **Lifetime ownership and cost** — ownership map and supported ranges, or `Insufficient inputs for a monetary estimate`.
9. **Vendor research** — include only when applicable; state status, scope, shortlist, evidence, limitations, and questions.
10. **Evidence tasks** — ordered actions that can change the decision.
11. **Handoff** — a concise submission for the product or automation team, including the next human decision.
12. **What may be missing or uncertain** — material gaps, disagreement, and limits.

Do not pad empty sections. For quick triage, return the current direction, request, necessity, known/unknown evidence, and next two or three evidence tasks before continuing the interview.

## JSON contract

- Set `schema_version` to `1.0.0`.
- Use an ISO 8601 UTC timestamp in `generated_at`.
- Use `readiness` to show how far the request has progressed:
  - `triage`
  - `discovery-needed`
  - `assessment-ready`
  - `handoff-ready`
- Use one allowed direction in `recommendation.direction`.
- Use `null` for an unassigned requester weight, unassessed fit, reviewer weight, aggregate score, completeness, currency, horizon, amount, owner, or source. Do not use zero as a substitute for unknown.
- Keep `facts`, `interpretations`, `assumptions`, `constraints`, `contradictions`, and `unknowns` separate.
- Preserve requested and reviewed weights separately.
- Store displayed score and completeness percentages from 0 to 100, rounded to one decimal place. Keep both `null` when any applicable requester weight is unassigned.
- Use `research.status = not-applicable` when the buy path is not plausible.
- Use `research.status = awaiting-confirmation` after preparing a Deep Research brief but before the user confirms it.
- A handoff may be useful while `submission_ready` is false; in that case it must state the missing evidence and recommended discovery work.

## Consistency checks

Before delivery:

- the Markdown and JSON use the same direction, confidence, readiness, and research status;
- every numeric score has a rationale and confidence;
- weighted scores and completeness use the formula in `solution-ladder.md`;
- cost ranges contain only supplied or cited inputs;
- sources support the associated claims and use accessible URLs when research ran;
- blocking conditions appear in both the recommendation and handoff;
- no real confidential content is suggested for public feedback.
