from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet
from .views import login_view, logout_view, user_list,user_detail,user_edit,settings_view
from . import views
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings_view, name='settings'),
    path('', views.user_list, name='users_list'),
    path('add/', views.user_add, name='user_add'),
    path('<int:pk>/', views.user_detail, name='user_detail'),  # هذا مهم
    path('<int:pk>/edit/', user_edit, name='user_edit'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
]
