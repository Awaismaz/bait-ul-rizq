from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Project


class ProjectListView(ListView):
    """List all public projects"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.filter(is_public=True).order_by('-created_at')


class ProjectDetailView(DetailView):
    """Project detail page"""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(is_public=True)


class ProjectApplicationView(CreateView):
    """Project application form for beneficiaries"""
    model = Project
    template_name = 'projects/project_application.html'
    fields = ['title', 'category', 'community', 'beneficiary_name', 'beneficiary_phone',
              'beneficiary_email', 'beneficiary_address', 'beneficiary_cnic', 'family_size',
              'description', 'business_plan', 'requested_amount', 'currency']

    def form_valid(self, form):
        form.instance.status = 'PENDING'
        messages.success(self.request, _('Your application has been submitted successfully! We will review it and contact you soon.'))
        return super().form_valid(form)

    def get_success_url(self):
        return '/projects/apply/success/'


class ProjectApplicationSuccessView(TemplateView):
    """Application success page"""
    template_name = 'projects/application_success.html'
