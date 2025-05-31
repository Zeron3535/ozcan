from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Temel Ayarlar'), {
            'fields': ('site_name', 'welcome_message', 'logo', 'favicon')
        }),
        (_('İletişim Bilgileri'), {
            'fields': ('contact_phone', 'contact_email')
        }),
        (_('Sosyal Medya'), {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url')
        }),
        (_('Telegram Bot'), {
            'fields': ('telegram_bot_enabled', 'telegram_admin_ids')
        }),
        (_('SEO Ayarları'), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        return SiteSettings.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the singleton instance
        return False
