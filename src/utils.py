"""Utility Functions"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import pyotp

logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if log_file:
        os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format
        )


def generate_totp(secret: str) -> str:
    """Generate Time-based OTP.
    
    Args:
        secret: Base32 encoded TOTP secret from Kotak
        
    Returns:
        6-digit OTP code
        
    Raises:
        ValueError: If secret is invalid
    """
    try:
        totp = pyotp.TOTP(secret)
        return totp.now()
    except Exception as e:
        logger.error(f"Failed to generate TOTP: {e}")
        raise ValueError(f"Invalid TOTP secret: {e}")


def validate_credentials(client_code: str, mpin: str, api_key: str) -> bool:
    """Validate required credentials.
    
    Args:
        client_code: Kotak client code
        mpin: MPIN for authentication
        api_key: API key from Kotak
        
    Returns:
        True if all credentials are provided
    """
    if not all([client_code, mpin, api_key]):
        logger.error("Missing required credentials")
        return False
    return True


def mask_credential(credential: str, visible_chars: int = 4) -> str:
    """Mask sensitive credential for logging.
    
    Args:
        credential: The credential to mask
        visible_chars: Number of characters to show at end
        
    Returns:
        Masked credential string
    """
    if len(credential) <= visible_chars:
        return "*" * len(credential)
    return "*" * (len(credential) - visible_chars) + credential[-visible_chars:]


def is_token_expired(expiry_time: datetime) -> bool:
    """Check if token has expired.
    
    Args:
        expiry_time: Token expiry datetime
        
    Returns:
        True if token is expired
    """
    return datetime.now() >= expiry_time


def get_token_expiry(expires_in_seconds: int) -> datetime:
    """Calculate token expiry time.
    
    Args:
        expires_in_seconds: Seconds until token expires
        
    Returns:
        Datetime when token expires
    """
    return datetime.now() + timedelta(seconds=expires_in_seconds)


def format_response(response_data: Dict[str, Any], pretty: bool = True) -> str:
    """Format API response for display.
    
    Args:
        response_data: API response dictionary
        pretty: Pretty print JSON
        
    Returns:
        Formatted response string
    """
    import json
    if pretty:
        return json.dumps(response_data, indent=2)
    return str(response_data)


def retry_request(func, max_retries: int = 3, delay: int = 1):
    """Decorator for retrying failed requests.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        delay: Delay between retries in seconds
    """
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                    import time
                    time.sleep(delay)
                else:
                    logger.error(f"All {max_retries} attempts failed")
                    raise
    return wrapper