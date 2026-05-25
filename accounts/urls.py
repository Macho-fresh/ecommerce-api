from django.urls import path, include
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_view'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
]