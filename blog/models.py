from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField


class BlogCategory(models.Model):
    """Categories for blog posts"""

    name = models.CharField(max_length=100, verbose_name=_("Category Name"))
    name_ur = models.CharField(max_length=100, blank=True, verbose_name=_("Name (Urdu)"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Blog posts for updates and stories"""

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    title_ur = models.CharField(max_length=200, blank=True, verbose_name=_("Title (Urdu)"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name=_("Category")
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts',
        verbose_name=_("Author")
    )

    excerpt = models.TextField(
        max_length=300,
        blank=True,
        verbose_name=_("Excerpt"),
        help_text=_("Short description for preview")
    )
    excerpt_ur = models.TextField(
        max_length=300,
        blank=True,
        verbose_name=_("Excerpt (Urdu)")
    )

    content = RichTextField(verbose_name=_("Content"))
    content_ur = RichTextField(blank=True, verbose_name=_("Content (Urdu)"))

    featured_image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        verbose_name=_("Featured Image")
    )

    is_published = models.BooleanField(default=False, verbose_name=_("Published"))
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Featured Post"),
        help_text=_("Show on homepage")
    )

    views_count = models.PositiveIntegerField(default=0, verbose_name=_("Views"))

    published_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Published Date")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
