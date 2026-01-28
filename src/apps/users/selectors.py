"""
User database query selectors.
"""
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from .models import UserRole

User = get_user_model()


def get_executors() -> QuerySet:
    """
    Get all active executors.

    Returns:
        QuerySet of active users with executor role
    """
    return User.objects.filter(
        role=UserRole.EXECUTOR,
        is_active=True,
    )


def get_user_by_id(user_id: int) -> User | None:
    """
    Get user by ID.

    Args:
        user_id: User's ID

    Returns:
        User instance or None if not found
    """
    return User.objects.filter(id=user_id).first()
