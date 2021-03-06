from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from my_projekt.models import Car, CartContent, Cart, User_Profile, Car_Complekt
from my_projekt.forms import SearchForm, LoginForm, RegisterForm, ProfileChange
from my_projekt.models import Post
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django.core.paginator import Paginator
from my_projekt.models import Car
from django.db.models import Q
from django.core import serializers
from api.restshop.Serializers import CartContentSerializer
import json


class ContactListView(ListView):
    paginate_by = 5
    model = Car


def listing(request):
    contact_list = Car.objects.all()
    paginator = Paginator(contact_list, 25)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'car_list.html', {'page_obj': page_obj})


# Create your views here.

class MasterView(View):

    def get_cart_records(self, cart=None, response=None, ):
        cart = self.get_cart() if cart is None else cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []

        if response:
            response.set_cookie('cart_count', len(cart_records))
            return response

        return cart_records

    def get_cart(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            car = Car(id=self.request.COOKIES.get('car_id'))
            quantity = self.request.COOKIES.get('qty')
            # cart_content1 = CartContent(self.request.COOKIES.get('cart_content'))
            # cart_records = self.get_cart_records()
            try:
                cart = Cart.objects.get(user_id=user_id)
                # cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=car)
                # cart_content.qty = quantity
                # cart_content.save()
            except ObjectDoesNotExist:
                cart = Cart(user_id=user_id,
                            total_cost=0,
                            )
                cart.save()
                cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=car)
                cart_content.qty = quantity
                cart_content.save()
        else:
            car = Car(id=self.request.COOKIES.get('car_id'))
            quantity = self.request.COOKIES.get('qty')
            session_key = self.request.session.session_key
            self.request.session.modified = True
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=car)
                cart_content.qty = quantity
                cart_content.save()
            except ObjectDoesNotExist:
                cart = Cart(session_key=session_key,
                            total_cost=0)
                cart.save()

        return cart


def index(request):
    return render(request, 'my_index.html')


def index2(request):
    return render(request, 'tesla_model_X.html')


def log_in(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['login']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            user_id = user.id
            cart = Cart.objects.get(user_id=user_id)
            cart_records = CartContent.objects.filter(cart_id=cart.id)
            login(request, user)
            response = redirect('/')
            response.set_cookie('cart_count', len(cart_records))
            return response
        else:
            form.add_error('login', 'Bad login or password')
            form.add_error('password', 'Bad login or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'login.html', {'form': form})


class bay_a_car(MasterView):
    user_profiles = User_Profile.objects.all()
    all_cars = Car.objects.all()

    def get(self, request):
        if self.request.user.is_authenticated:
            avatars = User_Profile.objects.get(user=request.user)
        else:
            avatars = '/static/img/no_avatar.png'
        paginator = Paginator(self.all_cars, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = SearchForm()
        if self.request.user.is_authenticated:
            cart_content = self.get_cart_records()
            response = render(request, 'bay_tesla_cars.html',
                              {'cars': page_obj, 'form': form, 'user': request.user, 'avatars': avatars,
                               'page_obj': page_obj})
            response.set_cookie('cart_count', len(cart_content))
            return response
        else:
            return render(request, 'bay_tesla_cars.html',
                          {'cars': page_obj, 'form': form, 'user': request.user, 'avatars': avatars,
                           'page_obj': page_obj})

    def post(self, request):
        all_cars = Car.objects.all()
        form = SearchForm(request.POST)
        search = request.POST.get('search')
        if form.is_valid() and search:
            all_cars = all_cars.filter(
                Q(title__contains=search) | Q(description__contains=search) | Q(color__contains=search) | Q(
                    price__contains=search))
        else:
            form = SearchForm()

        if self.request.user.is_authenticated:
            avatars = User_Profile.objects.get(user=request.user)
            cart_content = self.get_cart_records()
            response = render(request, 'bay_tesla_cars.html', {'cars': all_cars, 'form': form,
                                                               'user': request.user, 'avatars': avatars})
            response.set_cookie('cart_count', len(cart_content))
            return response
        else:
            avatars = '/static/img/no_avatar.png'
            response = render(request, 'bay_tesla_cars.html', {'cars': all_cars, 'form': form,
                                                               'user': request.user, 'avatars': avatars})
            return response


def user_avatar(request):
    avatars = User_Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'avatars': avatars, })


def log_out(request):
    logout(request)
    response = redirect('/')
    response.delete_cookie('cart_count')
    return response


def oauth(request):
    context = {
        'posts': Post.objects.order_by('-date')
        if request.user.is_authenticated else []
    }

    return render(request, 'login.html', context)


class CartView(MasterView):

    def get(self, request):
        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_total = cart.get_total() if cart else 0

        context = {
            'cart_records': cart_records,
            'cart_total': cart_total,
        }
        return render(request, 'cart.html', context)

    def post(self, request):
        if self.request.user.is_authenticated:
            car = Car.objects.get(id=request.POST.get('car_id'))
            cart = self.get_cart()
            quantity = request.POST.get('qty')
            cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=car)
            cart_content.qty = quantity
            cart_content.save()
            response = self.get_cart_records(cart, redirect('/bay_a_car/#car-{}'.format(car.id), ))
            return response
        else:
            car = Car.objects.get(id=request.POST.get('car_id'))
            cart = self.get_cart()
            quantity = request.POST.get('qty')
            car_records = car.id
            records = (CartContent.objects.filter(cart_id=cart.id).values('product', 'qty', 'id'))
            rec = json.dumps(list(records))
            response = self.get_cart_records(cart, redirect('/bay_a_car/#car-{}'.format(car.id), ))
            response.set_cookie('car_id', car_records)
            response.set_cookie('qty', quantity)
            response.set_cookie('cart_content', rec)
            return response


class DeleteContent(MasterView):

    def get(self, request):
        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_records.delete()
        if self.request.user.is_authenticated:
            response = redirect('/cart/')
            response.delete_cookie('car_id')
            response.delete_cookie('qty')
            return response

        return render(request, 'cart_delete.html')


def change_profile(request):
    if request.method == 'POST':
        form = ProfileChange(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('Change_profile.html')
    else:
        form = ProfileChange()

    return render(request, 'Change_profile.html', {'form': form})


def car_complekt(request):
    all_complekt = Car_Complekt.objects.all()

    return render(request, 'car_complekt.html', {'car_complekts': all_complekt})
