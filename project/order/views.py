from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
