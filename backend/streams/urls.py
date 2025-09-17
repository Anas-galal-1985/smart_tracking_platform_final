from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.stream_list, name="stream_list"),
    path("upload/", views.upload_stream, name="upload_stream"),
    path("<int:pk>/", views.stream_detail, name="stream_detail"),
    path("<int:pk>/feed/", views.video_feed, name="video_feed"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
