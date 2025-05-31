from django.urls import path
from . import views

app_name = 'professionals'

urlpatterns = [
    path('profil/', views.ProfessionalProfileView.as_view(), name='profile'),
    path('profil/olustur/', views.CreateProfileView.as_view(), name='create_profile'),
    path('profil/duzenle/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('hizmetler/', views.ServiceListView.as_view(), name='service_list'),
    path('hizmetler/ekle/', views.ServiceCreateView.as_view(), name='add_service'),
    path('hizmetler/<int:pk>/duzenle/', views.ServiceUpdateView.as_view(), name='update_service'),
    path('hizmetler/<int:pk>/sil/', views.ServiceDeleteView.as_view(), name='delete_service'),
    path('calisma-saatleri/', views.WorkingHoursView.as_view(), name='working_hours'),
    path('<slug:category_slug>/<int:pk>/', views.ProfessionalDetailView.as_view(), name='professional_detail'),
] 
