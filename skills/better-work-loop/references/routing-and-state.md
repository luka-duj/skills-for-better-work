# Routing and State

## Direction routing

| Process direction | Loop action |
|---|---|
| `eliminate-or-stop` | Record the decision and end without shaping or building. |
| `insufficient-evidence` | Keep the loop in decision discovery and surface the smallest evidence tasks. |
| `process-redesign` | Shape a workflow simulation, service rehearsal, or interface only when it tests a material uncertainty. |
| `use-existing-capability` | Shape a configuration or workflow test; do not change the live tool without separate authorization. |
| `buy-or-configure` | Shape a vendor-sandbox test only when access and authority exist; otherwise preserve a test brief. |
| `integrate-or-automate` | Shape the smallest end-to-end automated slice with simulated external writes by default. |
| `custom-build` | Shape one differentiated vertical slice; do not broaden it into the envisioned full product. |
| `co-evolve-through-experiment` | Shape a reversible process-and-tool experiment with fallback and a stop decision. |

## Loop location

Use `<current-project>/output/better-work-loop/<loop-id>/` with:

```text
loop-state.md
loop-state.json
slices/
  01/
    shape.md
    shape.json
    prototype/
    build.md
    build.json
    proof.md
    proof.json
    review-handoff.md
    review-handoff.json
```

Use a short, collision-safe loop ID such as `<YYYY-MM-DD>-<initiative-slug>-<suffix>`. Each JSON artifact records its predecessor path and SHA-256 digest. Do not silently accept a changed predecessor.

`loop-state.md` and `loop-state.json` are the only mutable summaries. Preserve their complete transition and decision history. Write updates atomically when the environment supports it. Phase artifacts are immutable; a retry that changes evidence receives a new timestamped file, and a changed hypothesis receives a new numbered slice.

## Loop states

- Phases: `decide`, `shape`, `build`, `prove`, `handoff`, `complete`.
- Statuses: `active`, `waiting-for-human`, `blocked`, `completed`, `stopped`.
- Build gate: `pending`, `accepted`, or `rejected`.
- Current decisions: `continue-decision-discovery`, `shape-slice`, `decide-build-gate`, `build-accepted-slice`, `seek-user-evidence`, `prepare-review-handoff`, `stop`, `revise-process`, `adapt-prototype`, `retest`, or `prepare-pilot-review`.

The loop state points to evidence; it does not replace specialist artifacts. Use `null` for an unavailable owner, path, digest, or decision rather than inventing a value.

## Resume and artifact mechanics

- During initial discovery, keep a prose recap until an initiative packet exists; the loop-state contract requires that source packet. Do not fabricate a path to satisfy the schema.
- On resume, read loop-state, then only the current phase's predecessor artifacts. Verify their recorded digests before continuing. Reuse an accepted gate for unchanged scope. If the next step needs a missing answer, ask that question without restarting discovery.
- After writing a ready shape with a pending gate, record phase `shape`, status `waiting-for-human`, and decision `decide-build-gate`. The next action must identify the exact shape pair and ask the owner to accept, revise, or reject it.
- Record paths relative to the current project root, using `/` separators, or absolute paths when necessary. Compute SHA-256 from the saved file bytes with an available runtime; never invent or manually transcribe a digest. Save a predecessor before hashing it.
- For a legacy 2.1.0 packet, use `legacy-` plus the first 16 hex characters of SHA-256 of the UTF-8 string `<recorded path>\n<file digest>`. Label the ID as derived in the decision history. Preserve that recorded path and ID on resume; do not rewrite the legacy packet.
- Read the current phase's schema when serializing its output. Missing knowledge stays null or an evidence task as the schema permits; examples supply structure, never facts or approvals.
- If no execution or file tools exist, deliver a readable decision and next action in chat and state that durable artifacts and technical verification were not completed. Do not claim a saved or verified loop.
- After proof, create the review handoff. `adapt-prototype` and `retest` do not authorize unlimited retries. Continue a requested revision within the accepted slice; a changed hypothesis or material boundary needs a new slice and gate.
- When `retest` is caused by missing representative-user evidence, record phase `handoff`, status `waiting-for-human`, and decision `seek-user-evidence` after the handoff exists. The handoff must contain a runnable session plan and exact resume instruction.
- Use `completed` only for a deliberate stop, an explicitly closed iteration, or a `prepare-pilot-review` handoff. A future human task is not completed work merely because the agent cannot perform it alone.
