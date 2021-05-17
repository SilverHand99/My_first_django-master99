from django.test import TestCase
from django.urls import reverse
from my_projekt.models import User


class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='ibrahim', password='16.10.1999',)

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

    def test_view_bay(self):
        resp = self.client.get(reverse('bay'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'bay_tesla_cars.html')

    def test_view_cart(self):
        resp = self.client.get(reverse('cart'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cart.html')

    def test_view_register(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

    def test_view_modelX(self):
        resp = self.client.get(reverse('Model_X'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tesla_model_X.html')

    def test_view_car_complekt(self):
        resp = self.client.get(reverse('complekt'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'car_complekt.html')

    def test_view_car_login(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

    def test_view_car_logout(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)

    def test_view_cart_delete(self):
        resp = self.client.get(reverse('delete'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cart_delete.html')

    def test_view_avatars(self):
        self.client.login(username='ibrahim', password='16.10.1999')
        resp = self.client.get(reverse('avatars'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'profile.html')

    def test_view_change_profile(self):
        resp = self.client.get(reverse('change_profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'Change_profile.html')



