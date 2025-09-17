from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet, ProfileViewSet, login_view, logout_view
from cameras.views import CameraViewSet
from tracking.views import TrackedObjectViewSet
from dashboard.views import dashboard_view
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'cameras', CameraViewSet)
router.register(r'tracked_objects', TrackedObjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/cameras/', include('cameras.urls')),
    path('api/tracking/', include('tracking.urls')),
    path('streams/', include('streams.urls')),

    # Frontend Pages
    path('', dashboard_view, name='dashboard'),        # لوحة التحكم
    path('login/', login_view, name='login'),          # تسجيل الدخول
    path('logout/', logout_view, name='logout'),       # تسجيل الخروج
    path('accounts/', include('accounts.urls')),       # إدارة المستخدمين
    path('cameras/', include('cameras.urls')),         # إدارة الكاميرات
    path('tracking/', include('tracking.urls')),       # إدارة التتبع
    path('wanted/', include('wanted.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)