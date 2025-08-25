#!/usr/bin/env python3
"""
ONDC Search Request URL Details
===============================

This script provides the complete search request URL details with all components
"""

import json
import uuid
from datetime import datetime, timezone

def get_timestamp():
    """Generate ONDC-compliant timestamp format: YYYY-MM-DDTHH:mm:ss.sssZ"""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def prepare_search_request_url():
    """Prepare complete search request URL details"""
    
    print("🎯 ONDC SEARCH REQUEST URL PREPARATION")
    print("=" * 60)
    
    # Base URL components
    base_url = "https://neo-server.rozana.in"
    endpoint = "/search"
    full_url = f"{base_url}{endpoint}"
    
    print("📋 URL COMPONENTS:")
    print("=" * 30)
    print(f"🌐 Base URL: {base_url}")
    print(f"🔗 Endpoint: {endpoint}")
    print(f"🎯 Full URL: {full_url}")
    print(f"🔧 Method: POST")
    print(f"📋 Content-Type: application/json")
    print()
    
    # Generate request details
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = get_timestamp()
    
    print("🔑 REQUEST IDENTIFIERS:")
    print("=" * 30)
    print(f"📊 Transaction ID: {transaction_id}")
    print(f"📧 Message ID: {message_id}")
    print(f"📅 Timestamp: {timestamp}")
    print()
    
    # Complete request structure
    search_request = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:011",
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": "neo-server.rozana.in",
            "bap_uri": "https://neo-server.rozana.in",
            "transaction_id": transaction_id,
            "message_id": message_id,
            "timestamp": timestamp,
            "ttl": "PT30S"
        },
        "message": {
            "intent": {
                "item": {
                    "descriptor": {
                        "name": "Test Product from Pramaan Store"
                    }
                },
                "fulfillment": {
                    "type": "Delivery",
                    "end": {
                        "location": {
                            "gps": "28.6139,77.2090",
                            "address": {
                                "area_code": "110037"
                            }
                        }
                    }
                },
                "payment": {
                    "@ondc/org/buyer_app_finder_fee_type": "percent",
                    "@ondc/org/buyer_app_finder_fee_amount": "3"
                },
                "tags": [
                    {
                        "code": "bap_terms",
                        "list": [
                            {
                                "code": "static_terms",
                                "value": ""
                            },
                            {
                                "code": "static_terms_new",
                                "value": "https://neo-server.rozana.in/static-terms/bap/1.0/tc.pdf"
                            },
                            {
                                "code": "effective_date",
                                "value": "2023-10-01T00:00:00.000Z"
                            }
                        ]
                    }
                ]
            }
        }
    }
    
    print("📄 COMPLETE REQUEST PAYLOAD:")
    print("=" * 40)
    print(json.dumps(search_request, indent=2))
    print()
    
    # cURL command
    curl_command = f'''curl -X POST \\
  {full_url} \\
  -H "Content-Type: application/json" \\
  -d '{json.dumps(search_request, separators=(',', ':'))}'
'''
    
    print("🔧 CURL COMMAND:")
    print("=" * 20)
    print(curl_command)
    print()
    
    # Postman details
    print("📮 POSTMAN CONFIGURATION:")
    print("=" * 30)
    print(f"• Method: POST")
    print(f"• URL: {full_url}")
    print(f"• Headers:")
    print(f"  - Content-Type: application/json")
    print(f"• Body: Raw JSON (see payload above)")
    print()
    
    # Python requests format (if using requests library)
    python_code = f'''import requests
import json

url = "{full_url}"
headers = {{
    "Content-Type": "application/json"
}}
payload = {json.dumps(search_request, indent=4)}

response = requests.post(url, headers=headers, json=payload)
print(f"Status: {{response.status_code}}")
print(f"Response: {{response.text}}")
'''
    
    print("🐍 PYTHON REQUESTS FORMAT:")
    print("=" * 30)
    print(python_code)
    print()
    
    # Summary
    print("📊 SEARCH REQUEST SUMMARY:")
    print("=" * 30)
    print(f"✅ URL: {full_url}")
    print(f"✅ Method: POST")
    print(f"✅ BAP ID: neo-server.rozana.in")
    print(f"✅ Domain: ONDC:RET10")
    print(f"✅ Environment: preprod")
    print(f"✅ Buyer App Finder Fee: 3%")
    print(f"✅ BAP Terms: Included")
    print(f"✅ Timestamp Format: ONDC Compliant")
    print(f"✅ Location: Delhi (110037)")
    print(f"✅ Search Type: Item by name")

if __name__ == "__main__":
    prepare_search_request_url()