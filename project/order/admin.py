from django.contrib import admin
from .models import *

class ItemInline(admin.StackedInline):
    model = Item

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'price', 'is_pay', 'created')
    list_filter = ('is_pay', 'created')
    list_per_page = 10
    inlines = [ItemInline]


admin.site.register(Order, OrderAdmin)
