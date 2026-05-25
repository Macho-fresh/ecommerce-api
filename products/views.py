from django.shortcuts import render
from rest_framework import generics, filters
from .models import Product
from .serializer import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]

    filterset_fields = ['category', 'is_available'] 
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

