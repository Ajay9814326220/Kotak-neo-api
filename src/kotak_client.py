"""Main Kotak Neo API Client"""

import logging
from typing import Dict, Any, Optional, List
import requests
from requests.exceptions import RequestException

from .auth import KotakAuth, AuthenticationError
from .constants import ENDPOINTS, HTTPStatus, ERROR_MESSAGES, REQUEST_TIMEOUT
from .utils import setup_logging, mask_credential

logger = logging.getLogger(__name__)


class KotakNeoClient:
    """Main client for Kotak Neo API interactions"""
    
    def __init__(self, api_key: str = None, api_secret: str = None, 
                 client_code: str = None, mpin: str = None, 
                 pkz: str = None, totp_secret: str = None):
        """Initialize Kotak Neo API client.
        
        Args:
            api_key: API Key from Kotak (or set KOTAK_API_KEY env var)
            api_secret: API Secret from Kotak
            client_code: Your Kotak client code
            mpin: Your MPIN
            pkz: Your PKZ
            totp_secret: TOTP secret for 2FA
        """
        import os
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        setup_logging(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE")
        )
        
        # Get credentials from arguments or environment
        self.api_key = api_key or os.getenv("KOTAK_API_KEY")
        self.api_secret = api_secret or os.getenv("KOTAK_API_SECRET")
        self.client_code = client_code or os.getenv("KOTAK_CLIENT_CODE")
        self.mpin = mpin or os.getenv("KOTAK_MPIN")
        self.pkz = pkz or os.getenv("KOTAK_PKZ")
        self.totp_secret = totp_secret or os.getenv("KOTAK_TOTP_SECRET")
        
        # Validate all credentials are provided
        if not all([self.api_key, self.client_code, self.mpin, self.pkz, self.totp_secret]):
            raise ValueError("Missing required credentials. Set environment variables or pass as arguments.")
        
        # Initialize authentication
        self.auth = KotakAuth(
            api_key=self.api_key,
            api_secret=self.api_secret,
            client_code=self.client_code,
            mpin=self.mpin,
            pkz=self.pkz,
            totp_secret=self.totp_secret
        )
        
        logger.info(f"KotakNeoClient initialized for {mask_credential(self.client_code)}")
    
    def login(self) -> str:
        """Login and get access token.
        
        Returns:
            Access token
        """
        try:
            token = self.auth.login()
            logger.info("Successfully logged in")
            return token
        except AuthenticationError as e:
            logger.error(f"Login failed: {e}")
            raise
    
    def _make_request(self, method: str, endpoint_key: str, 
                     params: Dict = None, json_data: Dict = None) -> Dict[str, Any]:
        """Make API request with error handling.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint_key: Key in ENDPOINTS dictionary
            params: Query parameters
            json_data: JSON payload
            
        Returns:
            API response dictionary
            
        Raises:
            ApiError: If request fails
        """
        try:
            # Check token validity
            if not self.auth.is_token_valid():
                logger.warning("Token expired, refreshing...")
                self.auth.refresh()
            
            url = ENDPOINTS.get(endpoint_key)
            if not url:
                raise ValueError(f"Unknown endpoint: {endpoint_key}")
            
            headers = self.auth.get_headers()
            
            logger.debug(f"{method} {url}")
            
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            # Handle response
            if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
                return response.json()
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logger.warning("Token invalid, attempting refresh...")
                self.auth.refresh()
                return self._make_request(method, endpoint_key, params, json_data)
            else:
                error_msg = ERROR_MESSAGES.get(response.status_code, response.text)
                logger.error(f"API request failed: {error_msg}")
                raise ApiError(f"Request failed ({response.status_code}): {error_msg}")
                
        except RequestException as e:
            logger.error(f"Network error: {e}")
            raise ApiError(f"Network error: {e}")
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            raise
    
    def get_holdings(self) -> Dict[str, Any]:
        """Get portfolio holdings.
        
        Returns:
            Holdings data
        """
        logger.info("Fetching holdings...")
        return self._make_request("GET", "holdings")
    
    def get_positions(self) -> Dict[str, Any]:
        """Get current positions.
        
        Returns:
            Positions data
        """
        logger.info("Fetching positions...")
        return self._make_request("GET", "positions")
    
    def get_funds(self) -> Dict[str, Any]:
        """Get fund information.
        
        Returns:
            Funds data
        """
        logger.info("Fetching funds...")
        return self._make_request("GET", "funds")
    
    def place_order(self, symbol: str, quantity: int, price: float,
                   order_type: str = "BUY", product: str = "CNC",
                   price_type: str = "LIMIT", order_validity: str = "DAY",
                   **kwargs) -> Dict[str, Any]:
        """Place a new order.
        
        Args:
            symbol: Trading symbol (e.g., "RELIANCE-EQ")
            quantity: Order quantity
            price: Order price
            order_type: BUY or SELL
            product: CNC, MIS, or NRML
            price_type: LIMIT or MARKET
            order_validity: DAY, IOC, GTD, or GTC
            **kwargs: Additional parameters
            
        Returns:
            Order response with order ID
        """
        payload = {
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "orderType": order_type,
            "product": product,
            "priceType": price_type,
            "orderValidity": order_validity,
            **kwargs
        }
        
        logger.info(f"Placing {order_type} order: {symbol} x {quantity} @ {price}")
        return self._make_request("POST", "orders", json_data=payload)
    
    def get_orders(self, order_id: Optional[str] = None) -> Dict[str, Any]:
        """Get order status.
        
        Args:
            order_id: Optional specific order ID
            
        Returns:
            Order status data
        """
        params = {"orderId": order_id} if order_id else None
        logger.info(f"Fetching orders{f' {order_id}' if order_id else '...'}")
        return self._make_request("GET", "orders", params=params)
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order.
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        logger.info(f"Cancelling order: {order_id}")
        return self._make_request(
            "POST", 
            "cancel_order",
            json_data={"orderId": order_id}
        )


class ApiError(Exception):
    """Custom exception for API errors"""
    pass