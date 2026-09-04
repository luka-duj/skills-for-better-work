# Vendor Research

Use this branch only when `buy-or-configure` remains a credible direction after process and option assessment.

## Research brief

Before searching, make these fields explicit:

- decision and intended users;
- required capabilities and material exceptions;
- geography, language, accessibility, scale, and evaluation date;
- systems, data types, integrations, identity, permissions, audit, and retention;
- security, privacy, legal, compliance, procurement, hosting, and residency constraints;
- budget assumptions and total-cost horizon, if known;
- implementation capacity, support model, and required time to operation;
- disqualifiers and acceptable compromises;
- expected shortlist depth and evidence standard.

Ask only for missing fields that can materially change the shortlist. Label unknowns rather than filling them.

## Deep Research handoff

If the user already requested Deep Research and `$deep-research` is available, pass the complete brief to it. Otherwise, show the scope and ask the user to confirm the substantial research run.

Require the research result to:

- search current, decision-relevant sources;
- prioritize official product, pricing, security, privacy, compliance, API, integration, support, status, and contract documentation;
- use independent evidence where first-party claims cannot establish operational fit;
- compare definitions, versions, geography, limits, and update dates;
- identify contradictions and unavailable evidence;
- cite every material vendor claim near the claim;
- explain why each shortlisted vendor was included and why plausible alternatives were excluded;
- stop when another search is unlikely to change the shortlist or confidence materially.

Treat reviews, directories, analyst lists, forums, and vendor comparisons as discovery signals unless their methods and applicability are clear.

## Bounded fallback

When `$deep-research` is unavailable but browsing is available:

1. search official sources for the required capabilities and constraints;
2. build a small plausible candidate set rather than claiming a complete market scan;
3. verify the most consequential capability, price, security, integration, and geography claims;
4. search for evidence that disconfirms the leading candidate;
5. disclose the searches, gaps, and reduced depth.

When browsing is unavailable, return the research brief and evaluation matrix with `research-status: not-run`. Do not supply a remembered shortlist.

## Research output

Return:

- research scope, date, geography, and limitations;
- shortlisted vendors with inclusion reasoning;
- excluded or deferred vendors with reasoning;
- evidence table with source, claim, confidence, and access date;
- unresolved pricing, implementation, security, legal, and fit questions;
- tailored demo, proof-of-concept, reference-customer, procurement, and exit questions;
- implications for the shared option scorecard;
- what evidence remains necessary before selection.

Do not rank a vendor from marketing breadth, popularity, or a feature checklist alone. The shortlist informs human procurement and technical review; it does not approve a vendor.
