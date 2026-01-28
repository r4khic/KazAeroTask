"""
Ticket filters for API.
"""
import django_filters

from .models import Ticket, TicketPriority, TicketStatus


class TicketFilter(django_filters.FilterSet):
    """Filter for tickets."""

    status = django_filters.ChoiceFilter(choices=TicketStatus.choices)
    priority = django_filters.ChoiceFilter(choices=TicketPriority.choices)

    class Meta:
        model = Ticket
        fields = ['status', 'priority']
