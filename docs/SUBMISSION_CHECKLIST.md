# Requirements cross-check

| Requirement | Status | Evidence |
|---|---|---|
| Same-schema batch engine | Implemented | `product/cli.py`, `product/engine.py` |
| One-command local web app | Implemented | `cd product && ./run.sh` |
| Reviewer queue, actions and rationale | Implemented locally | `product/app.py`, `product/api.py` |
| Manager rule change and before/after preview | Implemented locally | `product/app.py`, `product/api.py` |
| Tests | 26 passed in build environment | `product/tests/` |
| Architecture sketch | Included | `docs/ARCHITECTURE.md` |
| AI model, rough cost, rationale | Included as proposed, not run | `docs/EXECUTIVE_BRIEF.md` |
| Evaluation and rollback | Included, historical replay only | `docs/EXECUTIVE_BRIEF.md` |
| Max 8-slide presentation | Included, 8 slides | `slides/` |
| AI coding tools reflection | Included | `README.md` |
| Click-through business demo | Included | `product/RefundOps_Case_Workspace.html` |
| Real 3–5 minute recording | **COMPLETE** | `recording/RefundOps_Connected_Demo.mp4`, 4m17s, silent captions |
| Public Git repository URL | **COMPLETE** | https://github.com/Or04/refundops-ai |
| Hosted live demo | Not required; not provided | Local / offline demos |

## New UI QA
- Browser-rendered with Playwright `page.set_content` (the environment blocks file:// and localhost navigation).
- Verified 21 queue rows, RF-1070 case view, fraud approval disabled, reviewer action recorded in ledger, policy replay after $50→$75.
- A completed 4m17s browser recording of the connected app is included; it is captioned and silent (not narrated).
