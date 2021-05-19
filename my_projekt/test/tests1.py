from django.test import TestCase
from my_projekt.models import Category, Company, Car, Cart, CartContent, User_Profile, User


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
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title='dwdwd', description='dwdwdwd')
        Company.objects.create(title='dwdwdw')

    def test_create_car(self):
        categories = Category.objects.get(id=1)
        company = Company.objects.get(id=1)
        payload = {
            'title': 'electro car',
            'description': 'dawdasdw',
            'price': 3412341,
            'categories': [categories.id],
            'company': company.id,
        }
        car = Car.objects.create(**payload)
        company_objects_for_car = Company.objects.all()
        car.company.set(company_objects_for_car)  # Присвоение типов many-to-many напрямую недопустимо
        car.save()

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

    def test_delete_company(self):
        payload = {
            'title': 'title123',
        }
        company = Company.objects.create(**payload)
        pk = company.pk
        company.delete()
        with self.assertRaises(Company.DoesNotExist):
            company = Company.objects.get(pk=pk)


class UserProfileTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_superuser(username='Add123', password='12.34.54.56', id=1)
        payload = {
            'user': user.id,
            'description': 'dwdwdwd',
        }
        user_profile = User_Profile.objects.create(**payload)
        self.assertEqual(user_profile.description, payload['description'])