from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom User model for BanaRandevu system"""
    
    USER_TYPE_CHOICES = (
        ('admin', _('Yönetici')),
        ('professional', _('Profesyonel')),
    )
    
    user_type = models.CharField(
        _("Kullanıcı Tipi"),
        max_length=20, 
        choices=USER_TYPE_CHOICES,
        default='professional'
    )
    
    telegram_id = models.CharField(
        _("Telegram ID"), 
        max_length=100, 
        null=True, 
        blank=True
    )
    
    telegram_active = models.BooleanField(
        _("Telegram Aktif Mi"), 
        default=False
    )
    
    membership_expires = models.DateField(
        _("Üyelik Bitiş Tarihi"), 
        null=True, 
        blank=True
    )
    
    is_membership_active = models.BooleanField(
        _("Üyelik Aktif Mi"), 
        default=True
    )
    
    class Meta:
        verbose_name = _("Kullanıcı")
        verbose_name_plural = _("Kullanıcılar")
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'
    
    @property
    def is_professional(self):
        return self.user_type == 'professional'
