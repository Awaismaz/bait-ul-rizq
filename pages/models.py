from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class Page(models.Model):
    """Static content pages like About, Policies, etc."""

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    title_ur = models.CharField(max_length=200, blank=True, verbose_name=_("Title (Urdu)"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))

    content = RichTextField(verbose_name=_("Content"))
    content_ur = RichTextField(blank=True, verbose_name=_("Content (Urdu)"))

    is_published = models.BooleanField(default=True, verbose_name=_("Published"))
    show_in_footer = models.BooleanField(
        default=False,
        verbose_name=_("Show in Footer"),
        help_text=_("Display link in footer menu")
    )
    show_in_header = models.BooleanField(
        default=False,
        verbose_name=_("Show in Header"),
        help_text=_("Display link in header menu")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['title']

    def __str__(self):
        return self.title
