# Agent Review Board

A local-first Streamlit app that routes AI workflow proposals through a three-agent review pipeline and produces a structured verdict: **APPROVE**, **REVISE**, or **REJECT**.

---

## Purpose

Organizations adopting AI automation need a lightweight way to assess proposals before committing resources. This app simulates a multi-agent review board that scores each proposal on risk and business value, then applies fixed decision thresholds to produce a consistent, auditable outcome — with no external APIs or cloud dependencies.

---

## Features

- Three independent review agents (Risk, Value, Decision Synthesizer)
- Deterministic, keyword-based scoring — identical input always produces identical output
- Fixed decision thresholds with confidence scoring
- Append-only JSON audit log for every review
- Simple Streamlit UI — no login, no database, runs entirely on your machine

---

## Architecture

```
app.py                        # Streamlit UI and audit log writer
agents/
  risk_agent.py               # Scores 4 risk dimensions (1–5 each)
  value_agent.py              # Scores 4 value dimensions (1–5 each)
  decision_synthesizer.py     # Applies thresholds, returns verdict
data/
  sample_cases.json           # Reference proposals with expected verdicts
outputs/
  audit_log.json              # Appended at runtime (gitignored)
tests/
  test_agents.py              # 19 unit tests
requirements.txt
```

### How the agents work

**Risk Agent** scores these dimensions from the proposal text:

| Dimension | What it detects |
|-----------|----------------|
| Operational | Production exposure, outages, live deployments |
| Safety | Sensitive data, PII, privacy concerns |
| Compliance | GDPR, HIPAA, regulatory keywords |
| Reliability | Experimental, prototype, untested systems |

**Value Agent** scores these dimensions:

| Dimension | What it detects |
|-----------|----------------|
| Business Value | Revenue, customer impact, strategic goals |
| Efficiency | Automation, speed gains, manual work elimination |
| Cost Reduction | Savings, budget impact |
| Deployment Upside | Breadth of rollout (team → enterprise) |

Each dimension is scored 1–5. The agent returns a per-dimension score and an average.

**Decision Synthesizer** applies fixed thresholds:

| Condition | Verdict |
|-----------|---------|
| `avg_risk >= 4.0` | REJECT |
| `avg_risk <= 2.5` AND `avg_value >= 3.5` | APPROVE |
| Otherwise | REVISE |

Confidence is derived mathematically from how far the scores sit from the decision boundaries. It is capped at 99% — the system never claims certainty.

---

## Installation

Requires Python 3.9 or later.

```bash
pip install -r requirements.txt
```

---

## Running the app

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

---

## How to test

```bash
python -m pytest tests/
```

Expected output: **19 passed**.

The test suite covers:
- Score range validation (1–5 per dimension)
- Average math correctness
- Verdict boundary conditions (reject at 4.0, approve at 2.5/3.5)
- Required output keys
- Confidence range (0–100)

---

## Example workflow inputs

Try pasting these into the app to see different verdicts:

**Likely APPROVE**
> Deploy an AI agent to automate weekly financial reports. Streamline the budget process for the team and reduce manual effort.

**Likely REJECT**
> Migrate a critical production ML pipeline that handles sensitive PII data and GDPR compliance requirements. Experimental prototype not yet fully tested.

**Likely REVISE**
> Improve the customer satisfaction dashboard with automated insights. Moderate deployment with some new components across the team.

All three cases are also stored in `data/sample_cases.json` for reference.

---

## Audit log

Every submission is appended to `outputs/audit_log.json`. Each entry records:

- Timestamp
- Proposal text
- All per-dimension scores (risk and value)
- Verdict, confidence, and rationale

The audit log is **gitignored** — it stays on your local machine and is not committed to the repository.

---

## Environment configuration

A `.env` file may be used for local configuration. It is listed in `.gitignore` and is **never committed to the repository**. Each developer maintains their own local copy.

---

## Limitations

- Scoring is keyword-based, not semantic. Unusual phrasing may not trigger the expected score tier.
- The decision thresholds are fixed. There is no way to adjust them from the UI.
- The audit log grows unboundedly — there is no built-in pruning or rotation.
- The app is single-user and not designed for concurrent access to the audit log.

---

## Future improvements

- Semantic scoring using an embedded language model (still local, e.g. via Ollama)
- Configurable thresholds exposed through a settings panel
- Audit log viewer with filtering and export
- Multi-user support with per-user log partitioning
- CI integration to score proposals from a pull request description
