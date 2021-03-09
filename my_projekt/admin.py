from django.contrib import admin
from .models import Car, Category

admin.site.register(Category)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_categories', 'description']