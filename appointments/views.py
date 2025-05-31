from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import Appointment, Message
from professionals.models import ProfessionalProfile, Service
from .forms import AppointmentForm, MessageForm
from django.contrib import messages as django_messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.http import JsonResponse
from main.models import SiteSettings
from professionals.views import ProfessionalRequiredMixin

class AppointmentListView(ProfessionalRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    
    def get_queryset(self):
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        today = timezone.now().date()
        return Appointment.objects.filter(
            professional=profile,
            date__gte=today
        ).order_by('date', 'start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['title'] = _("Gelecek Randevular")
        return context

class PastAppointmentListView(ProfessionalRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    
    def get_queryset(self):
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        today = timezone.now().date()
        return Appointment.objects.filter(
            professional=profile,
            date__lt=today
        ).order_by('-date', '-start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        context['title'] = _("Geçmiş Randevular")
        context['past'] = True
        return context

class AppointmentDetailView(ProfessionalRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'
    
    def get_queryset(self):
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        return Appointment.objects.filter(professional=profile)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        appointment = self.get_object()
        context['messages'] = appointment.messages.all().order_by('created_at')
        context['message_form'] = MessageForm()
        return context

class UpdateAppointmentStatusView(ProfessionalRequiredMixin, UpdateView):
    model = Appointment
    fields = ['status']
    http_method_names = ['post']
    
    def get_queryset(self):
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        return Appointment.objects.filter(professional=profile)
    
    def form_valid(self, form):
        status = form.cleaned_data['status']
        status_text = dict(Appointment.STATUS_CHOICES)[status]
        django_messages.success(self.request, _(f"Randevu durumu '{status_text}' olarak güncellendi."))
        return super().form_valid(form)
    
    def get_success_url(self):
        appointment = self.get_object()
        return reverse('appointments:appointment_detail', kwargs={'pk': appointment.pk})

class AppointmentMessagesView(ProfessionalRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    http_method_names = ['post']
    
    def form_valid(self, form):
        appointment = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        profile = get_object_or_404(ProfessionalProfile, user=self.request.user)
        
        # Check if the appointment belongs to this professional
        if appointment.professional != profile:
            return JsonResponse({'error': _("Bu randevuya erişim izniniz yok.")}, status=403)
        
        form.instance.appointment = appointment
        form.instance.from_professional = True
        return super().form_valid(form)
    
    def get_success_url(self):
        appointment = self.get_object()
        return reverse('appointments:appointment_detail', kwargs={'pk': appointment.pk})

class CreateAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/create_appointment.html'
    
    def get_initial(self):
        initial = super().get_initial()
        professional_id = self.kwargs.get('professional_id')
        service_id = self.kwargs.get('service_id')
        
        professional = get_object_or_404(ProfessionalProfile, pk=professional_id)
        service = get_object_or_404(Service, pk=service_id, professional=professional)
        
        initial['professional'] = professional
        initial['service'] = service
        
        return initial
    
    def form_valid(self, form):
        appointment = form.save(commit=False)
        service = appointment.service
        
        # Calculate end time based on service duration
        start_datetime = timezone.datetime.combine(
            appointment.date, 
            appointment.start_time
        )
        end_datetime = start_datetime + timezone.timedelta(minutes=service.duration_minutes)
        appointment.end_time = end_datetime.time()
        
        # Save appointment
        appointment.save()
        
        # Create success message
        django_messages.success(
            self.request, 
            _("Randevunuz başarıyla oluşturuldu. Profesyonel onayladıktan sonra size telefon numaranız üzerinden ulaşacaktır.")
        )
        
        return redirect('main:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.load()
        
        professional_id = self.kwargs.get('professional_id')
        service_id = self.kwargs.get('service_id')
        
        professional = get_object_or_404(ProfessionalProfile, pk=professional_id)
        service = get_object_or_404(Service, pk=service_id, professional=professional)
        
        context['professional'] = professional
        context['service'] = service
        
        return context
