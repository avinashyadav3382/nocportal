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

class MCT_Data(models.Model):
    type_choices = [
        ('MCT', 'MCT'),
        ('MCT LSV', 'MCT LSV'),]
    
    location_choices = [
        ('Mount Abu', 'Mount Abu'),
        ('Kasauli', 'Kasauli')
    ]
    location = models.CharField(max_length=100, choices=location_choices)
    data_type = models.CharField(max_length=20, choices=type_choices)
    total_counter = models.IntegerField()
    fully_ops_counter = models.IntegerField(default=0)
    restricted_ops_counter = models.IntegerField(default=0)
    non_ops_counter = models.IntegerField(default=0)
    misc_counter = models.IntegerField(default=0)
    last_updated_by = models.CharField(max_length=100, blank=True)
    last_updated = models.DateTimeField(auto_now=True)


class AECMSData(models.Model):
    type_choices = [
        ('IACCS', 'IACCS'),
        ('DC', 'DC'),]
    node_name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=type_choices)
    