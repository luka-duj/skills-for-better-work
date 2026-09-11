<p align="center">
  <img src="assets/repository-header.png" alt="Skills for Better Work — from complexity to clearer decisions, with lukadujmovic.com" width="100%">
</p>

# Skills for Better Work

AI skills for PMs and workflow owners who need a clearer decision before committing to a tool or automation.

**Better Work Loop** helps both sides of an internal request understand the problem, decide whether anything should be built, shape the smallest useful test, build only that slice, examine the evidence, and prepare the next decision.

Built by [Luka Dujmovic](https://lukadujmovic.com/) around a simple principle: understand the work first, then build what helps people do it better.

> **Public alpha (`0.4.0-alpha`).** Built and tested natively in Codex. The same six skill folders can be imported into Claude Code with small setup changes: use Claude Code's skills folder and slash-command invocation, and adjust paths or tool permissions when the environment differs. Equivalent behavior is not claimed. The complete loop still needs representative-user evaluation.

[Install and try it](#install) · [See how the loop works](#better-work-loop) · [Use the decision skill only](#process-before-platform)

## Better Work Loop

`understand → decide → shape → build or rehearse → prove → hand off`

The result is not automatically “build more.” The loop can recommend stopping, adapting the process, retesting a smaller slice, or preparing a pilot review.

| Skill | What it helps you do |
|---|---|
| `better-work-loop` | Start and coordinate the complete loop. |
| `process-before-platform` | Decide whether to stop, change the process, use an existing capability, or test something. |
| `shape-the-slice` | Choose one user job and one uncertainty worth testing. |
| `build-the-slice` | Build or rehearse only the local slice you accepted. |
| `prove-before-pilot` | Separate technical checks from user evidence and recommend the next step. |
| `prepare-review-handoff` | Package the decision, test, limitations, and next user session for reviewers. |

The agent asks you to accept the concrete slice and evidence plan before building. It asks again only when the work would introduce a new cost, external effect, sensitive-data boundary, live-system change, deployment, or material increase in scope.

A prototype that runs is not automatically validated. Technical checks can establish `agent-verified`; only a representative person completing the target job and passing every critical boundary and downstream-use check can establish the deliberately narrow `validated` status. Missing user evidence leaves the loop waiting for a human review. Neither status approves a pilot or production deployment.

## Install

1. [Download the repository ZIP](https://github.com/luka-duj/skills-for-better-work/archive/refs/heads/main.zip) and extract it.
2. Follow the [installation guide](docs/installation.md) to copy all six skill folders without overwriting an existing installation.
3. Open a writable project and invoke the complete loop by name.

### Codex

Install the folders under `~/.agents/skills`, then invoke `$better-work-loop` from the skill selector or your prompt.

### Claude Code

Import the same folders under `~/.claude/skills`, then invoke `/better-work-loop`. Claude Code can read the shared `SKILL.md` packages; ignore the Codex-only `agents/openai.yaml` metadata and adjust paths or tool permissions if your environment differs.

See [compatibility and limitations](docs/compatibility.md) for the exact boundary.

## The six skills in detail

Each skill can be invoked directly when you already have the input from the previous phase. Use Better Work Loop when you want the collection to coordinate the complete journey.

### Better Work Loop

Use `better-work-loop` when an internal process, automation, or tooling request should move from an unclear starting point to a responsible next decision.

It helps the requester and receiving team:

- understand the current work before committing to a solution;
- coordinate the five specialist skills without repeatedly asking for the same context;
- preserve decisions, accepted scope, evidence, and unresolved questions between phases;
- stop, adapt, retest, or prepare a pilot review based on what the evidence supports.

It maintains a readable record of the loop and links the decision, shape, build, proof, and review artifacts. It does not approve budgets, architecture, pilot access, deployment, or production use.

Start the complete loop with:

```text
Use $better-work-loop to take this sanitized internal-workflow need through the smallest responsible test and evidence loop:

[Describe the outcome you need, the people involved, what happens today, and anything that must not change. Unknown details can stay unknown.]
```

Start with the problem in your own words; you do not need to choose a technology or prepare structured data. The agent asks focused questions, preserves important unknowns, and presents one concrete slice for acceptance before building or rehearsing it. To resume later, provide the path to the saved `loop-state.json` from the previous handoff.

### Process Before Platform

Use `process-before-platform` when a request arrives with a preferred tool or solution but the underlying work and outcome are not yet clear.

It helps the requester and receiving team:

- understand the outcome, affected people, current work, rules, handoffs, and exceptions;
- compare stopping, simplifying, using an existing tool, buying, automating, building, or running a bounded experiment;
- separate known facts from assumptions and important unknowns;
- decide whether to route the request, investigate further, reframe it, or stop it.

It creates a readable decision brief and a matching structured packet for the next team or phase. It does not approve initiatives, budgets, procurement, vendors, architecture, pilots, or production changes.

Use the decision skill by itself with:

```text
Use $process-before-platform to evaluate this sanitized internal tooling or automation request:

[Describe the request, desired outcome, current process, and known constraints.]
```

### Shape the Slice

Use `shape-the-slice` after the decision phase supports testing a process change, existing capability, configuration, integration, automation, or custom build.

It helps the requester and receiving team:

- choose one risky assumption that can change the next decision;
- select one representative user and one complete job to test;
- find the earliest useful handoff or decision instead of prototyping an entire workflow;
- choose the lightest useful format: a rehearsal, clickable prototype, runnable slice, or configuration sandbox;
- agree on boundaries, non-goals, critical scenarios, and the evidence needed before building.

It creates an inspectable shape brief and asks the owner to accept, revise, or reject that exact slice. It does not build the prototype, choose unneeded technology, or turn later possibilities into current scope.

### Build the Slice

Use `build-the-slice` when a Shape the Slice brief has an accepted build gate.

It helps the requester and delivery team:

- build or rehearse only the accepted capabilities and user job;
- keep a process rehearsal non-technical when code would not improve the learning;
- include the important exceptions, refusal behavior, fallback, and downstream handoff;
- verify what works technically and record what remains incomplete;
- keep live systems, sensitive data, paid services, and deployment outside the ordinary prototype.

It creates the bounded prototype or rehearsal plus a readable build report and matching structured record. It does not expand the scope, deploy the result, or claim that technical success proves user value.

### Prove Before Pilot

Use `prove-before-pilot` after a prototype or rehearsal exists and the team needs to understand what it actually demonstrates.

It helps the requester and review team:

- check the result against the original hypothesis, user job, boundaries, and success criteria;
- separate technical checks, agent-run scenarios, stakeholder feedback, and observed user behavior;
- test normal work, exceptions, missing information, contradictions, refusals, fallback, and downstream use;
- keep failed, disputed, and untested evidence visible;
- recommend stopping, revising the process, adapting the prototype, retesting, or preparing a pilot review.

It creates a proof report and, when user evidence is missing, a ready-to-run session plan. It does not invent user feedback, treat a working demo as validation, or approve a pilot.

### Prepare Review Handoff

Use `prepare-review-handoff` after proof when business, PM/PO, and delivery reviewers need one decision-ready package rather than a chain of disconnected files.

It helps the review group:

- see the current process, stakeholder-stated ideal, and proposed target process without confusing one for another;
- understand the selected slice, excluded work, prototype location, and evidence level;
- review the outcome from business, product, and delivery perspectives;
- carry unresolved decisions, failed checks, and the next user session forward;
- resume the loop without reconstructing the previous work.

It creates a readable review handoff and matching structured record, then connects it to the saved loop state. It does not strengthen weak evidence, design an unapproved architecture, or authorize implementation, a pilot, or production use.

In Claude Code, use the same skill names with slash-command syntax—for example, `/shape-the-slice`—after following the [Claude Code installation guidance](docs/installation.md#claude-code).

## Feedback and maintenance

[Report a reproducible problem](https://github.com/luka-duj/skills-for-better-work/issues/new/choose) using a fully sanitized case. Include what you tried, what happened, and what you expected. Use [private vulnerability reporting](SECURITY.md) for security issues.

Luka maintains this project on a best-effort basis, with no response SLA or guarantee that a proposal will be accepted. [Contribution guidance](CONTRIBUTING.md) explains the scope.

## For maintainers

See the [technical guide](docs/technical-guide.md) for the package map, output contracts, evaluation fixtures, and validation commands. Python is needed only for repository checks, not to install or use the skills.

## About the author

Built by [Luka Dujmovic](https://lukadujmovic.com/), an AI-native Product Manager, Enterprise Product Owner, and builder. I start with the work and the people doing it, then decide where technology earns its place.

If this is useful, star the repository so you can find it again.

## License

Apache License 2.0. See [LICENSE](LICENSE).
