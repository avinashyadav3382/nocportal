from django.urls import path
from .views import india_map_view, SiteMapAPIView, contact_info_view, status_history_all_sites, site_status_history_view, recent_status_changes
from .views import mct_satcom_data_view, add_mct_satcom_entry, mct_satcom_india_map, india_map_iaccs_status
urlpatterns = [
    path("", india_map_view, name="india-map"),
    path("api/sites/map/", SiteMapAPIView.as_view(), name="site-map-api"),
    path("api/site-contact-info/<str:sitename>/", contact_info_view, name="contact-info"),
    path("api/status-history/<str:sitename>/", site_status_history_view, name="site-status-history"),
    path("api/status-history/", status_history_all_sites, name="status-history-all-sites"),
    path("api/recent-status-changes/", recent_status_changes, name="recent-status-changes"),
    path('mct-satcom-data/', mct_satcom_data_view, name='mct_satcom_data'),
    path('mct-satcom-data/add/', add_mct_satcom_entry, name='add_mct_satcom_entry'),
    path('api/mct-satcom/', mct_satcom_india_map, name='mct_satcom_india_map'),
    path('india_map_iaccs_status/', india_map_iaccs_status, name='india_map_iaccs_status'),
]
