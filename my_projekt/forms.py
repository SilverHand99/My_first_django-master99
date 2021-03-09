from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, help_text='Обязательное поле')
    email = forms.CharField(widget=forms.EmailInput, max_length=100, help_text='Обязательное поле.', required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=100, help_text='')
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=100, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100,
                            help_text='')
    password = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
    search = forms.CharField(required=False, label='', )
