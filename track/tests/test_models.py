from django.contrib.auth.models import User
from django.test import TestCase

from track.models import WeightMeasurement, WeightRecord


class WeightMeasurementTest(TestCase):

    def test_weight_as_kg(self):
        self.assertEqual(self.measurement.weight_as('kg'), 74.6)

    def test_weight_as_stone(self):
        self.assertEqual(self.measurement.weight_as('stone'), 11.7)

    def test_weight_as_none(self):
        self.assertEqual(self.measurement.weight_as(None), 74.6)

    def test_weight_as_invalid(self):
        self.assertEqual(self.measurement.weight_as('foo'), 74.6)

    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='User1')
        user1_record = WeightRecord.objects.create(person=user1)
        self.measurement = WeightMeasurement.objects.create(weight_record=user1_record, weight=74.6)
