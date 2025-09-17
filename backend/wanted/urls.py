from django.urls import path
from . import views

urlpatterns = [
    path('', views.wanted_list, name='wanted_list'),
    path('add/', views.wanted_add, name='wanted_add'),
    path('<int:pk>/', views.wanted_detail, name='wanted_detail'),
    path('<int:pk>/edit/', views.wanted_edit, name='wanted_edit'),
    path('<int:pk>/delete/', views.wanted_delete, name='wanted_delete'),
]
