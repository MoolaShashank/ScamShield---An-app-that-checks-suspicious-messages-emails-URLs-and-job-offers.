from pathlib import Path
import joblib
from django.conf import settings


def predict(text):
    model_path, vectorizer_path = Path(settings.ML_MODEL_PATH), Path(settings.ML_VECTORIZER_PATH)
    if not (model_path.exists() and vectorizer_path.exists()):
        return {"available": False, "prediction": None, "confidence": None}
    try:
        model, vectorizer = joblib.load(model_path), joblib.load(vectorizer_path)
        probability = float(model.predict_proba(vectorizer.transform([text]))[0][1])
        return {"available": True, "prediction": "scam" if probability >= .5 else "legitimate", "confidence": round(probability, 3)}
    except Exception:
        return {"available": False, "prediction": None, "confidence": None}
