from django.test import TestCase


class HomePageTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)

    # def test_uses_correct_template(self):
    #     response = self.client.get('/tracker/')
    #
    #     self.assertTemplateUsed(response, 'home.html')
    #
    # def test_renders_home_page(self):
    #     season = Season.objects.get(year=2017)
    #     expected_html = render_to_string('home.html', {
    #         'season': season,
    #         'navigation': [
    #             ('', 'Switch Season'),
    #             ('', 'Add Season')
    #         ]
    #     })
    #
    #     response = self.client.get('/championship/')
    #
    #     self.assertMultiLineEqual(response.content.decode(), expected_html)