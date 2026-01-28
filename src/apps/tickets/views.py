"""
Ticket API views.
"""
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import TicketFilter
from .permissions import (
    CanAssignTicket,
    CanCompleteOrRejectTicket,
    CanCreateTicket,
    CanViewAllTickets,
    CanViewAssignedTickets,
    CanViewOwnTickets,
)
from .selectors import get_all_tickets, get_tickets_assigned_to, get_tickets_by_creator
from .serializers import (
    TicketAssignSerializer,
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
)
from .services import assign_ticket, complete_ticket, create_ticket, reject_ticket


class MyTicketsView(APIView):
    """API view for applicant's own tickets."""

    permission_classes = [CanViewOwnTickets]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter

    @extend_schema(
        responses={200: TicketListSerializer(many=True)},
        summary='Мои заявки',
        description='Получение списка заявок, созданных текущим пользователем (заявителем)',
    )
    def get(self, request: Request) -> Response:
        """
        Get current user's tickets.

        Args:
            request: HTTP request

        Returns:
            Response with list of user's tickets
        """
        tickets = get_tickets_by_creator(request.user)

        # Apply filters
        filterset = TicketFilter(request.query_params, queryset=tickets)
        if filterset.is_valid():
            tickets = filterset.qs

        serializer = TicketListSerializer(tickets, many=True)
        return Response(serializer.data)


@extend_schema_view(
    get=extend_schema(
        responses={200: TicketListSerializer(many=True)},
        summary='Все заявки',
        description='Получение списка всех заявок (только для оператора)',
    ),
    post=extend_schema(
        request=TicketCreateSerializer,
        responses={201: TicketDetailSerializer},
        summary='Создать заявку',
        description='Создание новой заявки (только для заявителя)',
    ),
)
class TicketListCreateView(APIView):
    """API view for listing and creating tickets."""

    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter

    def get_permissions(self):
        """Return permissions based on HTTP method."""
        if self.request.method == 'POST':
            return [CanCreateTicket()]
        return [CanViewAllTickets()]

    def get(self, request: Request) -> Response:
        """
        Get all tickets (operator only).

        Args:
            request: HTTP request

        Returns:
            Response with list of all tickets
        """
        tickets = get_all_tickets()

        # Apply filters
        filterset = TicketFilter(request.query_params, queryset=tickets)
        if filterset.is_valid():
            tickets = filterset.qs

        serializer = TicketListSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Create a new ticket (applicant only).

        Args:
            request: HTTP request with ticket data

        Returns:
            Response with created ticket data
        """
        serializer = TicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = create_ticket(
            created_by=request.user,
            **serializer.validated_data,
        )

        return Response(
            TicketDetailSerializer(ticket).data,
            status=status.HTTP_201_CREATED,
        )


class TicketAssignView(APIView):
    """API view for assigning ticket to executor."""

    permission_classes = [CanAssignTicket]

    @extend_schema(
        request=TicketAssignSerializer,
        responses={200: TicketDetailSerializer},
        summary='Назначить исполнителя',
        description='Назначение исполнителя на заявку (только для оператора)',
    )
    def patch(self, request: Request, ticket_id: str) -> Response:
        """
        Assign executor to ticket.

        Args:
            request: HTTP request with executor ID
            ticket_id: Ticket's UUID

        Returns:
            Response with updated ticket data
        """
        serializer = TicketAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = assign_ticket(
            ticket_id=ticket_id,
            executor_id=serializer.validated_data['assigned_to'],
            assigned_by=request.user,
        )

        return Response(TicketDetailSerializer(ticket).data)


class AssignedTicketsView(APIView):
    """API view for executor's assigned tickets."""

    permission_classes = [CanViewAssignedTickets]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter

    @extend_schema(
        responses={200: TicketListSerializer(many=True)},
        summary='Назначенные мне заявки',
        description='Получение списка заявок, назначенных текущему пользователю (исполнителю)',
    )
    def get(self, request: Request) -> Response:
        """
        Get tickets assigned to current user.

        Args:
            request: HTTP request

        Returns:
            Response with list of assigned tickets
        """
        tickets = get_tickets_assigned_to(request.user)

        # Apply filters
        filterset = TicketFilter(request.query_params, queryset=tickets)
        if filterset.is_valid():
            tickets = filterset.qs

        serializer = TicketListSerializer(tickets, many=True)
        return Response(serializer.data)


class TicketCompleteView(APIView):
    """API view for completing a ticket."""

    permission_classes = [CanCompleteOrRejectTicket]

    @extend_schema(
        responses={200: TicketDetailSerializer},
        summary='Завершить заявку',
        description='Отметить заявку как выполненную (только для исполнителя)',
    )
    def patch(self, request: Request, ticket_id: str) -> Response:
        """
        Complete a ticket.

        Args:
            request: HTTP request
            ticket_id: Ticket's UUID

        Returns:
            Response with updated ticket data
        """
        ticket = complete_ticket(
            ticket_id=ticket_id,
            executor=request.user,
        )

        return Response(TicketDetailSerializer(ticket).data)


class TicketRejectView(APIView):
    """API view for rejecting a ticket."""

    permission_classes = [CanCompleteOrRejectTicket]

    @extend_schema(
        responses={200: TicketDetailSerializer},
        summary='Отклонить заявку',
        description='Отклонить заявку (только для исполнителя)',
    )
    def patch(self, request: Request, ticket_id: str) -> Response:
        """
        Reject a ticket.

        Args:
            request: HTTP request
            ticket_id: Ticket's UUID

        Returns:
            Response with updated ticket data
        """
        ticket = reject_ticket(
            ticket_id=ticket_id,
            executor=request.user,
        )

        return Response(TicketDetailSerializer(ticket).data)
