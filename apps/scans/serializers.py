from rest_framework import serializers
from .models import Scan, DetectionSignal


class TextAnalyzeSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=10000)


class URLAnalyzeSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=2048)


class SignalSerializer(serializers.ModelSerializer):
    class Meta: model = DetectionSignal; fields = ("code", "category", "title", "description", "evidence", "weight")


class ScanSerializer(serializers.ModelSerializer):
    signals = SignalSerializer(many=True, read_only=True)
    class Meta: model = Scan; fields = ("id", "input_type", "score", "risk_level", "summary", "ml_available", "ml_prediction", "ml_confidence", "created_at", "signals")
