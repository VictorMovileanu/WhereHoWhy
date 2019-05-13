import datetime

from django.test import TestCase

from skyfly.models import SkyflyRequest
from skyfly.tasks import query_kiwi


class KiwiTest(TestCase):

    def test_kiwi_query(self):
        request_hash = hash(self)
        SkyflyRequest.objects.create(request_hash=request_hash)
        destinations = [
            {'city': 'CDG', 'price': 300, 'color': '#0b25f5'},  # Paris
            {'city': 'BUD', 'price': 300, 'color': '#13cc11'},  # Budapest
            {'city': 'MPL', 'price': 300, 'color': '#1196cc'},  # Montpellier
            {'city': 'ARN', 'price': 300, 'color': '#ec20c0'},  # Stockholm
            {'city': 'SPU', 'price': 300, 'color': '#a125ce'},  # Split
            {'city': 'VIE', 'price': 300, 'color': '#f11010'},  # Vienna
            {'city': 'CPH', 'price': 300, 'color': '#f1e208'},  # Copenhagen
            {'city': 'CIA', 'price': 300, 'color': '#25ce7a'},  # Rom
            {'city': 'AIA', 'price': 300, 'color': '#1365cc'},  # Athens
            {'city': 'IST', 'price': 300, 'color': '#f59f0b'},  # Istanbul
        ]
        today = datetime.datetime.now()
        days_to_friday = 4 - today.weekday()
        friday_in_one_month = today + datetime.timedelta(days=days_to_friday) + datetime.timedelta(days=28)
        dates = [
            {'from': (friday_in_one_month + datetime.timedelta(days=7*i)).strftime('%d/%m/%Y'),
             'until': (friday_in_one_month + datetime.timedelta(days=7*i) + datetime.timedelta(days=2)).strftime('%d/%m/%Y')}
            for i in range(4)
        ]
        query_kiwi(request_hash, destinations, dates)
