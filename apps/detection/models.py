from django.db import models


class DetectionRule(models.Model):
    code = models.CharField(max_length=80, unique=True)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=120)
    pattern = models.CharField(max_length=500)
    weight = models.PositiveSmallIntegerField(default=10)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TrainingExample(models.Model):
    text = models.TextField()
    label = models.BooleanField(help_text="True means scam")
    source = models.CharField(max_length=120, default="admin")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
