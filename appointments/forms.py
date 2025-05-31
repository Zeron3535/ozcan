from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Appointment, Message
from professionals.models import ProfessionalProfile, Service
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['professional', 'service', 'date', 'start_time',
                  'customer_name', 'customer_surname', 'customer_phone', 'customer_note']
        widgets = {
            'professional': forms.HiddenInput(),
            'service': forms.HiddenInput(),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'customer_note': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        professional = cleaned_data.get('professional')
        service = cleaned_data.get('service')
        
        if date and start_time and professional and service:
            # Check if the date is in the past
            today = timezone.now().date()
            now = timezone.now().time()
            
            if date < today or (date == today and start_time < now):
                raise forms.ValidationError(_("Geçmiş bir tarih ve saat seçemezsiniz."))
            
            # Check if there's an overlap with another appointment
            start_datetime = timezone.datetime.combine(date, start_time)
            end_datetime = start_datetime + timezone.timedelta(minutes=service.duration_minutes)
            end_time = end_datetime.time()
            
            overlapping_appointments = Appointment.objects.filter(
                professional=professional,
                date=date,
                status__in=['pending', 'confirmed']
            ).exclude(
                start_time__gte=end_time
            ).exclude(
                end_time__lte=start_time
            )
            
            if overlapping_appointments.exists():
                raise forms.ValidationError(_("Seçtiğiniz zaman diliminde başka bir randevu bulunmaktadır."))
        
        return cleaned_data

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': _('Mesajınızı yazın...')}),
        } 