from django.test import TestCase
from my_projekt.models import Category, Company, Car, Cart, CartContent, User_Profile, User, Location


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
        self.company = Company.objects.create(title='zxczxc')
        payload = {
            'title': 'electro car',
            'description': 'dawdasdw',
            'price': 3412341,
            'company': self.company,
        }
        car = Car.objects.create(**payload)

        self.assertEqual(car.description, payload['description'])

    def test_update_car(self):
        self.company = Company.objects.create(title='zxczxc')
        new_car = 'new test title'
        payload = {
            'title': 'electro car',
            'description': 'dawdasdw',
            'price': 3412341,
            'company': self.company,
        }
        car = Car.objects.create(**payload)
        car.title = new_car
        car.save()
        car.refresh_from_db()
        self.assertEqual(car.title, new_car)

    def test_delete_car(self):
        self.company = Company.objects.create(title='zxczxc')
        payload = {
            'title': 'electro car',
            'description': 'dawdasdw',
            'price': 3412341,
            'company': self.company,
        }
        car = Car.objects.create(**payload)
        pk = car.pk
        car.delete()
        with self.assertRaises(Car.DoesNotExist):
            car = Car.objects.get(pk=pk)


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

    def test_create_cart(self):
        self.location = Location.objects.create(country='russia')
        payload = {
            'description': 'dwdwdwd',
            'location': self.location
        }
        profile = User_Profile.objects.create(**payload)
        self.assertEqual(profile.description, payload['description'])

    def test_user_profile_update(self):
        self.location = Location.objects.create(country='russia')
        profile_title = 'title'
        payload = {
            'description': 'dwdwdwd',
            'location': self.location
        }
        profile = User_Profile.objects.create(**payload)
        profile.title = profile_title
        profile.save()
        profile.refresh_from_db()
        self.assertEqual(profile.title, profile_title)

    def test_delete_profile(self):
        self.location = Location.objects.create(country='russia')
        payload = {
            'description': 'dwdwdwd',
            'location': self.location
        }
        profile = User_Profile.objects.create(**payload)
        pk = profile.pk
        profile.delete()
        with self.assertRaises(User_Profile.DoesNotExist):
            profile = User_Profile.objects.get(pk=pk)


class TestCart(TestCase):
    def test_create_cart(self):
        payload = {
            'total_cost': 12412412,
            'session_key': 'gfd6576588'
        }
        cart = Cart.objects.create(**payload)
        self.assertEqual(cart.total_cost, payload['total_cost'])

    def test_cart_update(self):
        cart_cost = 12412443543
        payload = {
            'total_cost': 12412412,
            'session_key': 'gfd6576588'
        }
        cart = Cart.objects.create(**payload)
        cart.total_cost = cart_cost
        cart.save()
        cart.refresh_from_db()
        self.assertEqual(cart.total_cost, cart_cost)

    def test_delete_profile(self):
        payload = {
            'total_cost': 12412412,
            'session_key': 'gfd6576588'
        }
        cart = Cart.objects.create(**payload)
        pk = cart.pk
        cart.delete()
        with self.assertRaises(Cart.DoesNotExist):
            cart = Cart.objects.get(pk=pk)


class TestContent(TestCase):
    def test_create_content(self):
        self.car = Car.objects.create(title='dsdwddawd', price=124124, description='dwdwdwd')
        self.cart = Cart.objects.create(session_key='ddsfwd12412', total_cost=124121)
        payload = {
            'product': self.car,
            'cart': self.cart
        }
        content = CartContent.objects.create(**payload)
        self.assertEqual(content.product, payload['product'])

    def test_content_update(self):
        qty_cost = 124
        self.car = Car.objects.create(title='dsdwddawd', price=124124, description='dwdwdwd')
        self.cart = Cart.objects.create(session_key='ddsfwd12412', total_cost=124121)
        payload = {
            'product': self.car,
            'cart': self.cart,
            'qty': 12
        }
        content = CartContent.objects.create(**payload)
        content.total_cost = qty_cost
        content.save()
        content.refresh_from_db()
        self.assertEqual(content.total_cost, qty_cost)

    def test_delete_delete(self):
        self.car = Car.objects.create(title='dsdwddawd', price=124124, description='dwdwdwd')
        self.cart = Cart.objects.create(session_key='ddsfwd12412', total_cost=124121)
        payload = {
            'product': self.car,
            'cart': self.cart
        }
        content = CartContent.objects.create(**payload)
        pk = content.pk
        content.delete()
        with self.assertRaises(CartContent.DoesNotExist):
            content = CartContent.objects.get(pk=pk)
