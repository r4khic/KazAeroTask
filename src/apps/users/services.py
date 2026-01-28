"""
User business logic services.
"""
from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
    *,
    email: str,
    password: str,
    first_name: str = '',
    last_name: str = '',
    role: str = 'applicant',
) -> User:
    """
    Create a new user.

    Args:
        email: User's email address
        password: User's password
        first_name: User's first name
        last_name: User's last name
        role: User's role (applicant, operator, executor)

    Returns:
        Created user instance
    """
    return User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role,
    )
