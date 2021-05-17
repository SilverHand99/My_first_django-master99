from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill


class Company(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название Категории', help_text='введите название Категория')
    description = models.CharField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Car(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, verbose_name='Картинка', null=True)
    title = models.CharField(max_length=100, verbose_name='Название', help_text='введите название')
    categories = models.ManyToManyField(Category, verbose_name='категория', related_name='categories', blank=True, null=True)
    description = models.CharField(max_length=500, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='цена')
    company = models.ForeignKey(Company,  verbose_name='компания', on_delete=models.SET_NULL, null=True,)

    def get_categories(self):
        self.short_description = "Категории"
        return ', '.join([cat.title for cat in self.categories.all()])

    def __str__(self):
        return self.title


class Post(object):
    objects = None


class Cart(models.Model):
    session_key = models.CharField(max_length=999, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_cost = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    def get_total(self):
        items = CartContent.objects.filter(cart=self.id)
        total = 0
        for item in items:
            total += item.product.price * item.qty
        return total

    def get_cart_content(self):
        return CartContent.objects.filter(cart=self.id)


class CartContent(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Car, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(null=True)


class Location(models.Model):
    country = models.CharField(max_length=250)

    def __str__(self):
        return self.country


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='аватарка')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    # avatar
    def __str__(self):
        return self.user.username


class Car_Complekt(models.Model):
    items = models.ManyToManyField(Car, verbose_name='товары', related_name='cars', blank=True)
    sell = models.PositiveIntegerField(default=0, null=True)
    total_before = models.PositiveIntegerField(null=True, default=0)
    total_after = models.PositiveIntegerField(null=True, default=0)

    def get_car(self):
        self.short_description = "car"
        return ', '.join([cat.title for cat in self.items.all()])

    def __str__(self):
        return str(self.id)

    def get_total(self):
        sell = Car_Complekt.sell
        items = Car.objects.filter(Car_Complekt=self.id)
        total = 0
        for item in items:
            total += item.product.price % 100 * sell
        return total
