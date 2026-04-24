"""Place Order Example"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.kotak_client import KotakNeoClient
from src.utils import format_response


def main():
    """Place a sample order"""
    print("="*60)
    print("Kotak Neo API - Place Order")
    print("="*60)
    print()
    
    # Order parameters
    SYMBOL = "RELIANCE-EQ"  # Change to desired symbol
    QUANTITY = 1
    PRICE = 2500.0
    ORDER_TYPE = "BUY"
    PRODUCT = "CNC"
    
    try:
        # Initialize and login
        print("[1] Initializing client...")
        client = KotakNeoClient()
        client.login()
        print("✓ Logged in successfully")
        print()
        
        # Display order details
        print("[2] Order Details:")
        print(f"  Symbol: {SYMBOL}")
        print(f"  Type: {ORDER_TYPE}")
        print(f"  Quantity: {QUANTITY}")
        print(f"  Price: ₹{PRICE}")
        print(f"  Product: {PRODUCT}")
        print()
        
        # Confirm order
        confirm = input("Do you want to place this order? (yes/no): ").lower()
        if confirm != "yes":
            print("Order cancelled.")
            return 0
        print()
        
        # Place order
        print("[3] Placing order...")
        response = client.place_order(
            symbol=SYMBOL,
            quantity=QUANTITY,
            price=PRICE,
            order_type=ORDER_TYPE,
            product=PRODUCT
        )
        
        # Display response
        order_id = response.get('orderId')
        status = response.get('status', 'UNKNOWN')
        
        print(f"✓ Order placed successfully!")
        print()
        print("[4] Order Response:")
        print(f"  Order ID: {order_id}")
        print(f"  Status: {status}")
        print()
        
        print("[5] Full Response (JSON):")
        print(format_response(response))
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())