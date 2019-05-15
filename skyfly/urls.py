from django.urls import path
from .views import app_index, submit, skyfly_request

app_name = 'skyfly'
urlpatterns = [
    path('', app_index, name='index'),
    path('submit/', submit, name='submit'),
    path('request/<str:request_hash>', skyfly_request, name='request')
]
