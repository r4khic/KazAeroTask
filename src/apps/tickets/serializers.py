"""
Ticket serializers.
"""
from rest_framework import serializers

from apps.users.selectors import get_executors
from apps.users.serializers import UserShortSerializer

from .models import Ticket, TicketPriority


class TicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for ticket creation."""

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']

    def validate_priority(self, value: str) -> str:
        """Validate priority value."""
        if value not in TicketPriority.values:
            raise serializers.ValidationError(
                f'Недопустимый приоритет. Допустимые значения: {", ".join(TicketPriority.values)}'
            )
        return value


class TicketListSerializer(serializers.ModelSerializer):
    """Serializer for ticket list."""

    created_by = UserShortSerializer(read_only=True)
    assigned_to = UserShortSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'status',
            'status_display',
            'priority',
            'priority_display',
            'created_by',
            'assigned_to',
            'created_at',
        ]


class TicketDetailSerializer(serializers.ModelSerializer):
    """Serializer for ticket detail."""

    created_by = UserShortSerializer(read_only=True)
    assigned_to = UserShortSerializer(read_only=True)
    assigned_by = UserShortSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'status',
            'status_display',
            'priority',
            'priority_display',
            'created_by',
            'assigned_to',
            'assigned_by',
            'created_at',
            'updated_at',
            'completed_at',
        ]


class TicketAssignSerializer(serializers.Serializer):
    """Serializer for ticket assignment."""

    assigned_to = serializers.IntegerField()

    def validate_assigned_to(self, value: int) -> int:
        """Validate that assigned_to is an active executor."""
        executor = get_executors().filter(id=value).first()
        if not executor:
            raise serializers.ValidationError(
                'Указанный пользователь не является активным исполнителем.'
            )
        return value
