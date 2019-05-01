import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def app_index(request):
    return render(request, 'skyfly/index.html')


@require_http_methods(['POST'])
def submit(request):
    data = json.loads(request.POST.get('data', ''))
    return JsonResponse({})
