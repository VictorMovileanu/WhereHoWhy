import csv
import json
import os
from datetime import datetime

import pytz
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from skyfly.models import SkyflyRequest
from .tasks import query_kiwi


class IndexView(View):

    def get(self, request):
        return render(request, 'skyfly/index.html')

    def post(self, request):
        try:
            data = json.loads(request.POST.get('data', ''))
            destinations, dates = self._generate_submission_data(data)
        except AssertionError:
            return JsonResponse({'error_msg': 'Faulty submission data'}, status=400)
        else:
            if destinations and dates:
                combinations = []
                for destination in destinations:
                    for date in dates:
                        combinations.append((destination, date))
                skyfly_request_instance = SkyflyRequest.objects.create(left_combinations=len(combinations))

                chunk_size = settings.SIMULTANEOUS_REQUESTS
                for i in range(0, len(combinations), chunk_size):
                    chunk = combinations[i:i + chunk_size]
                    chunk = [tup + (skyfly_request_instance.unique_id,) for tup in chunk]  # todo: refactor this
                    query_kiwi.delay(chunk)
                redirect_url = reverse('skyfly:request', kwargs={'request_uuid': skyfly_request_instance.unique_id})
                return JsonResponse({'redirect_url': redirect_url})
            else:
                JsonResponse({'error_msg': 'No data submitted!'}, status=400)

    def _generate_submission_data(self, data):
        destinations = data['destination-table']
        dates = data['date-table']

        self._validate_destinations(destinations)
        self._validate_dates(dates)

        return destinations, dates

    @staticmethod
    def _validate_destinations(destinations):
        with open(os.path.join(settings.BASE_DIR, 'static/data/iata_codes.json')) as json_file:
            iata_code_list = json.load(json_file)
        for dst in destinations:
            assert dst['city'] in iata_code_list
            assert type(dst['price']) == int
            try:
                int(dst['color'][1:3], 16)
                int(dst['color'][3:5], 16)
                int(dst['color'][5:], 16)
            except ValueError:
                raise AssertionError

    @staticmethod
    def _validate_dates(dates):
        for date in dates:
            try:
                datetime.strptime(date['from'], '%d/%m/%Y')
                datetime.strptime(date['until'], '%d/%m/%Y')
            except ValueError:
                raise AssertionError


def csv_serve_view(request, request_uuid):
    response = HttpResponse(content_type='text/csv')
    grouped_flights = SkyflyRequest.objects.get(unique_id=request_uuid).flights.grouped_by_city()
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
    return render(request, 'skyfly/skyfly_request.html', {'request_uuid': request_uuid})


def skyfly_request_info(request, request_uuid):
    skyfly_request_object = SkyflyRequest.objects.get(unique_id=request_uuid)
    if skyfly_request_object.left_combinations == 0:
        status = 'finished'
    else:
        status = 'running'
    return JsonResponse({'status': status})


def _datetime_to_seconds(dt_object):
    """Number of seconds from the date ot the datetime object to 1. January 1970"""
    delta_datetime = (dt_object - datetime(1970, 1, 1, tzinfo=pytz.utc))
    return int(delta_datetime.total_seconds())
