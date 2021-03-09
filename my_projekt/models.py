from django.db import models


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
    categories = models.ManyToManyField(Category, verbose_name='категория', )
    description = models.CharField(max_length=500, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='цена')

    def get_categories(self):
        self.short_description = "Категории"
        return ', '.join([cat.title for cat in self.categories.all()])

    def __str__(self):
        return self.title


class Post(object):
    objects = None