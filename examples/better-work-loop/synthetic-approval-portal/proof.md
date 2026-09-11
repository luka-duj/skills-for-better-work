# Prove Before Pilot — Synthetic approval portal

## Evidence decision

- **Status:** `agent-verified`, not validated.
- **Observed:** technical and synthetic checks cover completeness, missing information, exception routing, and refusal to approve.
- **Critical failures:** none observed in the synthetic checks.
- **Missing evidence:** no representative coordinator or reviewer has used the prototype.
- **Recommendation:** `retest` with representative users.
- **Owner:** synthetic example owner.

The prototype is ready for a guided user session. It is not ready for pilot review because job completion without coaching and downstream reviewer usability remain unassessed.

## Ready-to-run session plan

Timebox the session to 30 minutes with an operations coordinator and an approver. Ask them to attempt SCN-1, SCN-2, and SCN-5 without explaining the fields or route. Record completion without coaching, wrong routes, hesitation, and any source context the reviewer must reconstruct. Stop if the prototype appears to approve, real sensitive data is entered, or the summary cannot begin a review. Resume by appending sanitized `user-observation` sessions and rerunning the proof decision.

Requester comments made without a target-job attempt are `stakeholder-feedback`; they are not user-observation evidence.

## What may be missing or uncertain

This is a fictional example showing the contract. It is not evidence that the Better Work Loop or the prototype works for a real organization.
