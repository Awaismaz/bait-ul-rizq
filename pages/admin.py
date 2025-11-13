from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'show_in_header', 'show_in_footer', 'created_at']
    list_filter = ['is_published', 'show_in_header', 'show_in_footer']
    search_fields = ['title', 'title_ur', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_published', 'show_in_header', 'show_in_footer']

    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'title_ur', 'slug')
        }),
        (_('Body'), {
            'fields': ('content', 'content_ur')
        }),
        (_('Visibility'), {
            'fields': ('is_published', 'show_in_header', 'show_in_footer')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
