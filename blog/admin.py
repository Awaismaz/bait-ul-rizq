from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ur', 'slug']
    search_fields = ['name', 'name_ur']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'is_featured',
                    'views_count', 'published_date', 'created_at']
    list_filter = ['is_published', 'is_featured', 'category', 'published_date', 'created_at']
    search_fields = ['title', 'title_ur', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    list_editable = ['is_published', 'is_featured']
    date_hierarchy = 'published_date'
    autocomplete_fields = ['author', 'category']

    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'title_ur', 'slug', 'category', 'author')
        }),
        (_('Excerpt'), {
            'fields': ('excerpt', 'excerpt_ur')
        }),
        (_('Body'), {
            'fields': ('content', 'content_ur')
        }),
        (_('Media'), {
            'fields': ('featured_image',)
        }),
        (_('Publishing'), {
            'fields': ('is_published', 'is_featured', 'published_date')
        }),
        (_('Statistics'), {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-set author and published date"""
        if not obj.author:
            obj.author = request.user
        if obj.is_published and not obj.published_date:
            from django.utils import timezone
            obj.published_date = timezone.now()
        super().save_model(request, obj, form, change)
