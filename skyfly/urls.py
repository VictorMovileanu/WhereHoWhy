from django.urls import path
from .views import app_index, submit

urlpatterns = [
    path('', app_index, name='skyfly'),
    path('submit/', submit, name='submit')
]
