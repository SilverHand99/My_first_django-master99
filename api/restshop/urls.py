from django.urls import include, path
from rest_framework import routers
from api.restshop import views
from api.restshop.views import RegisterView


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet,)
router.register(r'groups', views.GroupViewSet)
router.register(r'cars', views.CarViewSet, basename='car')
router.register(r'categories', views.CategorySet, basename='Category')
router.register(r'CartContent', views.CartContentSet)
router.register(r'cart', views.CartSet)
router.register(r'company', views.CompanySet, basename='company')
router.register(r'kit', views.ComplektViewSet, basename='kit')
router.register(r'profile', views.UserProfileDetailView, basename='profile')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("all-profiles/", views.UserProfileListCreateView.as_view(), name="all-profiles"),
    path('register', RegisterView.as_view()),
]
