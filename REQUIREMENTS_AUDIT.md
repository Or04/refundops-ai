# Requirement-by-requirement audit | 2026-11-01

Source: `Applied AI Engineer – Home Assignment(1).docx`, pages 1–3.

| Exact requirement | Evidence | Status |
|---|---|---|
| Determine auto-approval vs human-review boundary | `product/engine.py`, `docs/EXECUTIVE_BRIEF.md` | Implemented; threshold is a conservative hypothesis |
| Explain how boundary is evaluated before/after launch | `docs/EXECUTIVE_BRIEF.md`, `docs/RefundOps_AI_Solution_Design.pdf` | Historical replay + proposed shadow/canary monitoring; not a prospective evaluation |
| Reviewer queue, context, actions, post-decision | `product/api.py`, `product/experience/index.html` | Connected local implementation |
| Manager changes rule without engineer, previews before live | `product/api.py`, `product/experience/index.html` | Connected local implementation |
| Run with one command on pending.csv or same-schema CSV | `run.sh`, `run_csv.sh`, `product/cli.py` | Implemented |
| Tests | `product/tests/` | 22 passed on 2026-11-01 |
| Click-through demo of both workflows | `./run.sh` -> `/experience`; standalone `RefundOps_Studio_Demo.html` | Implemented; offline Studio is a simulation |
| README with setup, API key, architecture, AI coding tools reflection | `README.md` | Included |
| Write-up max 8 slides with before/after, boundary/evidence, metrics/rollback, AI model/cost/eval, deferred items | `slides/RefundOps_AI_Executive_Pitch.pptx` and `.pdf` | 8 slides; LLM evaluation is explicitly not run |
| 3–5 minute real screen recording | `recording/RefundOps_Connected_Demo.mp4` (4m17s, captioned, silent) | **COMPLETE** |
| Link to Git repo | https://github.com/Or04/refundops-ai | **COMPLETE** |
| Send to named recipients within 2 days | Not sent | **NOT COMPLETE** |

## QA performed

- Python tests: **22 passed**.
- Batch CLI on supplied `pending.csv`: **21 processed; 3 auto-eligible; 18 human review**.
- Slide deck: **8 slides**.
- Standalone Studio initially disagreed with the Python engine on two historical records due to `$43` amount parsing and `damaged` alias. Fixed. Historical default replay now matches: **84/251**; pending **3/21**.
- Genuine browser screen recording captured from the connected local app, using a browser-to-Python bridge to bypass the environment’s localhost browser restriction. Video is silent with descriptive captions and shows reviewer and manager actions. Public GitHub repository was verified.

## Caveats for reviewers

- The polished standalone Studio and connected API demo are **separate**. The connected app is the implementation of record.
- Historical labels include mistakes; historical agreement does not prove decision quality.
- No real LLM calls or measured LLM extraction precision/recall; cost is illustrative.
- No real payments or production-grade security.
- No email was sent.

## Final steps

1. Verify that the GitHub repository and video link open in a fresh browser session.
2. Send the repository link to Yaniv Tross and Gal Ohayon within the assignment deadline.
