# Technical guide

## Repository map

- `pack.json` — pack order, version, schemas, and reference-environment boundary.
- `skills/` — six independently invocable skills with local references and schemas.
- `examples/better-work-loop/` — maintainer fixtures for end-to-end artifact-chain validation.
- `evals/` — decision and loop behavioral fixtures plus the manual forward-test protocol.
- `scripts/validate.py` — dependency-free structural, schema, transition, digest, and example validation.
- `tests/` — regression tests for the validator and example packet.
- `launch/` — publication checklist, milestone series, and optional announcement draft.

## Validate

With Python 3.11 or newer:

```bash
python scripts/validate.py
python -m unittest discover -s tests
```

The validator checks all six packages, links, JSON Schema subsets, aligned Markdown and JSON, predecessor hashes, transition rules, initiative and loop invariants, all three process-view contracts, review handoff consistency, score calculations, and evaluation fixture structure. Behavioral quality still requires clean-context forward tests against both evaluation sets.

The repository includes evaluation fixtures for maintainers. Consult the [evaluation protocol](../evals/README.md); fixture-based runs do not establish representative-user validation or business impact.

To check a generated phase artifact, keep a repository checkout available and run:

```bash
python scripts/validate.py --artifact /path/to/project/output/better-work-loop/my-loop/slices/01/proof.json --kind proof --project-root /path/to/project
```

Use `shape`, `build`, `proof`, `handoff`, or `loop` for `--kind`. Recorded relative paths resolve from `--project-root`, not the skill installation folder. The checker verifies structure and evidence-chain consistency; it cannot establish that a reported human observation actually happened. Copying just the skill folders does not install this repository checker. Without it, the agent must check the local schemas and report that automated chain validation was unavailable.


[Output contract](../skills/process-before-platform/references/output-contract.md) · [Evaluation protocol](../evals/README.md) · [Back to the README](../README.md)
