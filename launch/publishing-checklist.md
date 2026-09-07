# Publishing Checklist

Repository visibility and announcement remain separate owner-controlled actions. The public-alpha package can be prepared while private; checks that require unauthenticated access must happen immediately after the visibility switch and before announcement.

Last audited: 7 September 2026. Checked items reflect verified repository state, not authorization to publish.

## Repository

- [x] Review the complete reachable Git history for private or employer-specific information, copied third-party packages, and files that were later reverted.
- [x] Confirm the public default branch does not retain the reverted `imagegen` and `product-design` package import in its reachable history.
- [x] Confirm the repository contains only generalized methods and synthetic examples.
- [x] Run `python scripts/validate.py` and `python -m unittest discover -s tests` against the release candidate.
- [x] Review five full synthetic packets spanning standard change, privacy discovery, bounded experiment, stop, and buy-or-configure outcomes; validate each final JSON packet.
- [ ] Before announcement, complete two genuine turn-by-turn requester tests: one straightforward operational request and one high-risk privacy or compliance request.
- [x] Confirm the Apache-2.0 license and attribution.
- [x] Confirm `SKILL.md` name, description, license, and metadata pass both the Codex package validator and relevant Agent Skills checks.
- [x] Confirm icons, header, internal links, and installation commands are present and consistent with the package layout.
- [x] Test installation and explicit first-turn invocation in a clean Codex environment.
- [x] Test each additional client named as behaviorally supported; otherwise describe it only as format-compatible.
- [x] Keep GitHub Issues enabled with structured, sanitization-aware templates; defer Discussions until there is a moderation need and owner.
- [x] Verify the repository description and topics without unsupported claims.
- [ ] Change visibility to public only through the owner's deliberate switch.

## Immediately after the visibility switch

- [ ] Enable private vulnerability reporting and verify the route linked from `SECURITY.md`.
- [ ] Verify the repository, README assets, and raw skill files open without authentication.
- [ ] Confirm the default branch and latest GitHub Actions validation are green.
- [ ] Create the first tagged release only after the public state is verified.

## LinkedIn

- [x] Put the final repository URL in the prepared LinkedIn draft.
- [ ] Change the GitHub profile README from private alpha to public alpha and link the repository.
- [ ] Pin the repository when GitHub profile permissions allow it.
- [ ] Re-run truth, ownership, confidentiality, originality, usefulness, voice, and CTA gates.
- [ ] Confirm no real internal case can be inferred from the wording.
- [ ] Check the final post and link preview in the LinkedIn composer.
- [ ] Publish only after an explicit owner instruction covering the final copy.

## After release

- [ ] Keep public feedback sanitized; remove or privately report accidental disclosures promptly.
- [ ] Record meaningful behavior changes in `CHANGELOG.md` and a matching evaluation fixture.
- [ ] Publish a follow-up only when usage or feedback changes the product.
