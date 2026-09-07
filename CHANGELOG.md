# Changelog

## Unreleased

### Changed

- Updated `process-before-platform` to `0.2.2-alpha` with a lighter routing-first discovery path that closes safely with explicit evidence tasks instead of forcing every coverage question into the live conversation.
- Clarified the `reframe` versus `discovery-needed` tie-break and kept initiative fit separate from readiness.
- Made requester-weighted scorecards explicitly directional and withheld rankings until review and critical conditions are resolved.
- Strengthened scorecard validation for complete criterion coverage, ranking caveats, reviewed weights, and critical conditions; added regression coverage and a regulated high-risk behavioral fixture.
- Made stakeholder conversations and the readable handoff default to plain language, with a concise decision snapshot before detailed analysis.
- Defined submission readiness as “ready to send now,” prevented contradictory missing-field and do-not-submit states, and added regression tests.
- Required known conditional work to appear as a process branch while leaving unsupported recovery detail explicitly unmapped.
- Kept generated requests and evaluation runs out of source control by default, and clarified that behavioral tests must run as real turn-by-turn conversations.
- Declared the Apache-2.0 license, open-format compatibility boundary, author, and alpha version in validator-compatible skill metadata.
- Added client-specific installation guidance for Codex, Claude Code, Claude.ai, and other Agent Skills-compatible clients.
- Distinguished cross-client package compatibility from behavior tested in the Codex reference environment.
- Added clean-history, cross-client claim, profile handoff, and post-publication vulnerability-reporting gates to the publishing checklist.
- Passed a clean-context Codex smoke test for the vague-request first turn: safety warning, no invented facts, one focused discovery question, and no premature JSON or packet.
- Clarified that the skills can be used with Claude and other compatible AI systems while Codex remains the native, best-supported reference implementation.
- Refreshed the repository positioning around clearer decisions, better systems, and practical AI.
- Added a direct link to [lukadujmovic.com](https://lukadujmovic.com/) and replaced the active repository header with a 1200 × 320 brand banner.
- Prepared the repository copy, package metadata, security route, and announcement draft for a public-alpha visibility switch while keeping publication owner-controlled.

### Fixed

- Prevented ready handoffs from listing information as missing for submission.
- Prevented `do-not-submit` outcomes from being marked submission-ready.

## 0.2.1-alpha — 2026-09-05

- Added an evidence-gated BPMN-style Mermaid swimlane diagram to the final Markdown artifact, with the exact diagram source and coverage metadata in JSON.
- Added explicit `mapped`, `insufficient-evidence`, and `not-applicable` diagram states so incomplete discovery produces evidence tasks rather than an invented flow.
- Updated the active initiative-request schema to version 2.1.0 and added validation for actors, ordered-step coverage, start/end events, and Markdown/JSON diagram alignment.

## 0.2.0-alpha — 2026-09-05

- Made initiative-intake readiness the primary outcome while retaining the required solution ladder and buy-versus-build assessment.
- Added structured discovery for the current manual process, systems, information sources, data flows, and codified or person-held knowledge.
- Added vendor-neutral initiative-request JSON Schema version 2.0.0 and aligned Markdown and JSON example artifacts.
- Added portable target-system field mappings and task-local, collision-safe artifact rules without automatic ticket creation.
- Retained the v1 decision schema and example for alpha traceability; new runs use v2.

## 0.1.1-alpha — 2026-09-04

- Changed the interaction contract so questionnaire rounds are prose-only.
- The readable handoff and JSON decision packet are now generated once, after the adaptive questionnaire is complete or explicitly closed with remaining unknowns converted into evidence tasks.

## 0.1.0-alpha — 2026-09-04

- Added the explicit-only `process-before-platform` Codex skill.
- Added adaptive discovery, solution-ladder, ownership/TCO, vendor-research, and output-contract guidance.
- Added decision-packet JSON Schema version 1.0.0.
- Added the synthetic approval-portal walkthrough and ten behavioral fixtures.
- Added dependency-free validation, regression tests, and read-only GitHub Actions checks.
- Added redaction-safe contribution and issue guidance.
- Clarified the no-action disposition and made unassigned scorecard weights schema-valid after independent forward testing.

The first public release and LinkedIn announcement remain owner-controlled actions.
