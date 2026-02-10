from django.contrib import admin
from .models import Site, SiteStatusHistory, MCT_Data, AECMSData


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("sitename", "color", )
    search_fields = ("sitename",)


@admin.register(SiteStatusHistory)
class SiteStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("site", "past_status", "current_status", "status_changed_at")
    search_fields = ("site__sitename", "past_status", "current_status")

@admin.register(MCT_Data)
class MCT_DataAdmin(admin.ModelAdmin):
    list_display = ("location", "data_type", "last_updated_by", "last_updated")
    search_fields = ("location", "data_type", "last_updated_by")

@admin.register(AECMSData)
class AECMSDataAdmin(admin.ModelAdmin):
    list_display = ("node_name", "type", "status")
    search_fields = ("node_name", "type", "status")