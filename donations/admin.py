from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from .models import Donation, DonationAllocation


class DonationAllocationInline(admin.TabularInline):
    """Inline for donation allocations"""
    model = DonationAllocation
    extra = 1
    readonly_fields = ['allocated_date']
    autocomplete_fields = ['project']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'amount', 'currency', 'payment_method', 'date_received',
                    'allocated_amount_display', 'remaining_amount_display', 'receipt_issued', 'created_at']
    list_filter = ['currency', 'payment_method', 'receipt_issued', 'date_received', 'donor__community']
    search_fields = ['donor__name', 'donor__donor_id', 'reference_number']
    readonly_fields = ['created_at', 'updated_at', 'allocated_amount_display',
                       'remaining_amount_display', 'is_fully_allocated_display']
    autocomplete_fields = ['donor']
    date_hierarchy = 'date_received'
    inlines = [DonationAllocationInline]

    fieldsets = (
        (_('Donor Information'), {
            'fields': ('donor',)
        }),
        (_('Donation Details'), {
            'fields': ('amount', 'currency', 'payment_method', 'reference_number', 'date_received')
        }),
        (_('Allocation Status'), {
            'fields': ('allocated_amount_display', 'remaining_amount_display', 'is_fully_allocated_display'),
            'classes': ('collapse',)
        }),
        (_('Receipt'), {
            'fields': ('receipt_issued',)
        }),
        (_('Notes'), {
            'fields': ('notes',),
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
        # Managers only see their community's donations
        if request.user.community:
            return qs.filter(donor__community=request.user.community)
        return qs.none()

    def allocated_amount_display(self, obj):
        """Display allocated amount"""
        return f"{obj.allocated_amount()} {obj.currency}"
    allocated_amount_display.short_description = _("Allocated Amount")

    def remaining_amount_display(self, obj):
        """Display remaining amount"""
        return f"{obj.remaining_amount()} {obj.currency}"
    remaining_amount_display.short_description = _("Remaining Amount")

    def is_fully_allocated_display(self, obj):
        """Display allocation status"""
        return obj.is_fully_allocated()
    is_fully_allocated_display.boolean = True
    is_fully_allocated_display.short_description = _("Fully Allocated")


@admin.register(DonationAllocation)
class DonationAllocationAdmin(admin.ModelAdmin):
    list_display = ['donation', 'project', 'amount', 'allocated_date']
    list_filter = ['allocated_date', 'donation__currency', 'project__community']
    search_fields = ['donation__donor__name', 'project__title', 'project__beneficiary_name']
    readonly_fields = ['allocated_date']
    autocomplete_fields = ['donation', 'project']
    date_hierarchy = 'allocated_date'

    fieldsets = (
        (_('Allocation'), {
            'fields': ('donation', 'project', 'amount')
        }),
        (_('Details'), {
            'fields': ('allocated_date', 'notes'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Restrict queryset based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'DIRECTOR':
            return qs
        # Managers only see their community's allocations
        if request.user.community:
            return qs.filter(
                donation__donor__community=request.user.community,
                project__community=request.user.community
            )
        return qs.none()
