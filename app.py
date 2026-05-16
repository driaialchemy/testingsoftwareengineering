import os
import json
import datetime

import streamlit as st

from agents.risk_agent import score_risk
from agents.value_agent import score_value
from agents.decision_synthesizer import synthesize

AUDIT_LOG_PATH = os.path.join(os.path.dirname(__file__), "outputs", "audit_log.json")


def append_audit(proposal: str, risk_scores: dict, value_scores: dict, result: dict) -> None:
    os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)

    if os.path.exists(AUDIT_LOG_PATH):
        with open(AUDIT_LOG_PATH, "r") as f:
            try:
                log = json.load(f)
            except json.JSONDecodeError:
                log = []
    else:
        log = []

    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "proposal": proposal,
        "risk_scores": risk_scores,
        "value_scores": value_scores,
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "rationale": result["rationale"],
    }
    log.append(entry)

    with open(AUDIT_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


st.set_page_config(page_title="Agent Review Board", layout="centered")
st.title("Agent Review Board")
st.markdown("Submit an AI workflow proposal for multi-agent review.")

proposal = st.text_area(
    "AI Workflow Proposal",
    placeholder="Describe the AI workflow or automation you want to deploy...",
    height=180,
)

if st.button("Submit for Review", type="primary"):
    if not proposal.strip():
        st.warning("Please enter a proposal before submitting.")
    else:
        with st.spinner("Agents reviewing..."):
            risk_scores = score_risk(proposal)
            value_scores = score_value(proposal)
            result = synthesize(risk_scores, value_scores)
            append_audit(proposal, risk_scores, value_scores, result)

        verdict = result["verdict"]
        color_map = {"APPROVE": "green", "REVISE": "orange", "REJECT": "red"}
        color = color_map[verdict]

        st.markdown(f"## Verdict: :{color}[{verdict}]")
        st.metric("Confidence", f"{result['confidence']}%")
        st.markdown(f"**Rationale:** {result['rationale']}")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Risk Scores")
            for k, v in risk_scores.items():
                if k != "average":
                    st.write(f"- {k.replace('_', ' ').title()}: {v}/5")
            st.write(f"**Average: {risk_scores['average']}/5**")

        with col2:
            st.subheader("Value Scores")
            for k, v in value_scores.items():
                if k != "average":
                    st.write(f"- {k.replace('_', ' ').title()}: {v}/5")
            st.write(f"**Average: {value_scores['average']}/5**")

        st.success("Review logged to outputs/audit_log.json")

st.divider()
if st.checkbox("Show audit log (last 5 entries)"):
    if os.path.exists(AUDIT_LOG_PATH):
        with open(AUDIT_LOG_PATH) as f:
            log = json.load(f)
        if log:
            st.json(log[-5:])
        else:
            st.info("Audit log is empty.")
    else:
        st.info("No audit entries yet.")
