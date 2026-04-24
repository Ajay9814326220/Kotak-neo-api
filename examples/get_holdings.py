"""Get Portfolio Holdings Example"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.kotak_client import KotakNeoClient
from src.utils import format_response


def main():
    """Fetch and display holdings"""
    print("="*60)
    print("Kotak Neo API - Portfolio Holdings")
    print("="*60)
    print()
    
    try:
        # Initialize and login
        print("[1] Initializing client...")
        client = KotakNeoClient()
        client.login()
        print("✓ Logged in successfully")
        print()
        
        # Fetch holdings
        print("[2] Fetching holdings...")
        response = client.get_holdings()
        print("✓ Holdings retrieved")
        print()
        
        # Process holdings
        holdings = response.get('holdings', [])
        print(f"[3] Portfolio Summary:")
        print(f"  Total Holdings: {len(holdings)}")
        print()
        
        if holdings:
            print("[4] Holdings Details:")
            print("-" * 60)
            print(f"{'Symbol':<15} {'Qty':<8} {'Avg Price':<12} {'Current':<12} {'P&L':<12}")
            print("-" * 60)
            
            total_value = 0
            for holding in holdings:
                symbol = holding.get('symbol', 'N/A')
                quantity = holding.get('quantity', 0)
                avg_price = holding.get('avgPrice', 0)
                ltp = holding.get('ltp', 0)
                pnl = (ltp - avg_price) * quantity if avg_price > 0 else 0
                
                print(f"{symbol:<15} {quantity:<8} {avg_price:<12.2f} {ltp:<12.2f} {pnl:<12.2f}")
                total_value += ltp * quantity
            
            print("-" * 60)
            print(f"Portfolio Value: ₹{total_value:,.2f}")
            print()
        
        # Raw response (optional)
        print("[5] Full Response (JSON):")
        print(format_response(response))
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())