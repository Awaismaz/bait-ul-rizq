from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Community, CustomUser, Donor, Volunteer


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'community_type', 'is_active', 'created_at']
    list_filter = ['community_type', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'community_type', 'description', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'community', 'is_staff']
    list_filter = ['role', 'community', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']

    fieldsets = UserAdmin.fieldsets + (
        (_('Bait ul Rizq Information'), {
            'fields': ('role', 'community', 'phone')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Bait ul Rizq Information'), {
            'fields': ('role', 'community', 'phone')
        }),
    )

    def get_queryset(self, request):
        """Restrict queryset based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'DIRECTOR':
            return qs
        # Managers only see their community
        if request.user.community:
            return qs.filter(community=request.user.community)
        return qs.none()


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['donor_id', 'name', 'email', 'phone', 'community', 'total_donated', 'is_anonymous', 'created_at']
    list_filter = ['community', 'is_anonymous', 'created_at']
    search_fields = ['donor_id', 'name', 'email', 'phone']
    readonly_fields = ['donor_id', 'created_at', 'updated_at', 'total_donated']

    fieldsets = (
        (_('Donor ID'), {
            'fields': ('donor_id',),
            'description': _('This unique 9-digit ID is generated automatically and should be provided to the donor for tracking their donations.')
        }),
        (_('Personal Information'), {
            'fields': ('name', 'email', 'phone', 'address', 'community')
        }),
        (_('Privacy'), {
            'fields': ('is_anonymous',),
            'description': _('Anonymous donors will not have their names displayed publicly.')
        }),
        (_('Internal'), {
            'fields': ('notes', 'total_donated'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Restrict queryset based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'DIRECTOR':
            return qs
        # Managers only see their community
        if request.user.community:
            return qs.filter(community=request.user.community)
        return qs.none()

    def total_donated(self, obj):
        """Display total donated amount"""
        return f"${obj.total_donated():,.2f}"
    total_donated.short_description = _("Total Donated")


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'community', 'is_approved', 'created_at']
    list_filter = ['community', 'is_approved', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_approved']

    fieldsets = (
        (_('Personal Information'), {
            'fields': ('name', 'email', 'phone', 'address', 'community')
        }),
        (_('Application Details'), {
            'fields': ('skills', 'availability', 'message')
        }),
        (_('Approval'), {
            'fields': ('is_approved',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Restrict queryset based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'DIRECTOR':
            return qs
        # Managers only see their community
        if request.user.community:
            return qs.filter(community=request.user.community)
        return qs.none()
