# Publishing Checklist

Publication is a separate owner-controlled action. Completing the private alpha does not authorize changing repository visibility or posting to LinkedIn.

## Repository

- [ ] Review the complete reachable Git history for private or employer-specific information, copied third-party packages, and files that were later reverted.
- [ ] Confirm the public default branch does not retain the reverted `imagegen` and `product-design` package import in its reachable history.
- [ ] Confirm the repository contains only generalized methods and synthetic examples.
- [ ] Run `python scripts/validate.py` and `python -m unittest discover -s tests` from a clean checkout.
- [ ] Forward-test every applicable behavioral fixture and record failures privately.
- [ ] Confirm the Apache-2.0 license and attribution.
- [ ] Confirm `SKILL.md` name, description, license, and metadata pass both the Codex package validator and relevant Agent Skills checks.
- [ ] Confirm icons, header, links, and installation commands render correctly.
- [ ] Test installation and explicit invocation in a clean Codex environment.
- [ ] Test each additional client named as behaviorally supported; otherwise describe it only as format-compatible.
- [ ] Configure issue labels and enable GitHub Discussions only if there is an owner for moderation.
- [ ] Verify the repository description and topics without unsupported claims.
- [ ] Change visibility to public only after an explicit owner instruction.
- [ ] Immediately enable private vulnerability reporting after the repository becomes public, then verify the reporting path before announcing it.
- [ ] Verify the repository and raw files open without authentication.
- [ ] Create the first tagged release only after the public state is verified.

## LinkedIn

- [ ] Replace `[PUBLIC_REPOSITORY_URL]` with the verified public URL.
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
