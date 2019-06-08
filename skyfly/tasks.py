from __future__ import absolute_import, unicode_literals

import logging
import traceback
from datetime import datetime

import pytz
from billiard.pool import Pool
from celery import shared_task
import requests
from django.conf import settings

from skyfly.models import SkyflyRequest, KiwiResponse, KiwiException

logger = logging.getLogger('skyfly')


def process_request(i):
    destination, date, request_uuid = i

    try:
        skyfly_request_object = SkyflyRequest.objects.get(unique_id=request_uuid)
    except SkyflyRequest.DoesNotExist:
        raise Exception(f'SkyflyRequest object with hash {request_uuid} does not exist')
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
            KiwiException.objects.create(
                skyfly_request=skyfly_request_object,
                exception_message=str(e),
                data=trip,
                traceback=traceback.format_exc()
            )
            logger.exception(e)

    skyfly_request_object.left_combinations -= 1
    skyfly_request_object.save()

    return skyfly_request_object


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


@shared_task
def query_kiwi(chunk):

    pool = Pool(settings.SIMULTANEOUS_REQUESTS)
    pool.map(process_request, chunk)
