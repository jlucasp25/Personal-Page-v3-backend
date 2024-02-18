from django.shortcuts import render
from django.views.generic import TemplateView

from personal_page.core.models import Project


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["projects"] = Project.objects.all()
        return ctx
