from django.urls import path
from .api import AnalyzeTextAPI, AnalyzeURLAPI, ScanListAPI, ScanDetailAPI

urlpatterns = [path("analyze/text/", AnalyzeTextAPI.as_view()), path("analyze/url/", AnalyzeURLAPI.as_view()), path("scans/", ScanListAPI.as_view()), path("scans/<uuid:pk>/", ScanDetailAPI.as_view())]
