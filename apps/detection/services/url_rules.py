import re
from urllib.parse import urlparse
from .feature_extractor import url_features

SUSPICIOUS_WORDS = ("login", "verify", "secure", "account", "update", "bank", "wallet", "crypto", "bonus", "prize", "gift")


def _signal(code, category, title, severity, description, evidence):
    return {"code": code, "category": category, "title": title, "description": description, "severity": severity, "evidence": evidence}


def scan_url(url):
    parsed = urlparse(url)
    features = url_features(url)
    host = parsed.hostname or ""
    signals = []
    if features["is_ip_host"]:
        signals.append(_signal("IP_HOST", "url_structure", "IP address used as host", 20, "Legitimate consumer links usually use a recognizable domain name.", host))
    if features["subdomain_count"] >= 3:
        signals.append(_signal("EXCESS_SUBDOMAINS", "url_structure", "Excessive subdomains", 12, "Many subdomains can make the real destination harder to recognize.", host))
    if features["url_length"] > 160:
        signals.append(_signal("LONG_URL", "url_structure", "Unusually long URL", 8, "Long links can hide important destination details.", url[:160]))
    if features["query_parameter_count"] > 6:
        signals.append(_signal("MANY_PARAMETERS", "url_structure", "Many URL parameters", 8, "The link includes an unusually large number of parameters.", parsed.query[:120]))
    if features["has_punycode"]:
        signals.append(_signal("PUNYCODE", "url_structure", "Internationalized domain encoding", 20, "Encoded domains can be used to visually imitate another domain.", host))
    if features["has_userinfo"] or "@" in parsed.netloc:
        signals.append(_signal("USERINFO", "url_structure", "Misleading @ symbol in URL", 20, "A user-info section can obscure the actual host name.", parsed.netloc))
    if features["encoding_ratio"] > .05:
        signals.append(_signal("EXCESS_ENCODING", "url_structure", "Excessive URL encoding", 10, "Heavy encoding can conceal where a link leads.", url[:120]))
    if not features["has_https"]:
        signals.append(_signal("NO_HTTPS", "transport", "No HTTPS", 5, "This link does not use encrypted HTTPS transport.", parsed.scheme or "no scheme"))
    hits = [word for word in SUSPICIOUS_WORDS if word in f"{host}{parsed.path}".lower()]
    if hits:
        signals.append(_signal("SUSPICIOUS_KEYWORDS", "url_content", "Sensitive-account keywords in URL", min(20, 5 * len(hits)), "The URL uses terms commonly found in credential or reward lures.", ", ".join(hits)))
    return signals, sorted({s["category"] for s in signals}), features
