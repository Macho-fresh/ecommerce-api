from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = 'product.name', read_only = True)
    product_price = serializers.DecimalField(source = 'products.price', read_only = True, max_digits = 10, decimal_places = 2)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'quantity',
            'total_price'
        ]

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only = True)
    cart_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'items',
            'cart_total',
            'created_at'
        ]

    def get_cart_total(self, obj):
        total = 0

        for item in obj.items.all():
            total += item.product.price * item.quantity

        return total