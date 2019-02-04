from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from track.models import WeightRecord


def home_page(request):
    return render(request, 'home.html')


def chart(request):
    if request.method == 'GET':
        data = {}

        for record in WeightRecord.objects.all():
            name = '{} {}'.format(record.person.first_name, record.person.last_name)
            measurements = []

            for measurement in record.measurements.all():
                measurements.append((measurement.weight, measurement.unit))

            data[name.strip()] = measurements

        return JsonResponse(data)

    return HttpResponse(status=400, reason='Only GET requests are allowed')
