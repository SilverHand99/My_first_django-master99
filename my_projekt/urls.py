from django.urls import path, include
from my_projekt import views
from django.conf import settings
from django.contrib.auth import logout

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.log_in, name="login"),
    path('register/', views.register, name="register"),
    path('bay_a_car/', views.bay_a_car, name='bay'),
    path('logout/', views.log_out, name="logout"),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', views.oauth, name="register"),
    path('cart/', views.CartView.as_view(), name='cart'),
]
