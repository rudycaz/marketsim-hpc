from marketsim.scoring import compute_trend_score, label_from_score


def test_label_from_score():
    assert label_from_score(85) == "Strong Bullish"
    assert label_from_score(70) == "Bullish"
    assert label_from_score(50) == "Neutral"
    assert label_from_score(30) == "Bearish"
    assert label_from_score(10) == "Strong Bearish"


def test_compute_trend_score_bounds():
    score = compute_trend_score(0.5, 0.0, 50, 50)
    assert 0 <= score <= 100
