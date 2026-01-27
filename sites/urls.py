from django.urls import path
from .views import india_map_view, SiteMapAPIView, contact_info_view

urlpatterns = [
    path("", india_map_view, name="india-map"),
    path("api/sites/map/", SiteMapAPIView.as_view(), name="site-map-api"),
    path("api/contact-info/<str:site_name>/", contact_info_view, name="contact-info")

]
