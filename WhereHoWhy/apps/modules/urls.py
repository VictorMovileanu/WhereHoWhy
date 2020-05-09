from django.urls import path

from WhereHoWhy.apps.modules.views import QuoteView

app_name = "modules"
urlpatterns = [
    path('quote/<uuid:uuid>/', QuoteView.as_view(), name="quote"),
]
