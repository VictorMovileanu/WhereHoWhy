from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class AboutMeView(TemplateView):
    template_name = "frontpage/about_me.html"
