from django.db import models
from django.db.models import F, Min, Max, FloatField, ExpressionWrapper

from utils.abstract_models import TimeStampedModel


class FlightsManager(models.Manager):

    def grouped_by_city(self, limit=10):
        qs = super().get_queryset()
        cities = super().get_queryset().distinct('city').values_list('city', flat=True)
        result = {}
        for city in cities:
            sub_qs = qs.filter(city=city)
            sub_qs = sub_qs.annotate(time_per_euro=F('trip_duration')/F('price'))
            min_ = sub_qs.aggregate(Min('time_per_euro'))['time_per_euro__min']
            max_ = sub_qs.aggregate(Max('time_per_euro'))['time_per_euro__max']
            # we want the minimum opacity to be 0.2 and maximum 1
            sub_qs = sub_qs.annotate(opacity=ExpressionWrapper(self._linear_function(F('time_per_euro'), min_, max_),
                                                               output_field=FloatField()))
            sub_qs = sub_qs.order_by('-opacity')
            result[city] = sub_qs[:limit]
        return result

    @staticmethod
    def _linear_function(x, min_, max_):
        # linear increase between 0.2 and 1
        return 0.8 * (x - max_) / (max_ - min_) + 1


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
    flights = FlightsManager()  # INFO: usage: i.flights(manager='flights')


class KiwiException(TimeStampedModel):
    skyfly_request = models.ForeignKey(SkyflyRequest, on_delete=models.CASCADE, related_name='exceptions')
    exception_message = models.TextField()
    data = models.TextField()
