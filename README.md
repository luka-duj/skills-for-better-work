<p align="center">
  <img src="assets/repository-header.png" alt="Skills for Better Work — from complexity to clearer decisions, with lukadujmovic.com" width="100%">
</p>

# Skills for Better Work

Practical AI skills for turning complex work into clearer decisions, better systems, and AI that earns its place.

The packages follow the [Agent Skills open format](https://agentskills.io/specification), so they can be installed in compatible clients including Codex and Claude. They are designed, exercised, and maintained in Codex. Codex is the reference environment and the only client covered by this repository's documented behavioral evaluations today.

Built by [Luka Dujmovic](https://lukadujmovic.com/) around a simple principle: understand the work first, then build what helps people do it better.

> **Status:** Public alpha (`0.2.2-alpha`). The method and output contract are usable and tested in Codex, but the collection is still evolving. Use sanitized context, review consequential decisions with the accountable people, and expect behavior to vary in other clients.

## Compatibility

| Client | Support in this repository |
|---|---|
| Codex | Native reference environment. Installation, automated validation, and behavioral evaluation guidance are maintained for Codex first. |
| Claude Code | Compatible with the shared Agent Skills package format. Installation is documented below; equivalent runtime behavior has not yet been claimed or verified here. |
| Claude.ai | The skill folder can be uploaded as a ZIP through the Skills settings. Tool access and output behavior depend on the Claude environment. |
| Other Agent Skills clients | The package may be portable when the client supports the open format, referenced files, and required filesystem operations. Check the client's installation and invocation rules. |

Compatibility describes package format, not identical behavior. Test the skill in your chosen client before using it for consequential work. The Codex-specific `agents/openai.yaml` file provides interface metadata and explicit-invocation policy for Codex; other clients can ignore it.

## Available skill: Process Before Platform

`process-before-platform` helps business requesters and PMs turn a rough internal process, tooling, or automation request into a clearer next decision before anyone commits to software.

It uses everyday language and asks only for information that can change the direction, expose an important risk, or improve the handoff. Its default is simple: understand and improve the work before choosing a tool. When the process genuinely cannot be learned without trying a capability, it can instead recommend a small, reversible experiment.

It helps the requester and receiving team:

- understand the outcome, affected people, and evidence;
- see how the work, systems, handoffs, rules, and exceptions fit together;
- compare stopping, simplifying, using existing tools, buying, automating, building, or testing on a small scale;
- make ownership and important unknowns visible;
- decide whether to route the request now, investigate further, reframe it, or stop it.

It does not approve initiatives, procurement, budgets, vendors, or architecture.

## Use it

The skill is intentionally explicit-only. Invoke it by name:

```text
Use $process-before-platform to evaluate this internal tooling request:

[Paste a sanitized request or describe the situation.]
```

The skill runs an adaptive questionnaire first. It asks one primary question per round and does not emit JSON while answers are still being collected. Once the questionnaire is complete—or the requester explicitly closes it with remaining unknowns recorded as evidence tasks—it writes two sibling files under `<current-project>/output/process-before-platform/`:

- a plain-language Markdown brief that starts with the recommendation, reason, handoff status, next action, and cautions;
- a vendor-neutral JSON initiative packet conforming to schema version 2.1.0;
- an evidence-gated BPMN-style Mermaid process diagram embedded in Markdown and preserved as source in JSON;
- visible facts, assumptions, unknowns, and evidence tasks;
- a comparison of credible process and technology options;
- an ownership and total-cost view where inputs support it;
- a current direction, confidence, caveats, and blocking conditions.

The artifacts are generated once at the end of the completed questionnaire, not at invocation or after every answer. Existing files are never overwritten. Target-system field mappings are included only when exact metadata is known, and the skill never creates the remote ticket without a separate explicit request.

See the [synthetic approval-portal walkthrough](skills/process-before-platform/examples/synthetic-approval-portal/README.md) for a complete example.

## Install

### Codex

Copy the skill folder into your Codex skills directory, then restart or reload Codex if needed.

PowerShell:

```powershell
Copy-Item -Recurse .\skills\process-before-platform "$env:USERPROFILE\.codex\skills\process-before-platform"
```

macOS or Linux:

```bash
cp -R ./skills/process-before-platform ~/.codex/skills/process-before-platform
```

Invoke it explicitly as `$process-before-platform`.

### Claude Code

Copy the same folder into your personal Claude skills directory.

PowerShell:

```powershell
Copy-Item -Recurse .\skills\process-before-platform "$env:USERPROFILE\.claude\skills\process-before-platform"
```

macOS or Linux:

```bash
cp -R ./skills/process-before-platform ~/.claude/skills/process-before-platform
```

Invoke it as `/process-before-platform`. Claude Code reads the shared `SKILL.md` and referenced files; the Codex-specific interface metadata is not required.

### Claude.ai

Create a ZIP archive of the `skills/process-before-platform` folder, then upload it under **Settings → Capabilities → Skills**. Confirm the current upload and tool requirements in Anthropic's documentation before relying on it.

### Other compatible clients

Install the `skills/process-before-platform` folder using the client's Agent Skills instructions. Invocation syntax, permissions, and filesystem access vary by client.

## Repository map

- `skills/process-before-platform/` — installable skill, references, schema, icons, and example.
- `evals/` — synthetic behavioral cases and the manual forward-test protocol.
- `scripts/validate.py` — dependency-free structural and contract validation.
- `tests/` — regression tests for the validator and example packet.
- `launch/` — publication checklist, milestone series, and optional announcement draft.

## Validate

With Python 3.11 or newer:

```bash
python scripts/validate.py
python -m unittest discover -s tests
```

The validator checks the skill package, links, JSON Schema subset, aligned synthetic Markdown and JSON initiative artifacts, BPMN-style diagram evidence and step coverage, required solution-ladder coverage, system references, score calculations, and evaluation fixture structure. Behavioral quality still requires forward-testing the skill against the cases in `evals/`.

## Feedback

Use the issue templates for reproducible behavior problems and method proposals. Describe only synthetic or fully sanitized situations. Never paste a real internal request, generated initiative packet, vendor document, or screenshot unless you have authority to make every detail public.

GitHub Discussions and a private feedback channel are deliberately deferred until publication and demonstrated need.

## License

Apache License 2.0. See [LICENSE](LICENSE).
