"""Kotak Neo API Integration Package"""

__version__ = "1.0.0"
__author__ = "Ajay9814326220"
__description__ = "Python integration for Kotak Securities Neo API"

from .kotak_client import KotakNeoClient
from .auth import KotakAuth

__all__ = ["KotakNeoClient", "KotakAuth"]