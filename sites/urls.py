from django.urls import path
from .views import india_map_view, SiteMapAPIView, contact_info_view, status_history_all_sites, site_status_history_view
from .views import mct_data_view, mct_india_map, india_map_iaccs_status, view_past_history
urlpatterns = [
    path("", india_map_view, name="india-map"),
    path("api/sites/map/", SiteMapAPIView.as_view(), name="site-map-api"),
    path("api/site-contact-info/<str:sitename>/", contact_info_view, name="contact-info"),
    path("api/status-history/<str:sitename>/", site_status_history_view, name="site-status-history"),
    path("api/status-history/", status_history_all_sites, name="status-history-all-sites"),
    path("view_past_history/", view_past_history, name="view-past-history"),
    path('mct-data/', mct_data_view, name='mct_data'),
    path('api/mct-data/', mct_india_map, name='mct_india_map'),
    path('india_map_iaccs_status/', india_map_iaccs_status, name='india_map_iaccs_status'),
    
]
