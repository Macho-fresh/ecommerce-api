from django.urls import path
from .views import CartView, AddToCart, RemoveCartItem

urlpatterns = [
    path('', CartView.as_view()),
    path('add-to-cart/', AddToCart.as_view()),
    path('remove-cart-item/<int:pk>', RemoveCartItem.as_view())
]