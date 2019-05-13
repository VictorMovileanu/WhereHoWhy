from django.db import models

from utils.abstract_models import TimeStampedModel


class SkyflyRequest(TimeStampedModel):
    request_hash = models.CharField(max_length=255, unique=True)


class KiwiResponse(TimeStampedModel):
    skyfly_request = models.ForeignKey(SkyflyRequest, on_delete=models.CASCADE)
    departure = models.DateTimeField(null=True)
    arrival = models.DateTimeField(null=True)
    city = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    trip_duration = models.PositiveIntegerField('Trip duration in seconds')
    deep_link = models.URLField()
    color = models.CharField(max_length=10)
