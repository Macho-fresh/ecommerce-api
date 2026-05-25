from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializer import CartSerializer, CartItemSerializer
from products.models import Product

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user = self.request.user)

        return cart
    
class AddToCart(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        product = Product.objects.get(id=product_id)
        cart,created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        serializer = CartItemSerializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class UpdateCartItemQuantity(generics.UpdateAPIView):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def put(self, request, *args, **kwargs):
#         cart_item = self.get_object()

#         quantity = request.data.get('quantity')

#         if quantity:
#             cart_item.quantity = quantity
#             cart_item.save()

#         serializer = self.get_serializer(cart_item)

#         return Response(serializer.data)

class RemoveCartItem(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]