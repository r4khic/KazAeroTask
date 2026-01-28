"""
Ticket permission classes.
"""
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.users.models import UserRole

from .models import Ticket


class CanCreateTicket(BasePermission):
    """Permission for creating tickets (applicant only)."""

    message = 'Только заявители могут создавать заявки.'

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user can create tickets."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.APPLICANT
        )


class CanViewAllTickets(BasePermission):
    """Permission for viewing all tickets (operator only)."""

    message = 'Только операторы могут просматривать все заявки.'

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user can view all tickets."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.OPERATOR
        )


class CanAssignTicket(BasePermission):
    """Permission for assigning tickets (operator only)."""

    message = 'Только операторы могут назначать исполнителей.'

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user can assign tickets."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.OPERATOR
        )


class CanViewAssignedTickets(BasePermission):
    """Permission for viewing assigned tickets (executor only)."""

    message = 'Только исполнители могут просматривать назначенные им заявки.'

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user can view assigned tickets."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.EXECUTOR
        )


class CanCompleteOrRejectTicket(BasePermission):
    """Permission for completing or rejecting tickets (executor only)."""

    message = 'Только исполнители могут завершать или отклонять заявки.'

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user can complete or reject tickets."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.EXECUTOR
        )

    def has_object_permission(self, request: Request, view: APIView, obj: Ticket) -> bool:
        """Check if user is assigned to this ticket."""
        return obj.assigned_to == request.user


class CanViewOwnTickets(BasePermission):
    """Permission for viewing own tickets (applicant only)."""

    message = 'Только заявители могут просматривать свои заявки.'

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user can view own tickets."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.APPLICANT
        )
