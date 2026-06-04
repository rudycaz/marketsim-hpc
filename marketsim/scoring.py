def label_from_score(score: float) -> str:
    if score >= 80:
        return "Strong Bullish"
    if score >= 61:
        return "Bullish"
    if score >= 41:
        return "Neutral"
    if score >= 21:
        return "Bearish"
    return "Strong Bearish"


def compute_trend_score(probability_up: float, expected_return: float, momentum: float, risk_score: float) -> float:
    """Combine simulation and technical signals into a 0-100 trend score."""
    sim_score = probability_up * 100
    return_score = 50 + expected_return * 250  # +20% maps near 100, -20% maps near 0.
    return_score = max(0, min(100, return_score))

    score = (
        0.45 * sim_score
        + 0.25 * return_score
        + 0.20 * momentum
        + 0.10 * risk_score
    )
    return float(max(0, min(100, score)))
