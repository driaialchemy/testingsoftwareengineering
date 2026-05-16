def score_risk(proposal: str) -> dict:
    """Score proposal across 4 risk dimensions (1=low, 5=high)."""
    text = proposal.lower()

    # operational risk: production exposure, outages, deployments
    operational = 1
    if any(w in text for w in ["outage", "downtime", "failure", "crash"]):
        operational = 5
    elif any(w in text for w in ["production", "critical", "live"]):
        operational = 4
    elif any(w in text for w in ["deploy", "migration", "cutover"]):
        operational = 3
    elif any(w in text for w in ["staging", "test", "sandbox"]):
        operational = 2

    # safety risk: harm, privacy, sensitive data exposure
    safety = 1
    if any(w in text for w in ["unsafe", "dangerous", "hazard", "harm"]):
        safety = 5
    elif any(w in text for w in ["sensitive", "privacy", "pii", "personal data"]):
        safety = 4
    elif any(w in text for w in ["user data", "confidential"]):
        safety = 3
    elif any(w in text for w in ["internal", "restricted"]):
        safety = 2

    # compliance risk: regulatory violations, audits, governance
    compliance = 1
    if any(w in text for w in ["illegal", "violation", "breach", "non-compliant"]):
        compliance = 5
    elif any(w in text for w in ["gdpr", "hipaa", "pci", "sox", "regulation"]):
        compliance = 4
    elif any(w in text for w in ["audit", "policy", "governance"]):
        compliance = 3
    elif any(w in text for w in ["review", "approval"]):
        compliance = 2

    # reliability risk: maturity of the system or component
    reliability = 1
    if any(w in text for w in ["unreliable", "unstable", "flaky", "broken"]):
        reliability = 5
    elif any(w in text for w in ["experimental", "prototype", "alpha", "beta"]):
        reliability = 4
    elif any(w in text for w in ["untested", "poc"]):
        reliability = 3
    elif any(w in text for w in ["proven", "mature"]):
        reliability = 2

    scores = {
        "operational": operational,
        "safety": safety,
        "compliance": compliance,
        "reliability": reliability,
    }
    scores["average"] = round(sum(scores.values()) / len(scores), 2)
    return scores
