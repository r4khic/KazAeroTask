"""
User serializers.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'role',
        ]

    def validate(self, attrs: dict) -> dict:
        """Validate that passwords match."""
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Пароли не совпадают.'
            })
        return attrs

    def create(self, validated_data: dict) -> User:
        """Create user with hashed password."""
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'created_at']
        read_only_fields = ['id', 'email', 'role', 'created_at']


class UserShortSerializer(serializers.ModelSerializer):
    """Short serializer for user in nested representations."""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']
