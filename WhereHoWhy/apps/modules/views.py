from django.views.generic import DetailView

from WhereHoWhy.apps.modules.models import Quote


class QuoteView(DetailView):
    template_name = "modules/quote.html"
    model = Quote
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
