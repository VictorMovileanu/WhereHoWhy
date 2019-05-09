import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .tasks import query_kiwi


def app_index(request):
    return render(request, 'skyfly/index.html')


@require_http_methods(['POST'])
def submit(request):
    request_hash, destinations, dates = _generate_submission_data(request)
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
