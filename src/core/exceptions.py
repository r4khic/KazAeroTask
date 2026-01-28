"""
Custom exceptions for business logic errors.
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class ApplicationError(APIException):
    """Base exception for application errors."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Произошла ошибка приложения.'
    default_code = 'application_error'


class PermissionDeniedError(ApplicationError):
    """Exception for permission denied errors."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'У вас нет прав для выполнения этого действия.'
    default_code = 'permission_denied'


class NotFoundError(ApplicationError):
    """Exception for not found errors."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Запрашиваемый ресурс не найден.'
    default_code = 'not_found'


class ValidationError(ApplicationError):
    """Exception for validation errors."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ошибка валидации данных.'
    default_code = 'validation_error'


class TicketAlreadyAssignedError(ApplicationError):
    """Exception when ticket is already assigned."""
    default_detail = 'Заявка уже назначена исполнителю.'
    default_code = 'ticket_already_assigned'


class TicketNotAssignedError(ApplicationError):
    """Exception when ticket is not assigned yet."""
    default_detail = 'Заявка ещё не назначена исполнителю.'
    default_code = 'ticket_not_assigned'


class TicketWrongStatusError(ApplicationError):
    """Exception when ticket has wrong status for operation."""
    default_detail = 'Недопустимый статус заявки для данной операции.'
    default_code = 'ticket_wrong_status'


class TicketNotYoursError(PermissionDeniedError):
    """Exception when trying to modify someone else's ticket."""
    default_detail = 'Эта заявка не назначена вам.'
    default_code = 'ticket_not_yours'
