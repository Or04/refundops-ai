# RefundOps AI | Windward Applied AI Engineer Home Assignment

**Submission scope:** a conservative refund decision engine, connected reviewer and policy-manager workflows, tests, historical replay, and a standalone UX concept. This is a sandbox: no real refunds are executed.

## Start in one command

Requires Python 3.10+ and an internet connection on first run to install dependencies. From the repository root:

```bash
./run.sh
```

Open `http://127.0.0.1:8000/experience` for the **connected local product**. Its queue, decisions, policy replay and audit are backed by the Python API and engine.

To run a new CSV with the same columns:

```bash
./run_csv.sh /path/to/new.csv /path/to/decisions.csv
```

To run tests:

```bash
cd product && python3 -m pytest -q
```

## Demo for business users

- **Connected app (primary evidence):** `./run.sh`, then `/experience`. Show reviewer queue, investigation, decision with rationale, manager policy draft, historical replay and activation.
- **Polished offline UX:** open `RefundOps_Studio_Demo.html` in Chrome. It embeds assignment CSV data and mirrors the policy's conservative decision boundary; browser-only reviewer/policy actions are simulated and not connected to Python.
- **Presentation:** `slides/RefundOps_AI_Executive_Pitch.pdf` (8 slides).
- **Solution design:** `docs/RefundOps_AI_Solution_Design.pdf`.
- **Requirement audit:** `REQUIREMENTS_AUDIT.md`.

## Architecture

CSV -> normalization -> deterministic, versioned policy engine -> auto-eligible OR prioritized human review. A bounded read-only investigation workflow retrieves evidence and provides an auditable trace. Reviewer actions and manager policy changes run through the local FastAPI service; historical replay uses the same engine. No payment calls. See `docs/ARCHITECTURE.md`.

## AI usage and API key

**No live LLM is used in the current executable system.** This is intentional: financial eligibility, fraud holds and policy enforcement must be deterministic and testable. The optional proposed LLM evidence extractor would use GPT-4.1 mini for structured free-text extraction, never for authorizing payments. Set `OPENAI_API_KEY` server-side if implementing that deferred module; the shipped code does not read or need an API key. Cost estimates in the design document are planning assumptions, not verified current provider prices. No empirical LLM evaluation is claimed.

## AI coding tools reflection

AI-assisted code generation was used for the UI, engine, tests and documentation. One AI-suggested shortcut to auto-approve fraud cases on the basis of a free-text phrase such as “fraud team confirmed” was **rejected for production**: untrusted notes cannot establish authenticated approval. The connected API blocks these unsafe auto-approval toggles. The work was checked against source CSVs, automated tests and replay.

## Evaluation and limitations

21 pending: 3 auto-eligible / 18 review. 251 historical: 84 auto-eligible / 167 review. Historical agreement is **not** proof of financial safety, model accuracy or causality. A labeled holdout, shadow-mode evaluation and production outcomes monitoring are required before enabling money movement. No authentication, production audit store, live LLM, payment integration or deployment is claimed.

## Submission completeness

**Still required before sending:** (1) publish this folder to a Git repository and include its URL; (2) capture a genuine 3–5 minute screen recording of the connected app and link/embed it. The source brief explicitly requires both. A recording script is provided under `recording/`. Do not label the storyboard GIF or static screenshots as a recording.
