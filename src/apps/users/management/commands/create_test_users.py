"""
Management command to create test users.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.users.models import UserRole

User = get_user_model()


class Command(BaseCommand):
    """Create test users for each role."""

    help = 'Creates test users for applicant, operator, and executor roles'

    def handle(self, *args, **options) -> None:
        """Execute the command."""
        test_users = [
            {
                'email': 'applicant@test.com',
                'password': 'testpass123',
                'first_name': 'Иван',
                'last_name': 'Заявителев',
                'role': UserRole.APPLICANT,
            },
            {
                'email': 'operator@test.com',
                'password': 'testpass123',
                'first_name': 'Мария',
                'last_name': 'Операторова',
                'role': UserRole.OPERATOR,
            },
            {
                'email': 'executor@test.com',
                'password': 'testpass123',
                'first_name': 'Алексей',
                'last_name': 'Исполнителев',
                'role': UserRole.EXECUTOR,
            },
        ]

        for user_data in test_users:
            email = user_data['email']
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {email} already exists, skipping')
                )
                continue

            User.objects.create_user(**user_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created user: {email} ({user_data["role"]})')
            )

        self.stdout.write(self.style.SUCCESS('Test users creation completed'))
