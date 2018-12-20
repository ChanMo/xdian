from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from shop.models import Shop
from .models import *
from .serializers import *

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.queryset
        shop_id = self.request.query_params.get('shop', 0)
        shop = get_object_or_404(Shop, pk=shop_id)
        queryset = queryset.filter(category__shop=shop)
        serializer = ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
