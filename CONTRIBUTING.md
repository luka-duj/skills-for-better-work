# Contributing

Contributions should improve an observable decision or remove a demonstrated failure. Do not add rules merely because one phrasing or format feels preferable.

## Protect private information

Use synthetic or fully sanitized examples. Do not submit:

- company, customer, employee, or vendor-confidential names;
- real internal requests, process maps, screenshots, contracts, or decision packets;
- credentials, personal data, security details, private architecture, or non-public pricing;
- claims or examples you do not have authority to license under Apache-2.0.

If sanitizing a case would remove the information needed to reproduce the problem, describe the behavior abstractly instead of sharing the source.

## Propose a change

For a behavior defect, explain:

1. the synthetic or generalized input;
2. the observed direction or question;
3. the expected behavior;
4. the decision principle or safety issue involved;
5. which evaluation fixture should prevent regression.

For Better Work Loop changes, also identify the affected phase and predecessor artifact. Preserve stable IDs, hashes, the single ordinary build gate, the distinct current/stated-ideal/proposed-target process views, source-problem and target-node traceability, slice boundaries, evidence-type labels, the review handoff, and the distinction between `agent-verified` and representative-user `validated`.

For a method proposal, explain the problem it solves, where it should apply, where it should not apply, and what evidence would show that the change is better.

## Validate

Run:

```bash
python scripts/validate.py
python -m unittest discover -s tests
```

Then forward-test the affected cases in `evals/cases.json` and `evals/loop-cases.json`. Record behavior rather than matching exact prose. A fixture-based walkthrough can validate structure and routing but cannot satisfy a representative-user evidence gate.

## Pull requests

Keep changes focused. Preserve explicit invocation, evidence labeling, human decision ownership, the boundary between process discovery and solution commitment, and the boundary between a bounded local prototype and pilot or production work.
