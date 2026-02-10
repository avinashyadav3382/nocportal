import random
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Site, SiteStatusHistory, MCT_Data
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from .models import MCT_Data, AECMSData

# sites/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from .models import MCT_Data
from .forms import (
    MountAbuUpdateForm,
    KasauliUpdateForm,
    AdminMCTUpdateForm
)

# -----------------------------
# HTML PAGE (Map Dashboard)
# -----------------------------
def india_map_view(request):
    """
    NOC Map Dashboard page
    """
    sites = Site.objects.all()

    return render(request, "sites/test3.html", {"sites": sites})



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
        fake_times = [datetime.now() - timedelta(hours=random.randint(1, 72)) for _ in range(200)]
        fake_idx = 0
        for site in sites:
            data.append({
                "title": site.sitename,
                "latitude": site.latitude,
                "longitude": site.longitude,
                "color": site.color,
                "problem_since": fake_times[fake_idx].isoformat(),
                "address" : site.address,
            })
            fake_idx = (fake_idx + 1) % len(fake_times)

        return Response(data)


def contact_info_view(request, sitename):
    contacts = Site.objects.filter(sitename=sitename).values(
        "id","sitename", "phone", "address"
    )
    return JsonResponse(list(contacts), safe=False)


def site_status_history_view(request, sitename):
    site = Site.objects.get(sitename=sitename)
    history = site.status_history.all().values(
        "site__sitename", "past_status", "current_status", "status_changed_at"
    )
    return JsonResponse(list(history), safe=False)

def status_history_all_sites(request):
    history = SiteStatusHistory.objects.all().values(
        "site__sitename", "past_status", "current_status", "status_changed_at"
    )
    return JsonResponse(list(history), safe=False)


def view_past_history(request):
    # send which are changed in last 48 hours 
    time_diff = timezone.now() - timedelta(hours=48)
    data_list = SiteStatusHistory.objects.filter(
        status_changed_at__gte=time_diff
    ).values(
        "site__sitename", "past_status", "current_status", "status_changed_at"
    )
    return render(request, 'sites/past_history.html', {'data_list': data_list})



@login_required
def mct_data_view(request):
    user = request.user
    username = user.username.lower()
    is_admin = 'admin' in username

    if is_admin:
        queryset = MCT_Data.objects.all()
        EditForm = AdminMCTUpdateForm
    elif 'user1' in username or 'abu' in username:
        queryset = MCT_Data.objects.filter(location='Mount Abu')
        EditForm = MountAbuUpdateForm
    elif 'user2' in username:
        queryset = MCT_Data.objects.filter(location='Kasauli')
        EditForm = KasauliUpdateForm
    else:
        queryset = MCT_Data.objects.none()
        messages.warning(request, "You don't have permission to view these records.")
        EditForm = None

    EditFormSet = modelformset_factory(
        MCT_Data,
        form=EditForm,
        extra=0,
        can_delete=False
    )

    if request.method == 'POST':
        formset = EditFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            updated_count = 0
            for instance in instances:
                if instance.pk:
                    instance.last_updated_by = user.username
                    instance.last_updated = timezone.now()
                    instance.save()
                    updated_count += 1
            messages.success(request, f"{updated_count} records updated successfully!")
            return redirect(request.path)
        else:
            messages.error(request, "Please correct the errors.")
    else:
        formset = EditFormSet(queryset=queryset)

    return render(request, 'sites/mct_satcom_data.html', {
        'edit_formset': formset,
        'is_admin': is_admin,
    })


def mct_india_map(request):
    
    data = MCT_Data.objects.all().values(
        "location", "data_type", "total_counter", "fully_ops_counter", "restricted_ops_counter", "non_ops_counter", "misc_counter", "last_updated"
    )
    return JsonResponse(list(data), safe=False)





def india_map_iaccs_status(request):
    #only down node names
    data2 = AECMSData.objects.filter(status='DOWN').values("node_name", "type", "status").values("node_name", "type", "status")

    return JsonResponse(list(data2), safe=False)
