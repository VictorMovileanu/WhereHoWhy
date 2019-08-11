from __future__ import absolute_import, unicode_literals

import logging
import traceback
from datetime import datetime

from dateutil import parser
import pytz
from billiard.pool import Pool
from celery import shared_task
import requests
from django.conf import settings

from skyfly.models import SkyflyRequest, KiwiResponse, KiwiException

logger = logging.getLogger('skyfly')


def process_request(i):
    """
    We get here a tuple that contains the following: ('city-from', 'city-to', 'date-range', SkyflyRequest-uuid)
    :param i: Example: ('MUC', 'LUX', '11/08/2019 - 14/08/2019', 1235-12345-12354-1234-1234)
    :return: None. Results are saved to database
    """
    start, destination, date, request_uuid = i

    try:
        skyfly_request_object = SkyflyRequest.objects.get(unique_id=request_uuid)
    except SkyflyRequest.DoesNotExist:
        raise Exception(f'SkyflyRequest object with hash {request_uuid} does not exist')
    # WARNING: question: does it make any sense to check for duplicate hashes?

    parameters = {
        'date_from': date['from'],
        'date_to': date['from'],
        'return_from': date['until'],
        'return_to': date['until'],
        'fly_from': start,
        'fly_to': destination['code'],
        'partner': 'picky',
    }

    logger.debug(f'Querying Kiwi with the parameters: {parameters}')
    resp = requests.get(settings.KIWI_SEARCH_URL, params=parameters, headers={'apikey': settings.KIWI_API_KEY})

    for trip in resp.json()['data']:

        try:
            t_departure, t_arrival, trip_duration = _calculate_flight_duration_information(trip)

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


def _calculate_flight_duration_information(trip):
    route = trip['route']

    def parse_time(s):
        return parser.parse(s).timestamp()
    t_departure = parse_time(route[0]['local_departure'])
    t_arrival = parse_time(route[-1]['local_arrival'])
    t_departure_from_destination, t_arrival_at_destination = 0, 0

    for i in range(len(route)):
        if route[i]['return'] == 0 and route[i+1]['return'] != 0:
            t_arrival_at_destination = parse_time(route[i]['utc_arrival'])
            t_departure_from_destination = parse_time(route[i+1]['utc_departure'])
            break

    return t_departure, t_arrival, t_departure_from_destination - t_arrival_at_destination


@shared_task
def query_kiwi(chunk):
    """
    Distribute queries on multiple threads.
    The chunk is a list of tuples with following content:
    ('city-from', 'city-to', 'date-range', SkyflyRequest-uuid)
    """

    pool = Pool(settings.SIMULTANEOUS_REQUESTS)
    pool.map(process_request, chunk)
