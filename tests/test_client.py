"""Client Tests"""

import pytest
from unittest.mock import patch, MagicMock
from src.kotak_client import KotakNeoClient, ApiError


class TestKotakNeoClient:
    """Test KotakNeoClient class"""
    
    @pytest.fixture
    def client(self):
        """Create client instance for testing"""
        with patch.dict('os.environ', {
            'KOTAK_API_KEY': 'test_key',
            'KOTAK_API_SECRET': 'test_secret',
            'KOTAK_CLIENT_CODE': 'TEST001',
            'KOTAK_MPIN': '1234',
            'KOTAK_PKZ': 'test_pkz',
            'KOTAK_TOTP_SECRET': 'JBSWY3DPEBLW64TMMQ======'
        }):
            return KotakNeoClient()
    
    @patch('src.kotak_client.KotakAuth.login')
    def test_client_login(self, mock_login, client):
        """Test client login"""
        mock_login.return_value = "test_token"
        token = client.login()
        assert token == "test_token"
    
    @patch('src.kotak_client.requests.request')
    def test_get_holdings(self, mock_request, client):
        """Test get holdings"""
        client.auth.access_token = "test_token"
        client.auth.token_expiry = MagicMock()
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"holdings": []}
        mock_request.return_value = mock_response
        
        with patch.object(client.auth, 'is_token_valid', return_value=True):
            result = client.get_holdings()
            assert "holdings" in result
    
    @patch('src.kotak_client.requests.request')
    def test_place_order(self, mock_request, client):
        """Test place order"""
        client.auth.access_token = "test_token"
        client.auth.token_expiry = MagicMock()
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"orderId": "12345", "status": "SUCCESS"}
        mock_request.return_value = mock_response
        
        with patch.object(client.auth, 'is_token_valid', return_value=True):
            result = client.place_order(
                symbol="RELIANCE-EQ",
                quantity=1,
                price=2500.0
            )
            assert result["orderId"] == "12345"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])