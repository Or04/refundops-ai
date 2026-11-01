# 3–5 minute screen recording script (English)

**0:00–0:30 | Overview:** "RefundOps AI separates easy, low-risk refunds from cases requiring judgment. The demo uses the actual sample CSV and never moves real money. The overview shows 3 eligible approvals and 18 reviews."

**0:30–1:50 | Reviewer queue:** "Cases are prioritized by risk. Open a fraud-flagged or never-arrived case. Here are the notes, amount, history, and specific policy rule that routed it. A reviewer can approve, reject, issue a partial, escalate to fraud, or request evidence. A rationale is mandatory." Enter a rationale and record a decision. Show queue count decreases.

**1:50–3:00 | Policy studio:** "Operations can change thresholds without engineering. Increase the automatic approval cap, observe before/after totals and the exact requests affected, then acknowledge and publish. The shared decision engine updates the queue immediately. The stolen-card toggle is illustrative and not production-safe without verified fraud-team confirmation."

**3:00–3:45 | Decision explorer and audit:** "Every decision has a reason code and evidence label. Export the decisions. The audit shows session actions; production would need durable versioned logs and access controls."

**3:45–4:30 | Trade-offs:** "We deliberately don't let an LLM approve money. The historical replay selects 84 cases, all historically approved, but that is not an accuracy claim. Before launch we would shadow-test with human labels and monitor wrong approvals, chargebacks and appeals."

Recording instructions: launch `./run.sh`, record browser + microphone using your screen recorder, save as `docs/demo.mp4` and commit it or add a video link in README. Recording is not generated automatically in this package.
