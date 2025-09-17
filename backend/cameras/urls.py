from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CameraViewSet, camera_list_view,camera_detail_view,camera_edit_view
from . import views
router = DefaultRouter()
router.register(r'cameras', CameraViewSet)

urlpatterns = [
        # API endpoints
    path('', views.camera_list_view, name='camera_list'),
    path('add/', views.camera_create_view, name='camera_add'),
    path('<int:pk>/', views.camera_detail_view, name='camera_detail'),
    path('<int:pk>/edit/', views.camera_edit_view, name='camera_edit'),
    path('<int:pk>/delete/', views.camera_delete_view, name='camera_delete'),
]
