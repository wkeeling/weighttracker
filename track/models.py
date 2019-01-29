from django.db import models
from django.contrib.auth.models import User


class WeightRecord(models.Model):

    person = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'WeightRecord: {}'.format(self.person.username)


class WeightMeasurement(models.Model):

    weight_record = models.ForeignKey(WeightRecord, on_delete=models.CASCADE)
    weight_kg = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'WeightMeasurement: {} kg taken on {}'.format(
            self.weight_kg,
            self.created
        )
