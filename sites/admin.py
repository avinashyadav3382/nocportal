from django.contrib import admin
from .models import Site, ContactInfo


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "color", )
    search_fields = ("name",)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("site", "email", "phone")
    search_fields = ("site__name", "email", "phone")
