# Shape and Output Contract

## Inputs

Prefer a Better Work Loop initiative packet. Accept schema `2.3.0` directly. Accept `2.2.0` and `2.1.0` as legacy inputs; preserve `initiative_id` when present and derive it for `2.1.0`. Plain-language input is allowed when it contains enough supported decision evidence; record `source_type = plain-language` with null path, digest, and schema version. Otherwise route to `$process-before-platform`.

For standalone shaping without a router, choose a collision-safe loop ID, start at iteration 1, and use `output/better-work-loop/<loop-id>/slices/01/` within the current project. Preserve an existing initiative ID; for plain-language input assign a stable local ID and label it locally assigned in assumptions. Do not invent a source packet or create loop-state when no source initiative packet exists. A later build can consume the accepted shape directly.

For legacy input, use `legacy-` plus the first 16 hex characters of SHA-256 of the UTF-8 string `<recorded path>\n<file digest>`. Keep the exact recorded path and derived ID on subsequent phases.

## Readiness

- `ready-to-build`: one decision, source problem, selected handoff or decision, role chain, one primary user/job, one independently testable uncertainty, fidelity, slice, critical boundaries, scenarios, acceptance criteria, data constraints, and evidence plan are clear; the split assessment preserves any `must-split` decision about the source request and says the selected slice itself fits one slice.
- `needs-evidence`: shaping exposed a missing fact that could reverse the slice or make testing unsafe.
- `stopped`: the owner rejected the slice or the supported decision no longer justifies a prototype.

Build-gate status is separate from readiness. A ready shape can remain `pending`; `$build-the-slice` requires `accepted`.

## Output

Write an aligned pair named `shape.md` and `shape.json` under the active slice directory. If a phase artifact already exists, add a local-time suffix rather than overwrite it.

Start Markdown with **Shape decision**: what is being tested, which source problem and handoff it addresses, why this primary role and fidelity are appropriate, what source scope was split, what is excluded, whether the build gate is accepted, and what happens next. Then include the role chain, source and selected-slice split decisions, target-process coverage, target job, slice, scenarios, acceptance criteria, boundaries, evidence plan, assumptions, and uncertainties.

The JSON must conform to `../schemas/prototype-brief.schema.json`. Reference the source initiative by path and SHA-256 digest. Use stable target-process node, criterion, and scenario IDs so build, proof, and handoff artifacts can map back without relying on wording.
