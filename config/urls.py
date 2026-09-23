from django.contrib import admin
from django.urls import include, path
from django.views.decorators.http import require_GET
from django.http import JsonResponse


@require_GET
def health(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.accounts.urls")),
    path("scan/", include("apps.scans.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("api/v1/", include("apps.scans.api_urls")),
    path("health/", health, name="health"),
]
