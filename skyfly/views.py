import csv
import json
import os
from datetime import datetime

import pytz
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from skyfly.models import SkyflyRequest
from .tasks import query_kiwi


def app_index(request):
    return render(request, 'skyfly/index.html')


@require_http_methods(['POST'])
def submit(request):
    try:
        request_hash, destinations, dates = _generate_submission_data(request)
    except AssertionError:
        return JsonResponse({'error_msg': 'Faulty submission data'}, status=400)
    else:
        SkyflyRequest.objects.create(request_hash=request_hash)
        if destinations and dates:
            query_kiwi.delay(request_hash, destinations, dates)
        redirect_url = reverse('skyfly:request', kwargs={'request_hash': request_hash})
        return JsonResponse({'redirect_url': redirect_url})


def _generate_submission_data(request):
    data = json.loads(request.POST.get('data', ''))
    destinations = data['destination-table']
    dates = data['date-table']

    _validate_destinations(destinations)
    _validate_dates(dates)

    data.update({
        'user': request.user,
        'time': datetime.now()
    })
    request_hash = hash(str(data))
    return request_hash, destinations, dates


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


def _validate_dates(dates):
    for date in dates:
        try:
            datetime.strptime(date['from'], '%d/%m/%Y')
            datetime.strptime(date['until'], '%d/%m/%Y')
        except ValueError:
            raise AssertionError


def csv_serve_view(request, request_hash):
    response = HttpResponse(content_type='text/csv')
    flights = SkyflyRequest.objects.get(request_hash=request_hash).flights.all()
    response['Content-Disposition'] = f'attachment; filename="data.csv"'
    writer = csv.writer(response)
    writer.writerow(['label', 'y', 't0', 't1', 'delta_t', 'href', 'color', 'opacity'])
    for flight in flights:
        writer.writerow([flight.city, flight.price, _datetime_to_seconds(flight.departure),
                         _datetime_to_seconds(flight.arrival), flight.trip_duration,
                         flight.deep_link, flight.color, 0.5])
    return response


def iata_codes_serve_view(request):
    with open(os.path.join(settings.BASE_DIR, 'static/data/iata_codes.json')) as json_file:
        data = json.load(json_file)
    return JsonResponse({'data': data})


def skyfly_request(request, request_hash):
    return render(request, 'skyfly/skyfly_request.html', {'request_hash': request_hash})


def _datetime_to_seconds(dt_object):
    """Number of seconds from the date ot the datetime object to 1. January 1970"""
    delta_datetime = (dt_object - datetime(1970, 1, 1, tzinfo=pytz.utc))
    return int(delta_datetime.total_seconds())
