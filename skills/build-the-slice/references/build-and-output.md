# Build and Output Contract

## Destination

Default to `<loop-root>/slices/<iteration>/prototype/`. Use an existing repository only when the accepted brief names `nominated-existing-repository` and the user has authorized the requested local changes. Preserve unrelated worktree changes.

Context-adaptive technology selection follows this order:

1. use a documented or facilitated role-and-decision rehearsal for `workflow-simulation`; code is allowed only when the accepted shape says it is necessary to test interaction or logic;
2. use dependency-light static files for a contained clickable interaction;
3. use the nominated repository's existing stack for a runnable vertical slice;
4. introduce a new framework or dependency only when it materially enables the test.

No deployment or live-system write is part of ordinary build completion.

## Output

Write `build.md` and `build.json` beside `prototype/`. If a build artifact already exists, create a timestamped retry and keep the earlier evidence.

Start Markdown with **Build result**: what can now be exercised, the delivered format, whether code was used and why, technical status, how to run it, what remains unverified, and important cautions. Then include implemented capabilities, target-process coverage, files, commands, verification, scenario coverage, instrumentation, external effects, gaps, assumptions, and uncertainties.

The JSON must conform to `../schemas/prototype-build.schema.json`. Reference the exact shape artifact by path and SHA-256 digest. Use the criterion and scenario IDs from the shape brief.

`external_effects.live_writes` and `external_effects.deployed` must remain `false` for a normal local prototype. If either would become true, set `requires_separate_authorization = true`, stop before the effect, and report `blocked` or `built-with-gaps`.
