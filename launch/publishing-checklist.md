# Publishing Checklist

Publication is a separate owner-controlled action. Completing the private alpha does not authorize changing repository visibility or posting to LinkedIn.

## Repository

- [ ] Review the complete Git history for private or employer-specific information.
- [ ] Confirm the repository contains only generalized methods and synthetic examples.
- [ ] Run `python scripts/validate.py` and `python -m unittest discover -s tests` from a clean checkout.
- [ ] Forward-test every applicable behavioral fixture and record failures privately.
- [ ] Confirm the Apache-2.0 license and attribution.
- [ ] Confirm icons, header, links, and installation commands render correctly.
- [ ] Enable private vulnerability reporting before public release.
- [ ] Configure issue labels and enable GitHub Discussions only if there is an owner for moderation.
- [ ] Verify the repository description and topics without unsupported claims.
- [ ] Change visibility to public only after an explicit owner instruction.
- [ ] Verify the repository and raw files open without authentication.
- [ ] Create the first tagged release only after the public state is verified.

## LinkedIn

- [ ] Replace `[PUBLIC_REPOSITORY_URL]` with the verified public URL.
- [ ] Re-run truth, ownership, confidentiality, originality, usefulness, voice, and CTA gates.
- [ ] Confirm no real internal case can be inferred from the wording.
- [ ] Check the final post and link preview in the LinkedIn composer.
- [ ] Publish only after an explicit owner instruction covering the final copy.

## After release

- [ ] Keep public feedback sanitized; remove or privately report accidental disclosures promptly.
- [ ] Record meaningful behavior changes in `CHANGELOG.md` and a matching evaluation fixture.
- [ ] Publish a follow-up only when usage or feedback changes the product.
