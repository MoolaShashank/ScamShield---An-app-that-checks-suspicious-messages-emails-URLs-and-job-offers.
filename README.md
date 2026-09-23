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
```

Open `http://127.0.0.1:8000/`. Run the quality suite with `pytest`.

## Optional ML

Seed safe examples then train a baseline:

```cmd
python manage.py seed_demo_data
python manage.py train_text_model
```

Use only appropriately licensed/public or synthetic data. Model artifacts are ignored by Git. The app remains functional if they are missing.

## API

- `POST /api/v1/analyze/text/` with `{ "text": "..." }`
- `POST /api/v1/analyze/url/` with `{ "url": "https://example.com" }`
- `GET /api/v1/scans/` (authenticated)
- `GET` or `DELETE /api/v1/scans/<uuid>/` (owner only)

## Privacy and security notes

Do not submit passwords, OTPs, PINs, CVVs, or full card data. In production set a unique `SECRET_KEY`, `DEBUG=False`, proper `ALLOWED_HOSTS`, HTTPS, and a PostgreSQL `DATABASE_URL`. Configure an explicit retention policy for stored scans. The MVP analyzes URLs as strings only to avoid SSRF and remote-content execution.

## Deployment

Set environment variables from `.env.example`, use PostgreSQL, then run migrations and `collectstatic`. The supplied Docker stack starts Gunicorn and serves static files through WhiteNoise. Configure TLS at the platform/proxy layer before enabling the production settings.

## Limitations and roadmap

Scores indicate patterns, not objective probabilities or proof of fraud. Suggested next work: a properly evaluated data set, stronger safe rule management, accessibility audit, localized user guidance, feedback collection, and independently designed SSRF defenses before any optional remote URL retrieval.
