# tracking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import TrackedObject
from .serializers import TrackedObjectSerializer
from .forms import TrackedObjectForm
from django.db import models
from django.core.paginator import Paginator
# صلاحية: القراءة للجميع، التعديل للأدمن فقط
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

# API ViewSet
class TrackedObjectViewSet(viewsets.ModelViewSet):
    queryset = TrackedObject.objects.all()
    serializer_class = TrackedObjectSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['camera', 'timestamp']
    search_fields = ['label', 'camera__name']
    ordering_fields = ['timestamp', 'track_id']
    ordering = ['timestamp']

# صفحات الويب
def trackedobject_list_view(request):
    query = request.GET.get('q', '')
    if query:
        tracked_objects = TrackedObject.objects.filter(
            models.Q(label__icontains=query) |
            models.Q(camera__name__icontains=query)
        ).order_by('timestamp')
    else:
        tracked_objects = TrackedObject.objects.all().order_by('timestamp')
    
    return render(request, 'tracking/trackedobject_list.html', {
        'tracked_objects': tracked_objects,
        'query': query
    })

def trackedobject_detail_view(request, pk):
    tracked_object = get_object_or_404(TrackedObject, pk=pk)
    return render(request, 'tracking/trackedobject_detail.html', {'object': tracked_object})

@login_required
def tracked_add(request):
    if not request.user.is_staff:
        messages.error(request, "ليس لديك صلاحية لإضافة كائنات متتبعة.")
        return redirect('tracked_list')
    
    if request.method == 'POST':
        form = TrackedObjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة الكائن المتتبع بنجاح!")
            return redirect('tracked_list')
        else:
            messages.error(request, "حدث خطأ، يرجى التأكد من صحة البيانات.")
    else:
        form = TrackedObjectForm()
    
    return render(request, 'tracking/trackedobject_form.html', {'form': form})

@login_required
def trackedobject_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "ليس لديك صلاحية تعديل الكائنات المتتبعة.")
        return redirect('tracked_list')
    
    tracked_obj = get_object_or_404(TrackedObject, pk=pk)
    
    if request.method == 'POST':
        form = TrackedObjectForm(request.POST, instance=tracked_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الكائن المتتبع بنجاح!")
            return redirect('tracked_list')
        else:
            messages.error(request, "حدث خطأ، يرجى التأكد من صحة البيانات.")
    else:
        form = TrackedObjectForm(instance=tracked_obj)
    
    return render(request, 'tracking/trackedobject_form.html', {'form': form})

@login_required
def tracked_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "ليس لديك صلاحية حذف الكائنات المتتبعة.")
        return redirect('tracked_list')
    
    obj = get_object_or_404(TrackedObject, pk=pk)
    
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "تم حذف الكائن المتتبع بنجاح!")
        return redirect('tracked_list')
    
    return render(request, 'tracking/tracked_confirm_delete.html', {'object': obj})



def trackedobject_list_view(request):
    query = request.GET.get('q', '')

    if query:
        tracked_objects = TrackedObject.objects.filter(
            models.Q(label__icontains=query) |
            models.Q(camera__name__icontains=query)
        ).order_by('timestamp')
    else:
        tracked_objects = TrackedObject.objects.all().order_by('timestamp')

    # Pagination: 10 عناصر لكل صفحة
    paginator = Paginator(tracked_objects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tracking/trackedobject_list.html', {
        'page_obj': page_obj,
        'query': query
    })