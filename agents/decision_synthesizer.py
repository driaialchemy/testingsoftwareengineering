def synthesize(risk_scores: dict, value_scores: dict) -> dict:
    """
    Apply fixed thresholds to produce a verdict:
      REJECT  if avg_risk >= 4.0
      APPROVE if avg_risk <= 2.5 AND avg_value >= 3.5
      REVISE  otherwise
    """
    avg_risk = risk_scores["average"]
    avg_value = value_scores["average"]

    if avg_risk >= 4.0:
        verdict = "REJECT"
        # confidence scales with how far above the reject threshold risk sits
        confidence = round(min(50 + (avg_risk - 4.0) / 1.0 * 50, 99.0), 1)
        rationale = (
            f"High risk profile (avg risk: {avg_risk}/5.0) exceeds the acceptable threshold of 4.0. "
            "Proposal requires significant risk mitigation before reconsideration."
        )
    elif avg_risk <= 2.5 and avg_value >= 3.5:
        verdict = "APPROVE"
        risk_margin = (2.5 - avg_risk) / 2.5
        value_margin = (avg_value - 3.5) / 1.5
        confidence = round(min(50 + (risk_margin + value_margin) / 2 * 49, 99.0), 1)
        rationale = (
            f"Acceptable risk (avg: {avg_risk}/5.0) combined with strong value (avg: {avg_value}/5.0). "
            "Proposal satisfies both approval criteria."
        )
    else:
        verdict = "REVISE"
        confidence = 60.0
        rationale = (
            f"Risk score (avg: {avg_risk}/5.0) and value score (avg: {avg_value}/5.0) "
            "do not clearly satisfy APPROVE or REJECT criteria. "
            "Revise the proposal to lower risk or increase demonstrated value."
        )

    return {
        "verdict": verdict,
        "confidence": confidence,
        "rationale": rationale,
        "avg_risk": avg_risk,
        "avg_value": avg_value,
    }
