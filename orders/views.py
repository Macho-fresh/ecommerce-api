from django.shortcuts import render


from .models import Order, OrderItem, Payment
from django.conf import settings
from cart.models import Cart
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
import uuid

def create_order_from_cart(user):
    cart = Cart.objects.get(user=user)

    if not cart.items.exists():
        raise Exception("Cart is empty")

    
    order = Order.objects.create(user=user)

    total = 0

    
    for item in cart.items.all():

        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )

        total += item.product.price * item.quantity

        
        
  
    
    order.total_price = total
    order.save()

    
    

    return order


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = create_order_from_cart(request.user)

        return Response({
            "message": "Order created",
            "order_id": order.id,
            "total": order.total_price
        })

class InitializePayment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id = order_id, user = request.user)
        reference = str(uuid.uuid4())
        
        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            reference=reference
        )

        url = "https://api.paystack.co/transaction/initialize"

        headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
        }

        data = {
            'email': request.user.email,
            'amount': int(order.total_price * 100),
            'reference' : reference,
            "callback_url": "http://127.0.0.1:8000/api/orders/verify/"  
        }

        response = requests.post(url,json=data, headers=headers)
        response_data = response.json()
        return Response(response_data)

class VerifyPayment(APIView):
    def get(self, request):
        reference = request.GET.get('reference')
        url = f"https://api.paystack.co/transaction/verify/{reference}"

        headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }

        response = requests.get(url, headers=headers)

        response_data = response.json()
        cart = Cart.objects.get(user=request.user)
        print(response_data['status'])

        if response_data["status"] == True and response_data["data"]["status"] == "success":

            payment = Payment.objects.get(reference=reference)

            payment.status = "success"
            payment.save()

            order = payment.order
            order.is_paid = True
            order.save()
            
            for item in cart.items.all():
                item.product.inventory -= item.quantity
                item.product.save()

            cart.items.all().delete()

            return Response({
                "message": "Payment successful"
            })

        return Response({
            "message": "Payment failed"
        })