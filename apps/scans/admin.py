from django.contrib import admin
from .models import Scan, DetectionSignal


class SignalInline(admin.TabularInline): model = DetectionSignal; extra = 0; readonly_fields = ("created_at",)


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "input_type", "score", "risk_level", "created_at")
    list_filter = ("input_type", "risk_level", "ml_available")
    search_fields = ("id", "user__username")
    inlines = [SignalInline]
