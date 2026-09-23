from pathlib import Path
import csv
import joblib
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Evaluate a trained model against a labeled CSV with text,label columns."
    def add_arguments(self, parser): parser.add_argument("--data", required=True)
    def handle(self, *args, **options):
        try:
            from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
        except ImportError as exc:
            raise CommandError(f"ML dependencies could not load: {exc}.") from exc
        if not (Path(settings.ML_MODEL_PATH).exists() and Path(settings.ML_VECTORIZER_PATH).exists()):
            raise CommandError("Model artifacts are missing. Run train_text_model first.")
        with Path(options["data"]).open(encoding="utf-8", newline="") as handle: rows = list(csv.DictReader(handle))
        if not rows: raise CommandError("The evaluation dataset is empty.")
        model, vectorizer = joblib.load(settings.ML_MODEL_PATH), joblib.load(settings.ML_VECTORIZER_PATH)
        labels = [int(row["label"]) for row in rows]
        probabilities = model.predict_proba(vectorizer.transform([row["text"] for row in rows]))[:, 1]
        predictions = (probabilities >= .5).astype(int)
        metrics = f"accuracy={accuracy_score(labels, predictions):.3f} precision={precision_score(labels, predictions, zero_division=0):.3f} recall={recall_score(labels, predictions, zero_division=0):.3f} f1={f1_score(labels, predictions, zero_division=0):.3f}"
        if len(set(labels)) == 2: metrics += f" roc_auc={roc_auc_score(labels, probabilities):.3f}"
        self.stdout.write(metrics)
