# ONDC Gateway Search Request Summary

## Attempted Search Requests

### 1. Basic Search Request (send_search_request.py)
- **Status**: ❌ Failed (401 Unauthorized)
- **Error**: "The auth header is not valid"
- **Issue**: Used placeholder signatures and Bearer token authentication

### 2. Signed Search Request (send_search_request_signed.py)
- **Status**: ❌ Failed (401 Unauthorized)
- **Error**: "The auth header not found"
- **Issue**: Used ONDC-specific headers but gateway expected Authorization header

### 3. Corrected Search Request (send_search_request_corrected.py)
- **Status**: ❌ Failed (401 Unauthorized)
- **Error**: "The auth header is not valid"
- **Issue**: Used proper ONDC signature format but authentication still failed

## Request Details

### Transaction IDs Generated
1. `99324fff-3a86-4c5b-a137-8be4852fef48`
2. `e6f5ea4c-2987-49a3-a0b5-c407f1fb074b`
3. `05c9af8f-55ac-408f-b0af-df70f21cc246`

### Payload Structure
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in/callback",
    "transaction_id": "<uuid>",
    "message_id": "<uuid>",
    "timestamp": "<iso_timestamp>",
    "ttl": "PT30S"
  },
  "message": {
    "intent": {
      "fulfillment": {
        "start": {"location": {"gps": "28.6139,77.2090"}},
        "end": {"location": {"gps": "28.6139,77.2090"}}
      },
      "payment": {
        "@ondc/org/buyer_app_finder_fee_type": "percent",
        "@ondc/org/buyer_app_finder_fee_amount": "3"
      },
      "category": {"id": "ONDC:RET10"},
      "item": {"descriptor": {"name": "Groceries"}}
    }
  }
}
```

## Authentication Methods Tried

### 1. Bearer Token
```http
Authorization: Bearer <JWT_TOKEN>
```

### 2. ONDC Headers
```http
X-ONDC-Signature: <signature>
X-ONDC-Signature-Key: <key_id>
```

### 3. ONDC Signature Format
```http
Authorization: Signature keyId="neo-server.rozana.in",algorithm="ed25519",headers="(created) (expires) digest",signature="<signature>",created="<timestamp>",expires="<expiry>"
```

## Root Cause Analysis

The 401 authentication errors suggest that:

1. **Registration Required**: The subscriber may need to be properly registered and whitelisted with ONDC before accessing the gateway
2. **Authentication Method**: The gateway may require a different authentication method than what we've tried
3. **Endpoint Access**: The search endpoint may not be publicly accessible or may require specific permissions
4. **Environment**: The preprod gateway may have different requirements than production

## Current Status

### ✅ What's Working
- Organization configuration is properly set up
- Cryptographic keys are loaded successfully
- Payload structure follows ONDC specifications
- Local search endpoint is implemented and accessible

### ❌ What's Not Working
- Gateway authentication is failing
- Search requests are being rejected with 401 errors
- Need to determine correct authentication method

## Next Steps

### 1. Verify Registration Status
```bash
# Check if subscriber is properly registered
curl -X POST "https://preprod.registry.ondc.org/v2.0/lookup" \
  -H "Content-Type: application/json" \
  -d '{"subscriber_id": "neo-server.rozana.in"}'
```

### 2. Check ONDC Documentation
- Review ONDC gateway authentication requirements
- Verify the correct endpoint URL and method
- Check if there are specific preprod requirements

### 3. Alternative Approaches
- Test with production gateway instead of preprod
- Try different authentication methods
- Contact ONDC support for gateway access

### 4. Local Testing
- Test the local search endpoint first
- Verify the payload structure locally
- Ensure all cryptographic operations work correctly

## Files Created

1. **`scripts/send_search_request.py`** - Basic search request
2. **`scripts/send_search_request_signed.py`** - Search with ONDC signing
3. **`scripts/send_search_request_corrected.py`** - Search with proper authentication
4. **`SEARCH_REQUEST_SUMMARY.md`** - This summary

## Recommendations

1. **Complete ONDC Registration**: Ensure the subscriber is fully registered and whitelisted
2. **Gateway Access**: Verify gateway access permissions with ONDC
3. **Authentication**: Determine the correct authentication method for the gateway
4. **Testing**: Start with local endpoint testing before gateway integration
5. **Documentation**: Review ONDC gateway documentation for specific requirements

---

**Last Updated**: August 22, 2025
**Status**: Authentication issues - requires ONDC gateway access verification 