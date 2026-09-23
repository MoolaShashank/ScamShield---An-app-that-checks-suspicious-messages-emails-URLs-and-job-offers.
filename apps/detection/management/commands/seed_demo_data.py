from django.core.management.base import BaseCommand
from apps.detection.models import TrainingExample

DEMO = [("Congratulations! You have won a prize. Pay the processing fee immediately to claim it.", True), ("Your account will be suspended today unless you verify your OTP.", True), ("We received your appointment request for tomorrow at 10:30 AM.", False), ("Your monthly electricity bill is ready in your official customer portal.", False)]


class Command(BaseCommand):
    help = "Seed safe demonstration training examples."
    def handle(self, *args, **options):
        for text, label in DEMO: TrainingExample.objects.get_or_create(text=text, defaults={"label": label, "source": "safe-demo"})
        self.stdout.write(self.style.SUCCESS("Safe demo examples seeded."))
