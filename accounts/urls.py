from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('giris/', views.CustomLoginView.as_view(), name='login'),
    path('cikis/', auth_views.LogoutView.as_view(), name='logout'),
    path('sifremi-unuttum/', views.ForgotPasswordView.as_view(), name='forgot_password'),
]
