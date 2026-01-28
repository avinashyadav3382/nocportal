# sites/models.py
from django.db import models
from django.utils import timezone

class Site(models.Model):

    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    color = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SiteStatusHistory(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="status_history"
    )
    past_status = models.CharField(max_length=50)
    current_status = models.CharField(max_length=50)
    status_changed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.site.name}: {self.past_status} → {self.current_status}"


class ContactInfo(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="contacts"
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.site.name} - {self.email}"
