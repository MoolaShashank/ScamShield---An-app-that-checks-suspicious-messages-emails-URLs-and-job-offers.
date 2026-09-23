import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from apps.scans.models import Scan


@pytest.mark.django_db
def test_anonymous_scan_is_not_saved(client):
    response = client.post(reverse("scans:text"), {"text": "Send your OTP immediately"})
    assert response.status_code == 200
    assert Scan.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_scan_is_saved_and_private(client):
    owner = User.objects.create_user("owner", password="testpass123")
    other = User.objects.create_user("other", password="testpass123")
    client.force_login(owner)
    client.post(reverse("scans:text"), {"text": "Send your OTP immediately"})
    scan = Scan.objects.get()
    assert scan.user == owner
    client.force_login(other)
    assert client.get(reverse("scans:detail", kwargs={"pk": scan.pk})).status_code == 404


@pytest.mark.django_db
def test_api_validation_and_history_permissions(client):
    assert client.get("/api/v1/scans/").status_code in {401, 403}
    response = client.post("/api/v1/analyze/text/", data={"text": "Urgent: send OTP"}, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["risk_level"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


@pytest.mark.django_db
def test_signup_and_protected_dashboard(client):
    assert client.get(reverse("dashboard:home")).status_code == 302
    response = client.post(reverse("signup"), {"username": "newuser", "email": "new@example.com", "password1": "SecurePass123!", "password2": "SecurePass123!"})
    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()
    assert client.get(reverse("dashboard:home")).status_code == 200
