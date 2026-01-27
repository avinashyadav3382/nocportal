from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Site, ContactInfo


# -----------------------------
# HTML PAGE (Map Dashboard)
# -----------------------------
def india_map_view(request):
    """
    NOC Map Dashboard page
    """
    sites = Site.objects.all()

    return render(request, "sites/test_map_copy2.html", {"sites": sites})


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
