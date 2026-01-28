"""
Ticket URL routes.
"""
from django.urls import path

from .views import (
    AssignedTicketsView,
    MyTicketsView,
    TicketAssignView,
    TicketCompleteView,
    TicketListCreateView,
    TicketRejectView,
)

app_name = 'tickets'

urlpatterns = [
    path('my/', MyTicketsView.as_view(), name='my-tickets'),
    path('', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('assigned/', AssignedTicketsView.as_view(), name='assigned-tickets'),
    path('<uuid:ticket_id>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
    path('<uuid:ticket_id>/complete/', TicketCompleteView.as_view(), name='ticket-complete'),
    path('<uuid:ticket_id>/reject/', TicketRejectView.as_view(), name='ticket-reject'),
]
