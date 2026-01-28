"""
User API views.
"""
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserRegisterSerializer, UserSerializer


class RegisterView(APIView):
    """API view for user registration."""

    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: UserSerializer},
        summary='Регистрация пользователя',
        description='Создание нового пользователя в системе',
    )
    def post(self, request: Request) -> Response:
        """
        Register a new user.

        Args:
            request: HTTP request with user data

        Returns:
            Response with created user data
        """
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """API view for JWT token obtaining (login)."""

    @extend_schema(
        summary='Авторизация',
        description='Получение JWT токенов по email и паролю',
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TokenRefreshAPIView(TokenRefreshView):
    """API view for JWT token refresh."""

    @extend_schema(
        summary='Обновление токена',
        description='Обновление access токена по refresh токену',
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
