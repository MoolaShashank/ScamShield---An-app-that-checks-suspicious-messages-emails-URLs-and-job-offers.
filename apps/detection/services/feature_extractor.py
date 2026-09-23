import re
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s<>()]+", re.I)


def text_features(text):
    words = re.findall(r"\b\w+\b", text)
    letters = [c for c in text if c.isalpha()]
    return {
        "text_length": len(text), "word_count": len(words),
        "uppercase_ratio": sum(c.isupper() for c in letters) / len(letters) if letters else 0,
        "exclamation_count": text.count("!"), "question_count": text.count("?"),
        "url_count": len(URL_RE.findall(text)),
        "phone_number_count": len(re.findall(r"(?:\+?\d[\s.-]?){7,}\d", text)),
        "money_amount_count": len(re.findall(r"(?:[$₹€£]\s?\d|\b\d+(?:\.\d{2})?\s?(?:usd|inr|dollars?))", text, re.I)),
    }


def url_features(url):
    parsed = urlparse(url)
    host = parsed.hostname or ""
    return {
        "url_length": len(url), "has_https": parsed.scheme == "https",
        "is_ip_host": bool(re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host)),
        "subdomain_count": max(0, len(host.split(".")) - 2),
        "query_parameter_count": len([p for p in parsed.query.split("&") if p]),
        "has_punycode": "xn--" in host.lower(), "has_userinfo": bool(parsed.username or parsed.password),
        "encoding_ratio": url.count("%") / max(1, len(url)),
    }
