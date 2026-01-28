from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Site, ContactInfo, SiteStatusHistory


# -----------------------------
# HTML PAGE (Map Dashboard)
# -----------------------------
def india_map_view(request):
    """
    NOC Map Dashboard page
    """
    sites = Site.objects.all()

    return render(request, "sites/india_map_v_2.html", {"sites": sites})



# -----------------------------
# API FOR MAP DATA
# -----------------------------
class SiteMapAPIView(APIView):
    """
    Returns site coordinates and color for amCharts
    """

    def get(self, request):
        sites = Site.objects.all()
        data = []
        for site in sites:
            data.append({
                "title": site.name,
                "latitude": site.latitude,
                "longitude": site.longitude,
                "color": site.color,
            })

        return Response(data)


def contact_info_view(request, site_name):
    contacts = ContactInfo.objects.filter(site__name=site_name).values(
        "email", "phone", "address"
    )
    return JsonResponse(list(contacts), safe=False)


def site_status_history_view(request, site_name):
    site = Site.objects.get(name=site_name)
    history = site.status_history.all().values(
        "site__name", "past_status", "current_status", "status_changed_at"
    )
    return JsonResponse(list(history), safe=False)

def status_history_all_sites(request):
    history = SiteStatusHistory.objects.all().values(
        "site__name", "past_status", "current_status", "status_changed_at"
    )
    return JsonResponse(list(history), safe=False)


def recent_status_changes(request):
    # send which are changed in last 2 minutes
    two_minutes_ago = timezone.now() - timedelta(minutes=2)
    recent_changes = SiteStatusHistory.objects.filter(
        status_changed_at__gte=two_minutes_ago
    ).values(
        "site__name", "past_status", "current_status", "status_changed_at"
    )
    return JsonResponse(list(recent_changes), safe=False)