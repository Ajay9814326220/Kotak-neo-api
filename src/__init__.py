"""Kotak Neo API Integration Package"""

__version__ = "1.0.0"
__author__ = "Ajay9814326220"
__description__ = "Python integration for Kotak Securities Neo API"

from .kotak_client import KotakNeoClient, ApiError
from .auth import KotakAuth, AuthenticationError
from .exceptions import KotakApiException

__all__ = [
    "KotakNeoClient",
    "KotakAuth",
    "ApiError",
    "AuthenticationError",
    "KotakApiException"
]
