from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from .models import *

class WxaAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'avatar', 'created', 'updated')
    list_per_page = 12
    list_filter = ('created', 'updated')
    search_fields = ('nickname',)
    raw_id_fields = ('user',)
    date_hierarchy = 'created'
    readonly_fields = ('openid',)


TokenAdmin.raw_id_fields = ('user',)
admin.site.register(Wxa, WxaAdmin)
