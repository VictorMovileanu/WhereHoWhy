from django.contrib import admin

from django.contrib.admin import register
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from skyfly.models import SkyflyRequest, KiwiException


class ExceptionInlineAdmin(admin.TabularInline):
    model = KiwiException
    fields = ('exception_message', 'json_data', 'occurrences')
    readonly_fields = ('exception_message', 'json_data', 'occurrences')

    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(ExceptionInlineAdmin, self).get_queryset(request)
        return qs.order_by('exception_message').distinct('exception_message')

    def occurrences(self, obj):
        return self.model.objects.filter(exception_message=obj.exception_message).count()

    def json_data(self, obj):
        return mark_safe('<a href="www.wikipedia.org">Download json</a>')


@register(SkyflyRequest)
class SkyflyRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'href', 'number_of_flights', 'number_of_cities')
    inlines = (ExceptionInlineAdmin, )

    def href(self, obj):
        url = reverse('skyfly:request', kwargs={'request_hash': obj.request_hash})
        href = format_html(
            f'<a href={url}>{url}</a>'
        )
        return href

    def number_of_flights(self, obj):
        return obj.flights.count()

    def number_of_cities(self, obj):
        return obj.cities.count()
