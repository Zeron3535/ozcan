from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    """Site-wide settings model (singleton)"""
    site_name = models.CharField(_("Site Adı"), max_length=100, default="BanaRandevu")
    welcome_message = models.TextField(_("Karşılama Mesajı"), blank=True)
    contact_phone = models.CharField(_("İletişim Telefonu"), max_length=20, blank=True)
    contact_email = models.EmailField(_("İletişim E-posta"), blank=True)
    facebook_url = models.URLField(_("Facebook URL"), blank=True)
    instagram_url = models.URLField(_("Instagram URL"), blank=True)
    twitter_url = models.URLField(_("Twitter URL"), blank=True)
    logo = models.ImageField(_("Logo"), upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(_("Favicon"), upload_to='site/', blank=True, null=True)

    # Telegram bot settings
    telegram_bot_enabled = models.BooleanField(_("Telegram Bot Aktif"), default=False)
    telegram_admin_ids = models.TextField(_("Telegram Yönetici ID'leri"), blank=True, help_text=_("Virgülle ayrılmış Telegram ID'leri. Örn: 123456789,987654321"))

    # SEO settings
    meta_title = models.CharField(_("Meta Başlık"), max_length=100, blank=True)
    meta_description = models.TextField(_("Meta Açıklama"), blank=True)
    meta_keywords = models.CharField(_("Meta Anahtar Kelimeler"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Site Ayarları")
        verbose_name_plural = _("Site Ayarları")

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Make sure there's only one instance of SiteSettings
        self.pk = 1
        super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Load site settings or create default if doesn't exist"""
        try:
            return cls.objects.get(pk=1)
        except cls.DoesNotExist:
            return cls.objects.create()
