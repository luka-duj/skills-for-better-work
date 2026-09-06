# LinkedIn Alpha Release Draft

> **Private draft — do not publish yet.** Replace `[PUBLIC_REPOSITORY_URL]` only after the repository is deliberately made public and the publishing checklist passes.

## Final post

A broken process does not improve when you give it a UI.

It becomes easier to repeat.

Internal tooling requests often begin with a specific solution: a new portal, an automation, an AI assistant.

The reasonable-sounding next step is to show people the tool and define the process around it later.

That can work when the tool enables a genuinely new way of working. More often, it turns disputed rules, unnecessary approvals, unclear ownership and undocumented exceptions into software someone now has to maintain.

So I built **Process Before Platform**, an open Agent Skill for examining internal tooling and automation requests before a team commits to a solution.

I build and evaluate it natively in Codex. The package follows the open Agent Skills format, so it can also be installed in Claude Code and other compatible clients; tool access and behavior can vary by environment.

It helps a requester work through five questions:

1. Is this process or obligation still necessary?
2. What can be removed, simplified or standardised first?
3. What evidence shows the problem, frequency and consequence?
4. Should we use something we already own, buy, configure, integrate, automate, build, or test process and technology together?
5. Who will own security, infrastructure, quality, support, change, incidents, upgrades and retirement after the first release?

The output is a ticket-ready Markdown initiative request and a portable JSON packet. It documents the manual process, existing systems, information sources, and codified or person-held knowledge before completing the solution ladder. Missing answers become evidence tasks. They do not become plausible-sounding assumptions.

The first walkthrough uses a completely synthetic request for a custom approval portal. The initial solution changes because the approval rules, exceptions and ownership are not stable enough to encode responsibly.

The alpha is here: [PUBLIC_REPOSITORY_URL]

Try it on a sanitised internal request and tell me where the questions, direction or handoff fail. Please keep real company and customer information out of public issues.

## Evaluation

Hard gates:

- Truth and ownership: pass. The post uses Luka's stated point of view and the implemented synthetic example; it makes no private case or performance claim.
- Confidentiality: pass. It contains no employer, customer, system, vendor, or internal-program details.
- Thesis clarity: pass. The first three lines state the mechanism and the body stays on that idea.
- Originality: pass. No creator wording, story, or result is borrowed.
- CTA alignment: pass after publication. It asks for a sanitized real-request test and failure report.

Quality score: 37/40

- Hook: 5
- Relevance: 5
- Specificity: 5
- Credibility: 4
- Useful payload: 5
- Structure: 5
- Voice: 4
- Close: 4

Credibility and voice should be reassessed after Luka reads the final public repository and adjusts any wording he would not defend in conversation.

## Confirm before publishing

- Repository visibility is public by a separate owner-approved action.
- The public repository URL replaces the placeholder and opens without authentication.
- Installation instructions work from a clean environment.
- The repository distinguishes Codex-native evaluation from cross-client format compatibility and makes no unsupported parity claim.
- The repository contains no private source, internal case, credentials, or non-public artifacts.
- GitHub Issues and any Discussions category display the redaction warning.
- The final pasted copy and link preview are checked in LinkedIn.
