from django.contrib.auth.models import User
from django.test import TestCase

from track.models import WeightMeasurement, WeightRecord


class HomePageTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/')

        self.assertRedirects(response, '/track/')

    def test_uses_correct_template(self):
        response = self.client.get('/track/')

        self.assertTemplateUsed(response, 'home.html')

    def test_renders_home_page(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user1_record = WeightRecord.objects.create(person=user1)
        user2_record = WeightRecord.objects.create(person=user2)
        WeightMeasurement.objects.create(weight_record=user1_record, weight=74.6)
        WeightMeasurement.objects.create(weight_record=user2_record, weight=82.2)

        response = self.client.get('/track/')

        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<title>Weight Tracker - Home</title>', response.content.decode())
