# WINDWARD / DECISION INTELLIGENCE

**Refunds, under control.** An independent, Windward-inspired interview concept. Not an official Windward product.

# RefundOps AI | Applied AI Engineer Home Assignment

A working, local-first refund triage and policy-management demo. **No real payment processing.**

## One-command launch

```bash
./run.sh
```

Requires Python 3.10+. Open the Streamlit URL printed in the terminal (usually http://localhost:8501). Dependencies are installed by the script. Windows: `pip install -r requirements.txt && streamlit run app.py`.

## Batch evaluation, new files and tests

```bash
python cli.py --input data/pending.csv --output decisions.csv
python cli.py --input /path/to/new.csv --output /path/to/output.csv
python -m pytest -q
python analyze.py
```

New CSVs should use the same columns as `data/pending.csv`. The app supports CSV upload from its sidebar. Missing/invalid data routes to review, never approval. There are 12 unit tests. The default pending sample yields **3 approvals / 18 reviews**. The historical replay yields **84 approvals / 167 reviews**, but this is **not a prospective accuracy estimate**.

## Architecture

```text
CSV -> field normalization + fail-closed validation -> versioned policy rules
                                                  |-> AUTO_APPROVE recommendation (sandbox only)
                                                  |-> REVIEW -> human case details + recorded rationale
Policy manager -> draft thresholds/toggles -> replay on pending CSV -> diff -> explicit publish
                                               |-> shared engine, same as CLI and reviewer
```

The deterministic engine in `engine.py` is the single source of truth. The Streamlit app calls it for every preview and queue. The CLI runs the same function on any same-schema CSV. Session state stores policy changes and reviewer decisions for demo purposes only.

## Business policy and conservative interpretation

- Fraud flags go to the fraud team, regardless of amount. Manager can toggle a **demo-only** confirmation-note exception; this is not suitable for production without a verified fraud-team event.
- Change of mind after 14 days is sent to a human with an explicit *outside policy* warning; human should reject unless data is corrected. Missing delivery date goes to review.
- Damaged arrival above $50 requires photo evidence. A support note saying "photo attached" is only a proxy for verification, not a real attachment check.
- Never arrived requires carrier proof/investigation review. Wrong item requires confirmation of merchant error, then full refund. Late delivery remains discretionary for partials.
- For otherwise eligible small requests, default low-risk cohort: amount <=$50, tenure >=6 months, prior refunds <=1. This threshold is a **design assumption**, not a rule explicitly stated in the policy notes.
- Requests above $300 always route to a person by default; manager can change this. This is a demo configuration inspired by the assignment example, not the source policy.
- `approve` is a *routing recommendation* only, never a payment instruction. The system intentionally does not auto-reject in order to preserve human correction for messy evidence.

## Evidence and evaluation

The 251-row history contains 113 previous auto decisions and 138 human decisions, 9 recorded chargebacks, and 3 appeal reversals. It has 1,133 recorded human review minutes. Replaying the default policy on historical inputs selects 84 auto approvals; all 84 were historically approved, but this is **agreement**, not ground-truth correctness. Historical decisions are imperfect, outcome reporting is incomplete, and there is no prospective control group. The 21 pending cases yield 3 auto approvals and 18 human reviews. Treat both as descriptive sample statistics only.

**Before launch:** label a representative holdout with policy owners, audit all proposed auto-approvals for evidence and later outcomes, stratify by reason, amount and fraud, run shadow mode without issuing money, and block go-live if any known fraud, missing evidence or outside-window case is auto-approved. A zero-error observed sample does not prove zero error.

**After launch:** track auto-approval rate, confirmed erroneous-approval rate, dollars incorrectly refunded, chargebacks per 1,000 refunds, appeal overturns, manual minutes saved, and time-to-decision. Suggested initial guardrails (hypotheses): <=0.5% confirmed erroneous approvals; zero fraud-flag auto approvals without verified confirmation; no material chargeback increase vs baseline. Pause/rollback if a critical policy violation occurs, a guardrail breaches, or fraud signals rise. These are suggested thresholds requiring manager sign-off.

## AI judgment, model and cost

**Current runnable demo deliberately uses no LLM in the payment decision path.** Policy rules, money, fraud status and eligibility must be reproducible, explainable, and testable. The optional AI extension would use **GPT-4.1 mini** to extract structured, cited evidence from free-text support notes into a JSON schema, never to authorize refunds. An example planning assumption of 1,000 input + 200 output tokens at $0.40/$1.60 per million tokens gives ~$0.00072 per extraction, excluding retries and infrastructure. **This is a planning estimate, not a verified current price, and no API calls or model evaluation were run.** No API key is required for the runnable demo. If adding the optional extractor, set `OPENAI_API_KEY` in the environment, keep it server-side, and evaluate extraction against manually annotated examples before use. Do not treat model-generated text as independently verified fraud or carrier evidence.

## Workflow details

**Reviewer:** prioritized queue, case context and explanation, Approve / Reject / Partial / Escalate to fraud / Request evidence, rationale required, partial amount must be positive and less than requested. A decision removes the case from the current queue and enters the session audit.

**Manager:** edit thresholds and two illustrative exception switches, see before/after approvals and exact affected requests, export impact CSV, acknowledge risk, publish to session. Both pages immediately use the same new policy.

## Limitations and next steps

- No authentication, database, external carrier/payment/fraud integration or cloud deployment (per assignment scope).
- Audit and policy changes live only in Streamlit session memory; refreshing sessions loses state. Add durable event log, policy versioning, approval workflow, role-based access, rollback and dual control before production.
- Note keyword matching is weak evidence; real attachment verification and fraud-team attestations need trusted integrations.
- The manager's fraud-confirmed override is a **mocked evidence path**, explicitly not a production-safe integration.
- No actual LLM call, empirical LLM accuracy evaluation, or production pricing verification. Avoid misleading claims.
- No screen recording is included; `docs/DEMO_SCRIPT.md` provides a 3–5 minute recording walkthrough to capture locally.

## AI coding tools disclosure

AI coding assistance was used to draft the deterministic engine, UI, tests and documentation. A suggested approach to directly auto-approve fraud-flagged cases based on note wording was rejected for production: the demo keeps fraud on hold by default and labels the override as unsafe without authenticated verification. Generated code was reviewed with tests and historical replay; production security review is still required.


## Brand / product rationale
See [BRAND_AND_PRODUCT_NOTES.md](BRAND_AND_PRODUCT_NOTES.md).

## React Decision Intelligence (new)

The React interface is in `web/`, backed by `api.py` (FastAPI), which calls the **same `engine.py`** used by the CLI and original Streamlit demo. All case data comes from the original uploaded CSVs in `data/`. No fabricated cases, payments, external AI calls, or live Windward integration.

### Run locally

Requirements: Python 3.10+, Node.js 18+, npm. From the project root:

```bash
./run_react.sh
```

Open http://127.0.0.1:5173. API docs at http://127.0.0.1:8000/docs. The first run installs Python and npm dependencies and needs internet access. Alternatively run `python3 -m pip install -r requirements.txt fastapi 'uvicorn[standard]'`, `python3 -m uvicorn api:app --reload`, and in another terminal `cd web && npm install && npm run dev`.

### Features

- Command Center: real pending-file metrics, distribution and priority signals.
- Investigation Queue: searchable/filterable cases, rule and evidence trace, reviewer approve/reject/escalate with mandatory notes.
- Policy Simulator: preview proposed thresholds against pending and historical CSV rows, show changed classifications and incremental auto-approval exposure, then activate versioned policy with mandatory rationale.
- Audit Trail: local reviewer and policy events, demo reset.
- Analyst Brief: deterministic explanation derived from case evidence and rule; **not a real LLM**. Optional LLM enrichment remains deferred. No model-evaluation numbers are claimed.

### Safety and demo boundaries

- No actual payment execution. Auto-eligible means *eligible*, not transferred.
- The existing engine relies on note keyword matching for certain evidence; the API deliberately blocks activation of auto-approval for wrong-item or fraud-confirmed cases when confirmation is not independently verified.
- Demo state is stored in `.demo_state.json` and is local, not a production transactional database. No authentication, multiuser concurrency protection, or cloud deployment.
- Current policy configuration can be activated for threshold changes after preview. This is a demo, not an audited financial approval system.
- The design is inspired by public Windward brand/product language, and is not an official Windward product.

### Verification

`python3 -m pytest -q` executes the 12 original engine tests. Run `python3 -m pytest -q tests/test_api.py` for API tests. `cd web && npm run build` checks the frontend once npm dependencies are installed. A full browser E2E test is not included.

## Home assignment product focus
Start with [START_HERE.md](START_HERE.md). The React UI is a refund-specific Reviewer Queue and Policy Manager Simulator, not a generic Windward product. Its intelligence theme is only a design reference.

## Vision bonus: Policy Time Machine (implemented)

In **Policy simulator**, change a rule and click **Run impact simulation**. The counterfactual replay now displays historical changed classifications, newly auto-eligible cases, historical exposure, and actual historical decision/outcome notes for inspection. Historical labels are noisy and this is *not* a causal estimate of prevented chargebacks or model accuracy. This is the assignment's requested before/after simulator, extended into a concrete business decision workflow.

In **Decision audit**, previous policies can be restored with a required rationale. Rollback is version-checked, audited, and creates a **new** version; it never silently rewrites history. Risky free-text-based auto-approval remains blocked.

### Trust boundaries
- Every approval in this local sandbox is **eligibility only**; there is no payment integration.
- The optional insight panels are rule-grounded explanations, **not live LLM inference**.
- The user-provided CSVs are the only case source; historical outcomes are not automatically treated as ground truth.
- Policy changes cannot silently bypass fraud or warehouse verification.
- The React production build still requires `npm install` and browser QA in a network-enabled environment. Python tests were executed locally.


## Agentic Product Experience (new)

Run `uvicorn api:app --host 127.0.0.1 --port 8000` from the project root and open **http://127.0.0.1:8000/experience**. This standalone, dependency-free frontend is wired to the same FastAPI decision engine, reviewer actions, policy simulator, and audit ledger. The investigation agent executes a bounded 5-tool, read-only workflow (load case, check policy, lookup customer history, compare reason cohort, evaluate guardrails) and shows its evidence and gaps. This is **deterministic agent orchestration, not an LLM**. No external service or payments are called.


## Executive submission
Open `RefundOps_Interactive_Demo.html` directly for the polished offline storyboard. The connected local experience uses `./run.sh` then http://127.0.0.1:8000/experience. These are different execution modes. The offline experience is a browser simulation, not connected to the Python API.
