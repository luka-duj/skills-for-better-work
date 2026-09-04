# Application Evidence Gate

The future application is not an active implementation scope. It requires evidence that a conversational skill cannot handle a recurring job well enough.

## Start app discovery only when

All of the following are true:

1. The same limitation appears in at least three independent, sanitized uses.
2. The limitation concerns saved state, evidence-task tracking, requester-reviewer collaboration, reviewer weight confirmation, option comparison, decision history, vendor-research records, or workflow export.
3. At least one product or automation reviewer confirms that solving the limitation would materially improve the handoff or decision.
4. The limitation cannot be fixed responsibly through clearer questions, references, or output behavior in the skill.
5. A separate app-discovery scope and implementation plan receive owner approval.

Stars, impressions, downloads, and general enthusiasm do not satisfy this gate by themselves.

## Working app hypothesis

If the gate is met, explore a separate, self-hostable web application with:

- a guided requester experience;
- evidence tasks with owners and completion evidence;
- reviewer confirmation of criteria and weights;
- option and ownership comparison;
- an inspectable decision and change history;
- vendor-research provenance;
- controlled exports to team systems where justified;
- organizational control of deployment and sensitive data.

Do not select the architecture, hosting stack, integrations, commercial model, or data-retention design until discovery establishes user, security, operational, and self-hosting requirements.

## Evidence record

For each independent use, record only sanitized information:

`date | user type | decision context | skill outcome | observed limitation | workaround | reviewer consequence | repeat category | app implication`

Keep raw internal requests and generated packets outside the repository.
