"""
Ticket models.
"""
import uuid

from django.conf import settings
from django.db import models


class TicketStatus(models.TextChoices):
    """Ticket status choices."""
    NEW = 'new', 'Новая'
    IN_PROGRESS = 'in_progress', 'В работе'
    COMPLETED = 'completed', 'Выполнена'
    REJECTED = 'rejected', 'Отклонена'


class TicketPriority(models.TextChoices):
    """Ticket priority choices."""
    LOW = 'low', 'Низкий'
    MEDIUM = 'medium', 'Средний'
    HIGH = 'high', 'Высокий'


class Ticket(models.Model):
    """Helpdesk ticket model."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.NEW,
        db_index=True,
    )
    priority = models.CharField(
        'Приоритет',
        max_length=20,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM,
        db_index=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tickets',
        verbose_name='Создал',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_tickets',
        verbose_name='Исполнитель',
        null=True,
        blank=True,
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='distributed_tickets',
        verbose_name='Назначил',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['created_by', 'status']),
            models.Index(fields=['assigned_to', 'status']),
        ]

    def __str__(self) -> str:
        return f'{self.title} ({self.get_status_display()})'
