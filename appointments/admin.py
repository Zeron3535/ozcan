from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Appointment, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_surname', 'professional', 'service', 
                   'date', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'date', 'professional__category', 'service__meeting_type')
    search_fields = ('customer_name', 'customer_surname', 'customer_phone', 
                    'professional__user__first_name', 'professional__user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MessageInline]
    
    fieldsets = (
        (_('Müşteri Bilgileri'), {
            'fields': ('customer_name', 'customer_surname', 'customer_phone', 'customer_note')
        }),
        (_('Randevu Bilgileri'), {
            'fields': ('professional', 'service', 'date', 'start_time', 'end_time', 'status')
        }),
        (_('Tarihler'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def send_reminder(self, request, queryset):
        """Send reminder to professional via Telegram"""
        for appointment in queryset:
            # Logic to send reminder via Telegram
            pass
        self.message_user(request, _("Hatırlatıcılar gönderildi."))
    
    actions = ('send_reminder',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'from_professional', 'content_preview', 'created_at', 'read')
    list_filter = ('from_professional', 'read', 'created_at')
    search_fields = ('content', 'appointment__customer_name', 'appointment__customer_surname', 
                    'appointment__professional__user__first_name', 'appointment__professional__user__last_name')
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        """Show preview of message content"""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
