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


class ChartTest(TestCase):

    def test_renders_chart(self):
        response = self.client.get('/track/chart/')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        user1_data = data['User1']
        self.assertEqual([v['y'] for v in user1_data], [74.6, 71.1])
        user2_data = data['User 2']
        self.assertEqual([v['y'] for v in user2_data], [81.5, 82.2])

    def test_renders_chart_specifying_unit(self):
        response = self.client.get('/track/chart/?unit=stone')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        user1_data = data['User1']
        self.assertEqual([v['y'] for v in user1_data], [11.7, 11.2])
        user2_data = data['User 2']
        self.assertEqual([v['y'] for v in user2_data], [12.8, 12.9])

    def test_renders_chart_kg_when_unit_invalid(self):
        response = self.client.get('/track/chart/?unit=foo')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        user1_data = data['User1']
        self.assertEqual([v['y'] for v in user1_data], [74.6, 71.1])
        user2_data = data['User 2']
        self.assertEqual([v['y'] for v in user2_data], [81.5, 82.2])

    def test_renders_chart_kg_when_unit_empty(self):
        response = self.client.get('/track/chart/?unit=')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        user1_data = data['User1']
        self.assertEqual([v['y'] for v in user1_data], [74.6, 71.1])
        user2_data = data['User 2']
        self.assertEqual([v['y'] for v in user2_data], [81.5, 82.2])

    def test_renders_chart_data_400_when_post(self):
        response = self.client.post('/track/chart/')

        self.assertEqual(response.status_code, 400)

    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='User1')
        user2 = User.objects.create(username='user2', first_name='User', last_name='2')
        user1_record = WeightRecord.objects.create(person=user1)
        user2_record = WeightRecord.objects.create(person=user2)
        WeightMeasurement.objects.create(weight_record=user1_record, weight=74.6)
        WeightMeasurement.objects.create(weight_record=user1_record, weight=11.2, unit='stone')
        WeightMeasurement.objects.create(weight_record=user2_record, weight=81.5)
        WeightMeasurement.objects.create(weight_record=user2_record, weight=82.2)


class MyDataViewTest(TestCase):

    def test_uses_correct_template(self):
        response = self.client.get('/track/data/')

        self.assertTemplateUsed(response, 'data.html')

    def test_renders_data_kg(self):
        response = self.client.get('/track/data/?unit=kg')

        self.assertEqual(response.status_code, 200)
        self.assertIn('74.6&#160;kg', response.content.decode())

    def test_renders_data_stone(self):
        response = self.client.get('/track/data/?unit=stone')

        self.assertEqual(response.status_code, 200)
        self.assertIn('11.7&#160;stone', response.content.decode())

    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='User1')
        user1.set_password('password')
        user1.save()
        user2 = User.objects.create(username='user2', first_name='User', last_name='2')
        user1_record = WeightRecord.objects.create(person=user1)
        user2_record = WeightRecord.objects.create(person=user2)
        WeightMeasurement.objects.create(weight_record=user1_record, weight=74.6)
        WeightMeasurement.objects.create(weight_record=user1_record, weight=11.2, unit='stone')
        WeightMeasurement.objects.create(weight_record=user2_record, weight=81.5)
        WeightMeasurement.objects.create(weight_record=user2_record, weight=82.2)

        self.client.login(username=user1.username, password='password')


class AddMeasurementViewTest(TestCase):

    def test_uses_correct_template(self):
        response = self.client.get('/track/add/')

        self.assertTemplateUsed(response, 'add.html')

    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='User1')
        user1.set_password('password')
        user1.save()

        self.client.login(username=user1.username, password='password')
