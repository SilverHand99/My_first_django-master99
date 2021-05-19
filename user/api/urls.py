from django.urls import include, path
from rest_framework import routers
from api.restshop import views
from api.restshop.views import RegisterView

app_name = 'user'

urlpatterns = [
   path('register', RegisterView.as_view()),
]