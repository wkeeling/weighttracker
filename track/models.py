import operator

from django.db import models
from django.contrib.auth.models import User


class WeightRecord(models.Model):

    person = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.person.username


OPERATOR = {
    'kg': operator.truediv,
    'stone': operator.mul
}

UNITS = [
    ('kg', 'Kg'),
    ('stone', 'Stone')
]


class WeightMeasurement(models.Model):

    weight_record = models.ForeignKey(WeightRecord, on_delete=models.CASCADE, related_name='measurements')
    weight = models.FloatField()
    unit = models.CharField(max_length=10, choices=UNITS, default='kg')
    created = models.DateField(auto_now_add=True)

    def weight_as(self, unit):
        if unit not in OPERATOR:
            unit = 'kg'

        if unit == self.unit:
            return self.weight

        return round(OPERATOR[unit](self.weight, 0.157473), ndigits=1)

    def __str__(self):
        return '[{}] {} {} taken on {}'.format(
            self.weight_record,
            self.weight,
            self.unit,
            self.created
        )

    class Meta:
        ordering = ['-created']


class Settings(models.Model):
    # Note that it may be better to have this in a dedicated app (e.g. "account")
    # with a different URL path than /track/.

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_unit = models.CharField(max_length=10, choices=UNITS, default='kg')
    preferred_colour = models.CharField(max_length=20, default='#ff6666')

    def __str__(self):
        return '{} settings'.format(self.user.username)
