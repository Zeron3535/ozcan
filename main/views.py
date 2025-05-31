from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from professionals.models import Category, ProfessionalProfile, ExpertType, Specialization, City
from .models import SiteSettings
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.

class HomeView(TemplateView):
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['categories'] = Category.objects.filter(is_active=True).order_by('order')
        context['expert_types'] = ExpertType.objects.filter(is_active=True).order_by('order')
        context['specializations'] = Specialization.objects.filter(is_active=True).order_by('order')
        context['cities'] = City.objects.filter(is_active=True).order_by('order')
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'main/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'main/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['professionals'] = ProfessionalProfile.objects.filter(
            category=self.get_object(),
            user__is_active=True,
            user__is_membership_active=True
        ).order_by('order_in_category')
        return context

class ProfessionalSearchView(ListView):
    model = ProfessionalProfile
    template_name = 'main/search_results.html'
    context_object_name = 'professionals'
    
    def get_queryset(self):
        queryset = ProfessionalProfile.objects.filter(
            user__is_active=True,
            user__is_membership_active=True
        )
        
        # Text search
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) | 
                Q(user__last_name__icontains=query) |
                Q(short_bio__icontains=query) |
                Q(about__icontains=query) |
                Q(category__name__icontains=query) |
                Q(expert_type__name__icontains=query) |
                Q(specializations__name__icontains=query)
            ).distinct()
        
        # Expert type filter
        expert_type = self.request.GET.get('expert_type', '')
        if expert_type:
            try:
                expert_type_obj = ExpertType.objects.get(slug=expert_type, is_active=True)
                queryset = queryset.filter(expert_type=expert_type_obj)
            except ExpertType.DoesNotExist:
                pass
        
        # Specialization filter
        specialization = self.request.GET.get('specialization', '')
        if specialization:
            try:
                specialization_obj = Specialization.objects.get(slug=specialization, is_active=True)
                queryset = queryset.filter(specializations=specialization_obj)
            except Specialization.DoesNotExist:
                pass
        
        # Meeting type filter
        meeting_type = self.request.GET.get('meeting_type', '')
        if meeting_type == 'online':
            queryset = queryset.filter(offers_online=True)
        elif meeting_type == 'in_person':
            queryset = queryset.filter(offers_in_person=True)
        
        # City filter (only for in-person meetings)
        city = self.request.GET.get('city', '')
        if city and meeting_type == 'in_person':
            try:
                city_obj = City.objects.get(slug=city, is_active=True)
                queryset = queryset.filter(city=city_obj)
            except City.DoesNotExist:
                pass
        
        # Category filter (for backward compatibility)
        category = self.request.GET.get('category', '')
        if category:
            try:
                category_obj = Category.objects.get(slug=category, is_active=True)
                queryset = queryset.filter(category=category_obj)
            except Category.DoesNotExist:
                pass
        
        return queryset.order_by('expert_type', 'category', 'order_in_category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['query'] = self.request.GET.get('q', '')
        context['expert_types'] = ExpertType.objects.filter(is_active=True).order_by('order')
        context['specializations'] = Specialization.objects.filter(is_active=True).order_by('order')
        context['cities'] = City.objects.filter(is_active=True).order_by('order')
        
        # Pass current filter values for form state
        context['current_expert_type'] = self.request.GET.get('expert_type', '')
        context['current_specialization'] = self.request.GET.get('specialization', '')
        context['current_meeting_type'] = self.request.GET.get('meeting_type', '')
        context['current_city'] = self.request.GET.get('city', '')
        
        return context

# AJAX endpoint for dynamic specialization loading
def get_specializations_for_expert_type(request):
    """Return specializations for a given expert type"""
    expert_type_slug = request.GET.get('expert_type', '')
    
    if not expert_type_slug:
        specializations = Specialization.objects.filter(is_active=True).order_by('order')
    else:
        try:
            expert_type = ExpertType.objects.get(slug=expert_type_slug, is_active=True)
            specializations = expert_type.specializations.filter(is_active=True).order_by('order')
        except ExpertType.DoesNotExist:
            specializations = Specialization.objects.none()
    
    data = {
        'specializations': [
            {'slug': spec.slug, 'name': spec.name} 
            for spec in specializations
        ]
    }
    
    return JsonResponse(data)

# AJAX endpoint for getting cities (when in-person is selected)
def get_cities_for_meeting_type(request):
    """Return cities when in-person meeting type is selected"""
    meeting_type = request.GET.get('meeting_type', '')
    
    if meeting_type == 'in_person':
        cities = City.objects.filter(is_active=True).order_by('order')
        data = {
            'cities': [
                {'slug': city.slug, 'name': city.name} 
                for city in cities
            ],
            'show_city_field': True
        }
    else:
        data = {
            'cities': [],
            'show_city_field': False
        }
    
    return JsonResponse(data)
