from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('shop', 'name', 'sort', 'is_active')
    list_filter = ('is_active',)
    list_per_page = 10
    search_fields = ('name', 'shop__name')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'is_active', 'created')
    list_filter = ('is_active',)
    list_per_page = 10
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
