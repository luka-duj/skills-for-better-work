# Output Contract

After the questionnaire completion gate, create a ticket-ready Markdown file and a vendor-neutral JSON file conforming to `../schemas/initiative-request.schema.json`. Keep the two artifacts semantically aligned.

## Delivery timing

- Do not return JSON at invocation, after triage, or during questionnaire rounds.
- Do not expose a draft packet, partial JSON object, schema scaffold, or repeatedly regenerated packet while answers are still being collected.
- Interim turns contain the next primary question and, only when useful, a brief prose recap or diagnosis.
- Produce the two final artifacts only after all material questions are answered, converted into evidence tasks, marked not applicable, or explicitly deferred, and any applicable research branch is completed or deferred.
- A questionnaire can finish with material unknowns. In that case, represent them honestly in a final `insufficient-evidence` or other appropriately caveated packet rather than withholding the packet forever.
- If the user elects to stop early, first confirm that the current unknowns should become evidence tasks; that choice closes the questionnaire and permits final delivery.

## Artifact creation

- Resolve the current project root from the active repository or task-local workspace.
- Default to `<current-project>/output/process-before-platform/`.
- Use the shared basename `<YYYY-MM-DD>-<initiative-slug>` and extensions `.md` and `.json`.
- If either path exists, add a collision-safe local-time suffix; never overwrite.
- If no clear writable project root exists, ask the user for a destination near the end of the questionnaire.
- Write both files before final delivery, validate the JSON when a compatible validator is available, and return clickable links to both.
- Do not paste the full JSON into chat unless the user requests it.
- Do not create a remote ticket or mutate a ticketing system without a separate explicit request.

## Markdown initiative request

Use these sections when applicable:

1. **Initiative summary and fit** — name, summary, classification, rationale, readiness, requester, business owner, areas, reach, type, and proposed solution.
2. **Problem, necessity, and desired outcome** — keep the problem separate from the solution and show supporting evidence.
3. **Scope** — in scope, out of scope, adjacent work, and target capabilities.
4. **Current manual process** — trigger, completion, actors, ordered steps, decisions, information and knowledge used, handoffs, exceptions, rework, recovery, ownership, and pain points.
5. **Existing systems and information sources** — purpose, users, inputs, outputs, information collected or retrieved, source-of-truth role, transfers, integrations, access, ownership, and limitations.
6. **Knowledge landscape** — codified, partially codified, tribal, conflicting, stale, inaccessible, and missing knowledge with locations and owners.
7. **Target state and requirements** — capabilities, supported functional and non-functional needs, human control, rollout, adoption, support, and fallback.
8. **Value, priority, and success measures** — value hypothesis, baseline, measures, saved-time use, strategy link, urgency, deadline, budget status, and reach without invented numbers.
9. **Required solution assessment** — all plausible ladder options, scorecard, critical conditions, leading direction, and buy-versus-build implications.
10. **Dependencies, risks, and lifetime ownership** — named owners and next checks.
11. **Evidence tasks and pending discovery** — ordered actions that can change readiness or direction.
12. **Ticket handoff** — ticket title, concise body, target mapping status, submission readiness, missing submission fields, next workflow, and next human decision.
13. **What may be missing or uncertain** — source limits, disagreements, and gaps.

Do not pad empty sections. During quick triage, keep any direction, necessity, known/unknown evidence, and next questions in concise prose rather than using the final brief structure.

## JSON initiative packet

- Set `schema_version` to `2.0.0`.
- Use an ISO 8601 UTC timestamp in `generated_at`.
- Use `readiness` to show how far the request has progressed:
  - `discovery-needed`
  - `assessment-ready`
  - `ticket-ready`
- Use one allowed initiative-fit classification and one allowed direction in `recommendation.direction`.
- Populate `current_state.steps`, `current_state.systems`, `current_state.information_sources`, `current_state.knowledge_sources`, and `current_state.data_flows` at the depth supported by discovery. Use empty arrays only when nothing is known and create an evidence task when the gap is material.
- Keep `target_state` separate from `current_state` and from the requester-proposed solution.
- Keep the portable packet independent of any ticket vendor. Populate `handoff.target_system.field_mappings` only from known destination metadata.
- Use `null` for an unassigned requester weight, unassessed fit, reviewer weight, aggregate score, completeness, currency, horizon, amount, owner, or source. Do not use zero as a substitute for unknown.
- Keep `facts`, `interpretations`, `assumptions`, `constraints`, `contradictions`, and `unknowns` separate.
- Preserve requested and reviewed weights separately.
- Store displayed score and completeness percentages from 0 to 100, rounded to one decimal place. Keep both `null` when any applicable requester weight is unassigned.
- Use `research.status = not-applicable` when the buy path is not plausible.
- Use `research.status = awaiting-confirmation` after preparing a Deep Research brief but before the user confirms it.
- A handoff may be useful while `submission_ready` is false; in that case it must state the missing evidence and recommended discovery work.
- Record the actual output paths and `new-file-only` overwrite policy in `artifacts`.

## Consistency checks

Before delivery:

- the Markdown and JSON use the same initiative name, fit, direction, confidence, readiness, research status, submission status, and next decision;
- every current-state system, information source, knowledge source, and material process step appears consistently in both artifacts;
- every numeric score has a rationale and confidence;
- weighted scores and completeness use the formula in `solution-ladder.md`;
- cost ranges contain only supplied or cited inputs;
- sources support the associated claims and use accessible URLs when research ran;
- blocking conditions appear in both the recommendation and handoff;
- artifact paths share the same basename and both files exist;
- no real confidential content is suggested for public feedback.
