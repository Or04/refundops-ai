# RefundOps AI | Solution at a glance

## Problem
- Hundreds of refund requests weekly; a legacy approval rule handles a small subset.
- Low-risk requests consume the same reviewer capacity as fraud and evidence exceptions.
- Operational managers need policy control and impact preview without engineering work.

## Solution
1. Ingest a request from `pending.csv` or a new same-schema file.
2. Normalize fields and apply fail-closed deterministic eligibility rules.
3. Mark low-risk requests auto-eligible; route all exceptions to the human queue.
4. Run a bounded read-only investigation trace: request, policy, customer history, similar cases, guardrails.
5. Present a reviewer with the evidence, rationale and safe actions; block fraud-flag approvals in the browser demo.
6. Let the manager edit policy, replay historical decisions, inspect changed recommendations and explicitly activate locally.
7. Record demo actions in a browser-local ledger; production requires immutable server-side audit and RBAC.

## Why not delegate money to an LLM?
- LLMs can extract ambiguous evidence and suggest next steps, but cannot independently verify a cardholder, shipment or warehouse event.
- The policy engine remains deterministic; uncertain cases go to a person.
- Current investigation workflow is deterministic. Live LLM agent orchestration is a roadmap item.

## Evidence and measurement
- Pending sample: 21 cases; 3 auto-eligible, 18 review.
- History: 251 cases; 84 auto-eligible on replay. Historical agreement is not outcome accuracy.
- Before launch: adjudicated holdout, shadow-mode evaluation, guardrail checks and rollback criteria.
- Monitor auto-eligibility, reviewer minutes, erroneous approvals, chargebacks, and policy audit completeness.

## Scope / deliverables
- Interactive offline product: `product/RefundOps_Case_Workspace.html` (open in Chrome).
- Actual Python engine/API/reviewer/manager: `product/`, launch with `./run.sh`.
- Same-schema CLI: `python cli.py --input data/pending.csv --output decisions.csv`.
- Tests: `python -m pytest -q` (22 passed).
- Slides: `slides/` (8 slides). Architecture: `docs/ARCHITECTURE.md`.
- Screen recording and public Git repository URL remain to be provided.
