"""Portfolio Analysis Example"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.kotak_client import KotakNeoClient


def main():
    """Analyze portfolio"""
    print("="*70)
    print("Kotak Neo API - Portfolio Analysis")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()
    
    try:
        # Initialize and login
        print("[1] Initializing client...")
        client = KotakNeoClient()
        client.login()
        print("✓ Logged in successfully")
        print()
        
        # Get holdings and positions
        print("[2] Fetching portfolio data...")
        holdings_response = client.get_holdings()
        positions_response = client.get_positions()
        funds_response = client.get_funds()
        print("✓ Data retrieved")
        print()
        
        # Analyze holdings
        holdings = holdings_response.get('holdings', [])
        print("[3] Holdings Analysis:")
        print("-" * 70)
        
        if holdings:
            total_invested = 0
            total_current = 0
            total_pnl = 0
            
            for holding in holdings:
                symbol = holding.get('symbol', 'N/A')
                qty = holding.get('quantity', 0)
                avg = holding.get('avgPrice', 0)
                ltp = holding.get('ltp', 0)
                
                invested = avg * qty
                current = ltp * qty
                pnl = current - invested
                pnl_pct = (pnl / invested * 100) if invested > 0 else 0
                
                total_invested += invested
                total_current += current
                total_pnl += pnl
                
                print(f"{symbol:15} | Qty: {qty:6} | Avg: {avg:10.2f} | LTP: {ltp:10.2f}")
                print(f"                | Invested: ₹{invested:12,.2f} | Current: ₹{current:12,.2f}")
                print(f"                | P&L: ₹{pnl:12,.2f} ({pnl_pct:6.2f}%)")
                print("-" * 70)
            
            # Portfolio summary
            total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0
            
            print()
            print("[4] Portfolio Summary:")
            print(f"  Total Invested: ₹{total_invested:,.2f}")
            print(f"  Current Value:  ₹{total_current:,.2f}")
            print(f"  Total P&L:      ₹{total_pnl:,.2f} ({total_pnl_pct:.2f}%)")
            print(f"  Holdings Count: {len(holdings)}")
            print()
        else:
            print("No holdings found.")
            print()
        
        # Positions analysis
        positions = positions_response.get('positions', [])
        if positions:
            print("[5] Open Positions:")
            print(f"  Total Positions: {len(positions)}")
            for pos in positions:
                print(f"  - {pos.get('symbol')}: {pos.get('quantity')} units")
            print()
        
        # Funds
        funds = funds_response.get('funds', {})
        if funds:
            print("[6] Fund Details:")
            print(f"  Available: ₹{funds.get('available', 0):,.2f}")
            print(f"  Used: ₹{funds.get('used', 0):,.2f}")
            print(f"  Total: ₹{funds.get('total', 0):,.2f}")
        
        print()
        print("="*70)
        print("✓ Analysis complete")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())