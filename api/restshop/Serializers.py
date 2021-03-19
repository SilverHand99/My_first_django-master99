from django.contrib.auth.models import User, Group
from rest_framework import serializers
from my_projekt.models import Car, Category


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['description', 'title', 'id']


class CarSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    depth = 2

    class Meta:
        model = Car
        fields = ['url', 'title', 'price', 'description', 'categories', 'id']
