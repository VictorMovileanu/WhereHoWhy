from django.urls import path
from .views import app_index, submit, skyfly_request, csv_serve_view

app_name = 'skyfly'
urlpatterns = [
    path('', app_index, name='index'),
    path('submit/', submit, name='submit'),
    path('request/<str:request_hash>', skyfly_request, name='request'),
    path('data/<str:request_hash>', csv_serve_view, name='request-csv-data')
]
