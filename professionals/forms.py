from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ProfessionalProfile, Service, WorkingHours, Category, ExpertType, City
from django.forms import inlineformset_factory

class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProfile
        fields = ['short_bio', 'about', 'profile_picture', 'cv_file', 'phone_number', 'show_phone']
        widgets = {
            'short_bio': forms.Textarea(attrs={'rows': 3}),
            'about': forms.Textarea(attrs={'rows': 10}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'duration_minutes', 'meeting_type', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

WorkingHoursFormSet = inlineformset_factory(
    ProfessionalProfile,
    WorkingHours,
    fields=('day', 'start_time', 'end_time', 'is_active'),
    extra=1,
    can_delete=True
) 

class CreateProfileForm(forms.ModelForm):
    """Form for creating a new professional profile"""
    class Meta:
        model = ProfessionalProfile
        fields = ['category', 'expert_type', 'city', 'short_bio', 'about', 'offers_online', 'offers_in_person']
        widgets = {
            'short_bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'about': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'Textarea':
                field.widget.attrs['class'] = 'form-control'

        # Filter only active categories, expert types, and cities
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['expert_type'].queryset = ExpertType.objects.filter(is_active=True)
        self.fields['city'].queryset = City.objects.filter(is_active=True)

        # Add help text
        self.fields['category'].help_text = _("Hangi kategoride hizmet veriyorsunuz?")
        self.fields['expert_type'].help_text = _("Uzmanlık alanınız nedir?")
        self.fields['city'].help_text = _("Yüz yüze hizmet verdiğiniz şehir")
        self.fields['short_bio'].help_text = _("Kısa bir tanıtım yazısı (maksimum 255 karakter)")
        self.fields['about'].help_text = _("Kendinizi ve hizmetlerinizi detaylı olarak tanıtın")
