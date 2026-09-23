import re
from .feature_extractor import text_features, URL_RE
from .text_rules import scan_text
from .url_rules import scan_url
from .risk_engine import score, level_for, summary_for
from .ml_classifier import predict


class ScamAnalyzer:
    def analyze_text(self, text):
        normalized = " ".join(text.split())
        signals, categories = scan_text(normalized)
        for embedded in URL_RE.findall(normalized):
            url_signals, url_categories, _ = scan_url(embedded)
            signals.extend(url_signals)
            categories = sorted(set(categories) | set(url_categories))
        ml = predict(normalized)
        value = score(signals, ml)
        level = level_for(value)
        return {"input_type": "text", "normalized_input": normalized, "features": text_features(normalized), "score": value, "risk_level": level, "summary": summary_for(level), "signals": signals, "categories": categories, "ml": ml}

    def analyze_url(self, url):
        normalized = url.strip()
        signals, categories, features = scan_url(normalized)
        value = score(signals)
        level = level_for(value)
        return {"input_type": "url", "normalized_input": normalized, "features": features, "score": value, "risk_level": level, "summary": summary_for(level), "signals": signals, "categories": categories, "ml": {"available": False, "prediction": None, "confidence": None}}
