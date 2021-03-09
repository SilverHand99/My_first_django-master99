from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Car
from .forms import SearchForm, LoginForm, RegisterForm
from .models import Post


# Create your views here.


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
