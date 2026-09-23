import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Scan", fields=[("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)), ("input_type", models.CharField(choices=[("TEXT", "Text"), ("URL", "URL")], max_length=4)), ("original_input", models.TextField()), ("normalized_input", models.TextField(blank=True)), ("score", models.PositiveSmallIntegerField()), ("risk_level", models.CharField(choices=[("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High"), ("CRITICAL", "Critical")], max_length=8)), ("summary", models.TextField()), ("ml_available", models.BooleanField(default=False)), ("ml_prediction", models.CharField(blank=True, max_length=20)), ("ml_confidence", models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="scans", to=settings.AUTH_USER_MODEL))], options={"ordering": ["-created_at"]}),
        migrations.CreateModel(name="DetectionSignal", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("code", models.CharField(max_length=80)), ("category", models.CharField(max_length=80)), ("title", models.CharField(max_length=160)), ("description", models.TextField()), ("evidence", models.TextField(blank=True)), ("weight", models.PositiveSmallIntegerField()), ("created_at", models.DateTimeField(auto_now_add=True)), ("scan", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="signals", to="scans.scan"))]),
    ]
