import operator

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView

from track.models import WeightMeasurement, WeightRecord


def home_page(request):
    return render(request, 'home.html')


OPERATOR = {
    'kg': operator.truediv,
    'stone': operator.mul
}


def chart(request):
    if request.method == 'GET':
        weight_data = {}
        requested_unit = request.GET.get('unit')
        if requested_unit not in OPERATOR:
            requested_unit = 'kg'

        for record in WeightRecord.objects.all():
            name = '{} {}'.format(record.person.first_name, record.person.last_name)
            name = name.strip()
            weight_data[name] = []

            for measurement in record.measurements.all():
                weight = measurement.weight

                if measurement.unit != requested_unit:
                    weight = round(OPERATOR[requested_unit](weight, 0.157473), ndigits=1)

                weight_data[name].append({'x': measurement.created, 'y': weight})

        return JsonResponse(weight_data)

    return HttpResponse(status=400, reason='Only GET requests are allowed')


class DataView(ListView):

    model = WeightMeasurement
    template_name = 'data.html'
