# Executive presentation talking points (4–5 minutes)

1. **The operating problem (30s):** low-value requests consume reviewer time; high-risk requests wait in the same queue. The transformation goal is controlled delegation of decisions.
2. **Boundary (45s):** conservative rules first. Eligibility is not payment. $50 threshold is a hypothesis; evidence is noisy.
3. **Product walkthrough (90s):** open offline demo for visual flow; open connected `/experience` for API-backed case investigation; select RF-1070, inspect fraud hold and evidence trace, take human action; open policy studio, change cap $50->$75, run impact preview, inspect affected cases, activate only after acknowledgement. Offline and connected experiences are different modes.
4. **Agentic architecture (40s):** bounded investigation tools are implemented; LLM specialists are proposed. Show trust boundaries and where humans retain authority.
5. **Evaluation and economics (40s):** 3/21 pending eligible, 84/251 historical. Historical agreement is not accuracy. Shadow-mode and stop triggers are mandatory.
6. **Next steps (30s):** adjudicated labels, live extractor evals, durable audit and controlled canary.

Suggested answer to 'Why not let an LLM decide?': Because refund decisions move money; LLMs can extract and summarize ambiguous evidence, but eligibility and disbursement must remain deterministic and independently verifiable.
