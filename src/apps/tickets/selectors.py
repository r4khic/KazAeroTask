"""
Ticket database query selectors.
"""
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from .models import Ticket

User = get_user_model()


def get_all_tickets() -> QuerySet[Ticket]:
    """
    Get all tickets with related users.

    Returns:
        QuerySet of all tickets with optimized queries
    """
    return Ticket.objects.select_related(
        'created_by',
        'assigned_to',
        'assigned_by',
    ).all()


def get_tickets_by_creator(user: User) -> QuerySet[Ticket]:
    """
    Get tickets created by specific user.

    Args:
        user: User who created the tickets

    Returns:
        QuerySet of tickets created by the user
    """
    return Ticket.objects.select_related(
        'created_by',
        'assigned_to',
        'assigned_by',
    ).filter(created_by=user)


def get_tickets_assigned_to(user: User) -> QuerySet[Ticket]:
    """
    Get tickets assigned to specific user.

    Args:
        user: User who is assigned to the tickets

    Returns:
        QuerySet of tickets assigned to the user
    """
    return Ticket.objects.select_related(
        'created_by',
        'assigned_to',
        'assigned_by',
    ).filter(assigned_to=user)


def get_ticket_by_id(ticket_id: UUID) -> Ticket | None:
    """
    Get ticket by ID with related users.

    Args:
        ticket_id: Ticket's UUID

    Returns:
        Ticket instance or None if not found
    """
    return Ticket.objects.select_related(
        'created_by',
        'assigned_to',
        'assigned_by',
    ).filter(id=ticket_id).first()
