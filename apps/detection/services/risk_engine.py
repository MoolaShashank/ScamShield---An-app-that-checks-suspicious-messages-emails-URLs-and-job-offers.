from django.conf import settings


def level_for(score):
    if score >= 75: return "CRITICAL"
    if score >= 50: return "HIGH"
    if score >= 25: return "MEDIUM"
    return "LOW"


def summary_for(level):
    return {
        "LOW": "Low risk indicators detected.", "MEDIUM": "Some suspicious indicators detected.",
        "HIGH": "Strong scam indicators detected.", "CRITICAL": "Multiple severe scam indicators detected.",
    }[level]


def score(signals, ml=None):
    rule_score = min(100, sum(s["severity"] for s in {s["code"]: s for s in signals}.values()))
    if ml and ml.get("available"):
        final = round(settings.RULE_SCORE_WEIGHT * rule_score + settings.ML_SCORE_WEIGHT * (ml["confidence"] * 100))
    else:
        final = rule_score
    return min(100, max(0, final))
