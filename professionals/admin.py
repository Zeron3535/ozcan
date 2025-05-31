from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import (
    Category,
    ProfessionalProfile,
    Service,
    WorkingHours,
    ExpertType,
    Specialization,
    City,
    ProfessionalVideo,
    AppointmentSettings
)
from django import forms

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    fields = ('name', 'duration_minutes', 'meeting_type', 'price', 'show_price', 'is_active')

class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 1

class ProfessionalVideoInline(admin.TabularInline):
    model = ProfessionalVideo
    extra = 0
    max_num = 5
    fields = ('title', 'video_url', 'order', 'is_active')

class AppointmentSettingsInline(admin.StackedInline):
    model = AppointmentSettings
    extra = 0
    max_num = 1

@admin.register(ExpertType)
class ExpertTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview', 'order', 'is_active', 'is_visible')
    list_filter = ('is_active', 'is_visible')
    list_editable = ('order', 'is_active', 'is_visible')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<i class="{}"></i>', obj.icon)
        return '-'

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_expert_types', 'order', 'is_active', 'is_visible')
    list_filter = ('is_active', 'is_visible', 'expert_types')
    list_editable = ('order', 'is_active', 'is_visible')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('expert_types',)
    ordering = ('order', 'name')
    
    def get_expert_types(self, obj):
        return ", ".join([et.name for et in obj.expert_types.all()])

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'category', 'expert_type', 'city', 'experience_years', 
        'offers_online', 'offers_in_person', 'is_active', 'is_visible',
        'allow_social_media', 'get_video_count'
    )
    list_filter = (
        'category', 'expert_type', 'city', 'offers_online', 'offers_in_person', 
        'is_active', 'is_visible', 'allow_social_media', 'show_phone'
    )
    list_editable = ('is_active', 'is_visible', 'allow_social_media')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'short_bio')
    filter_horizontal = ('specializations',)
    inlines = [ServiceInline, WorkingHoursInline, ProfessionalVideoInline, AppointmentSettingsInline]

    fieldsets = (
        ('Temel Bilgiler', {'fields': ('user', 'category', 'expert_type', 'specializations', 'city')}),
        ('Profil Bilgileri', {'fields': ('short_bio', 'about', 'experience_years', 'profile_picture', 'cv_file')}),
        ('İletişim', {'fields': ('phone_number', 'show_phone')}),
        ('Hizmet Seçenekleri', {'fields': ('offers_online', 'offers_in_person')}),
        ('Sosyal Medya', {
            'fields': ('allow_social_media', 'website', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube'),
            'classes': ('collapse',),
            'description': 'Sosyal medya linklerini yönetmek için "Sosyal Medya Linklerine İzin Ver" seçeneği aktif olmalıdır.'
        }),
        ('Yönetim', {'fields': ('order_in_category', 'is_active', 'is_visible')}),
    )

    def get_video_count(self, obj):
        return obj.videos.count()

    @admin.display(description='Video Sayısı')
    def video_sayisi(self, obj):
        return self.get_video_count(obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if getattr(request.user, 'is_superuser', False):
            return qs
        return qs.filter(user=request.user)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'professional', 'duration_minutes', 'meeting_type', 'price', 'show_price', 'is_active')
    list_filter = ('meeting_type', 'is_active', 'show_price', 'professional__category', 'professional__expert_type')
    list_editable = ('price', 'show_price', 'is_active')
    search_fields = ('name', 'description', 'professional__user__first_name', 'professional__user__last_name')

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('professional', 'day', 'start_time', 'end_time', 'is_active')
    list_filter = ('day', 'is_active', 'professional__category', 'professional__expert_type')
    list_editable = ('is_active',)
    search_fields = ('professional__user__first_name', 'professional__user__last_name')

@admin.register(ProfessionalVideo)
class ProfessionalVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'professional', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'professional__category', 'professional__expert_type')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'professional__user__first_name', 'professional__user__last_name')
    ordering = ('professional', 'order')

@admin.register(AppointmentSettings)
class AppointmentSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'professional', 'min_advance_hours', 'max_advance_days', 
        'appointment_interval', 'auto_confirm', 'allow_cancellation'
    )
    list_filter = ('auto_confirm', 'allow_cancellation', 'professional__category')
    search_fields = ('professional__user__first_name', 'professional__user__last_name')
    
    fieldsets = (
        ('Profesyonel', {
            'fields': ('professional',)
        }),
        ('Randevu Zamanlaması', {
            'fields': ('min_advance_hours', 'max_advance_days', 'appointment_interval', 'buffer_time'),
            'description': 'Randevu alma ile ilgili zaman ayarları'
        }),
        ('İptal Politikası', {
            'fields': ('allow_cancellation', 'cancellation_hours'),
        }),
        ('Otomatik İşlemler', {
            'fields': ('auto_confirm',),
        }),
    )
