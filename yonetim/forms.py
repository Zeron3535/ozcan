from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class SimpleUserCreationForm(UserCreationForm):
    """
    A simplified form for creating new users in the admin panel.
    Makes it easy to add users with custom usernames and passwords.
    """
    first_name = forms.CharField(
        label=_("Ad"),
        max_length=150,
        required=True,
        help_text=_("Kullanıcının adı.")
    )
    
    last_name = forms.CharField(
        label=_("Soyad"),
        max_length=150,
        required=True,
        help_text=_("Kullanıcının soyadı.")
    )
    
    email = forms.EmailField(
        label=_("E-posta"),
        required=True,
        help_text=_("Kullanıcının e-posta adresi.")
    )
    
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 
            'password1', 'password2', 'user_type', 'is_active'
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make password help text more user-friendly
        self.fields['password1'].help_text = _("Güçlü bir şifre belirleyin. En az 8 karakter olmalıdır.")
        # Set default user type to 'professional'
        if 'user_type' in self.fields:
            self.fields['user_type'].initial = 'professional'
        # Set is_active to True by default
        if 'is_active' in self.fields:
            self.fields['is_active'].initial = True