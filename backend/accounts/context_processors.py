from .models import SiteSettings

def navbar_settings(request):
    settings = SiteSettings.objects.first()
    navbar_color = settings.navbar_color if settings else 'primary'
    return {'navbar_color': navbar_color}
