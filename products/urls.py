from django.urls import path
from .views import ProductView, ProductDetailAPIView

urlpatterns = [
    path('product/', ProductView.as_view()),
    path('product/<int:pk>/', ProductDetailAPIView.as_view())

]