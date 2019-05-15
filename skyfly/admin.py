from django.contrib import admin

from django.contrib.admin import register
from django.urls import reverse
from django.utils.html import format_html

from skyfly.models import SkyflyRequest


@register(SkyflyRequest)
class SkyflyRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'href')

    def href(self, obj):
        url = reverse('skyfly:request', kwargs={'request_hash': obj.request_hash})
        href = format_html(
            f'<a href={url}>{url}</a>'
        )
        return href
