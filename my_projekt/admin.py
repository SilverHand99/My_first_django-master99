from django.contrib import admin
from .models import Car, Category, User_Profile, Cart, CartContent

admin.site.register(Category)
admin.site.register(User_Profile)
admin.site.register(Cart)
admin.site.register(CartContent)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_categories', 'description']