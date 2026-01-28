"""
Ticket business logic services.
"""
from uuid import UUID

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.users.selectors import get_user_by_id
from core.exceptions import (
    NotFoundError,
    TicketAlreadyAssignedError,
    TicketNotAssignedError,
    TicketNotYoursError,
    TicketWrongStatusError,
)

from .models import Ticket, TicketStatus
from .selectors import get_ticket_by_id

User = get_user_model()


def create_ticket(
    *,
    title: str,
    description: str,
    priority: str,
    created_by: User,
) -> Ticket:
    """
    Create a new ticket.

    Args:
        title: Ticket title
        description: Ticket description
        priority: Ticket priority (low, medium, high)
        created_by: User creating the ticket

    Returns:
        Created ticket instance
    """
    return Ticket.objects.create(
        title=title,
        description=description,
        priority=priority,
        created_by=created_by,
    )


def assign_ticket(
    *,
    ticket_id: UUID,
    executor_id: int,
    assigned_by: User,
) -> Ticket:
    """
    Assign ticket to an executor.

    Args:
        ticket_id: Ticket's UUID
        executor_id: Executor user's ID
        assigned_by: Operator user assigning the ticket

    Returns:
        Updated ticket instance

    Raises:
        NotFoundError: If ticket or executor not found
        TicketAlreadyAssignedError: If ticket is already assigned
        TicketWrongStatusError: If ticket status is not 'new'
    """
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise NotFoundError('Заявка не найдена.')

    if ticket.status != TicketStatus.NEW:
        raise TicketWrongStatusError(
            'Назначить исполнителя можно только для новых заявок.'
        )

    if ticket.assigned_to:
        raise TicketAlreadyAssignedError()

    executor = get_user_by_id(executor_id)
    if not executor:
        raise NotFoundError('Исполнитель не найден.')

    ticket.assigned_to = executor
    ticket.assigned_by = assigned_by
    ticket.status = TicketStatus.IN_PROGRESS
    ticket.save(update_fields=['assigned_to', 'assigned_by', 'status', 'updated_at'])

    return ticket


def complete_ticket(
    *,
    ticket_id: UUID,
    executor: User,
) -> Ticket:
    """
    Mark ticket as completed.

    Args:
        ticket_id: Ticket's UUID
        executor: User completing the ticket

    Returns:
        Updated ticket instance

    Raises:
        NotFoundError: If ticket not found
        TicketNotAssignedError: If ticket is not assigned
        TicketNotYoursError: If ticket is not assigned to the executor
        TicketWrongStatusError: If ticket status is not 'in_progress'
    """
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise NotFoundError('Заявка не найдена.')

    if not ticket.assigned_to:
        raise TicketNotAssignedError()

    if ticket.assigned_to != executor:
        raise TicketNotYoursError()

    if ticket.status != TicketStatus.IN_PROGRESS:
        raise TicketWrongStatusError(
            'Завершить можно только заявки в статусе "В работе".'
        )

    ticket.status = TicketStatus.COMPLETED
    ticket.completed_at = timezone.now()
    ticket.save(update_fields=['status', 'completed_at', 'updated_at'])

    return ticket


def reject_ticket(
    *,
    ticket_id: UUID,
    executor: User,
) -> Ticket:
    """
    Reject a ticket.

    Args:
        ticket_id: Ticket's UUID
        executor: User rejecting the ticket

    Returns:
        Updated ticket instance

    Raises:
        NotFoundError: If ticket not found
        TicketNotAssignedError: If ticket is not assigned
        TicketNotYoursError: If ticket is not assigned to the executor
        TicketWrongStatusError: If ticket status is not 'in_progress'
    """
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise NotFoundError('Заявка не найдена.')

    if not ticket.assigned_to:
        raise TicketNotAssignedError()

    if ticket.assigned_to != executor:
        raise TicketNotYoursError()

    if ticket.status != TicketStatus.IN_PROGRESS:
        raise TicketWrongStatusError(
            'Отклонить можно только заявки в статусе "В работе".'
        )

    ticket.status = TicketStatus.REJECTED
    ticket.completed_at = timezone.now()
    ticket.save(update_fields=['status', 'completed_at', 'updated_at'])

    return ticket
