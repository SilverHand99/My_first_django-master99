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
    def test_create_car(self):
        payload = {
            'title': 'electro car',
            'description': 'dawdasdw',
            'price': 3412341,
        }
        car = Car.objects.create(**payload)
        self.assertEqual(car.description, payload['title', 'description', 'price'])


# class CarTest(TestCase):
#     def setUp(self):
#         car = Car.objects.create(title='Tesla', description='car')
#
#     def tearDown(self):
#         pass
#
#     @classmethod
#     def setUpTestData(cls):
#         category = Category.objects.create(description='elecrtro_car')
#
#     def test_something(self):
#         car = Car.objects.get(id=1)
#         category = Category.objects.get(id=1)
#         field_label = Category._meta.get_field('description').verbose_name
#         self.assertEqual(field_label, 'description')





