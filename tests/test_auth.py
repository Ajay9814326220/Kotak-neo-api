"""Authentication Tests"""

import pytest
import os
from unittest.mock import patch, MagicMock
from src.auth import KotakAuth, AuthenticationError
from src.utils import generate_totp


class TestKotakAuth:
    """Test KotakAuth class"""
    
    @pytest.fixture
    def auth_instance(self):
        """Create auth instance for testing"""
        return KotakAuth(
            api_key="test_key",
            api_secret="test_secret",
            client_code="TEST001",
            mpin="1234",
            pkz="test_pkz",
            totp_secret="JBSWY3DPEBLW64TMMQ======"  # Valid Base32
        )
    
    def test_auth_initialization(self, auth_instance):
        """Test auth initialization"""
        assert auth_instance.api_key == "test_key"
        assert auth_instance.client_code == "TEST001"
        assert auth_instance.access_token is None
    
    def test_missing_credentials(self):
        """Test missing credentials raises error"""
        with pytest.raises(ValueError):
            KotakAuth(
                api_key="test_key",
                api_secret="",
                client_code="",
                mpin="",
                pkz="",
                totp_secret=""
            )
    
    @patch('src.auth.requests.post')
    def test_login_success(self, mock_post, auth_instance):
        """Test successful login"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "accessToken": "test_token",
            "refreshToken": "refresh_token",
            "expiresIn": 3600
        }
        mock_post.return_value = mock_response
        
        token = auth_instance.login()
        assert token == "test_token"
        assert auth_instance.access_token == "test_token"
    
    @patch('src.auth.requests.post')
    def test_login_failure(self, mock_post, auth_instance):
        """Test login failure"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        
        with pytest.raises(AuthenticationError):
            auth_instance.login()
    
    def test_totp_generation(self):
        """Test TOTP generation"""
        totp = generate_totp("JBSWY3DPEBLW64TMMQ======")
        assert len(totp) == 6
        assert totp.isdigit()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])