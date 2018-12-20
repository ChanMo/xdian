from django.contrib import admin
from .models import *

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'is_active', 'start', 'end', 'created')
    list_filter = ('is_active', 'created')
    list_per_page = 10
    search_fields = ('name',)
    fieldsets = (
            (None, {
                'fields': ('name', 'manager')
            }),
            ('位置信息', {
                'classes': ('collapse',),
                'fields': ('region', 'street', 'longitude', 'latitude'),
            }),
            ('店铺设置', {
                'classes': ('collapse',),
                'fields': ('is_active', 'start', 'end')
            })
            )


admin.site.register(Shop, ShopAdmin)
