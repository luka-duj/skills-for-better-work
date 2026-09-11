---
name: build-the-slice
description: Build and technically verify one explicitly accepted internal-workflow prototype slice from a Shape the Slice brief. Use only when the user explicitly invokes $build-the-slice or the Better Work Loop routes an accepted build gate. Reuse a nominated stack or choose the simplest local implementation that tests the hypothesis; do not deploy or change live systems.
license: Apache-2.0
metadata:
  author: "Luka Dujmovic"
  version: "0.4.0-alpha"
  compatibility: "Agent Skills format; built and evaluated natively in Codex; requires referenced-file, local filesystem, and suitable build-tool access. Generated technology varies by context and client."
---

# Build the Slice

Create the accepted prototype as a small, inspectable vertical slice. Optimize for learning and downstream use, not generated-code volume or visual polish.

## Start

1. Read [build and output contract](references/build-and-output.md).
2. Load and validate the prototype brief. Verify its source path and SHA-256 digest when present.
3. Require `status = ready-to-build` and `build_gate.status = accepted`. Otherwise stop without creating prototype source.
4. Inspect the destination and approved fidelity before choosing technology. For `workflow-simulation`, create a role-and-decision rehearsal first. Use code only when `prototype.code_required = true` and the brief records the interaction or logic reason. Reuse a stack only when the user nominated that repository; otherwise use the simplest contained local format that can test the hypothesis.
5. Re-derive implementation checks from the brief's criteria and scenarios before writing code. Do not derive the definition of success from the implementation.

## Build

1. Implement only the stated capabilities, selected target-process nodes, and critical boundaries.
2. Use synthetic or sanitized data. Simulate writes to external systems unless a separate request explicitly authorizes a suitable sandbox.
3. Make the complete target job exercisable, including the useful output or handoff—not merely a landing page, scaffold, or disconnected screens.
4. Include visible, privacy-safe feedback for success and failure. Add only the instrumentation needed by the evidence plan.
5. Preserve an easy fallback or reset when the slice can change state.
6. Do not add authentication, production infrastructure, analytics services, paid dependencies, or vendor integrations unless the accepted brief requires them and the user separately authorizes the consequence.

## Verify

- Run the smallest relevant static, unit, integration, accessibility, or browser checks supported by the prototype.
- Exercise every critical acceptance criterion and scenario that can be checked without a representative user.
- Record the exact commands and observed outcomes. Do not mark a check passed when it was not run.
- Classify the result `built-and-verified`, `built-with-gaps`, `blocked`, or `not-built`.

## Deliver

Create the rehearsal or prototype plus `build.md` and `build.json` defined in [build and output contract](references/build-and-output.md). Record the delivered format and whether code was used. Link the exercisable entrypoint, readable report, and JSON. Do not call the result validated; that judgment belongs to `$prove-before-pilot`.

## Guardrails

- Stop when the predecessor changed, the gate is absent, or implementation would cross an unapproved external boundary.
- Treat generated tests as technical evidence, not user evidence.
- Do not silently expand scope to make the prototype appear complete.
- Do not describe a local build, vendor demo, or deployed preview as production evidence.
