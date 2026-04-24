"""API Constants and Configuration"""

import os
from enum import Enum

# API Base URLs
BASE_URL = os.getenv("KOTAK_BASE_URL", "https://api.kotaksecurities.com")
API_VERSION = os.getenv("KOTAK_API_VERSION", "v1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "sandbox")

# API Endpoints
ENDPOINTS = {
    "session": f"{BASE_URL}/trade/{API_VERSION}/session",
    "holdings": f"{BASE_URL}/trade/{API_VERSION}/portfolio/holdings",
    "positions": f"{BASE_URL}/trade/{API_VERSION}/portfolio/positions",
    "funds": f"{BASE_URL}/trade/{API_VERSION}/funds",
    "orders": f"{BASE_URL}/trade/{API_VERSION}/orders",
    "order_detail": f"{BASE_URL}/trade/{API_VERSION}/orders",
    "cancel_order": f"{BASE_URL}/trade/{API_VERSION}/orders",
}

# HTTP Headers
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Order Types
class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

# Product Types
class ProductType(str, Enum):
    CNC = "CNC"  # Cash and Carry
    MIS = "MIS"  # Margin Intraday Square Off
    NRML = "NRML"  # Normal

# Order Validity
class OrderValidity(str, Enum):
    DAY = "DAY"
    IOC = "IOC"  # Immediate or Cancel
    GTD = "GTD"  # Good Till Day
    GTC = "GTC"  # Good Till Cancel

# Price Types
class PriceType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"

# HTTP Status Codes
class HTTPStatus(int, Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

# Error Messages
ERROR_MESSAGES = {
    401: "Unauthorized - Invalid TOTP, MPIN, or Client Code",
    403: "Forbidden - Invalid PKZ or insufficient permissions",
    404: "Not Found - Resource does not exist",
    409: "Conflict - Invalid request parameters",
    500: "Server Error - Please try again later",
    503: "Service Unavailable - API is temporarily down",
}

# Timeouts
REQUEST_TIMEOUT = 30  # seconds
TOTP_EXPIRY = 30  # seconds

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/kotak_api.log")