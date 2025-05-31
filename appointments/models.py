from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from professionals.models import Service, ProfessionalProfile
from django.utils import timezone

class Appointment(models.Model):
    """Appointments model"""
    STATUS_CHOICES = (
        ('pending', _('Beklemede')),
        ('confirmed', _('Onaylandı')),
        ('cancelled', _('İptal Edildi')),
        ('completed', _('Tamamlandı')),
    )
    
    professional = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_("Profesyonel")
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_("Hizmet")
    )
    date = models.DateField(_("Tarih"))
    start_time = models.TimeField(_("Başlangıç Saati"))
    end_time = models.TimeField(_("Bitiş Saati"))
    
    # Customer information
    customer_name = models.CharField(_("Müşteri Adı"), max_length=100)
    customer_surname = models.CharField(_("Müşteri Soyadı"), max_length=100)
    customer_phone = models.CharField(_("Müşteri Telefonu"), max_length=20)
    customer_note = models.TextField(_("Müşteri Notu"), blank=True)
    
    # Appointment status
    status = models.CharField(
        _("Durum"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(_("Oluşturulma Zamanı"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncelleme Zamanı"), auto_now=True)
    
    class Meta:
        verbose_name = _("Randevu")
        verbose_name_plural = _("Randevular")
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.customer_name} {self.customer_surname} - {self.professional.user.get_full_name()} - {self.date} {self.start_time}"
    
    @property
    def is_past(self):
        """Check if appointment is in the past"""
        today = timezone.now().date()
        now = timezone.now().time()
        
        return self.date < today or (self.date == today and self.end_time < now)

class Message(models.Model):
    """Messages between professionals and customers"""
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_("Randevu")
    )
    from_professional = models.BooleanField(
        _("Profesyonelden mi?"),
        default=False,
        help_text=_("İleti profesyonel tarafından mı gönderildi?")
    )
    content = models.TextField(_("İçerik"))
    created_at = models.DateTimeField(_("Oluşturulma Zamanı"), auto_now_add=True)
    read = models.BooleanField(_("Okundu mu?"), default=False)
    
    class Meta:
        verbose_name = _("Mesaj")
        verbose_name_plural = _("Mesajlar")
        ordering = ['created_at']
    
    def __str__(self):
        sender = self.appointment.professional.user.get_full_name() if self.from_professional else self.appointment.customer_name
        return f"Mesaj: {sender} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"
