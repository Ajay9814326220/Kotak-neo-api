# Kotak Neo API Integration

A Python-based integration for Kotak Securities Neo API with secure authentication using TOTP, MPIN, and PKZ.

## Features

- ✅ OAuth 2.0 Authentication with TOTP support
- ✅ Secure credential management using environment variables
- ✅ Session token handling and refresh
- ✅ API endpoints for holdings, positions, funds, and orders
- ✅ Error handling and logging
- ✅ Ready for production deployment

## Prerequisites

- Python 3.8+
- Active Kotak Securities Neo account
- API Key and Secret from [Kotak Developer Portal](https://developer.kotaksecurities.com/)
- TOTP enabled on your account

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Ajay9814326220/kotak-neo-api.git
cd kotak-neo-api
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the root directory:
```env
KOTAK_API_KEY=your_api_key
KOTAK_API_SECRET=your_api_secret
KOTAK_CLIENT_CODE=your_client_code
KOTAK_MPIN=your_mpin
KOTAK_PKZ=your_pkz
KOTAK_TOTP_SECRET=your_totp_secret
LOG_LEVEL=INFO
```

## Quick Start

### 1. Generate TOTP and Link API

```python
from src.kotak_client import KotakNeoClient

# Initialize client
client = KotakNeoClient()

# Login and get access token
access_token = client.login()
print(f"Access Token: {access_token}")
```

### 2. Fetch Holdings

```python
holdings = client.get_holdings()
print(holdings)
```

### 3. Get Positions

```python
positions = client.get_positions()
print(positions)
```

### 4. Place an Order

```python
order = client.place_order(
    symbol="RELIANCE-EQ",
    quantity=1,
    price=2500.0,
    order_type="BUY",
    product="CNC"
)
print(order)
```

## File Structure

```
kotak-neo-api/
├── src/
│   ├── __init__.py
│   ├── kotak_client.py          # Main API client
│   ├── auth.py                  # Authentication logic
│   ├── utils.py                 # Utility functions
│   └── constants.py             # API endpoints and constants
├── examples/
│   ├── basic_login.py           # Login example
│   ├── get_holdings.py          # Fetch holdings
│   ├── place_order.py           # Place trade order
│   └── portfolio_analysis.py    # Portfolio analysis
├── tests/
│   ├── test_auth.py             # Authentication tests
│   └── test_client.py           # Client tests
├── .env.example                 # Environment template
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## API Endpoints Covered

- `POST /session` - Login and get access token
- `GET /portfolio/holdings` - Get holdings
- `GET /portfolio/positions` - Get positions
- `GET /funds` - Get fund information
- `POST /orders` - Place an order
- `GET /orders` - Get order status
- `POST /orders/{orderId}/cancel` - Cancel an order

## Error Handling

The client handles common errors:
- Invalid TOTP (401)
- Invalid MPIN/Client Code (403)
- Expired tokens (401)
- Network errors

## Security Best Practices

✅ Never commit `.env` file
✅ Use environment variables for credentials
✅ Rotate API keys periodically
✅ Enable 2FA on Kotak account
✅ Keep tokens secure in transit

## Troubleshooting

### Invalid TOTP Error
- Ensure your device clock is synchronized
- Regenerate TOTP secret from Kotak app
- Use the latest OTP number

### Authentication Failure
- Verify Client Code is correct
- Check MPIN hasn't been changed
- Confirm PKZ value from Kotak support

### Token Expired
- The client automatically handles token refresh
- If manual refresh needed, call `client.refresh_token()`

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - See LICENSE file for details

## Support

For issues specific to Kotak Neo API:
- [Kotak Developer Portal](https://developer.kotaksecurities.com/)
- [Kotak API Documentation](https://neo-docs.kotaksecurities.com/)

## Disclaimer

This is a third-party integration. Always test in sandbox mode before going live. Follow all Kotak Securities compliance guidelines.

---

**Last Updated:** 2026-04-24
**Status:** Production Ready