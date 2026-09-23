# ScamShield

ScamShield is a Django security utility that analyzes pasted messages and URL strings for common fraud indicators. It gives a 0–100 product risk score with plain-language reasons. It does **not** claim certainty and does not fetch or render submitted URLs.

## Features

- Anonymous text and URL scans with explainable rule-based indicators.
- Optional TF-IDF + logistic-regression classifier; safe rule-only fallback if artifacts are absent.
- Django authentication, private scan history, deletion controls, dashboard charts, and Django Admin.
- JSON API under `/api/v1/`; health check at `/health/`.
- CSRF protection, input limits, ORM-only persistence, production configuration, Docker support.

## Live Demo Previews

### 1. Risk Analysis Dashboard
<!-- Drag and drop your dashboard screenshot here -->

### 2. High-Risk Text Detection
<!-- Drag and drop a screenshot of a scan result here -->

### 3. URL Scanning 
<!-- Drag and drop a screenshot of a URL scan result here -->

## Architecture

`ScamAnalyzer` normalizes input, extracts features, applies deterministic text/URL rules, optionally blends model probability, then returns the risk result. Views do not fetch URLs. Authenticated results are stored as `Scan` and `DetectionSignal`; anonymous results are not persisted.

## Local setup

```cmd
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_detection_rules
python manage.py createsuperuser
python manage.py runserver
