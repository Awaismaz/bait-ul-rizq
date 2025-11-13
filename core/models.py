from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
import random
import string


class Community(models.Model):
    """Represents International or Pakistani donor communities"""

    COMMUNITY_TYPES = [
        ('INTL', 'International'),
        ('PAK', 'Pakistani'),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Community Name"))
    community_type = models.CharField(
        max_length=4,
        choices=COMMUNITY_TYPES,
        unique=True,
        verbose_name=_("Community Type")
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Community")
        verbose_name_plural = _("Communities")
        ordering = ['community_type']

    def __str__(self):
        return self.get_community_type_display()


class CustomUser(AbstractUser):
    """Extended user model with role-based access"""

    ROLE_CHOICES = [
        ('DIRECTOR', 'Director'),
        ('INTL_MANAGER', 'International Manager'),
        ('PAK_MANAGER', 'Pakistani Manager'),
        ('STAFF', 'Staff'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        verbose_name=_("Role")
    )
    community = models.ForeignKey(
        'Community',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members',
        verbose_name=_("Community")
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display() if self.role else 'No Role'})"

    def has_community_access(self, community):
        """Check if user has access to a specific community"""
        if self.role == 'DIRECTOR':
            return True
        if self.community == community:
            return True
        return False


def generate_donor_id():
    """Generate a unique 9-digit donor ID"""
    from core.models import Donor
    while True:
        donor_id = ''.join(random.choices(string.digits, k=9))
        if not Donor.objects.filter(donor_id=donor_id).exists():
            return donor_id


class Donor(models.Model):
    """Represents a donor with anonymous lookup capability"""

    donor_id = models.CharField(
        max_length=9,
        unique=True,
        default=generate_donor_id,
        editable=False,
        verbose_name=_("Donor ID")
    )
    name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    address = models.TextField(blank=True, verbose_name=_("Address"))
    community = models.ForeignKey(
        Community,
        on_delete=models.PROTECT,
        related_name='donors',
        verbose_name=_("Community")
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name=_("Anonymous Donor"),
        help_text=_("If checked, donor's name will not be publicly displayed")
    )
    notes = models.TextField(blank=True, verbose_name=_("Internal Notes"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Donor")
        verbose_name_plural = _("Donors")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.donor_id})"

    def get_display_name(self):
        """Return name for public display (Anonymous if flagged)"""
        return "Anonymous Donor" if self.is_anonymous else self.name

    def total_donated(self):
        """Calculate total amount donated"""
        from donations.models import Donation
        return Donation.objects.filter(donor=self).aggregate(
            total=models.Sum('amount')
        )['total'] or 0


class Volunteer(models.Model):
    """Represents volunteers/members of the organization"""

    name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    address = models.TextField(blank=True, verbose_name=_("Address"))
    community = models.ForeignKey(
        Community,
        on_delete=models.PROTECT,
        related_name='volunteers',
        verbose_name=_("Community")
    )
    skills = models.TextField(
        blank=True,
        verbose_name=_("Skills/Expertise"),
        help_text=_("What skills can you contribute?")
    )
    availability = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Availability"),
        help_text=_("When are you available to volunteer?")
    )
    message = models.TextField(
        blank=True,
        verbose_name=_("Message"),
        help_text=_("Why do you want to join?")
    )
    is_approved = models.BooleanField(default=False, verbose_name=_("Approved"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Volunteer")
        verbose_name_plural = _("Volunteers")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"
