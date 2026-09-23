from django.contrib import admin
from .models import DetectionRule, TrainingExample

admin.site.register(DetectionRule)
admin.site.register(TrainingExample)
