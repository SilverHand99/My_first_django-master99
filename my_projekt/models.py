from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название Категории', help_text='введите название Категория')
    description = models.CharField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Car(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, verbose_name='Картинка')
    title = models.CharField(max_length=100, verbose_name='Название', help_text='введите название')
    categories = models.ManyToManyField(Category, verbose_name='категория', related_name='categories')
    description = models.CharField(max_length=500, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='цена')

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


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='аватарка')

    # avatar
    def __str__(self):
        return self.user.username
