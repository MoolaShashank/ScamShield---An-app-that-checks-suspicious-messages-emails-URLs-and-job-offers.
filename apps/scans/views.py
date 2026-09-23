from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TextScanForm, URLScanForm
from .models import Scan
from .services import analyze_and_save


def text_scan(request):
    form = TextScanForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        result = analyze_and_save(request.user, "TEXT", form.cleaned_data["text"])
        return render(request, "scans/result.html", {"result": result})
    return render(request, "scans/scan_form.html", {"form": form, "mode": "text"})


def url_scan(request):
    form = URLScanForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        result = analyze_and_save(request.user, "URL", form.cleaned_data["url"])
        return render(request, "scans/result.html", {"result": result})
    return render(request, "scans/scan_form.html", {"form": form, "mode": "url"})


@login_required
def detail(request, pk):
    scan = get_object_or_404(Scan.objects.prefetch_related("signals"), pk=pk, user=request.user)
    result = {"scan": scan, "input_type": scan.input_type.lower(), "score": scan.score, "risk_level": scan.risk_level, "summary": scan.summary, "signals": [{"code": s.code, "category": s.category, "title": s.title, "description": s.description, "evidence": s.evidence, "severity": s.weight} for s in scan.signals.all()], "ml": {"available": scan.ml_available, "prediction": scan.ml_prediction, "confidence": scan.ml_confidence}}
    return render(request, "scans/result.html", {"result": result})


@login_required
def delete(request, pk):
    scan = get_object_or_404(Scan, pk=pk, user=request.user)
    if request.method == "POST":
        scan.delete()
        messages.success(request, "Scan deleted.")
    return redirect("dashboard:history")
