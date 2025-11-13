from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import ProjectCategory, Project, ProjectUpdate, Recovery


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ur', 'icon']
    search_fields = ['name', 'name_ur']


class ProjectUpdateInline(admin.TabularInline):
    """Inline for project updates"""
    model = ProjectUpdate
    extra = 0
    fields = ['title', 'title_ur', 'content', 'image', 'created_at']
    readonly_fields = ['created_at']


class RecoveryInline(admin.TabularInline):
    """Inline for recoveries"""
    model = Recovery
    extra = 1
    fields = ['amount', 'recovery_date', 'payment_method', 'reference_number']
    readonly_fields = []


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'beneficiary_name', 'category', 'community', 'status',
                    'requested_amount', 'approved_amount', 'funding_progress_display',
                    'is_featured', 'application_date']
    list_filter = ['status', 'community', 'category', 'is_featured', 'is_public', 'application_date']
    search_fields = ['title', 'title_ur', 'beneficiary_name', 'beneficiary_phone', 'beneficiary_cnic']
    readonly_fields = ['application_date', 'created_at', 'updated_at',
                       'total_funded', 'funding_progress_display', 'donor_count',
                       'recovery_progress_display']
    list_editable = ['is_featured']
    date_hierarchy = 'application_date'
    inlines = [ProjectUpdateInline, RecoveryInline]

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'title_ur', 'category', 'community')
        }),
        (_('Beneficiary Information'), {
            'fields': ('beneficiary_name', 'beneficiary_phone', 'beneficiary_email',
                      'beneficiary_address', 'beneficiary_cnic', 'family_size')
        }),
        (_('Project Description'), {
            'fields': ('description', 'description_ur', 'business_plan')
        }),
        (_('Financial Information'), {
            'fields': ('requested_amount', 'approved_amount', 'currency',
                      'total_funded', 'funding_progress_display')
        }),
        (_('Recovery Information'), {
            'fields': ('expected_monthly_recovery', 'recovery_start_date',
                      'total_recovered', 'recovery_progress_display'),
            'classes': ('collapse',)
        }),
        (_('Status & Workflow'), {
            'fields': ('status', 'application_date', 'approval_date',
                      'funding_date', 'establishment_date')
        }),
        (_('Documentation'), {
            'fields': ('image', 'documents'),
            'classes': ('collapse',)
        }),
        (_('Internal Notes'), {
            'fields': ('verification_notes', 'admin_notes'),
            'classes': ('collapse',)
        }),
        (_('Visibility'), {
            'fields': ('is_featured', 'is_public')
        }),
        (_('Statistics'), {
            'fields': ('donor_count',),
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
        # Managers only see their community's projects
        if request.user.community:
            return qs.filter(community=request.user.community)
        return qs.none()

    def funding_progress_display(self, obj):
        """Display funding progress as a colored bar"""
        progress = obj.funding_progress()
        color = 'green' if progress >= 100 else 'orange' if progress >= 50 else 'red'
        return format_html(
            '<div style="width:100px;background:#f0f0f0;border-radius:3px;">'
            '<div style="width:{}px;background:{};height:20px;border-radius:3px;text-align:center;color:white;">'
            '{}%</div></div>',
            int(progress), color, int(progress)
        )
    funding_progress_display.short_description = _("Funding Progress")

    def recovery_progress_display(self, obj):
        """Display recovery progress"""
        progress = obj.recovery_progress()
        return f"{progress:.1f}%"
    recovery_progress_display.short_description = _("Recovery Progress")


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'created_at']
    list_filter = ['created_at', 'project__community']
    search_fields = ['title', 'title_ur', 'project__title']
    readonly_fields = ['created_at']
    autocomplete_fields = ['project']

    fieldsets = (
        (_('Project'), {
            'fields': ('project',)
        }),
        (_('Update Content'), {
            'fields': ('title', 'title_ur', 'content', 'content_ur', 'image')
        }),
        (_('Timestamp'), {
            'fields': ('created_at',)
        }),
    )

    def get_queryset(self, request):
        """Restrict queryset based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'DIRECTOR':
            return qs
        if request.user.community:
            return qs.filter(project__community=request.user.community)
        return qs.none()


@admin.register(Recovery)
class RecoveryAdmin(admin.ModelAdmin):
    list_display = ['project', 'amount', 'recovery_date', 'payment_method', 'created_at']
    list_filter = ['recovery_date', 'payment_method', 'project__community']
    search_fields = ['project__title', 'project__beneficiary_name', 'reference_number']
    readonly_fields = ['created_at']
    autocomplete_fields = ['project']
    date_hierarchy = 'recovery_date'

    fieldsets = (
        (_('Project'), {
            'fields': ('project',)
        }),
        (_('Recovery Details'), {
            'fields': ('amount', 'recovery_date', 'payment_method', 'reference_number')
        }),
        (_('Notes'), {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        (_('Timestamp'), {
            'fields': ('created_at',)
        }),
    )

    def get_queryset(self, request):
        """Restrict queryset based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'DIRECTOR':
            return qs
        if request.user.community:
            return qs.filter(project__community=request.user.community)
        return qs.none()


# Enable autocomplete for related lookups
Project.search_fields = ['title', 'beneficiary_name']
