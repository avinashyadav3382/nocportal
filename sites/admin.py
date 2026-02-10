from django.contrib import admin
from .models import Site, SiteStatusHistory, MCT_SatcomData, AECMSData


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("sitename", "color", )
    search_fields = ("sitename",)


@admin.register(SiteStatusHistory)
class SiteStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("site", "past_status", "current_status", "status_changed_at")
    search_fields = ("site__name", "past_status", "current_status")

@admin.register(MCT_SatcomData)
class MCT_SatcomDataAdmin(admin.ModelAdmin):
    list_display = ("name", "data_type", "status", "last_updated_by", "last_updated")
    search_fields = ("name", "data_type", "status", "last_updated_by")

@admin.register(AECMSData)
class AECMSDataAdmin(admin.ModelAdmin):
    list_display = ("node_name", "type", "status")
    search_fields = ("node_name", "type", "status")