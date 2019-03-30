from django.urls import path
from .views import app_index

urlpatterns = [
    path('', app_index, name='skyfly')
]
