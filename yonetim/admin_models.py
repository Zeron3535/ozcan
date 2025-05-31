from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from yonetim.custom_admin import custom_admin_site
from yonetim.forms import SimpleUserCreationForm

User = get_user_model()

class CustomUserAdminSimplified(UserAdmin):
    """
    Simplified User admin for the custom admin site.
    Makes it easy to add new users with custom usernames and passwords.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active')
    list_filter = ('is_active', 'user_type')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    # Use our custom form for adding users
    add_form = SimpleUserCreationForm

    # Simplified fieldsets for better usability
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Kişisel Bilgiler'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Kullanıcı Ayarları'), {'fields': ('user_type', 'is_active')}),
        (_('Üyelik Bilgileri'), {'fields': ('membership_expires', 'is_membership_active')}),
        (_('Telegram Bilgileri'), {'fields': ('telegram_id', 'telegram_active')}),
    )

    # Simplified add form with only essential fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 'is_active'),
        }),
    )

# Register the User model with our custom admin site
custom_admin_site.register(User, CustomUserAdminSimplified)

# Register other important models with custom admin site if needed
# This ensures they appear in the custom admin with appropriate configurations
