from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, render
from apps.scans.models import Scan, DetectionSignal


@login_required
def home(request):
    scans = Scan.objects.filter(user=request.user)
    total = scans.count()
    category = DetectionSignal.objects.filter(scan__user=request.user).values("category").annotate(count=Count("id")).order_by("-count").first()
    trends = list(scans.annotate(day=TruncDate("created_at")).values("day").annotate(count=Count("id")).order_by("day"))
    distribution = list(scans.values("risk_level").annotate(count=Count("id")).order_by("risk_level"))
    context = {"total": total, "high_risk": scans.filter(risk_level__in=["HIGH", "CRITICAL"]).count(), "average": round(scans.aggregate(avg=Avg("score"))["avg"] or 0), "common_category": category["category"].replace("_", " ").title() if category else "—", "recent": scans[:8], "trend_labels": [str(item["day"]) for item in trends], "trend_values": [item["count"] for item in trends], "risk_labels": [item["risk_level"] for item in distribution], "risk_values": [item["count"] for item in distribution]}
    return render(request, "dashboard/home.html", context)


@login_required
def history(request):
    return render(request, "dashboard/history.html", {"scans": Scan.objects.filter(user=request.user)})


@login_required
def clear_history(request):
    if request.method == "POST":
        Scan.objects.filter(user=request.user).delete()
    return redirect("dashboard:history")
