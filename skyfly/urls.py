from django.urls import path
from .views import app_index, submit

app_name = 'skyfly'
urlpatterns = [
    path('', app_index, name='index'),
    path('submit/', submit, name='submit')
]
