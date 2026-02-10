# sites/models.py
from django.db import models
from django.utils import timezone

class Site(models.Model):

    sitename = models.CharField(max_length=100, unique=True)
    cmd = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)


    color = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sitename

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
        return f"{self.site.sitename}: {self.past_status} → {self.current_status}"

class MCT_SatcomData(models.Model):
    type_choices = [
        ('MCT_Vehicle', 'MCT_Vehicle'),
        ('SATCOM', 'SATCOM'),]
    status_choices = [
        ('FULLY_OPS', 'FULLY_OPS'),
        ('RESTRICTED_OPS', 'RESTRICTED_OPS'),
        ('NON_OPS', 'NON_OPS')]
    
    name = models.CharField(max_length=100, unique=True)
    data_type = models.CharField(max_length=20, choices=type_choices)
    status = models.CharField(max_length=20, choices=status_choices)
    last_updated_by = models.CharField(max_length=100, blank=True)
    last_updated = models.DateTimeField(auto_now=True)


class AECMSData(models.Model):
    type_choices = [
        ('IACCS', 'IACCS'),
        ('DC', 'DC'),]
    node_name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=type_choices)
    