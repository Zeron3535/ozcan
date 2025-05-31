from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ProfessionalProfile, Service, WorkingHours, Category, ExpertType, City
from .forms import ProfessionalProfileForm, ServiceForm, WorkingHoursFormSet, CreateProfileForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from main.models import SiteSettings

class ProfessionalRequiredMixin(LoginRequiredMixin):
    """Mixin to require a professional user"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'is_professional') or not request.user.is_professional:
            messages.error(request, _("Bu sayfaya erişim izniniz yok."))
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class ProfessionalProfileView(ProfessionalRequiredMixin, DetailView):
    model = ProfessionalProfile
    template_name = 'professionals/profile.html'
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has a profile
        try:
            ProfessionalProfile.objects.get(user=self.request.user)
        except ProfessionalProfile.DoesNotExist:
            # If no profile exists, redirect to the create profile page
            messages.info(request, _("Lütfen profesyonel profilinizi oluşturun."))
            return redirect('professionals:create_profile')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(ProfessionalProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        return context

class UpdateProfileView(ProfessionalRequiredMixin, UpdateView):
    model = ProfessionalProfile
    form_class = ProfessionalProfileForm
    template_name = 'professionals/update_profile.html'
    success_url = reverse_lazy('professionals:profile')

    def get_object(self, queryset=None):
        return get_object_or_404(ProfessionalProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _("Profiliniz başarıyla güncellendi."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        return context

class ServiceListView(ProfessionalRequiredMixin, ListView):
    model = Service
    template_name = 'professionals/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        return Service.objects.filter(professional=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        return context

class ServiceCreateView(ProfessionalRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'professionals/service_form.html'
    success_url = reverse_lazy('professionals:service_list')

    def form_valid(self, form):
        form.instance.professional = get_object_or_404(ProfessionalProfile, user=self.request.user)
        messages.success(self.request, _("Hizmet başarıyla eklendi."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['title'] = _("Yeni Hizmet Ekle")
        return context

class ServiceUpdateView(ProfessionalRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'professionals/service_form.html'
    success_url = reverse_lazy('professionals:service_list')

    def get_queryset(self):
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        return Service.objects.filter(professional=profile)

    def form_valid(self, form):
        messages.success(self.request, _("Hizmet başarıyla güncellendi."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['title'] = _("Hizmet Düzenle")
        return context

class ServiceDeleteView(ProfessionalRequiredMixin, DeleteView):
    model = Service
    template_name = 'professionals/service_confirm_delete.html'
    success_url = reverse_lazy('professionals:service_list')

    def get_queryset(self):
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        return Service.objects.filter(professional=profile)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Hizmet başarıyla silindi."))
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        return context

class WorkingHoursView(ProfessionalRequiredMixin, TemplateView):
    template_name = 'professionals/working_hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)

        if self.request.method == 'POST':
            formset = WorkingHoursFormSet(self.request.POST, instance=profile)
        else:
            formset = WorkingHoursFormSet(instance=profile)

        context['formset'] = formset
        context['profile'] = profile
        context['site_settings'] = SiteSettings.load()
        return context

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        formset = WorkingHoursFormSet(request.POST, instance=profile)

        if formset.is_valid():
            formset.save()
            messages.success(request, _("Çalışma saatleri başarıyla güncellendi."))
            return redirect('professionals:working_hours')

        return self.render_to_response(self.get_context_data(formset=formset))

class CreateProfileView(ProfessionalRequiredMixin, CreateView):
    """View for creating a new professional profile"""
    model = ProfessionalProfile
    form_class = CreateProfileForm
    template_name = 'professionals/create_profile.html'
    success_url = reverse_lazy('professionals:profile')

    def dispatch(self, request, *args, **kwargs):
        # Check if the user already has a profile
        try:
            profile = ProfessionalProfile.objects.get(user=self.request.user)
            messages.info(request, _("Zaten bir profiliniz var."))
            return redirect('professionals:profile')
        except ProfessionalProfile.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set the user before saving
        form.instance.user = self.request.user
        messages.success(self.request, _("Profiliniz başarıyla oluşturuldu."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['title'] = _("Profesyonel Profili Oluştur")
        return context

class ProfessionalDetailView(DetailView):
    model = ProfessionalProfile
    template_name = 'professionals/professional_detail.html'
    context_object_name = 'professional'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        professional = self.get_object()
        context['services'] = Service.objects.filter(
            professional=professional,
            is_active=True
        )
        context['working_hours'] = WorkingHours.objects.filter(
            professional=professional,
            is_active=True
        ).order_by('day')
        return context
