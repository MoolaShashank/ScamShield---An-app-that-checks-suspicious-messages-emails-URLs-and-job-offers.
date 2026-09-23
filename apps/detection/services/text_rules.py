import re

RULES = [
    ("CREDENTIAL_REQUEST", "credential_request", "Request for sensitive credentials", 25, r"\b(password|otp|one[- ]time password|verification code|\bpin\b|cvv|login details|banking details|card details)\b", "The content asks for credentials or verification information."),
    ("PAYMENT_REQUEST", "payment_request", "Request for money or payment", 20, r"\b(pay a fee|processing fee|activation fee|send money|transfer funds|deposit|crypto payment|gift card)\b", "The content asks for money before a claimed benefit or service."),
    ("URGENCY", "urgency", "Urgent or threatening language", 10, r"\b(urgent|immediately|act now|within 24 hours|final warning|account will be closed|last chance|respond now|suspended today)\b", "The content pressures you to act quickly."),
    ("PRIZE_CLAIM", "reward", "Prize or reward claim", 12, r"\b(congratulations|lottery|winner|prize|cashback approved|claim your reward)\b", "Unexpected prize claims are a common social-engineering lure."),
    ("JOB_FEE", "job_scam", "Job offer asking for a fee", 25, r"\b(work from home|easy money|guaranteed income|no experience required|registration fee|training fee|recruitment fee|pay to activate)\b", "The content contains job-offer language associated with advance-fee scams."),
    ("AUTHORITY_PRESSURE", "authority", "Authority or legal pressure", 15, r"\b(bank verification|tax department|police notice|government account|legal action|parcel customs)\b", "The content invokes authority to create pressure."),
]


def scan_text(text):
    signals = []
    categories = set()
    # The built-in catalogue is the safe source of patterns. Admin settings can
    # only enable/disable those entries or adjust their contribution.
    try:
        from apps.detection.models import DetectionRule
        overrides = {rule.code: rule for rule in DetectionRule.objects.all()}
    except Exception:
        overrides = {}
    for code, category, title, weight, pattern, description in RULES:
        override = overrides.get(code)
        if override and not override.active:
            continue
        if override:
            weight = override.weight
        match = re.search(pattern, text, re.I)
        if match:
            signals.append({"code": code, "category": category, "title": title, "description": description, "severity": weight, "evidence": match.group(0)})
            categories.add(category)
    if re.search(r"(?:\d\s){6,}\d|[\w.+-]+\s*\(at\)\s*[\w.-]+", text, re.I):
        signals.append({"code": "OBFUSCATED_CONTACT", "category": "obfuscation", "title": "Obfuscated contact details", "description": "Contact information is written in an unusual format.", "severity": 10, "evidence": "Obfuscated contact pattern"})
        categories.add("obfuscation")
    return signals, sorted(categories)
