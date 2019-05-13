from __future__ import absolute_import, unicode_literals

from datetime import datetime

from billiard.pool import Pool
from celery import shared_task
import requests

from skyfly.models import SkyflyRequest, KiwiResponse


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

    resp = requests.get(flights, params=parameters)
    print(resp.json())

    for trip in resp.json()['data']:

        try:
            t_departure, t_arrival, trip_duration = _calculate_flight_duration_information(trip, loc, destination)

            KiwiResponse.objects.create(
                skyfly_request=skyfly_request_object,
                city=trip['cityTo'],
                price=trip['price'],
                departure=datetime.utcfromtimestamp(t_departure),
                arrival=datetime.utcfromtimestamp(t_arrival),
                trip_duration=trip_duration,
                deep_link=trip['deep_link'],
                color=destination['color']
            )

        except Exception:
            pass  # could not be processed for some reason


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
