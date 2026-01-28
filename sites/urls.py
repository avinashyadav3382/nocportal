from django.urls import path
from .views import india_map_view, SiteMapAPIView, contact_info_view, status_history_all_sites, site_status_history_view, recent_status_changes

urlpatterns = [
    path("", india_map_view, name="india-map"),
    path("api/sites/map/", SiteMapAPIView.as_view(), name="site-map-api"),
    path("api/contact-info/<str:site_name>/", contact_info_view, name="contact-info"),
    path("api/status-history/<str:site_name>/", site_status_history_view, name="site-status-history"),
    path("api/status-history/", status_history_all_sites, name="status-history-all-sites"),
    path("api/recent-status-changes/", recent_status_changes, name="recent-status-changes"),

]
