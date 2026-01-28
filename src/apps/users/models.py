"""
User models.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserRole(models.TextChoices):
    """User role choices."""
    APPLICANT = 'applicant', 'Заявитель'
    OPERATOR = 'operator', 'Оператор'
    EXECUTOR = 'executor', 'Исполнитель'


class UserManager(BaseUserManager):
    """Custom user manager using email as username."""

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields
    ) -> 'User':
        """
        Create and return a regular user.

        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for user model

        Returns:
            Created user instance
        """
        if not email:
            raise ValueError('Email обязателен для создания пользователя')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields
    ) -> 'User':
        """
        Create and return a superuser.

        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for user model

        Returns:
            Created superuser instance
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.OPERATOR)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email as username."""

    email = models.EmailField(
        'Email',
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует.',
        },
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.APPLICANT,
    )
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Сотрудник', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        """Return user's full name."""
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    @property
    def is_applicant(self) -> bool:
        """Check if user is an applicant."""
        return self.role == UserRole.APPLICANT

    @property
    def is_operator(self) -> bool:
        """Check if user is an operator."""
        return self.role == UserRole.OPERATOR

    @property
    def is_executor(self) -> bool:
        """Check if user is an executor."""
        return self.role == UserRole.EXECUTOR
