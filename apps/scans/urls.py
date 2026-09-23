from django.urls import path
from . import views

app_name = "scans"
urlpatterns = [path("text/", views.text_scan, name="text"), path("url/", views.url_scan, name="url"), path("detail/<uuid:pk>/", views.detail, name="detail"), path("delete/<uuid:pk>/", views.delete, name="delete")]
