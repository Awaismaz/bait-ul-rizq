from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('donate/', views.DonateView.as_view(), name='donate'),
    path('donate/success/', views.DonateSuccessView.as_view(), name='donate_success'),
    path('donor-lookup/', views.DonorLookupView.as_view(), name='donor_lookup'),
    path('donor-lookup/<str:donor_id>/', views.DonorDetailView.as_view(), name='donor_detail'),
    path('volunteer-application/', views.VolunteerApplicationView.as_view(), name='volunteer_application'),
    path('volunteer-success/', views.VolunteerSuccessView.as_view(), name='volunteer_success'),
]
