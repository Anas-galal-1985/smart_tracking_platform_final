from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
# Create your views here.
# accounts/views.py
from rest_framework import viewsets, permissions, filters
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from django.core.paginator import Paginator
from django.contrib import messages
# صلاحية: القراءة للجميع، التعديل للأدمن فقط
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

# Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['id', 'username', 'date_joined']
    ordering = ['username']

# Profiles
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'role', 'user__username']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['created_at']

def user_list(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            models.Q(username__icontains=query) |
            models.Q(email__icontains=query)
        ).order_by('id')
    else:
        users = User.objects.all().order_by('id')
    
    # Pagination: 10 مستخدمين لكل صفحة
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/user_list.html', {
        'page_obj': page_obj,
        'query': query
    })
@login_required
def user_detail(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/user_detail.html', {'user_obj': user_obj})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile

from .forms import UserForm, ProfileForm
from .models import Profile

@login_required
def user_add(request):
    if not request.user.is_staff:
        return redirect('users_list')

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f"تم إنشاء المستخدم {user.username} بنجاح!")
            return redirect('users_list')
        else:
            messages.error(request, "حدث خطأ، يرجى التأكد من صحة البيانات.")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'accounts/user_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_edit': False
    })

@login_required
def user_edit(request, pk):
    if not request.user.is_staff:
        return redirect('users_list')

    user_obj = get_object_or_404(User, pk=pk)
    profile_obj, created = Profile.objects.get_or_create(user=user_obj)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user_obj)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"تم تعديل بيانات المستخدم {user_obj.username} بنجاح!")
            return redirect('users_list')
        else:
            messages.error(request, "حدث خطأ، يرجى التأكد من صحة البيانات.")
    else:
        user_form = UserForm(instance=user_obj)
        profile_form = ProfileForm(instance=profile_obj)

    return render(request, 'accounts/user_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_edit': True
    })
@login_required
def user_delete(request, pk):
    if not request.user.is_staff:
        return redirect('users_list')
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_obj.delete()
        return redirect('users_list')
    return render(request, 'accounts/user_confirm_delete.html', {'user_obj': user_obj})
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # إذا كان المستخدم مسجل الدخول مسبقًا

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password is incorrect.')

    return render(request, 'accounts/login.html')
# صفحة تسجيل الخروج
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

from .models import SiteSettings
from .forms import SiteSettingsForm


from django.shortcuts import render
from django.http import JsonResponse
from .models import SiteSettings
from .forms import SiteSettingsForm
from django.contrib.auth.decorators import login_required

@login_required
def settings_view(request):
    settings = SiteSettings.objects.first()  # نفترض وجود سجل واحد فقط
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings saved successfully!")
            return redirect('settings')  # سيعيد تحميل الصفحة مع اللون الجديد
    else:
        form = SiteSettingsForm(instance=settings)

    context = {
        "form": form,
        "navbar_color": settings.navbar_color
    }
    return render(request, "accounts/settings.html", context)