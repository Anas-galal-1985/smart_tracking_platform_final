from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.

# cameras/views.py

from .forms import CameraForm
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend  # استيراد فلتر Django
from .models import Camera
from .serializers import CameraSerializer
from django.contrib.auth.decorators import login_required
# صلاحية مخصصة: القراءة للجميع، التعديل للأدمن فقط
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    # إضافة فلترة، بحث، وترتيب
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'location']  # الحقول التي يمكن فلترتها مباشرة
    search_fields = ['name', 'location']
    ordering_fields = ['created_at', 'name']
    ordering = ['name']




@login_required
def camera_list_view(request):
    q = request.GET.get('q', '')
    if q:
        cameras = Camera.objects.filter(name__icontains=q) | Camera.objects.filter(location__icontains=q)
    else:
        cameras = Camera.objects.all()
    return render(request, 'cameras/camera_list.html', {'cameras': cameras, 'query': q})


def camera_detail_view(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    return render(request, 'cameras/camera_detail.html', {'camera': camera})

from django.contrib import messages


# إضافة كاميرا
@login_required
def camera_create_view(request):
    if not request.user.is_staff:
        return redirect('camera_list')
    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت إضافة الكاميرا بنجاح!")
            return redirect('camera_list')
        else:
            messages.error(request, "حدث خطأ، يرجى التأكد من صحة البيانات.")
    else:
        form = CameraForm()
    return render(request, 'cameras/camera_form.html', {'form': form, 'title': 'إضافة كاميرا'})

# تعديل كاميرا
@login_required
def camera_edit_view(request, pk):
    if not request.user.is_staff:
        return redirect('camera_list')
    camera_obj = get_object_or_404(Camera, pk=pk)
    if request.method == 'POST':
        form = CameraForm(request.POST, instance=camera_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الكاميرا بنجاح!")
            return redirect('camera_list')
        else:
            messages.error(request, "حدث خطأ، يرجى التأكد من صحة البيانات.")
    else:
        form = CameraForm(instance=camera_obj)
    return render(request, 'cameras/camera_form.html', {'form': form, 'title': 'تعديل الكاميرا'})

# حذف كاميرا
@login_required
def camera_delete_view(request, pk):
    if not request.user.is_staff:
        return redirect('camera_list')
    camera = get_object_or_404(Camera, pk=pk)
    if request.method == 'POST':
        camera.delete()
        messages.success(request, "تم حذف الكاميرا بنجاح!")
        return redirect('camera_list')
    return render(request, 'cameras/camera_confirm_delete.html', {'camera': camera})