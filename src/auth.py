"""Authentication Module for Kotak Neo API"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
import requests
from requests.exceptions import RequestException

from .constants import ENDPOINTS, HTTPStatus, ERROR_MESSAGES, REQUEST_TIMEOUT
from .utils import (
    generate_totp, 
    validate_credentials, 
    is_token_expired, 
    get_token_expiry,
    mask_credential
)

logger = logging.getLogger(__name__)


class KotakAuth:
    """Handle authentication with Kotak Neo API"""
    
    def __init__(self, api_key: str, api_secret: str, client_code: str, 
                 mpin: str, pkz: str, totp_secret: str):
        """Initialize authentication.
        
        Args:
            api_key: API Key from Kotak
            api_secret: API Secret from Kotak
            client_code: Your Kotak client code
            mpin: Your MPIN
            pkz: Your PKZ (device token)
            totp_secret: TOTP secret for 2FA
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.client_code = client_code
        self.mpin = mpin
        self.pkz = pkz
        self.totp_secret = totp_secret
        
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        
        # Validate credentials
        if not validate_credentials(client_code, mpin, api_key):
            raise ValueError("Missing required credentials")
    
    def login(self) -> str:
        """Authenticate and get access token.
        
        Returns:
            Access token for API calls
            
        Raises:
            AuthenticationError: If login fails
        """
        try:
            # Generate TOTP
            totp = generate_totp(self.totp_secret)
            
            # Prepare headers
            headers = {
                "consumerKey": self.api_key,
                "Content-Type": "application/json"
            }
            
            # Prepare payload
            payload = {
                "userid": self.client_code,
                "mpin": self.mpin,
                "totp": totp,
                "pkz": self.pkz
            }
            
            logger.info(f"Attempting login for client: {mask_credential(self.client_code)}")
            
            # Make request
            response = requests.post(
                ENDPOINTS["session"],
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            # Handle response
            if response.status_code == HTTPStatus.OK:
                data = response.json()
                self.access_token = data.get("accessToken") or data.get("token")
                self.refresh_token = data.get("refreshToken")
                
                # Set token expiry
                expires_in = data.get("expiresIn", 3600)
                self.token_expiry = get_token_expiry(expires_in)
                
                logger.info(f"Login successful. Token expires in {expires_in}s")
                return self.access_token
            else:
                error_msg = ERROR_MESSAGES.get(response.status_code, "Unknown error")
                logger.error(f"Login failed ({response.status_code}): {error_msg}")
                raise AuthenticationError(f"Login failed: {error_msg}")
                
        except RequestException as e:
            logger.error(f"Request failed: {e}")
            raise AuthenticationError(f"Network error during login: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            raise AuthenticationError(f"Login failed: {e}")
    
    def refresh(self) -> str:
        """Refresh access token using refresh token.
        
        Returns:
            New access token
            
        Raises:
            AuthenticationError: If refresh fails
        """
        if not self.refresh_token:
            raise AuthenticationError("No refresh token available")
        
        try:
            headers = {
                "consumerKey": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "refreshToken": self.refresh_token
            }
            
            logger.info("Attempting token refresh")
            
            response = requests.post(
                ENDPOINTS["session"],
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == HTTPStatus.OK:
                data = response.json()
                self.access_token = data.get("accessToken") or data.get("token")
                expires_in = data.get("expiresIn", 3600)
                self.token_expiry = get_token_expiry(expires_in)
                
                logger.info("Token refreshed successfully")
                return self.access_token
            else:
                error_msg = ERROR_MESSAGES.get(response.status_code, "Unknown error")
                logger.error(f"Token refresh failed: {error_msg}")
                raise AuthenticationError(f"Token refresh failed: {error_msg}")
                
        except RequestException as e:
            logger.error(f"Request failed during token refresh: {e}")
            raise AuthenticationError(f"Token refresh failed: {e}")
    
    def is_token_valid(self) -> bool:
        """Check if current token is valid.
        
        Returns:
            True if token exists and hasn't expired
        """
        if not self.access_token or not self.token_expiry:
            return False
        return not is_token_expired(self.token_expiry)
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for API requests.
        
        Returns:
            Dictionary with authorization headers
            
        Raises:
            AuthenticationError: If no valid token
        """
        if not self.is_token_valid():
            raise AuthenticationError("No valid token. Please login first.")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }


class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass