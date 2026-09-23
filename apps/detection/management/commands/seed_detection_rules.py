from django.core.management.base import BaseCommand
from apps.detection.models import DetectionRule
from apps.detection.services.text_rules import RULES


class Command(BaseCommand):
    help = "Seed the built-in detection-rule catalogue."
    def handle(self, *args, **options):
        for code, category, name, weight, pattern, _ in RULES:
            DetectionRule.objects.update_or_create(code=code, defaults={"category": category, "name": name, "pattern": pattern, "weight": weight, "active": True})
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(RULES)} detection rules."))
