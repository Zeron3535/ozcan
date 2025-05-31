from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('kategoriler/', views.CategoryListView.as_view(), name='category_list'),
    path('kategori/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('arama/', views.ProfessionalSearchView.as_view(), name='search'),
    
    # AJAX endpoints for dynamic filtering
    path('api/specializations/', views.get_specializations_for_expert_type, name='api_specializations'),
    path('api/cities/', views.get_cities_for_meeting_type, name='api_cities'),
] 