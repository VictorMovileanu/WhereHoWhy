import datetime

from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class SubmissionTests(TestCase):

    def test_kiwi_query(self):
        settings.SIMULTANEOUS_REQUESTS = 0
        url = reverse('skyfly:index')
        data = {
            'city-from_0': 'MUC',
            'city-from_1': 'LUX',
            'city-to_2': 'CDG',
            'city-to_3': 'BUD',
        }

        for n, date_range in enumerate(self._generate_dates()):
            data['flight-date_' + str(n)] = date_range

        self.client.post(url, data)

    @staticmethod
    def _generate_dates():
        today = datetime.datetime.now()
        days_to_friday = 4 - today.weekday()
        friday_in_one_month = today + datetime.timedelta(days=days_to_friday) + datetime.timedelta(days=28)
        dates = [
            {'from': (friday_in_one_month + datetime.timedelta(days=7*i)).strftime('%d/%m/%Y'),
             'until': (friday_in_one_month + datetime.timedelta(days=7*i) + datetime.timedelta(days=2)).strftime('%d/%m/%Y')}
            for i in range(2)
        ]

        result = []
        for date in dates:
            d = date['from'] + " - " + date['until']
            result.append(d)
        return result
