from django.urls import path
from .views import CheckoutAPIView, InitializePayment, VerifyPayment

urlpatterns = [
    path('', CheckoutAPIView.as_view()),
    path('pay/<int:order_id>/', InitializePayment.as_view()),
    path('verify/', VerifyPayment.as_view())
]