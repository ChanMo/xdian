from rest_framework import serializers
from .models import *

class WxaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wxa
        fields = ('user', 'nickname', 'avatar')
