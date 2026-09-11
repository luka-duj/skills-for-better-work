# Security and Data Safety

Skills for Better Work contains prompt-based decision aids and local prototype workflows. The pack does not provide a secure storage, execution, deployment, or access-control boundary for internal information.

## Safe use

- Follow your organization's rules for AI tools, data classification, procurement, and access.
- Remove confidential business context, personal data, credentials, security details, private architecture, and protected vendor material before using the skill.
- Treat generated recommendations, vendor comparisons, effort ranges, and scores as decision support requiring human review.
- Verify current vendor, legal, compliance, pricing, and security claims from authoritative sources.
- Build with synthetic or sanitized data by default. Inspect generated prototype source and dependencies before running it.
- Keep live writes, external services, deployment, credentials, paid resources, and sensitive-data tests outside the ordinary Better Work Loop. They require a separate explicit request and the relevant organizational approvals.
- Treat `agent-verified` and `validated` as bounded evidence labels, not security review, pilot approval, production readiness, or assurance that every failure mode was found.
- Do not store participant identity, raw user-test transcripts, screenshots, or sensitive inputs in proof artifacts by default.

## Reporting a vulnerability

Use GitHub's private [Report a vulnerability](https://github.com/luka-duj/skills-for-better-work/security/advisories/new) route. Private vulnerability reporting is enabled for this repository. Do not include exploit details, credentials, or real organizational data in a public issue, discussion, or website contact form.
