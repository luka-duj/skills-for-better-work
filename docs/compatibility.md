# Compatibility and limitations

The pack is built and tested natively in Codex. It uses the [Agent Skills open format](https://agentskills.io/specification), so the same complete skill folders can also be imported into Claude Code with small setup changes.

| Client | What changes |
|---|---|
| Codex | Install under `~/.agents/skills` and invoke with `$better-work-loop`. This is the reference environment for the repository's tests and behavioral evaluations. |
| Claude Code | Install under `~/.claude/skills` and invoke with `/better-work-loop`. Ignore the Codex-only `agents/openai.yaml` metadata. Adjust paths or tool permissions when the environment differs. |

Using the same instruction packages does not guarantee identical behavior across models or clients. The complete loop has not been behaviorally verified in Claude Code, so review consequential outputs and keep generated artifacts in a writable, sanitized project.

## Human ownership

The skills help prepare decisions. They do not approve procurement, budgets, architecture, initiatives, pilot access, or production changes. A plausible result still needs review by the responsible person. No claim of measured ROI, adoption, or production readiness is made.

## Sources

Installation guidance checked September 11, 2026 against [OpenAI's local skill locations](https://learn.chatgpt.com/docs/build-skills) and [Claude Code's skill documentation](https://code.claude.com/docs/en/skills). Recheck these sources if your installed client behaves differently.

[Return to the README](../README.md)
