"""
User permission classes.
"""
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import UserRole


class IsApplicant(BasePermission):
    """Permission class for applicant role."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user has applicant role."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.APPLICANT
        )


class IsOperator(BasePermission):
    """Permission class for operator role."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user has operator role."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.OPERATOR
        )


class IsExecutor(BasePermission):
    """Permission class for executor role."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check if user has executor role."""
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.EXECUTOR
        )
