from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackedObjectViewSet
from .views import trackedobject_list_view,trackedobject_detail_view,trackedobject_edit
from . import views
router = DefaultRouter()
router.register(r'tracked-objects', TrackedObjectViewSet)

urlpatterns = [

    path('', views.trackedobject_list_view, name='tracked_list'),
    path('add/', views.tracked_add, name='tracked_add'),
    path('<int:pk>/', views.trackedobject_detail_view, name='tracked_detail'),
    path('<int:pk>/edit/', views.trackedobject_edit, name='tracked_edit'),
    path('<int:pk>/delete/', views.tracked_delete, name='tracked_delete'),
]
