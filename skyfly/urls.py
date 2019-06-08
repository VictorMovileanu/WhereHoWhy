from django.urls import path
from .views import IndexView, skyfly_request, csv_serve_view, iata_codes_serve_view, skyfly_request_info

app_name = 'skyfly'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('request/<str:request_hash>/', skyfly_request, name='request'),
    path('data/iata-codes/', iata_codes_serve_view, name='iata-codes'),
    path('data/<str:request_hash>/', csv_serve_view, name='request-csv-data'),
    path('info/<str:request_hash>/', skyfly_request_info, name='request-info')
]
