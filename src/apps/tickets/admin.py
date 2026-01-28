"""
Ticket admin configuration.
"""
from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin configuration for Ticket model."""

    list_display = [
        'id',
        'title',
        'status',
        'priority',
        'created_by',
        'assigned_to',
        'created_at',
    ]
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description', 'created_by__email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    raw_id_fields = ['created_by', 'assigned_to', 'assigned_by']
    ordering = ['-created_at']
