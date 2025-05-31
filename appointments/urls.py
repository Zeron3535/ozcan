from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment_list'),
    path('gecmis/', views.PastAppointmentListView.as_view(), name='past_appointment_list'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<int:pk>/durum/', views.UpdateAppointmentStatusView.as_view(), name='update_status'),
    path('<int:pk>/mesajlar/', views.AppointmentMessagesView.as_view(), name='messages'),
    path('ekle/<int:professional_id>/<int:service_id>/', views.CreateAppointmentView.as_view(), name='create'),
] 