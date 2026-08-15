def calculate_risk_score(
    issue_detected,
    severity,
    sentiment,
    warranty_related=False,
    safety_issue=False,
    repeat_issue=False,
    hours_since_repair=None
):
    score = 0

    if issue_detected:
        score += 25

    severity_scores = {
        "Low": 5,
        "Medium": 15,
        "High": 25,
        "Critical": 35
    }

    score += severity_scores.get(severity, 0)

    sentiment_scores = {
        "Positive": 0,
        "Neutral": 5,
        "Negative": 15
    }

    score += sentiment_scores.get(sentiment, 0)

    if warranty_related:
        score += 10

    if safety_issue:
        score += 25

    if repeat_issue:
        score += 15

    if hours_since_repair is not None:
        if hours_since_repair <= 24:
            score += 10
        elif hours_since_repair <= 48:
            score += 5

    return min(score, 100)


def classify_risk(score):
    if score >= 80:
        return "Critical"

    if score >= 60:
        return "High"

    if score >= 30:
        return "Medium"

    return "Low"


def get_recommended_action(
    score,
    issue_detected,
    safety_issue=False,
    warranty_related=False
):
    if safety_issue:
        return "Immediate Human Escalation"

    if score >= 80:
        return "Immediate Technician Escalation"

    if warranty_related and issue_detected:
        return "Warranty Review + Technician Revisit"

    if score >= 60:
        return "Technician Revisit"

    if score >= 30:
        return "Support Follow-up"

    return "Close Case"