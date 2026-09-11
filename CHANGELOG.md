# Changelog

## Unreleased

### Changed

- Expanded the README with plain-language guidance for all six skills, including when each skill applies, what it helps people do, what it produces, and which decisions remain outside its scope.

## 0.4.0-alpha — 2026-09-11

- Updated the pack to `0.4.0-alpha` with a sixth explicit-only skill, `prepare-review-handoff`.
- Added separate evidence contracts for the observed current process, stakeholder-stated ideal, and agent-proposed target-process design in initiative schema `2.3.0`; unmodified 2.1 and 2.2 packets remain valid legacy inputs.
- Added role-chain separation, source-problem references, stable target-process node coverage, an earliest-handoff slice, a force-split assessment, and explicit code justification to shaping schema `1.1.0`.
- Added fidelity-delivery enforcement to build schema `1.1.0`, preventing a workflow rehearsal from silently expanding into software.
- Added `stakeholder-feedback`, representative-session semantics, and a ready-to-run user-session plan to proof schema `1.1.0`.
- Added the handoff phase, review-handoff schema and example, business/PM-PO/delivery review tracks, and waiting-for-human semantics when representative evidence is missing.
- Added five sanitized behavioral regression cases targeting failures observed in a complex multi-role workflow trial. Synthetic agent trials do not count as business-user validation.
- Passed five isolated subagent regression runs covering incomplete current evidence, intake-first slicing, forced splitting, no-code rehearsal, stakeholder-feedback classification, review handoff, and waiting-state behavior. One stale evaluation hash chain was corrected before the run was accepted.
- Corrected repeat-install commands so existing skill destinations receive package contents rather than redundant nested skill directories.

### Workhorse usability audit

- Made shaping the single build-gate owner, preserved pending shapes for resume, and clarified same-conversation routing and unavailable-user behavior.
- Deferred decision-stage output mechanics until artifact creation and documented phase-local context loading.
- Added generated phase-artifact validation with an explicit project root; fixed legacy identity handling, source identity checks, predecessor phase consistency, critical-flag preservation, and pilot-review evidence gating.
- Added realistic requester/resume evaluation cases and explicit target-model evidence limits. No model-performance or release-readiness claim is added.

### Better Work Loop foundation

### Added

- Added the `0.3.0-alpha` Better Work Loop pack manifest and explicit-only `$better-work-loop`, `$shape-the-slice`, `$build-the-slice`, and `$prove-before-pilot` skills around the existing decision skill.
- Added versioned shape, build, proof, and loop-state JSON schemas with aligned Markdown contracts, stable IDs, predecessor SHA-256 references, one ordinary build gate, and append-preserving iteration history.
- Added a dependency-free maintainer fixture and end-to-end artifact chain that deliberately remains `agent-verified` until representative-user evidence exists.
- Added ten loop behavioral fixtures covering stop, insufficient evidence, non-code process rehearsal, build authorization, external effects, evidence honesty, critical failures, artifact drift, and v2.1 compatibility.
- Expanded repository validation and regression coverage across the five-skill pack, cross-artifact integrity, scenario and criterion coverage, evidence classifications, and transition invariants.

### Changed

- Updated `process-before-platform` to `0.3.0-alpha` and initiative schema `2.2.0` with a stable `initiative_id` and optional `prototype-shaping` handoff. Valid schema `2.1.0` packets remain accepted as legacy input without rewriting them.
- Updated `process-before-platform` to `0.2.2-alpha` with a lighter routing-first discovery path that closes safely with explicit evidence tasks instead of forcing every coverage question into the live conversation.
- Clarified the `reframe` versus `discovery-needed` tie-break and kept initiative fit separate from readiness.
- Made requester-weighted scorecards explicitly directional and withheld rankings until review and critical conditions are resolved.
- Strengthened scorecard validation for complete criterion coverage, ranking caveats, reviewed weights, and critical conditions; added regression coverage and a regulated high-risk behavioral fixture.
- Made stakeholder conversations and the readable handoff default to plain language, with a concise decision snapshot before detailed analysis.
- Defined submission readiness as “ready to send now,” prevented contradictory missing-field and do-not-submit states, and added regression tests.
- Required known conditional work to appear as a process branch while leaving unsupported recovery detail explicitly unmapped.
- Kept generated requests and evaluation runs out of source control by default, and clarified that behavioral tests must run as real turn-by-turn conversations.
- Declared the Apache-2.0 license, open-format compatibility boundary, author, and alpha version in validator-compatible skill metadata.
- Added installation guidance for Codex and Claude Code.
- Distinguished Claude Code import compatibility from behavior tested in the Codex reference environment.
- Added clean-history, cross-client claim, profile handoff, and post-publication vulnerability-reporting gates to the publishing checklist.
- Passed a clean-context Codex smoke test for the vague-request first turn: safety warning, no invented facts, one focused discovery question, and no premature JSON or packet.
- Clarified that the skills are built natively for Codex and can be imported into Claude Code with small setup changes, without claiming equivalent behavior.
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

The LinkedIn announcement remains owner-controlled.
