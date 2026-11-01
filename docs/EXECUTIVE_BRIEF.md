# RefundOps AI | Executive Decision Brief
**Audience:** AI Transformation Director and VP AI  
**Positioning:** Decision intelligence for refund operations, not a chatbot approving money.

## 1. Transformation opportunity
**Before:** A legacy auto-approval rule handles some small refunds; people inspect most remaining cases. Low-risk work competes with fraud and policy exceptions for the same review capacity. **After:** auditable deterministic triage routes safe requests to automatic eligibility and ambiguous/high-risk cases to a prioritized reviewer, while managers preview and approve rule changes without engineering support.

## 2. Decision boundary and why
Start conservative: valid amount; known fraud status; no fraud flag; supported reason; all required evidence; amount <= $50; tenure >=6 months; prior refunds in 12 months <=1; change-of-mind within 14 days. Route missing data, fraud, carrier disputes, late delivery, wrong item without trusted merchant confirmation, and discretionary partials to people. **$50/tenure/prior-refund limits are design hypotheses, not sourced policy.** Never auto-reject. No actual payments.

## 3. Evidence (descriptive, not predictive)
Historical file: 251 decided cases; 113 previous automated decisions, 138 human decisions, 9 recorded chargebacks, 3 appeal reversals, 1,133 recorded human review minutes. Default historical replay: 84 eligible for auto-approval, 167 review; all 84 were historically approved, which measures agreement with noisy decisions, **not accuracy**. Pending sample: 21 cases, 3 auto-eligible and 18 review. This is a small biased sample and cannot establish financial safety.

## 4. Two operational mechanisms
**Reviewer:** searchable prioritized queue; case details, source evidence, decision rationale, agent trace, approve/reject/partial/escalate/request evidence with rationale; record event. **Manager:** draft threshold change, simulate on pending and historical inputs, inspect exact cases and exposure, acknowledge risk, activate a version or restore a prior version. Production requires durable approval and event history.

## 5. Applied AI judgment
The current running decision path is deterministic. A bounded five-tool investigation workflow provides traceable investigation; it is **not a live LLM agent**. Proposed LLM use: structured extraction from free-text support notes, schema-constrained with citations, followed by evidence verification. GPT-4.1 mini is a candidate, not integrated or evaluated. Illustrative token estimate: 1,000 input + 200 output at assumed $0.40/$1.60 per million => $0.00072/extraction (not verified current pricing). Avoid LLM-based payment authorization, policy enforcement or hallucinated evidence.

## 6. Success scorecard and release gates
- **Efficiency:** auto-eligibility %, median time-to-decision, reviewer minutes saved, p90 queue age.
- **Safety:** confirmed erroneous auto-approval rate, dollars wrongly refunded, chargebacks per 1,000 refunds, appeal reversals, fraud exceptions.
- **Governance:** % policy changes previewed, % with named approver, audit completeness, rollback time.
- **Prelaunch:** annotate representative holdout, stratify by amount/reason/fraud, shadow mode and compare with adjudicated outcomes. Block if any known fraud or missing-evidence case is auto-eligible.
- **Initial proposed stop triggers (to be approved by business owner):** any critical guardrail violation; >0.5% confirmed erroneous auto approvals; material increase in chargebacks vs control. Stop auto-approval, revert policy, preserve trace, investigate cohort.

## 7. Economics: example, not measured ROI
At 300 requests/week, 33.5% auto-eligibility and 2 minutes avoided per request => about 100 reviews and 3.35 labor hours saved weekly (~174 hours/year), before rework, verification, and monitoring. Historical replay eligibility is not a production forecast.

## 8. Delivery, limitations and next steps
Implemented: local CLI, Streamlit UI, FastAPI experience, offline polished HTML, deterministic engine, policy replay, bounded investigation, tests. Not implemented: live LLM, durable multi-user audit, payment integrations, browser E2E, production security or hosted deployment. No actual screen recording is included. Next: annotated evaluation set, shadow mode, production-grade event store and approvals, optional LLM extractor with measured precision/recall and latency, then a narrow canary rollout.

## 9. AI coding tool reflection
AI assistance accelerated drafting of rules, UI and tests. A proposed note-based shortcut to auto-approve fraud-confirmed requests was rejected as production unsafe: a text phrase is not an authenticated fraud-team attestation. Safety overrides remain blocked in the connected API.
