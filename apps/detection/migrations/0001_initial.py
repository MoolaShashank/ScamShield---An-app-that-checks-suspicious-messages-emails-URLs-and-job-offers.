from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="DetectionRule", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("code", models.CharField(max_length=80, unique=True)), ("category", models.CharField(max_length=50)), ("name", models.CharField(max_length=120)), ("pattern", models.CharField(max_length=500)), ("weight", models.PositiveSmallIntegerField(default=10)), ("active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True))]),
        migrations.CreateModel(name="TrainingExample", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("text", models.TextField()), ("label", models.BooleanField(help_text="True means scam")), ("source", models.CharField(default="admin", max_length=120)), ("active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True))]),
    ]
