from pathlib import Path
import csv
import joblib
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Train the optional TF-IDF + logistic-regression text classifier."
    def add_arguments(self, parser): parser.add_argument("--data", default="ml/data/training.csv")
    def handle(self, *args, **options):
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
            from sklearn.model_selection import train_test_split
        except ImportError as exc:
            raise CommandError(f"ML dependencies could not load: {exc}. Rule-based analysis remains available.") from exc
        path = Path(options["data"])
        if not path.exists(): raise CommandError(f"Dataset not found: {path}")
        with path.open(encoding="utf-8", newline="") as f: rows = list(csv.DictReader(f))
        labels = [int(r["label"]) for r in rows]
        if len(rows) < 10 or len(set(labels)) < 2: raise CommandError("Need at least ten examples and both labels.")
        texts = [r["text"] for r in rows]
        x_train, x_test, y_train, y_test = train_test_split(texts, labels, test_size=.25, random_state=42, stratify=labels)
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")
        model = LogisticRegression(max_iter=1000, class_weight="balanced").fit(vectorizer.fit_transform(x_train), y_train)
        predictions = model.predict(vectorizer.transform(x_test))
        Path(settings.ML_MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, settings.ML_MODEL_PATH); joblib.dump(vectorizer, settings.ML_VECTORIZER_PATH)
        self.stdout.write(self.style.SUCCESS(f"Model saved. accuracy={accuracy_score(y_test, predictions):.3f} precision={precision_score(y_test, predictions, zero_division=0):.3f} recall={recall_score(y_test, predictions, zero_division=0):.3f} f1={f1_score(y_test, predictions, zero_division=0):.3f}"))
