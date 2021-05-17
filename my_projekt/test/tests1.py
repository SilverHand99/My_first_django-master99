from django.test import TestCase
from my_projekt.models import Category, Company, Car


class TestCategory(TestCase):
    def test_create_category_success(self):
        payload = {
            'title': 'test_title'
        }
        category = Category.objects.create(**payload)
        self.assertEqual(category.title, payload['title'])

    def test_create_category_fail(self):
        payload = {
            'title': 'test_title',
            'unknown_field': 'value'
        }
        with self.assertRaises(TypeError):
            Category.objects.create(**payload)

    """
    Testing model updating function.
    """

    def test_update_category(self):
        new_title = 'new test title'
        payload = {
            'title': 'test_title',
        }
        category = Category.objects.create(**payload)
        category.title = new_title
        category.save()
        category.refresh_from_db()
        self.assertEqual(category.title, new_title)

    """
    Testing model deleting function.
    """

    def test_delete_category(self):
        payload = {
            'title': 'test_title',
        }
        category = Category.objects.create(**payload)
        pk = category.pk
        category.delete()
        with self.assertRaises(Category.DoesNotExist):
            category = Category.objects.get(pk=pk)


class TestCar(TestCase):
    def setUp(self):
        Company.objects.create(title='title')
        Category.objects.create(title='wddwd', description='dwdwd')

    def test_create_car(self):
        categories = Category.objects.get(id=1)
        company = Company.objects.get(id=1)
        payload = {
            'title': 'electro car',
            'description': 'dawdasdw',
            'price': 3412341,
            'categories': [categories],
            'company': company,
        }
        car = Car.objects.create(**payload)
        self.assertEqual(car.description, payload['description'])


class TestCompany(TestCase):
    def create_company(self):
        payload = {
            'title': 'wdwdwd'
        }
        company = Company.objects.create(**payload)
        self.assertEqual(company.title, payload['title'])

    def test_company_update(self):
        company_title = 'title'
        payload = {
            'title': 'company_title'
        }
        company = Company.objects.create(**payload)
        company.title = company_title
        company.save()
        company.refresh_from_db()
        self.assertEqual(company.title, company_title)



