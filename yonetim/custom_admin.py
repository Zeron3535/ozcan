from django.contrib.admin import AdminSite
from django.contrib.auth import logout
from django.apps import apps


class CustomAdminSite(AdminSite):
    def login(self, request, extra_context=None):
        # Force logout to ensure admin login form always requires credentials
        logout(request)
        return super().login(request, extra_context)

    # Customize admin site
    site_header = "BanaRandevu Yönetim Paneli"
    site_title = "BanaRandevu Yönetim"
    index_title = "Hoş Geldiniz"


custom_admin_site = CustomAdminSite(name='custom_admin')

# Import custom admin model registrations
# This will override the automatic registrations for specific models
from yonetim import admin_models

# Automatically register all models from installed apps
# This will skip models that are already registered
for model in apps.get_models():
    try:
        custom_admin_site.register(model)
    except Exception as e:
        pass 
