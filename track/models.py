from django.db import models
from django.contrib.auth.models import User


class WeightRecord(models.Model):

    person = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'WeightRecord: {}'.format(self.person.username)


class WeightMeasurement(models.Model):

    UNITS = [
        ('kg', 'Kg'),
        ('stone', 'Stone')
    ]

    weight_record = models.ForeignKey(WeightRecord, on_delete=models.CASCADE)
    weight = models.FloatField()
    unit = models.CharField(max_length=10, choices=UNITS, default='kg')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'WeightMeasurement: {} {} taken on {}'.format(
            self.weight,
            self.unit,
            self.created
        )
