import csv
import json
from datetime import datetime

import pytz
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from skyfly.models import SkyflyRequest
from .tasks import query_kiwi


def app_index(request):
    return render(request, 'skyfly/index.html')


@require_http_methods(['POST'])
def submit(request):
    request_hash, destinations, dates = _generate_submission_data(request)
    SkyflyRequest.objects.create(request_hash=request_hash)
    if destinations and dates:
        query_kiwi.delay(request_hash, destinations, dates)
    return JsonResponse({'request_hash': request_hash})


def _generate_submission_data(request):
    data = json.loads(request.POST.get('data', ''))
    destinations = data['destination-table']
    dates = data['date-table']
    data.update({
        'user': request.user,
        'time': datetime.now()
    })
    request_hash = hash(str(data))
    return request_hash, destinations, dates


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


def skyfly_request(request, request_hash):
    return render(request, 'skyfly/skyfly_request.html', {'request_hash': request_hash})


def _datetime_to_seconds(dt_object):
    """Number of seconds from the date ot the datetime object to 1. January 1970"""
    delta_datetime = (dt_object - datetime(1970, 1, 1, tzinfo=pytz.utc))
    return int(delta_datetime.total_seconds())
