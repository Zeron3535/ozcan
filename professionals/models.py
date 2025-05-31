from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ExpertType(models.Model):
    """Expert types like Doctor, Psychologist, Lawyer, etc."""
    name = models.CharField(_("Uzman Türü"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Açıklama"), blank=True)
    icon = models.CharField(_("İkon CSS Sınıfı"), max_length=100, blank=True, help_text="Örn: fas fa-user-md")
    is_active = models.BooleanField(_("Aktif Mi"), default=True)
    is_visible = models.BooleanField(_("Görünür Mü"), default=True, help_text=_("Web sitesinde görünsün mü?"))
    order = models.PositiveIntegerField(_("Sıralama"), default=0)
    
    class Meta:
        verbose_name = _("Uzman Türü")
        verbose_name_plural = _("Uzman Türleri")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Specialization(models.Model):
    """Specializations that belong to expert types"""
    name = models.CharField(_("Uzmanlık Dalı"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    expert_types = models.ManyToManyField(
        ExpertType,
        related_name='specializations',
        verbose_name=_("Uzman Türleri"),
        help_text=_("Bu uzmanlık dalının hangi uzman türlerine ait olduğunu seçin")
    )
    description = models.TextField(_("Açıklama"), blank=True)
    is_active = models.BooleanField(_("Aktif Mi"), default=True)
    is_visible = models.BooleanField(_("Görünür Mü"), default=True, help_text=_("Web sitesinde görünsün mü?"))
    order = models.PositiveIntegerField(_("Sıralama"), default=0)
    
    class Meta:
        verbose_name = _("Uzmanlık Dalı")
        verbose_name_plural = _("Uzmanlık Dalları")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class City(models.Model):
    """Cities for location-based filtering"""
    name = models.CharField(_("Şehir Adı"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    is_active = models.BooleanField(_("Aktif Mi"), default=True)
    order = models.PositiveIntegerField(_("Sıralama"), default=0)
    
    class Meta:
        verbose_name = _("Şehir")
        verbose_name_plural = _("Şehirler")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Category(models.Model):
    """Professional categories like Doctors, Teachers, etc."""
    name = models.CharField(_("Kategori Adı"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Açıklama"), blank=True)
    is_active = models.BooleanField(_("Aktif Mi"), default=True)
    order = models.PositiveIntegerField(_("Sıralama"), default=0)
    
    class Meta:
        verbose_name = _("Kategori")
        verbose_name_plural = _("Kategoriler")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProfessionalProfile(models.Model):
    """Profile for professionals"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_("Kullanıcı")
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='professionals',
        verbose_name=_("Kategori")
    )
    expert_type = models.ForeignKey(
        ExpertType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='professionals',
        verbose_name=_("Uzman Türü")
    )
    specializations = models.ManyToManyField(
        Specialization,
        blank=True,
        related_name='professionals',
        verbose_name=_("Uzmanlık Dalları"),
        help_text=_("Birden fazla dal seçebilirsiniz")
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='professionals',
        verbose_name=_("Şehir"),
        help_text=_("Yüz yüze hizmet verdiğiniz şehir")
    )
    experience_years = models.PositiveIntegerField(
        _("Deneyim Yılı"),
        null=True,
        blank=True,
        help_text=_("Toplam profesyonel deneyim yılı")
    )
    short_bio = models.CharField(_("Kısa Tanıtım"), max_length=255, blank=True)
    about = models.TextField(_("Hakkında"), blank=True)
    profile_picture = models.ImageField(
        _("Profil Resmi"), 
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    cv_file = models.FileField(
        _("CV Dosyası"), 
        upload_to='cv_files/',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        _("Telefon Numarası"), 
        max_length=20, 
        blank=True,
        help_text=_("İsteğe bağlı, profilde görünecek")
    )
    show_phone = models.BooleanField(
        _("Telefon Numarası Gösterilsin Mi"), 
        default=False
    )
    offers_online = models.BooleanField(
        _("Online Hizmet Veriyor"),
        default=True,
        help_text=_("Online görüşme hizmeti sunuyor mu?")
    )
    offers_in_person = models.BooleanField(
        _("Yüz Yüze Hizmet Veriyor"),
        default=True,
        help_text=_("Yüz yüze görüşme hizmeti sunuyor mu?")
    )
    
    # Social Media Links
    website = models.URLField(_("Web Sitesi"), blank=True, null=True)
    facebook = models.URLField(_("Facebook"), blank=True, null=True)
    twitter = models.URLField(_("Twitter"), blank=True, null=True)
    instagram = models.URLField(_("Instagram"), blank=True, null=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True, null=True)
    youtube = models.URLField(_("YouTube"), blank=True, null=True)
    
    # Admin controls for social media
    allow_social_media = models.BooleanField(
        _("Sosyal Medya Linklerine İzin Ver"),
        default=True,
        help_text=_("Yönetici tarafından kontrol edilir")
    )
    
    order_in_category = models.PositiveIntegerField(
        _("Kategori İçinde Sıralama"), 
        default=0
    )
    
    # Status
    is_active = models.BooleanField(_("Aktif Mi"), default=True)
    is_visible = models.BooleanField(_("Görünür Mü"), default=True)
    
    class Meta:
        verbose_name = _("Profesyonel Profili")
        verbose_name_plural = _("Profesyonel Profilleri")
        ordering = ['category', 'order_in_category', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.category.name}"
    
    @property
    def bio(self):
        """Backward compatibility"""
        return self.short_bio
    
    @property
    def profile_image(self):
        """Backward compatibility"""
        return self.profile_picture

class ProfessionalVideo(models.Model):
    """Videos for professional profiles (max 5 per profile)"""
    professional = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name=_("Profesyonel")
    )
    title = models.CharField(_("Video Başlığı"), max_length=200)
    video_url = models.URLField(
        _("Video URL"), 
        help_text=_("YouTube, Vimeo vb. video linki")
    )
    order = models.PositiveIntegerField(_("Sıralama"), default=0)
    is_active = models.BooleanField(_("Aktif Mi"), default=True)
    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Profesyonel Videosu")
        verbose_name_plural = _("Profesyonel Videoları")
        ordering = ['professional', 'order', '-created_at']
    
    def __str__(self):
        return f"{self.professional.user.get_full_name()} - {self.title}"
    
    def clean(self):
        # Check if professional already has 5 videos
        super().clean()
        if self.professional:
            existing_count = self.professional.videos.exclude(pk=self.pk).count()
            if existing_count >= 5:
                raise ValidationError(_("Bir profesyonel en fazla 5 video ekleyebilir."))

class Service(models.Model):
    """Services offered by professionals"""
    MEETING_TYPE_CHOICES = (
        ('online', _('Online')),
        ('face_to_face', _('Yüz Yüze')),
        ('both', _('Her İkisi')),
    )
    
    professional = models.ForeignKey(
        ProfessionalProfile, 
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name=_("Profesyonel")
    )
    name = models.CharField(_("Hizmet Adı"), max_length=100)
    description = models.TextField(_("Açıklama"), blank=True)
    duration_minutes = models.PositiveIntegerField(_("Süre (Dakika)"), default=60)
    meeting_type = models.CharField(
        _("Görüşme Tipi"),
        max_length=20,
        choices=MEETING_TYPE_CHOICES,
        default='face_to_face'
    )
    price = models.DecimalField(
        _("Fiyat"), 
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Hizmet ücreti (TL)")
    )
    show_price = models.BooleanField(
        _("Fiyat Gösterilsin Mi"), 
        default=True
    )
    is_active = models.BooleanField(_("Aktif Mi"), default=True)
    
    class Meta:
        verbose_name = _("Hizmet")
        verbose_name_plural = _("Hizmetler")
        ordering = ['professional', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.professional.user.get_full_name()}"

class AppointmentSettings(models.Model):
    """Dynamic appointment settings for professionals"""
    professional = models.OneToOneField(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name='appointment_settings',
        verbose_name=_("Profesyonel")
    )
    
    # Appointment settings
    min_advance_hours = models.PositiveIntegerField(
        _("Minimum İleri Tarih (Saat)"),
        default=24,
        help_text=_("Randevu alınabilecek minimum saat öncesi")
    )
    max_advance_days = models.PositiveIntegerField(
        _("Maximum İleri Tarih (Gün)"),
        default=30,
        help_text=_("Randevu alınabilecek maximum gün sonrası")
    )
    appointment_interval = models.PositiveIntegerField(
        _("Randevu Aralığı (Dakika)"),
        default=30,
        help_text=_("Randevular arası minimum süre")
    )
    buffer_time = models.PositiveIntegerField(
        _("Ara Süre (Dakika)"),
        default=0,
        help_text=_("Randevular arası dinlenme süresi")
    )
    
    # Cancellation policy
    allow_cancellation = models.BooleanField(
        _("İptal İzni"),
        default=True
    )
    cancellation_hours = models.PositiveIntegerField(
        _("İptal Süresi (Saat)"),
        default=24,
        help_text=_("Randevu öncesi kaç saat önce iptal edilebilir")
    )
    
    # Auto-confirmation
    auto_confirm = models.BooleanField(
        _("Otomatik Onay"),
        default=False,
        help_text=_("Randevular otomatik onaylansın mı?")
    )
    
    class Meta:
        verbose_name = _("Randevu Ayarları")
        verbose_name_plural = _("Randevu Ayarları")
    
    def __str__(self):
        return f"{self.professional.user.get_full_name()} - Randevu Ayarları"

class WorkingHours(models.Model):
    """Working hours for professionals"""
    DAY_CHOICES = (
        (0, _('Pazartesi')),
        (1, _('Salı')),
        (2, _('Çarşamba')),
        (3, _('Perşembe')),
        (4, _('Cuma')),
        (5, _('Cumartesi')),
        (6, _('Pazar')),
    )
    
    professional = models.ForeignKey(
        ProfessionalProfile, 
        on_delete=models.CASCADE,
        related_name='working_hours',
        verbose_name=_("Profesyonel")
    )
    day = models.IntegerField(_("Gün"), choices=DAY_CHOICES)
    start_time = models.TimeField(_("Başlangıç Saati"))
    end_time = models.TimeField(_("Bitiş Saati"))
    is_active = models.BooleanField(_("Aktif Mi"), default=True)
    
    class Meta:
        verbose_name = _("Çalışma Saati")
        verbose_name_plural = _("Çalışma Saatleri")
        ordering = ['day', 'start_time']
        unique_together = ['professional', 'day']
    
    def __str__(self):
        day_name = dict(self.DAY_CHOICES)[self.day]
        return f"{self.professional.user.get_full_name()} - {day_name} {self.start_time}-{self.end_time}"
