# RefundOps AI | Requirement Alignment & QA Report

**Date:** 2026-11-01  
**Basis:** Original `Applied AI Engineer – Home Assignment(1).docx`, repository code, sample CSVs and supplied demo video.  
**Status:** **Functionally aligned for a scoped sandbox submission; not production-ready.** Visual browser QA and a fresh recording of the white interface remain open.

## Requirement traceability

| Assignment requirement | Evidence | Result |
|---|---|---|
| Part 1: safe auto-approval boundary | `product/engine.py`, policy rules, CSV data | PASS as conservative hypothesis; no payment execution |
| Part 1: evidence before and after launch | 251-row historical replay; monitoring and shadow-mode plan | PARTIAL: no labeled holdout or production outcome study |
| Part 2: reviewer queue, context, actions, outcomes | `/experience`, `/api/overview`, `/api/review`, `/api/agent/investigate` | PASS at API/integration level; browser visual QA blocked |
| Part 2: manager changes policy and previews impact | `/api/policy/simulate`, `/api/policy/activate`, `/api/policy/rollback` | PASS; activation now requires matching versioned preview |
| One-command run on supplied or same-schema CSV | `./run.sh`; `./run_csv.sh input.csv output.csv` | PASS; caller-relative path issue fixed |
| Automated tests | `python3 -m pytest -q` at repository root | PASS: **26 tests** |
| Clickable business demo | connected `/experience` plus offline Studio | PASS in code; not fully visually verified in current browser environment |
| README, API key, architecture, AI coding tools reflection | `README.md`, `docs/ARCHITECTURE.md` | PASS; no API key needed by shipped deterministic system |
| Max 8-slide write-up with boundary, evidence, metrics, AI/model/cost/eval, deferrals | `slides/RefundOps_AI_Executive_Pitch.pdf` | PASS on scope and length (8 slides); empirical LLM evaluation unavailable |
| 4:12 white-UI walkthrough video | `recording/RefundOps_White_Studio_Demo.mp4` | PASS for duration: **256.75 s (4:17)**; older dark UI, silent captions |
| Repository link | https://github.com/Or04/refundops-ai | PASS once QA fixes pushed |
| Email submission within 2 days | Outside repository | NOT VERIFIED / NOT SENT |

## QA executed

- Unit/API regression: **26 passed**; root-level invocation.
- CLI: 21 pending records processed; **3 auto-eligible, 18 human review**.
- Historical replay documented: 84 of 251 auto-eligible under current conservative policy. This is a rule-based classification, not evidence of financial safety.
- JavaScript syntax: `node --check` passes for connected UI.
- Presentation: exactly **8 slides**.
- Recording: valid MP4, duration **4:16.75**, captioned and silent.
- GitHub CI must be checked after pushing this QA patch.

## Issues found and corrected

1. **HIGH | Fraud approval bypass:** reviewer API previously accepted `approve` for a fraud-flagged request. Now rejects with HTTP 409; matching UI action hidden.
2. **HIGH | Unpreviewed policy activation:** manager API previously allowed direct activation without running historical replay. Now requires a matching preview of the exact policy on the current version.
3. **MEDIUM | Stale review queue:** resolved and escalated cases were still counted as open. Now filtered to `needs_review`.
4. **MEDIUM | Duplicate review decisions:** previously possible to overwrite an existing reviewer outcome. Now rejected with HTTP 409.
5. **MEDIUM | CLI relative paths:** `run_csv.sh` changed into `product/` before resolving user paths. Fixed by resolving absolute paths first.
6. **LOW | Root-level tests:** tests imported modules and CSVs relative to `product/`, failing when invoked from repository root. Fixed test paths and added `pytest.ini`.

## Known limitations and remaining gaps

- **No browser visual sign-off:** Chromium navigation to localhost and file URLs was blocked by the execution environment. The white connected interface's source and JavaScript syntax were inspected, but pixel-level layout, responsive behavior, accessibility, and full click paths have **not** been verified end-to-end.
- **Recording is out of date visually:** it shows the connected dark UI before the white restyle. Functional workflow is represented, but for a consistent executive presentation, re-record the white experience.
- **Not a live LLM agent:** investigation is a bounded deterministic tool trace. Proposed GPT-4.1 mini extraction, model cost and evaluation are a roadmap, not deployed evidence. No model accuracy metrics can be claimed.
- **No production identity, payments, external fraud/warehouse verification or durable transactional database.** In particular, source notes are untrusted; unsafe auto-approval toggles are blocked by the API. The underlying engine includes optional unsafe experimental branches that must remain disabled outside the sandbox.
- **Manager replay is counterfactual rule classification, not causal evidence of lower fraud/loss.** Real rollout needs labeled evaluation, shadow mode, guardrail monitoring and a kill switch.
- **State is stored in a local JSON file** for demonstration only. No concurrent transaction guarantees or immutable audit log.
- **Submission email has not been sent.** Confirm recipient addresses and deadline from original brief.

## Release recommendation

**GO for a clearly labeled sandbox take-home demonstration after CI passes. NO-GO for financial production use.** Prefer connected `/experience` as implementation evidence; label offline Studio as a visual simulation. Re-record white UI before final email if possible.
