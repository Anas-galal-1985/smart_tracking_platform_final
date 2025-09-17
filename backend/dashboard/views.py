from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from cameras.models import Camera
from tracking.models import TrackedObject

@login_required
def dashboard_view(request):
    context = {
        'total_users': Profile.objects.count(),
        'total_cameras': Camera.objects.count(),
        'total_tracked': TrackedObject.objects.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)
