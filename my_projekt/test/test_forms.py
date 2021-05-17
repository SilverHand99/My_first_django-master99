from django.test import TestCase

from my_projekt.forms import SearchForm, RegisterForm, EditForm


class RegisterFormTest(TestCase):
    def test_register_success(self):
        data = {
            'email': '1233141',
            'username': 'dsdwd',
            'password1': '1234',
            'password2': '1234',
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_register_passwords_compare_f1ail(self):
        data = {
            'email': 'addd21@dsdw.dad',
            'username': 'addd21',
            'password1': '16_cry_baby',
            'password2': '16_cry_baby',
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_register_passwords_compare_fail(self):
        data = {
            'email': 'addd21@dsdw.dad',
            'username': 'addd21',
            'password1': '16_cry_baby',
            'password2': '14_cry_baby',
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())


class EditFormTest(TestCase):
    def test_edit_username_form_true(self):
        data = {
            'username': 'add123',
            'email': 'dasd@dad.com',
            'last_name': 'addd123213',
            'first_name': 'addd21424',

        }
        form = EditForm(data=data)
        self.assertTrue(form.is_valid())

    def test_edit_username_form_false(self):
        data = {
            'username': 'add123',
            'email': 'das',
            'last_name': 'addd123213',
            'first_name': 'addd21424',
            }
        print(data)
        form = EditForm(data=data)
        self.assertTrue(form.is_valid())

