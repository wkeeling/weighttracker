from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.list import ListView

from track.models import WeightMeasurement, WeightRecord


def home_page(request):
    return render(request, 'home.html')


def chart(request):
    if request.method == 'GET':
        weight_data = {}
        unit = request.GET.get('unit')

        for record in WeightRecord.objects.all():
            name = '{} {}'.format(record.person.first_name, record.person.last_name)
            name = name.strip()
            weight_data[name] = []

            for measurement in record.measurements.all():
                weight_data[name].append({'x': measurement.created, 'y': measurement.weight_as(unit)})

        return JsonResponse(weight_data)

    return HttpResponse(status=400, reason='Only GET requests are allowed')


class MyDataView(LoginRequiredMixin, ListView):

    model = WeightMeasurement
    template_name = 'data.html'

    def get_queryset(self):
        return WeightMeasurement.objects.filter(
            weight_record=WeightRecord.objects.get(person=self.request.user))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        unit = self.request.GET.get('unit')
        measurements = []

        for measurement in data['object_list']:
            measurements.append({
                'weight': measurement.weight_as(unit),
                'created': measurement.created,
                'unit': unit
            })

        data['object_list'] = measurements
        return data
