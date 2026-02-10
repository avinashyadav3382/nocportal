import random
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Site, SiteStatusHistory, MCT_SatcomData
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from .models import MCT_SatcomData, AECMSData

# sites/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from .models import MCT_SatcomData
from .forms import (
    MCTSatcomEditForm,
    MCTSatcomAdminAddForm,
    MCTAddForm,
    SatcomAddForm
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


def recent_status_changes(request):
    # send which are changed in last 2 minutes
    two_minutes_ago = timezone.now() - timedelta(minutes=2)
    recent_changes = SiteStatusHistory.objects.filter(
        status_changed_at__gte=two_minutes_ago
    ).values(
        "site__sitename", "past_status", "current_status", "status_changed_at"
    )
    return JsonResponse(list(recent_changes), safe=False)




@login_required
def mct_satcom_data_view(request):
    user = request.user
    username = user.username.lower()
    is_admin = 'admin' in username

    # Filter queryset based on user permission
    if is_admin:
        queryset = MCT_SatcomData.objects.all()
    elif 'user1' in username:
        queryset = MCT_SatcomData.objects.filter(data_type='MCT_Vehicle')
    elif 'user2' in username:
        queryset = MCT_SatcomData.objects.filter(data_type='SATCOM')
    else:
        queryset = MCT_SatcomData.objects.none()
        messages.warning(request, "You don't have permission to view these records.")

    # Formset for batch editing status
    EditFormSet = modelformset_factory(
        MCT_SatcomData,
        form=MCTSatcomEditForm,
        extra=0,
        can_delete=False
    )

    if request.method == 'POST':
        edit_formset = EditFormSet(request.POST, queryset=queryset)
        if edit_formset.is_valid():
            instances = edit_formset.save(commit=False)
            updated_count = 0
            for instance in instances:
                if instance.pk:
                    instance.last_updated_by = user.username
                    instance.last_updated = timezone.now()
                    instance.save()
                    updated_count += 1
            messages.success(request, f"{updated_count} records updated successfully!")
            return redirect('mct_satcom_data')
        else:
            messages.error(request, "Please correct the errors in the table.")
    else:
        edit_formset = EditFormSet(queryset=queryset)

    return render(request, 'sites/mct_satcom_data.html', {
        'edit_formset': edit_formset,
        'is_admin': is_admin,
    })


@login_required
def add_mct_satcom_entry(request):
    user = request.user
    username = user.username.lower()
    is_admin = 'admin' in username

    # Choose correct add form based on user
    if is_admin:
        AddFormClass = MCTSatcomAdminAddForm
    elif 'user1' in username:
        AddFormClass = MCTAddForm
    elif 'user2' in username:
        AddFormClass = SatcomAddForm
    else:
        messages.error(request, "You don't have permission to add new entries.")
        return redirect('mct_satcom_data')

    if request.method == 'POST':
        add_form = AddFormClass(request.POST)
        if add_form.is_valid():
            new_instance = add_form.save(commit=False)

            # Auto-set data_type for non-admins (view-level constraint)
            if not is_admin:
                if 'user1' in username:
                    new_instance.data_type = 'MCT_Vehicle'
                elif 'user2' in username:
                    new_instance.data_type = 'SATCOM'

            new_instance.last_updated_by = user.username
            new_instance.last_updated = timezone.now()
            new_instance.save()

            messages.success(request, f"New entry '{new_instance.name}' added successfully!")
            return redirect('mct_satcom_data')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        add_form = AddFormClass()

    return render(request, 'sites/mct_satcom_add.html', {
        'add_form': add_form,
        'is_admin': is_admin,
    })


def mct_satcom_india_map(request):
    """
    API to return MCT/SATCOM data for map visualization
    """
    data = []
    entries = MCT_SatcomData.objects.all()
    for entry in entries:
        data.append({
            "name": entry.name,
            "data_type": entry.data_type,
            "status": entry.status,
            "last_updated_by": entry.last_updated_by,
            "last_updated": entry.last_updated.isoformat(),
        })
    return JsonResponse(data, safe=False)

def india_map_iaccs_status(request):
    #only down node names
    data2 = AECMSData.objects.filter(status='DOWN').values("node_name", "type", "status").values("node_name", "type", "status")

    return JsonResponse(list(data2), safe=False)
