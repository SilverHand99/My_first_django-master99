from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.restshop.Serializers import UserSerializer, GroupSerializer, CarSerializer, CategorySerializer, CartSerializer, \
    CartContentSerializer, UserProfileSerializer, ComplektSerializer, CompanySerializer
from my_projekt.models import Car, Category, Cart, CartContent, User_Profile, Car_Complekt, Company
from rest_framework.views import APIView, Response
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# Create your views here.

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategorySet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartContentSet(viewsets.ModelViewSet):
    queryset = CartContent.objects.all()
    serializer_class = CartContentSerializer


class UserProfileListCreateView(ListCreateAPIView):
    queryset = User_Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User_Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ComplektView(RetrieveUpdateDestroyAPIView):
    queryset = Car_Complekt.objects.all()
    serializer_class = ComplektSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanySet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
