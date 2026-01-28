"""
User URL routes.
"""
from django.urls import path

from .views import LoginView, RegisterView, TokenRefreshAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshAPIView.as_view(), name='token-refresh'),
]
