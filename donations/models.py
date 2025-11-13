from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Donor, Community
from decimal import Decimal


class Donation(models.Model):
    """Represents a donation from a donor"""

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('PKR', 'Pakistani Rupee'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]

    PAYMENT_METHODS = [
        ('BANK', 'Bank Transfer'),
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('MOBILE', 'Mobile Payment'),
        ('CHEQUE', 'Cheque'),
        ('OTHER', 'Other'),
    ]

    donor = models.ForeignKey(
        Donor,
        on_delete=models.PROTECT,
        related_name='donations',
        verbose_name=_("Donor")
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Amount")
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD',
        verbose_name=_("Currency")
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        default='BANK',
        verbose_name=_("Payment Method")
    )
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Reference/Transaction Number")
    )
    date_received = models.DateField(verbose_name=_("Date Received"))
    receipt_issued = models.BooleanField(
        default=False,
        verbose_name=_("Receipt Issued")
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Donation")
        verbose_name_plural = _("Donations")
        ordering = ['-date_received', '-created_at']

    def __str__(self):
        return f"{self.donor.name} - {self.amount} {self.currency} on {self.date_received}"

    def allocated_amount(self):
        """Calculate total amount allocated to projects"""
        return self.allocations.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

    def remaining_amount(self):
        """Calculate remaining unallocated amount"""
        return self.amount - self.allocated_amount()

    def is_fully_allocated(self):
        """Check if donation is fully allocated"""
        return self.remaining_amount() <= Decimal('0.00')


class DonationAllocation(models.Model):
    """Many-to-many relationship between donations and projects with allocation amounts"""

    donation = models.ForeignKey(
        Donation,
        on_delete=models.CASCADE,
        related_name='allocations',
        verbose_name=_("Donation")
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='allocations',
        verbose_name=_("Project")
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Allocated Amount"),
        help_text=_("Amount from this donation allocated to this project")
    )
    allocated_date = models.DateField(
        auto_now_add=True,
        verbose_name=_("Allocation Date")
    )
    notes = models.TextField(blank=True, verbose_name=_("Allocation Notes"))

    class Meta:
        verbose_name = _("Donation Allocation")
        verbose_name_plural = _("Donation Allocations")
        ordering = ['-allocated_date']
        unique_together = ['donation', 'project']

    def __str__(self):
        return f"{self.amount} {self.donation.currency} from {self.donation.donor.name} to {self.project.title}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Validate that allocation doesn't exceed donation amount
        if self.donation:
            total_allocated = self.donation.allocated_amount()
            if self.pk:
                # Exclude current allocation from total
                current_allocation = DonationAllocation.objects.filter(pk=self.pk).first()
                if current_allocation:
                    total_allocated -= current_allocation.amount

            if total_allocated + self.amount > self.donation.amount:
                remaining = self.donation.amount - total_allocated
                raise ValidationError(
                    f"Allocation exceeds donation amount. Only {remaining} {self.donation.currency} remaining."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
