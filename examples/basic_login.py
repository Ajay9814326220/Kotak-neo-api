"""Basic Login Example - Test your Kotak Neo API connection"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.kotak_client import KotakNeoClient
from src.auth import AuthenticationError


def main():
    """Test login functionality"""
    print("="*50)
    print("Kotak Neo API - Login Test")
    print("="*50)
    print()
    
    try:
        # Initialize client
        print("[1] Initializing Kotak Neo Client...")
        client = KotakNeoClient()
        print("✓ Client initialized successfully")
        print()
        
        # Attempt login
        print("[2] Attempting login...")
        access_token = client.login()
        print(f"✓ Login successful!")
        print()
        
        # Display token info
        print("[3] Token Information:")
        print(f"  Access Token: {access_token[:20]}..." if len(access_token) > 20 else access_token)
        print(f"  Token Status: Valid")
        print(f"  Expires: {client.auth.token_expiry}")
        print()
        
        # Test API call
        print("[4] Testing API call (Get Holdings)...")
        holdings = client.get_holdings()
        print(f"✓ API call successful!")
        print(f"  Holdings returned: {len(holdings.get('holdings', []))} positions")
        print()
        
        print("="*50)
        print("✓ All tests passed! API is properly configured.")
        print("="*50)
        
    except AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
        print("\nTroubleshooting:")
        print("- Verify KOTAK_CLIENT_CODE in .env")
        print("- Verify KOTAK_MPIN in .env")
        print("- Verify KOTAK_TOTP_SECRET in .env")
        print("- Verify KOTAK_PKZ in .env")
        print("- Check if your TOTP is fresh (< 30 seconds old)")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())