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
| 3–5 minute real screen recording | `recording/` contains only scripts | **NOT COMPLETE** |
| Link to Git repo | This directory is ready for commit | **NOT COMPLETE** |
| Send to named recipients within 2 days | Not sent | **NOT COMPLETE** |

## QA performed

- Python tests: **22 passed**.
- Batch CLI on supplied `pending.csv`: **21 processed; 3 auto-eligible; 18 human review**.
- Slide deck: **8 slides**.
- Standalone Studio initially disagreed with the Python engine on two historical records due to `$43` amount parsing and `damaged` alias. Fixed. Historical default replay now matches: **84/251**; pending **3/21**.
- No evidence of a genuine video capture or hosted repository was found in the supplied package. An attempted browser recording in this environment did not complete; no fabricated video is included.

## Caveats for reviewers

- The polished standalone Studio and connected API demo are **separate**. The connected app is the implementation of record.
- Historical labels include mistakes; historical agreement does not prove decision quality.
- No real LLM calls or measured LLM extraction precision/recall; cost is illustrative.
- No real payments or production-grade security.
- No email was sent.

## Final steps

1. Push this folder to a repository.
2. Record the connected demo for 3–5 minutes: reviewer queue -> case evidence -> decision -> manager rule -> historical preview -> activate -> audit.
3. Add video to the repository or link from README.
4. Share repository link with Yaniv Tross and Gal Ohayon.
