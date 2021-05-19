from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework import permissions
from api.restshop.Serializers import UserSerializer, GroupSerializer, CarSerializer, CategorySerializer, CartSerializer, \
    CartContentSerializer, UserProfileSerializer, ComplektSerializer, CompanySerializer, UserRegisterSerializer
from my_projekt.models import Car, Category, Cart, CartContent, User_Profile, Car_Complekt, Company
from rest_framework.views import APIView, Response
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully register of user'
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)
