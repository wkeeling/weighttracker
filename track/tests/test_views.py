import json

from django.contrib.auth.models import User
from django.template.loader import render_to_string
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
        expected_html = render_to_string('home.html')

        response = self.client.get('/track/')

        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(response.content.decode(), expected_html)

    def test_renders_chart_data(self):
        user1 = User.objects.create(username='user1', first_name='User1')
        user2 = User.objects.create(username='user2', first_name='User', last_name='2')
        user1_record = WeightRecord.objects.create(person=user1)
        user2_record = WeightRecord.objects.create(person=user2)
        WeightMeasurement.objects.create(weight_record=user1_record, weight=74.6)
        WeightMeasurement.objects.create(weight_record=user1_record, weight=11.2, unit='stone')
        WeightMeasurement.objects.create(weight_record=user2_record, weight=82.2)
        WeightMeasurement.objects.create(weight_record=user2_record, weight=81.5)

        response = self.client.get('/track/chart/')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['User1'], [[74.6, 'kg'], [11.2, 'stone']])
        self.assertEqual(data['User 2'], [[82.2, 'kg'], [81.5, 'kg']])

    def test_renders_chart_data_400_when_post(self):
        response = self.client.post('/track/chart/')

        self.assertEqual(response.status_code, 400)
