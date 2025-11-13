from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Donor, Volunteer, Community
from projects.models import Project
from blog.models import BlogPost


class HomeView(TemplateView):
    """Homepage view"""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(
            is_featured=True,
            is_public=True
        )[:6]
        context['featured_posts'] = BlogPost.objects.filter(
            is_published=True,
            is_featured=True
        )[:3]
        return context


class DonorLookupView(TemplateView):
    """Donor lookup page"""
    template_name = 'core/donor_lookup.html'

    def post(self, request, *args, **kwargs):
        donor_id = request.POST.get('donor_id', '').strip()
        if donor_id:
            try:
                donor = Donor.objects.get(donor_id=donor_id)
                return redirect('core:donor_detail', donor_id=donor_id)
            except Donor.DoesNotExist:
                messages.error(request, _('Invalid Donor ID. Please check and try again.'))
        return self.get(request, *args, **kwargs)


class DonorDetailView(DetailView):
    """Donor detail page showing donations and allocations"""
    model = Donor
    template_name = 'core/donor_detail.html'
    slug_field = 'donor_id'
    slug_url_kwarg = 'donor_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        donor = self.object
        context['donations'] = donor.donations.all().order_by('-date_received')
        context['total_donated'] = donor.total_donated()

        # Get all projects funded by this donor
        from donations.models import DonationAllocation
        allocations = DonationAllocation.objects.filter(
            donation__donor=donor
        ).select_related('project').order_by('-allocated_date')
        context['allocations'] = allocations

        return context


class VolunteerApplicationView(CreateView):
    """Volunteer application form"""
    model = Volunteer
    template_name = 'core/volunteer_application.html'
    fields = ['name', 'email', 'phone', 'address', 'community', 'skills', 'availability', 'message']

    def form_valid(self, form):
        messages.success(self.request, _('Thank you for your application! We will review it and contact you soon.'))
        return super().form_valid(form)

    def get_success_url(self):
        return '/volunteer-success/'


class VolunteerSuccessView(TemplateView):
    """Volunteer application success page"""
    template_name = 'core/volunteer_success.html'


class DonateView(TemplateView):
    """Donation page with payment methods"""
    template_name = 'core/donate.html'

    def post(self, request, *args, **kwargs):
        # Create donor and donation
        from donations.models import Donation

        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address', '')
        community_id = request.POST.get('community')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        payment_method = request.POST.get('payment_method')
        is_anonymous = request.POST.get('is_anonymous') == 'on'

        # Create or get donor
        community = Community.objects.get(id=community_id)
        donor, created = Donor.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': phone,
                'address': address,
                'community': community,
                'is_anonymous': is_anonymous
            }
        )

        # Create donation
        from datetime import date
        donation = Donation.objects.create(
            donor=donor,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            date_received=date.today()
        )

        # Store donor ID in session to show on success page
        request.session['donor_id'] = donor.donor_id
        request.session['donation_amount'] = str(amount)
        request.session['donation_currency'] = currency

        messages.success(
            request,
            _('Thank you for your generous donation! Your unique Donor ID is: {}').format(donor.donor_id)
        )
        return redirect('core:donate_success')


class DonateSuccessView(TemplateView):
    """Donation success page"""
    template_name = 'core/donate_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donor_id'] = self.request.session.get('donor_id')
        context['donation_amount'] = self.request.session.get('donation_amount')
        context['donation_currency'] = self.request.session.get('donation_currency')
        return context
