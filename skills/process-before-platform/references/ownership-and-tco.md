# Ownership and Total Cost

Use this reference when a technology path remains plausible. The purpose is to expose the product that must exist after the first release, not to manufacture an exact business case.

## Ownership map

For each plausible option, identify the responsible owner or mark it unknown for:

- product and process decisions;
- design and accessibility;
- software development or configuration;
- data quality, migration, retention, and deletion;
- integrations and upstream/downstream change;
- identity, permissions, audit, security, privacy, legal, and compliance;
- environments, hosting, deployment, backups, and disaster recovery;
- quality assurance, evaluation, and release acceptance;
- logs, monitoring, alerting, incidents, rollback, and service health;
- user support, training, documentation, adoption, and feedback;
- vendor management, licensing, renewals, usage limits, and price changes;
- maintenance, upgrades, technical debt, roadmap, and capacity;
- portability, replacement, data export, shutdown, and retirement.

Do not describe custom software as owned merely because someone can build the first version.

## Cost inputs

Keep monetary estimates in one declared currency and one declared horizon. Ask for ranges when uncertainty is material.

Possible one-time inputs:

- discovery and process redesign;
- procurement and legal/security review;
- licenses or setup fees;
- design, development, configuration, testing, and data work;
- integration and migration;
- rollout, training, communication, and transition;
- internal hours by role and loaded rate.

Possible recurring inputs:

- subscriptions, usage, hosting, storage, models, and observability;
- support, operations, incident response, security review, and compliance;
- maintenance, upgrades, regression testing, documentation, and vendor management;
- internal hours by role and loaded rate;
- expected replacement, exit, or retirement work.

## Range calculation

Calculate each scenario only from user-supplied or cited inputs:

`internal resource cost = sum(hours by role × loaded rate by role)`

`TCO = one-time cost + recurring cost across the stated horizon + internal resource cost + stated exit/retirement cost`

Use `low`, `base`, and `high` scenarios when inputs support them. Record source, date, confidence, and whether a value is quoted, estimated, or observed.

If the horizon, currency, rate, quantity, or recurring assumption is missing, do not silently choose one. Return `insufficient-inputs` and the ownership map.

## Comparison cautions

- Include process-change and adoption costs for every option, including buying.
- Separate a vendor list price from configured, integrated, operated cost.
- Separate first-release effort from ongoing ownership.
- Separate saved time from realized financial value. Time has value only when the organization can explain what changes as a result.
- Do not annualize a demo or short test as realized value.
- Do not run a full ROI, NPV, IRR, or payback analysis unless the user supplies the required financial inputs or requests a separate finance workflow.
