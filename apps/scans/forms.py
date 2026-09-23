from django import forms
from django.conf import settings
from urllib.parse import urlparse


class TextScanForm(forms.Form):
    text = forms.CharField(
        label="Message or email",
        max_length=settings.SCAN_MAX_LENGTH,
        help_text="You can paste an SMS, email, social message, or job offer.",
        widget=forms.Textarea(attrs={"rows": 9, "placeholder": "Paste the content you want to check...", "class": "form-control"}),
    )


class URLScanForm(forms.Form):
    url = forms.CharField(
        label="Website link",
        max_length=2048,
        help_text="We inspect the URL string only—we never open the website.",
        widget=forms.URLInput(attrs={"placeholder": "https://example.com", "class": "form-control"}),
    )

    def clean_url(self):
        url = self.cleaned_data["url"].strip()
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise forms.ValidationError("Please enter a valid URL such as https://example.com")
        return url
