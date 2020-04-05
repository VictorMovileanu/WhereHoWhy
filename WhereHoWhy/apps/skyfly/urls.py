from django.urls import path
from .views import IndexView, skyfly_request, csv_serve_view, iata_codes_serve_view, skyfly_request_status

app_name = 'skyfly'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('request/<uuid:request_uuid>/', skyfly_request, name='request'),
    path('request/<uuid:request_uuid>/status/', skyfly_request_status, name='request-status'),
    path('request/<uuid:request_uuid>/data/', csv_serve_view, name='request-csv-data'),
    path('data/iata-codes/', iata_codes_serve_view, name='iata-codes'),
]
