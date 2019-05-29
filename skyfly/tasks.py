from __future__ import absolute_import, unicode_literals

import logging
from datetime import datetime

import pytz
from billiard.pool import Pool
from celery import shared_task
import requests
from django.utils import timezone

from skyfly.models import SkyflyRequest, KiwiResponse, KiwiException

logger = logging.getLogger('skyfly')


def process_request(i):
    request_hash, destination, date = i

    try:
        skyfly_request_object = SkyflyRequest.objects.get(request_hash=request_hash)
    except SkyflyRequest.DoesNotExist:
        raise Exception(f'SkyflyRequest object with hash {request_hash} does not exist')
    # WARNING: question: does it make any sense to check for duplicate hashes?

    base_url = 'https://api.skypicker.com/'
    flights = base_url + 'flights'
    loc = 'MUC'

    parameters = {
        'date_from': date['from'],
        'date_to': date['from'],
        'return_from': date['until'],
        'return_to': date['until'],
        'fly_from': 'MUC',
        'fly_to': destination['city'],
        'partner': 'picky',
        'curr': 'EUR',
        'price_to': destination['price'],
    }

    logger.debug(f'Querying Kiwi with the parameters: {parameters}')
    resp = requests.get(flights, params=parameters)

    for trip in resp.json()['data']:

        try:
            t_departure, t_arrival, trip_duration = _calculate_flight_duration_information(trip, loc, destination['city'])

            # TODO: add admin inline for flights
            KiwiResponse.objects.create(
                skyfly_request=skyfly_request_object,
                city=trip['cityTo'],
                price=trip['price'],
                departure=datetime.fromtimestamp(t_departure, tz=pytz.UTC),
                arrival=datetime.fromtimestamp(t_arrival, tz=pytz.UTC),
                trip_duration=trip_duration,
                deep_link=trip['deep_link'],
                color=destination['color']
            )

        except Exception as e:
            # TODO: add admin inlines for exceptions
            KiwiException.objects.create(
                skyfly_request=skyfly_request_object,
                exception_message=str(e),
                data=trip
            )
            logger.exception(e)


def _calculate_flight_duration_information(trip, location, destination):
    if destination == 'anywhere':
        routes = trip['routes']
        destination = routes[0][1]
    route = trip['route']
    i = 0
    t_departure_from_location = route[0]['dTimeUTC']
    while route[i]['flyTo'] != destination:
        i += 1
    t_arrival_at_destination = route[i]['aTimeUTC']
    i += 1
    t_departure_from_destination = route[i]['dTimeUTC']
    while route[i]['flyTo'] != location:
        i += 1
    t_arrival_at_location = route[i]['aTimeUTC']
    return t_departure_from_location, t_arrival_at_location, t_departure_from_destination - t_arrival_at_destination


def f(request_hash, destinations, dates):
    for destination in destinations:
        for date in dates:
            yield request_hash, destination, date


@shared_task
def query_kiwi(request_hash, destinations, dates):

    pool = Pool(5)
    iterable = f(request_hash, destinations, dates)
    pool.map(process_request, iterable)
    skyfly_request_object = SkyflyRequest.objects.get(request_hash=request_hash)
    skyfly_request_object.completed = timezone.now()
    skyfly_request_object.save()
