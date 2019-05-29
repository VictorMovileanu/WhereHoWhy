from django.db import models

from utils.abstract_models import TimeStampedModel


class SkyflyRequest(TimeStampedModel):
    request_hash = models.CharField(max_length=255, unique=True)
    completed = models.DateTimeField(null=True)

    def __str__(self):
        return f'Skyfly Request {self.created}'


class KiwiResponse(TimeStampedModel):
    skyfly_request = models.ForeignKey(SkyflyRequest, on_delete=models.CASCADE, related_name='flights')
    departure = models.DateTimeField(null=True)
    arrival = models.DateTimeField(null=True)
    city = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    trip_duration = models.PositiveIntegerField('Trip duration in seconds')
    deep_link = models.URLField(max_length=2083)
    color = models.CharField(max_length=10)


class KiwiException(TimeStampedModel):
    skyfly_request = models.ForeignKey(SkyflyRequest, on_delete=models.CASCADE, related_name='exceptions')
    exception_message = models.TextField()
    data = models.TextField()
