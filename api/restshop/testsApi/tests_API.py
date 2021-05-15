from rest_framework.test import APIRequestFactory
from rest_framework import status
from my_projekt.models import Car, Category, Company
from my_projekt.models import User
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase


class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='Add234', password='16.10.1999.999')

    def test_create_car(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        url = reverse('Category-list')
        data = {'description': 'Tesla_X',
                'title': 'electro_car'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)


class AccountTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='Add12', password='16.10.1999.122', email='sdwddsd@dwd.swd')

    def test_create_account(self):
        self.client.login(username='Add12', password='16.10.1999.122', email='sdwddsd@dwd.swd')
        url = '/api/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)


class CarTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='Add234', password='16.10.1999.999')

    def test_create_car(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        category = Category.objects.create(description='sdsdwd', title='sdwdwd')
        company = Company.objects.create(title='sdwdwd')
        url = reverse('car-list',)
        data = {'description': 'Tesla_X',
                'title': 'electro_car',
                'price': 123421,
                'category': [category.id],
                'company': company.id,
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)


class CompanyTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='Add234', password='16.10.1999.999')

    def test_change_company(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        Company.objects.create(title='1231231', id='1')
        url = '/api/company/1/'
        data = {'title': 'Tesla_1234',
                'id': '1'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get(id="1").title, data['title'])


class CarChangeTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='Add234', password='16.10.1999.999')

    def test_change_company(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        company = Company.objects.create(title='zxczxc')
        categories = Category.objects.create(description='dwdwd', title='sdwdwd')
        car = Car.objects.create(title='1231231', description='sdwdsdw', price=121312, company=company)
        car.categories.add(categories.id)
        car.save()
        url = '/api/cars/1/'
        data = {'description': 'Tesla_X',
                'title': 'electro_car',
                'price': 123421,
                'category': [categories.id],
                'company': company.id,}
        response = self.client.put(url, data, format='json')
        car.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get(id="1").title, data['title'])


class CategoryTest2(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='Add2324', password='16.10.1999.9999')

    def test_change_category2(self):
        self.client.login(username='Add2324', password='16.10.1999.9999')
        Category.objects.create(description='dwdsdwd', title='1231231', id='1')
        url = '/api/categories/1/'
        data = {'title': 'Tesla_1234'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get(id="1").title, data['title'])
