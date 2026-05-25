from django.shortcuts import render
from rest_framework import generics
from .serializer import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer