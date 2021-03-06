from rest_framework.test import RequestsClient
from rest_framework.test import APIRequestFactory, RequestsClient
from rest_framework import status
from my_projekt.models import Car, Category, Company, User_Profile, Car_Complekt, Location
from my_projekt.models import User
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import requests
from requests.auth import HTTPBasicAuth


class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='Add234', password='16.10.1999.999')

    def test_create_category(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        url = reverse('Category-list')
        data = {'description': 'Tesla_X',
                'title': 'electro_car'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_change_category_with_put(self):
        Category.objects.create(description='dwdwd', title='sdwdwd')
        self.client.login(username='Add234', password='16.10.1999.999')
        url = '/api/categories/1/'
        data = {'description': 'Tesla_X',
                'title': 'electro_car'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get(id="1").title, data['title'])

    def test_change_category_with_patch(self):
        self.client.login(username='Add2324', password='16.10.1999.9999')
        Category.objects.create(description='dwdsdwd', title='1231231', id='1')
        url = '/api/categories/1/'
        data = {'title': 'Tesla_1234'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get(id="1").title, data['title'])

    def test_delete_category(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        url = reverse('Category-list')
        data = {'description': 'Tesla_X',
                'title': 'electro_car'}
        response = self.client.post(url, data, format='json')
        category = Category.objects.get(id=1)
        pk = category.pk
        category.delete()
        with self.assertRaises(Category.DoesNotExist):
            category = Category.objects.get(pk=pk)

    def test_reading_category(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        category = Category.objects.create(title='test', description='test')
        url = reverse('Category-list')
        data = {
            'title': 'test',
            'description': 'test'
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), category.title)
        self.assertEqual(data.get('description'), category.description)


class AccountTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='Add12', password='16.10.1999.122',
                                                  email='sdwddsd@dwd.swd', )

    def test_create_account(self):
        self.client.login(username='Add12', password='16.10.1999.122', email='sdwddsd@dwd.swd')
        url = '/api/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_change_account(self):
    #     self.client.login(username='Add12', password='16.10.1999.122', email='sdwddsd@dwd.swd')
    #     user = User.objects.create_user(username='Add1sd', password='16.10.1999.122', email='sdwddsddwd@dwd.swd', id=3)
    #     user.save()
    #     url = '/api/users/user.id/'
    #     data = {'username': 'Dadsdd122',
    #             'email': 'dwwdw@dwd.cdw',
    #             'password': '16.10.1999.122',
    #             }
    #     self.client.put(data, url, format='json')
    #     user.refresh_from_db()
    #     self.assertEqual(user.email, data['email'])


class CarTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='Add234', password='16.10.1999.999')

    def test_create_car(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        category = Category.objects.create(description='sdsdwd', title='sdwdwd')
        company = Company.objects.create(title='sdwdwd')
        url = reverse('car-list', )
        data = {'description': 'Tesla_X',
                'title': 'electro_car',
                'price': 123421,
                'category': [category.id],
                'company': company.id,
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)

    def test_change_car_with_put(self):
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
                'company': company.id, }
        response = self.client.put(url, data, format='json')
        car.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get(id="1").title, data['title'])

    def test_change_car_patch(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        category = Category.objects.create(description='sdsdwd', title='sdwdwd')
        company = Company.objects.create(title='sdwdwd')
        Car.objects.create(title='1231231', description='sdwdsdw', price=121312, company=company)
        url = '/api/cars/1/'
        data = {
            'price': 345346,
            'category': [category.id],
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get(id="1").price, data['price'])

    def test_delete_car(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        category = Category.objects.create(description='sdsdwd', title='sdwdwd')
        company = Company.objects.create(title='sdwdwd')
        url = reverse('car-list', )
        data = {'description': 'Tesla_X',
                'title': 'electro_car',
                'price': 123421,
                'category': [category.id],
                'company': company.id,
                }
        response = self.client.post(url, data, format='json')
        car = Car.objects.get(id=1)
        pk = car.pk
        car.delete()
        with self.assertRaises(Car.DoesNotExist):
            car = Car.objects.get(pk=pk)

    def test_reading_car(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        category = Category.objects.create(description='sdsdwd', title='sdwdwd')
        company = Company.objects.create(title='sdwdwd')
        car = Car.objects.create(title='electro_car', description='Tesla_X', price=123421, company=company)
        url = reverse('car-list', )
        data = {'description': 'Tesla_X',
                'title': 'electro_car',
                'price': 123421,
                'category': [category.id],
                'company': company.id,
                }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), car.title)
        self.assertEqual(data.get('description'), car.description)
        self.assertEqual(data.get('price'), car.price)


class CompanyTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='Add234', password='16.10.1999.999')

    def test_create_company(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        url = (reverse('company-list'))
        data = {'title': 'Tesla_1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)

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

    def test_change_company_patch(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        Company.objects.create(title='1231231')
        url = '/api/company/1/'
        data = {'title': 'Tesla_1234'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get(id="1").title, data['title'])

    def test_delete_company(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        url = (reverse('company-list'))
        data = {'title': 'Tesla_1234'}
        response = self.client.post(url, data, format='json')
        company = Company.objects.get(id=1)
        pk = company.pk
        company.delete()
        with self.assertRaises(Company.DoesNotExist):
            company = Company.objects.get(pk=pk)

    def test_reading_company(self):
        self.client.login(username='Add234', password='16.10.1999.999')
        url = (reverse('company-list'))
        company = Company.objects.create(title='Tesla_1234')
        data = {'title': 'Tesla_1234'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), company.title)


class TestLoginRegisterApi(APITestCase):

    def test_register(self):
        data = {
            'username': 'add234',
            'email': '16.10.1999.999',
            'password1': 'wwwwww_WW_WW',
            'password2': 'wwwwww_WW_WW'
        }
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def setUp(self):
        self.user = User.objects.create_user(username='Add234', password='16.10.1999.999')
        self.token = Token.objects.create(user=self.user)

    def test_login_with_token(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/login/')
        assert response.status_code == 200
        csrftoken = response.cookies['csrftoken']
        response = client.post('http://127.0.0.1:8000/login/', json={
            'username': 'Add234',
            'password': '16.10.1999.999'
        }, headers={'X-CSRFToken': csrftoken})
        assert response.status_code == 200



