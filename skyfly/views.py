import csv
import json
import os
import random
from collections import defaultdict
from datetime import datetime

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from skyfly import IATA_CODES
from skyfly.models import SkyflyRequest
from .tasks import query_kiwi, process_request


class IndexView(View):

    def __init__(self, **kwargs):
        super(IndexView, self).__init__(**kwargs)
        self.errors = defaultdict(list)

    def get(self, request):
        context = dict()
        skyfly_requests = SkyflyRequest.objects.order_by('-created')
        skyfly_requests = filter(lambda x: x.flights.count() != 0, skyfly_requests)
        context['skyfly_requests'] = skyfly_requests
        return render(request, 'skyfly/index.html', context)

    def post(self, request):
        cities_from, cities_to, flight_dates = self._parse_and_validate_submitted_data(request.POST)
        if self.errors:
            return JsonResponse(self.errors, status=400)
        else:
            combinations = []
            for start in cities_from:
                for destination in cities_to:
                    for date in flight_dates:
                        if start != destination:
                            combinations.append((start, destination, date))

            skyfly_request_instance = SkyflyRequest.objects.create(
                left_combinations=len(combinations),
                length_combinations=len(combinations),
            )

            email = request.POST.get('email')
            if email:
                url = reverse('skyfly:request', kwargs={'request_uuid': skyfly_request_instance.unique_id})
                url = request.build_absolute_uri(url)
                send_mail(
                    'Link to your request',
                    'Here is the link to your request: {}'.format(url),
                    'skyfly@wherehowhy.com',
                    [email],
                    fail_silently=True,  # todo handle error
                )

            if settings.SIMULTANEOUS_REQUESTS:
                chunk_size = settings.SIMULTANEOUS_REQUESTS
                for i in range(0, len(combinations), chunk_size):
                    chunk = combinations[i:i + chunk_size]
                    chunk = list(map(lambda x: x + (skyfly_request_instance.unique_id,), chunk))
                    query_kiwi.delay(chunk)
            else:
                for i in list(map(lambda x: x + (skyfly_request_instance.unique_id,), combinations)):
                    process_request(i)
            status_url = reverse('skyfly:request-status', kwargs={'request_uuid': skyfly_request_instance.unique_id})
            return JsonResponse({'status-url': status_url})

    def _parse_and_validate_submitted_data(self, data):
        # todo: validate flight dates lie in the future
        cities_from = [self._parse_location(data, key) for key in data.keys() if key.startswith('city-from')]
        cities_to = [self._parse_location(data, key) for key in data.keys() if key.startswith('city-to')]
        flight_dates = [self._parse_date_range(data, key) for key in data.keys() if key.startswith('flight-date')]

        cities_from = list(filter(None, cities_from))
        cities_to = [{'code': code, 'color': pick_random_color()} for code in filter(None, cities_to)]
        flight_dates = list(filter(None, flight_dates))

        for ary, label in [(cities_from, 'start location'), (cities_to, 'destination'), (flight_dates, 'date range')]:
            if not len(ary) > 0:
                self.errors['non-field-errors'].append('At least one {} is required'.format(label))
        return cities_from, cities_to, flight_dates

    @staticmethod
    def _validate_location(location):
        assert location in IATA_CODES

    def _parse_location(self, data, key):
        try:
            location = str(data[key]).upper()
            self._validate_location(location)
            return location
        except AssertionError:
            self.errors['input-errors'].append({
                'input_name': key,
                'message': 'Invalid location'
            })
            return None

    def _parse_date_range(self, data, key):
        date = data[key]
        date_from, date_until = map(lambda x: x.strip(), date.split("-"))
        try:
            datetime.strptime(date_from, '%d/%m/%Y')
            datetime.strptime(date_until, '%d/%m/%Y')
            return {'from': date_from, 'until': date_until}
        except ValueError:
            self.errors.append({
                'input_id': key,
                'message': 'Invalid date range format'
            })
            return None


def csv_serve_view(request, request_uuid):
    n = request.GET.get('n', None)
    if n:
        n = int(n)
    response = HttpResponse(content_type='text/csv')
    grouped_flights = SkyflyRequest.objects.get(unique_id=request_uuid).flights.grouped_by_city(limit=n)
    response['Content-Disposition'] = f'attachment; filename="data.csv"'
    writer = csv.writer(response)
    writer.writerow(['label', 'y', 't0', 't1', 'delta_t', 'href', 'color', 'opacity'])
    for city, flights in grouped_flights.items():
        for flight in flights:
            writer.writerow([flight.city, flight.price, _datetime_to_seconds(flight.departure),
                             _datetime_to_seconds(flight.arrival), flight.trip_duration,
                             flight.deep_link, flight.color, flight.opacity])
    return response


def iata_codes_serve_view(request):
    with open(os.path.join(settings.BASE_DIR, 'static/data/iata_codes.json')) as json_file:
        data = json.load(json_file)
    return JsonResponse({'data': data})


def skyfly_request(request, request_uuid):
    skyfly_request_object = SkyflyRequest.objects.get(unique_id=request_uuid)
    context = {
        'request_uuid': request_uuid,
        'finished': (skyfly_request_object.left_combinations == 0)
    }
    return render(request, 'skyfly/skyfly_request.html', context)


def skyfly_request_status(request, request_uuid):
    skyfly_request_instance = SkyflyRequest.objects.get(unique_id=request_uuid)
    progress = skyfly_request_instance.progress
    redirect_url = reverse('skyfly:request', kwargs={'request_uuid': skyfly_request_instance.unique_id})
    return JsonResponse({'progress': progress, 'redirect_url': redirect_url})


def _datetime_to_seconds(dt_object):
    """Number of seconds from the date ot the datetime object to 1. January 1970"""
    delta_datetime = (dt_object - datetime(1970, 1, 1, tzinfo=pytz.utc))
    return int(delta_datetime.total_seconds())


def pick_random_color():
    colors = ['#E52B50', '#FFBF00', '#9966CC', '#FBCEB1', '#7FFFD4', '#007FFF', '#89CFF0', '#000000', '#0000FF',
              '#0095B6', '#8A2BE2', '#DE5D83', '#CD7F32', '#964B00', '#800020', '#702963', '#960018', '#DE3163',
              '#007BA7', '#7FFF00', '#7B3F00', '#0047AB', '#6F4E37', '#B87333', '#FF7F50', '#DC143C', '#00FFFF',
              '#EDC9Af', '#7DF9FF', '#50C878', '#00FF3F', '#FFD700', '#808080', '#008000', '#3FFF00', '#4B0082',
              '#00A86B', '#29AB87', '#B57EDC', '#FFF700', '#C8A2C8', '#BFFF00', '#FF00FF', '#FF00AF', '#800000',
              '#E0B0FF', '#000080', '#CC7722', '#808000', '#FF6600', '#FF4500', '#DA70D6', '#D1E231', '#CCCCFF',
              '#1C39BB', '#FD6C9E', '#8E4585', '#003153', '#CC8899', '#800080', '#E30B5C', '#FF0000', '#C71585',
              '#FF007F', '#E0115F', '#FA8072', '#92000A', '#0F52BA', '#FF2400', '#C0C0C0', '#708090', '#A7FC00',
              '#00FF7F', '#D2B48C', '#483C32', '#008080', '#40E0D0', '#3F00FF', '#7F00FF', '#40826D', '#FFFF00']
    return random.choice(colors)
