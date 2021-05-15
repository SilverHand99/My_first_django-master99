from django.test import TestCase
from django.urls import reverse


class ViewTest(TestCase):

    def test_view(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_view2(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_template_used(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'my_index.html')
