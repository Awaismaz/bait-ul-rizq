from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Community
from decimal import Decimal


class ProjectCategory(models.Model):
    """Categories for different types of projects/businesses"""

    name = models.CharField(max_length=100, verbose_name=_("Category Name"))
    name_ur = models.CharField(max_length=100, blank=True, verbose_name=_("Name (Urdu)"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Bootstrap icon class (e.g., 'bi-shop')"),
        verbose_name=_("Icon")
    )

    class Meta:
        verbose_name = _("Project Category")
        verbose_name_plural = _("Project Categories")
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    """Represents a project/beneficiary business"""

    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved - Awaiting Funding'),
        ('FUNDED', 'Funded - In Progress'),
        ('ESTABLISHED', 'Established - Operating'),
        ('RECOVERING', 'Recovering Contributions'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
        ('ON_HOLD', 'On Hold'),
    ]

    # Basic Information
    title = models.CharField(max_length=200, verbose_name=_("Project Title"))
    title_ur = models.CharField(max_length=200, blank=True, verbose_name=_("Title (Urdu)"))
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects',
        verbose_name=_("Category")
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name=_("Community")
    )

    # Beneficiary Information
    beneficiary_name = models.CharField(max_length=200, verbose_name=_("Beneficiary Name"))
    beneficiary_phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    beneficiary_email = models.EmailField(blank=True, verbose_name=_("Email"))
    beneficiary_address = models.TextField(verbose_name=_("Address"))
    beneficiary_cnic = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("CNIC/ID Number")
    )
    family_size = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Family Size"),
        help_text=_("Number of family members")
    )

    # Project Details
    description = models.TextField(verbose_name=_("Project Description"))
    description_ur = models.TextField(blank=True, verbose_name=_("Description (Urdu)"))
    business_plan = models.TextField(
        blank=True,
        verbose_name=_("Business Plan"),
        help_text=_("Detailed business plan and sustainability strategy")
    )

    # Financial Information
    requested_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Requested Amount")
    )
    currency = models.CharField(
        max_length=3,
        choices=[('USD', 'USD'), ('PKR', 'PKR')],
        default='USD',
        verbose_name=_("Currency")
    )
    approved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Approved Amount")
    )

    # Recovery Information
    expected_monthly_recovery = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Expected Monthly Recovery"),
        help_text=_("Expected monthly contribution back to the system")
    )
    recovery_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Recovery Start Date")
    )
    total_recovered = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Total Recovered Amount")
    )

    # Status and Workflow
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name=_("Status")
    )
    application_date = models.DateField(
        auto_now_add=True,
        verbose_name=_("Application Date")
    )
    approval_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Approval Date")
    )
    funding_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Funding Date")
    )
    establishment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Establishment Date")
    )

    # Documentation
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        verbose_name=_("Project Image")
    )
    documents = models.FileField(
        upload_to='project_documents/',
        blank=True,
        null=True,
        verbose_name=_("Supporting Documents")
    )

    # Internal Notes
    verification_notes = models.TextField(
        blank=True,
        verbose_name=_("Verification Notes"),
        help_text=_("Internal notes from verification team")
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name=_("Admin Notes")
    )

    # Visibility
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Featured Project"),
        help_text=_("Show on homepage")
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name=_("Public Visibility"),
        help_text=_("Show on public website")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.beneficiary_name}"

    def total_funded(self):
        """Calculate total amount funded from donations"""
        return self.allocations.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

    def funding_progress(self):
        """Calculate funding progress percentage"""
        if not self.approved_amount or self.approved_amount == 0:
            return 0
        progress = (self.total_funded() / self.approved_amount) * 100
        return min(progress, 100)  # Cap at 100%

    def is_fully_funded(self):
        """Check if project is fully funded"""
        if not self.approved_amount:
            return False
        return self.total_funded() >= self.approved_amount

    def recovery_progress(self):
        """Calculate recovery progress percentage"""
        if not self.approved_amount or self.approved_amount == 0:
            return 0
        progress = (self.total_recovered / self.approved_amount) * 100
        return min(progress, 100)

    def donor_count(self):
        """Count unique donors for this project"""
        return self.allocations.values('donation__donor').distinct().count()


class ProjectUpdate(models.Model):
    """Progress updates for projects"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='updates',
        verbose_name=_("Project")
    )
    title = models.CharField(max_length=200, verbose_name=_("Update Title"))
    title_ur = models.CharField(max_length=200, blank=True, verbose_name=_("Title (Urdu)"))
    content = models.TextField(verbose_name=_("Update Content"))
    content_ur = models.TextField(blank=True, verbose_name=_("Content (Urdu)"))
    image = models.ImageField(
        upload_to='project_updates/',
        blank=True,
        null=True,
        verbose_name=_("Update Image")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Project Update")
        verbose_name_plural = _("Project Updates")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project.title} - {self.title}"


class Recovery(models.Model):
    """Track monthly recoveries from established projects"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='recoveries',
        verbose_name=_("Project")
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Recovery Amount")
    )
    recovery_date = models.DateField(verbose_name=_("Recovery Date"))
    payment_method = models.CharField(
        max_length=10,
        choices=[
            ('BANK', 'Bank Transfer'),
            ('CASH', 'Cash'),
            ('MOBILE', 'Mobile Payment'),
        ],
        default='CASH',
        verbose_name=_("Payment Method")
    )
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Reference Number")
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Recovery")
        verbose_name_plural = _("Recoveries")
        ordering = ['-recovery_date']

    def __str__(self):
        return f"{self.project.title} - {self.amount} on {self.recovery_date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update project's total recovered amount
        self.project.total_recovered = self.project.recoveries.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
        self.project.save()
