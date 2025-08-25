# Organization Configuration for ONDC API Calls

This configuration stores all the necessary details for **Rozana Rural Commerce Private Limited** to make ONDC API calls.

## Files Created

1. **`app/core/org_config.py`** - Main configuration class
2. **`scripts/use_org_config.py`** - Demo script showing configuration usage
3. **`scripts/example_api_call.py`** - Example API calls using the configuration

## Organization Details Stored

### Authentication
- **NO_TOKEN**: JWT token for API authentication
- **ED25519_PRIVATE_KEY**: Private key for signing (set via environment variable)
- **KEY_ID**: Key identifier (set via environment variable)

### Subscriber Information
- **Subscriber ID**: `neo-server.rozana.in`
- **BAP URI**: `https://neo-server.rozana.in/callback`
- **Domain**: `ONDC:RET10` (Retail)
- **Type**: `buyerApp`

### Company Details
- **Legal Entity Name**: Rozana Rural Commerce Private Limited
- **Business Address**: Rozana Rural Commerce Private Limited, Delhi, India
- **GST Number**: 07AAACR2082N4Z7
- **PAN Number**: AAACR7657Q
- **Date of Incorporation**: 23/06/2020

### Contact Information
- **Email ID**: digitalaccounts@rozana.in
- **Mobile Number**: 9991162341
- **Country**: IND (India)
- **City Code**: std:011 (Delhi)

### Authorized Signatory
- **Name**: Digital Accounts
- **Address**: Rozana Rural Commerce Private Limited, Delhi, India

### Technical Details
- **Unique Key ID**: 8fe65920-70a9-4771-b68d-0e9028015250

## Usage

### 1. Set Environment Variables

```bash
export ED25519_PRIVATE_KEY='your_private_key_here'
export KEY_ID='your_key_id_here'
```

### 2. Import and Use in Your Code

```python
from app.core.org_config import OrganizationConfig

# Get authentication headers
headers = OrganizationConfig.get_auth_headers()

# Get subscriber information
subscriber_info = OrganizationConfig.get_subscriber_info()

# Get company information
company_info = OrganizationConfig.get_company_info()
```

### 3. Example API Call

```python
import requests
from app.core.org_config import OrganizationConfig

# Make API call
headers = OrganizationConfig.get_auth_headers()
subscriber_data = OrganizationConfig.get_subscriber_info()

response = requests.post(
    "https://api.ondc.org/subscribe",
    headers=headers,
    json={
        "subscriber_id": subscriber_data["subscriber_id"],
        "domain": subscriber_data["domain"],
        "type": subscriber_data["type"],
        "callback_url": subscriber_data["bap_uri"],
        # ... other required fields
    }
)
```

## Available Methods

### `OrganizationConfig.get_auth_headers()`
Returns a dictionary with authentication headers:
```python
{
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}
```

### `OrganizationConfig.get_subscriber_info()`
Returns subscriber information for API calls:
```python
{
    "subscriber_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in/callback",
    "domain": "ONDC:RET10",
    "type": "buyerApp",
    "key_id": "<key_id_from_env>"
}
```

### `OrganizationConfig.get_company_info()`
Returns complete company information:
```python
{
    "legal_entity_name": "Rozana Rural Commerce Private Limited",
    "business_address": "Rozana Rural Commerce Private Limited, Delhi, India",
    "gst_number": "07AAACR2082N4Z7",
    "pan_number": "AAACR7657Q",
    "date_of_incorporation": "23/06/2020",
    "email_id": "digitalaccounts@rozana.in",
    "mobile_number": "9991162341",
    "country": "IND",
    "city_code": "std:011",
    "authorized_signatory_name": "Digital Accounts",
    "authorized_signatory_address": "Rozana Rural Commerce Private Limited, Delhi, India",
    "unique_key_id": "8fe65920-70a9-4771-b68d-0e9028015250"
}
```

## Running Examples

### View Configuration Demo
```bash
python scripts/use_org_config.py
```

### Run Example API Calls
```bash
python scripts/example_api_call.py
```

## Security Notes

1. **Sensitive Data**: The `ED25519_PRIVATE_KEY` and `KEY_ID` are loaded from environment variables for security
2. **Token Storage**: The NO_TOKEN is stored in the configuration file - consider moving to environment variables for production
3. **File Permissions**: Ensure the configuration file has appropriate permissions

## Integration with Existing Code

You can now use this configuration in your existing ONDC API scripts by importing the `OrganizationConfig` class and using its methods to get the required data for API calls. 