from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
import logging

# Create a logger
logger = logging.getLogger(__name__)

User = get_user_model()

# Create your views here.

class CustomLoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Use Django's built-in authenticate function which will use our custom backend
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect professional users to their profile page
                if hasattr(user, 'is_professional') and user.is_professional:
                    return redirect('professionals:profile')
                # Redirect other users to the homepage
                return redirect('main:home')
            else:
                messages.error(request, "Lütfen doğru kullanıcı adı ve parola girin. Her iki alanın da büyük/küçük harfe duyarlı olabileceğini unutmayın.")
        else:
            messages.error(request, "Lütfen doğru kullanıcı adı ve parola girin. Her iki alanın da büyük/küçük harfe duyarlı olabileceğini unutmayın.")

        return render(request, self.template_name, {'form': form})


class ForgotPasswordForm(forms.Form):
    """Form for the forgot password functionality"""
    username = forms.CharField(
        label="Kullanıcı Adı", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-0 bg-light', 'placeholder': 'Kullanıcı adınızı girin'})
    )
    phone = forms.CharField(
        label="Telefon Numarası", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-0 bg-light', 'placeholder': 'Telefon numaranızı girin'})
    )
    first_name = forms.CharField(
        label="Ad", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-0 bg-light', 'placeholder': 'Adınızı girin'})
    )
    last_name = forms.CharField(
        label="Soyad", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-0 bg-light', 'placeholder': 'Soyadınızı girin'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        # Either username or both first_name and last_name must be provided
        if not username and not (first_name and last_name):
            raise forms.ValidationError(
                "Lütfen kullanıcı adınızı veya ad ve soyadınızı girin."
            )

        return cleaned_data


def send_telegram_notification(message):
    """Send a notification to the admin via Telegram"""
    from main.models import SiteSettings

    token = settings.TELEGRAM_BOT_TOKEN
    site_settings = SiteSettings.load()

    if not token:
        logger.warning("Telegram bot token is not set. Notification not sent.")
        return False

    if not site_settings.telegram_bot_enabled:
        logger.warning("Telegram bot is disabled in site settings. Notification not sent.")
        return False

    # Get admin IDs from site settings, or use default if not set
    admin_ids = site_settings.telegram_admin_ids.strip()
    if not admin_ids:
        admin_ids = "7464909625"  # Default admin ID as fallback

    # Split by comma and remove whitespace
    admin_ids = [id.strip() for id in admin_ids.split(',') if id.strip()]

    if not admin_ids:
        logger.warning("No Telegram admin IDs configured. Notification not sent.")
        return False

    success = True

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        # Send to all configured admin IDs
        for chat_id in admin_ids:
            try:
                data = {
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
                response = requests.post(url, data=data)
                response.raise_for_status()
                logger.info(f"Telegram notification sent to {chat_id}")
            except Exception as e:
                logger.error(f"Failed to send Telegram notification to {chat_id}: {e}")
                success = False

        return success
    except Exception as e:
        logger.error(f"Failed to send Telegram notifications: {e}")
        return False


class ForgotPasswordView(View):
    template_name = 'accounts/forgot_password.html'

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            phone = form.cleaned_data.get('phone')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            # Try to find the user
            user = None
            if username:
                try:
                    # Case-insensitive lookup
                    user = User.objects.get(username__iexact=username)
                except User.DoesNotExist:
                    pass
            elif first_name and last_name:
                # Try to find by first_name and last_name (might return multiple users)
                users = User.objects.filter(
                    first_name__iexact=first_name,
                    last_name__iexact=last_name
                )
                if users.exists():
                    user = users.first()  # Take the first match

            if user:
                # Send notification to admin
                message = f"""
<b>Şifre Sıfırlama Talebi</b>

<b>Kullanıcı Bilgileri:</b>
Kullanıcı Adı: {user.username}
Ad: {user.first_name}
Soyad: {user.last_name}
Telefon: {phone}

@Ugruz
"""
                send_telegram_notification(message)

                messages.success(
                    request, 
                    "Şifre sıfırlama talebiniz alınmıştır. Yönetici sizinle iletişime geçecektir."
                )
                return redirect('accounts:login')
            else:
                # User not found, but don't reveal this information
                messages.success(
                    request, 
                    "Şifre sıfırlama talebiniz alınmıştır. Eğer bilgileriniz sistemde kayıtlıysa, yönetici sizinle iletişime geçecektir."
                )

                # Still send a notification to admin about the failed attempt
                message = f"""
<b>Başarısız Şifre Sıfırlama Girişimi</b>

<b>Girilen Bilgiler:</b>
Kullanıcı Adı: {username or 'Girilmedi'}
Ad: {first_name or 'Girilmedi'}
Soyad: {last_name or 'Girilmedi'}
Telefon: {phone}

@Ugruz
"""
                send_telegram_notification(message)

                return redirect('accounts:login')

        return render(request, self.template_name, {'form': form})
