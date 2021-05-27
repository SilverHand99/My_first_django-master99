from django.urls import path, include
from my_projekt import views
from django.conf import settings
from django.contrib.auth import logout
from my_projekt import translation

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.log_in, name="login"),
    path('register/', views.register, name="register"),
    path('bay_a_car/', views.bay_a_car.as_view(), name='bay'),
    path('logout/', views.log_out, name="logout"),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', views.oauth, name="register"),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('tesla_modelX/', views.index2, name='Model_X'),
    path('delete_cart/', views.delete_content.as_view(), name='delete'),
    path('profile/', views.user_avatar, name='avatars'),
    path('change_profile/', views.change_profile, name='change_profile'),
    path('complekt/', views.car_complekt, name='complekt'),
    path('car_pagination/', views.ContactListView, name='pagination'),
    path('i18n/', translation.set_language, name='set_language')
]
