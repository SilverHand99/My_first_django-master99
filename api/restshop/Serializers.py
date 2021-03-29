from django.contrib.auth.models import User, Group
from rest_framework import serializers
from my_projekt.models import Car, Category, Cart, CartContent, User_Profile


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

    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        instance = Car.objects.create(**validated_data)
        for category in categories:
            instance.categories.add(category)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        categories = validated_data.pop("categories", [])
        instance = super().update(instance, validated_data)
        for category in categories:
            instance.categories.add(category)
        instance.save()
        return instance


class CartContentSerializer(serializers.HyperlinkedModelSerializer):
    product = CarSerializer()

    class Meta:
        model = CartContent
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('product', [])
        instance = CartContent.objects.create(**validated_data)
        for product in products:
            instance.products.add(product)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        products = validated_data.pop("product", [])
        instance = super().update(instance, validated_data)
        for product in products:
            instance.categories.add(product)
        instance.save()
        return instance


class CartSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer
    depth = 1
    cart_content = CartContentSerializer(source='get_cart_content', many=True, default=None)

    class Meta:
        model = Cart
        fields = ['url', 'id', 'session_key', 'user', 'cart_content']

    def create(self, validated_data):
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User_Profile
        fields = '__all__'