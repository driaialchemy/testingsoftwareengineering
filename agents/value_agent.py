def score_value(proposal: str) -> dict:
    """Score proposal across 4 value dimensions (1=low, 5=high)."""
    text = proposal.lower()

    # business value: strategic and customer impact
    business_value = 1
    if any(w in text for w in ["revenue", "profit", "growth", "strategic"]):
        business_value = 5
    elif any(w in text for w in ["customer", "client", "satisfaction", "retention"]):
        business_value = 4
    elif any(w in text for w in ["productivity", "team", "process"]):
        business_value = 3
    elif any(w in text for w in ["improve", "better", "enhance"]):
        business_value = 2

    # efficiency: degree of automation or speed gain
    efficiency = 1
    if any(w in text for w in ["10x", "100x", "massive", "dramatic"]):
        efficiency = 5
    elif any(w in text for w in ["automate", "automation", "eliminate manual"]):
        efficiency = 4
    elif any(w in text for w in ["streamline", "optimize", "faster", "speed"]):
        efficiency = 3
    elif any(w in text for w in ["reduce", "less", "fewer"]):
        efficiency = 2

    # cost reduction: financial savings
    cost_reduction = 1
    if any(w in text for w in ["save million", "significant savings", "major cost"]):
        cost_reduction = 5
    elif any(w in text for w in ["cost saving", "cost reduction", "cheaper", "save money"]):
        cost_reduction = 4
    elif any(w in text for w in ["budget", "expense", "cost"]):
        cost_reduction = 3
    elif any(w in text for w in ["efficient", "lean"]):
        cost_reduction = 2

    # deployment upside: breadth of rollout
    deployment_upside = 1
    if any(w in text for w in ["enterprise", "scale", "millions of users"]):
        deployment_upside = 5
    elif any(w in text for w in ["department", "organization", "company-wide"]):
        deployment_upside = 4
    elif any(w in text for w in ["team", "group", "division"]):
        deployment_upside = 3
    elif any(w in text for w in ["project", "workflow", "pipeline"]):
        deployment_upside = 2

    scores = {
        "business_value": business_value,
        "efficiency": efficiency,
        "cost_reduction": cost_reduction,
        "deployment_upside": deployment_upside,
    }
    scores["average"] = round(sum(scores.values()) / len(scores), 2)
    return scores
