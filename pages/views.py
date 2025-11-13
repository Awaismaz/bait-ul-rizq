from django.shortcuts import render
from django.views.generic import DetailView
from .models import Page


class PageDetailView(DetailView):
    """Static page detail view"""
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return Page.objects.filter(is_published=True)
