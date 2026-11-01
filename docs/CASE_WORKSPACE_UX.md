# Case Workspace | UX and agentic design

## Design principles
- Agent-first, not chat-first: recommendation and explanation before controls.
- Evidence is first-class; every signal references supplied CSV fields.
- Reviewer can escalate, request evidence, approve with verification, or reject with a reason. Fraud-flagged cases cannot be approved in the browser UI.
- Read-only deterministic trace: get_refund_request, check_policy, get_customer_history, find_similar_cases, evaluate_guardrails, request_human_review.
- Manager policy preview replays all supplied history before explicit activation.
- Minimal enterprise palette: white, slate, navy; amber only for risk and green for safe status.

## Implementation boundaries
The standalone HTML embeds supplied CSV rows and ports the deterministic decision logic to JS for offline use. It is not connected to the Python API; localStorage actions are not durable server audit. No real refunds, LLM, authentication, or external APIs. The Python engine, API, Streamlit reviewer/manager, tests, and CLI are included separately.

## Suggested next iteration
Connect the same UI to the local FastAPI API, replace the deterministic trace with signed tool events, persist case state and immutable audit, implement LLM evidence extraction behind a typed schema and evaluation gate, and add production RBAC and payment integration.
