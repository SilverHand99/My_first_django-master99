from django.contrib.auth.models import User, Group
from rest_framework import serializers
from my_projekt.models import Car, Category, Cart, CartContent, User_Profile, Car_Complekt, Company


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


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

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
    user = UserSerializer()

    class Meta:
        model = User_Profile
        fields = '__all__'


class ComplektSerializer(serializers.ModelSerializer):
    items = CarSerializer(many=True)
    depth = 1

    class Meta:
        model = Car_Complekt
        fields = '__all__'


class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'wrong_password'})
        user.set_password(password)
        user.save()
        return user


