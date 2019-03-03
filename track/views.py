from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.list import ListView

from .forms import ProfileForm
from .models import Settings, WeightMeasurement, WeightRecord


def home_page(request):
    return render(request, 'home.html')


def chart(request):
    if request.method == 'GET':
        weight_data = {}
        unit = request.GET.get('unit')

        for record in WeightRecord.objects.all():
            name = '{} {}'.format(record.person.first_name, record.person.last_name)
            name = name.strip()
            weight_data[name] = {
                'colour': _get_preferred_colour(record),
                'measurements': []
            }

            for measurement in record.measurements.all():
                weight_data[name]['measurements'].append(
                    {'x': measurement.created, 'y': measurement.weight_as(unit)}
                )

        return JsonResponse(weight_data)

    return HttpResponse(status=400, reason='Only GET requests are allowed')


def _get_preferred_colour(record):
    try:
        return record.person.settings.preferred_colour
    except Settings.DoesNotExist:
        return ''


class MyDataView(LoginRequiredMixin, ListView):

    model = WeightMeasurement
    template_name = 'mydata.html'

    def get_queryset(self):
        return WeightMeasurement.objects.filter(
            weight_record=WeightRecord.objects.get(person=self.request.user))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page'] = 'mydata'
        unit = self.request.GET.get('unit', self._get_preferred_unit())
        measurements = []

        for measurement in data['object_list']:
            measurements.append({
                'weight': measurement.weight_as(unit),
                'created': measurement.created,
                'unit': unit
            })

        data['object_list'] = measurements
        return data

    def _get_preferred_unit(self):
        try:
            return self.request.user.settings.preferred_unit
        except Settings.DoesNotExist:
            return 'kg'


class AddMeasurementView(LoginRequiredMixin, CreateView):

    model = WeightMeasurement
    fields = ['weight', 'unit']
    template_name = 'add.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page'] = 'add'
        data['show_form'] = True

        latest = WeightMeasurement.objects.filter(
            weight_record=WeightRecord.objects.get(person=self.request.user)
        )

        if latest and latest[0].created == date.today():
            data['show_form'] = False

        return data

    def form_valid(self, form):
        form.instance.weight_record = WeightRecord.objects.get(person=self.request.user)
        return super().form_valid(form)


@login_required
def settings_view(request):
    try:
        settings = request.user.settings
    except Settings.DoesNotExist:
        settings = Settings(user=request.user, preferred_colour='#ff6666', preferred_unit='kg')
        settings.save()

    if request.method == 'GET':
        form = ProfileForm(instance=settings)
    elif request.method == 'POST':
        form = ProfileForm(instance=settings, data=request.POST)
        form.save()
    else:
        return HttpResponse(status=405)  # Method not allowed

    context = {
        'page': 'settings',
        'form': form
    }

    return render(request, 'settings.html', context)
