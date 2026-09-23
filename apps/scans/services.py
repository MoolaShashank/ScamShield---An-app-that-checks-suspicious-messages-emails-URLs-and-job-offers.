from decimal import Decimal
from apps.detection.services import ScamAnalyzer
from .models import Scan, DetectionSignal


def analyze_and_save(user, input_type, raw_input):
    analyzer = ScamAnalyzer()
    result = analyzer.analyze_text(raw_input) if input_type == "TEXT" else analyzer.analyze_url(raw_input)
    if user.is_authenticated:
        ml = result["ml"]
        scan = Scan.objects.create(user=user, input_type=input_type, original_input=raw_input, normalized_input=result["normalized_input"], score=result["score"], risk_level=result["risk_level"], summary=result["summary"], ml_available=ml["available"], ml_prediction=ml["prediction"] or "", ml_confidence=Decimal(str(ml["confidence"])) if ml["confidence"] is not None else None)
        DetectionSignal.objects.bulk_create([DetectionSignal(scan=scan, code=s["code"], category=s["category"], title=s["title"], description=s["description"], evidence=s.get("evidence", ""), weight=s["severity"]) for s in result["signals"]])
        result["scan"] = scan
    return result
