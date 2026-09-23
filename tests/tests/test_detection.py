import pytest
from apps.detection.services import ScamAnalyzer


@pytest.mark.django_db
def test_otp_and_urgency_is_high_risk():
    result = ScamAnalyzer().analyze_text("Final warning: send your OTP immediately or your account will be closed.")
    assert result["score"] >= 35
    assert {s["code"] for s in result["signals"]} >= {"CREDENTIAL_REQUEST", "URGENCY"}


@pytest.mark.django_db
def test_legitimate_message_is_low_risk():
    result = ScamAnalyzer().analyze_text("Your appointment is confirmed for tomorrow at 10:30 AM.")
    assert result["risk_level"] == "LOW"


@pytest.mark.django_db
def test_url_string_is_not_fetched_and_has_signals():
    result = ScamAnalyzer().analyze_url("http://user:pass@192.168.1.9/login?x=1")
    assert result["score"] >= 40
    assert {s["code"] for s in result["signals"]} >= {"IP_HOST", "USERINFO", "NO_HTTPS"}


@pytest.mark.django_db
def test_score_levels_are_bounded():
    result = ScamAnalyzer().analyze_text("OTP password CVV send money processing fee urgent act now lottery prize work from home registration fee legal action")
    assert 0 <= result["score"] <= 100
    assert result["risk_level"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
