"""Custom Exceptions for Kotak Neo API"""


class KotakApiException(Exception):
    """Base exception for Kotak API errors"""
    pass


class ApiError(KotakApiException):
    """Raised when API request fails"""
    pass


class AuthenticationError(KotakApiException):
    """Raised when authentication fails"""
    pass
