from .models import SiteSettings

def site_settings(request):
    """Global context processor for site settings"""
    return {
        'site_settings': SiteSettings.load()
    } 