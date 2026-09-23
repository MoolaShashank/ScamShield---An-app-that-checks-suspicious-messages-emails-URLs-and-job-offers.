import uuid
from django.conf import settings
from django.db import models


class Scan(models.Model):
    class InputType(models.TextChoices): TEXT = "TEXT", "Text"; URL = "URL", "URL"
    class RiskLevel(models.TextChoices): LOW = "LOW", "Low"; MEDIUM = "MEDIUM", "Medium"; HIGH = "HIGH", "High"; CRITICAL = "CRITICAL", "Critical"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="scans")
    input_type = models.CharField(max_length=4, choices=InputType.choices)
    original_input = models.TextField()
    normalized_input = models.TextField(blank=True)
    score = models.PositiveSmallIntegerField()
    risk_level = models.CharField(max_length=8, choices=RiskLevel.choices)
    summary = models.TextField()
    ml_available = models.BooleanField(default=False)
    ml_prediction = models.CharField(max_length=20, blank=True)
    ml_confidence = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ["-created_at"]


class DetectionSignal(models.Model):
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name="signals")
    code = models.CharField(max_length=80)
    category = models.CharField(max_length=80)
    title = models.CharField(max_length=160)
    description = models.TextField()
    evidence = models.TextField(blank=True)
    weight = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
