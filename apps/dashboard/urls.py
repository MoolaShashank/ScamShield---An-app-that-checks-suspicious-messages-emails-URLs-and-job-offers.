from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [path("", views.home, name="home"), path("history/", views.history, name="history"), path("history/clear/", views.clear_history, name="clear_history")]
