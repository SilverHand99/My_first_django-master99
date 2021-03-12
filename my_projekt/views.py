from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Car, CartContent, Cart
from .forms import SearchForm, LoginForm, RegisterForm
from .models import Post
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DeleteView, UpdateView


# Create your views here.
class MasterView(View):

    def get_cart_records(self, cart=None, response=None):
        cart = self.get_cart() if cart is None else cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []

        if response:
            response.set_cookie('cart_count', len(cart_records))
            return response

        return cart_records

    def get_cart(self, update_quantity=False):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except ObjectDoesNotExist:
                cart = Cart(user_id=user_id,
                            total_cost=0)
                cart.save()
        else:
            session_key = self.request.session.session_key
            self.request.session.modified = True
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                cart = Cart(session_key=session_key,
                            total_cost=0)
                cart.save()

            if self.request.user.is_authenticated:
                try:
                    cart = Cart.objects.get(session_key=session_key,
                                            total_cost=0)
                    cart.save()

                except ObjectDoesNotExist:
                    cart = Cart(session_key=session_key,
                                total_cost=0)
                    cart.save()

        return cart


def index(request):
    return render(request, 'my_index.html')


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
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
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'login.html', {'form': form})


def bay_a_car(request):
    all_cars = Car.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        search = request.POST.get('search')
        if form.is_valid() and search:
            all_cars = all_cars.filter(title__contains=search)
    else:
        form = SearchForm()

    return render(request, 'bay_tesla_cars.html',
                  {'cars': all_cars, 'form': form, 'user': request.user})


def log_out(request):
    logout(request)
    return redirect('/')


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
        car = Car.objects.get(id=request.POST.get('car_id'))
        cart = self.get_cart()
        quantity = request.POST.get('qty')
        cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=car)
        cart_content.qty = quantity
        cart_content.save()
        response = self.get_cart_records(cart, redirect('/bay_a_car/#car-{}'.format(car.id)))
        return response

    def remove(self, cart, request):
        if self.request.user.is_authenticated:
            try:
                cart = self.get_cart()
            except ObjectDoesNotExist:
                pass
            else:
                cart = Cart.objects.get(user=request.user, active=True)
                cart.delete_form_cart(cart)
            return redirect('cart')
        else:
            return redirect('cart.html')
