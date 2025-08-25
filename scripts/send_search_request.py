#!/usr/bin/env python3
"""
Send First Buyer Call (Search) to ONDC Gateway
"""

import sys
import os
import requests
import json
import uuid
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.org_config import OrganizationConfig

def create_search_payload():
    """Create a search payload for ONDC gateway"""
    
    # Get organization config
    subscriber_info = OrganizationConfig.get_subscriber_info()
    
    # Generate unique transaction ID
    transaction_id = str(uuid.uuid4())
    
    # Create search payload
    payload = {
        "context": {
            "domain": subscriber_info["domain"],
            "country": "IND",
            "city": "std:011",
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": subscriber_info["subscriber_id"],
            "bap_uri": subscriber_info["bap_uri"],
            "transaction_id": transaction_id,
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "ttl": "PT30S"
        },
        "message": {
            "intent": {
                "fulfillment": {
                    "start": {
                        "location": {
                            "gps": "28.6139,77.2090"  # Delhi coordinates
                        }
                    },
                    "end": {
                        "location": {
                            "gps": "28.6139,77.2090"  # Delhi coordinates
                        }
                    }
                },
                "payment": {
                    "@ondc/org/buyer_app_finder_fee_type": "percent",
                    "@ondc/org/buyer_app_finder_fee_amount": "3"
                },
                "category": {
                    "id": "ONDC:RET10"
                },
                "item": {
                    "descriptor": {
                        "name": "Groceries"
                    }
                }
            }
        }
    }
    
    return payload, transaction_id

def send_search_request():
    """Send search request to ONDC gateway"""
    
    # Create payload
    payload, transaction_id = create_search_payload()
    
    # Get authentication headers
    headers = OrganizationConfig.get_auth_headers()
    
    # Add ONDC specific headers
    headers.update({
        "X-ONDC-Signature": "placeholder_signature",  # Will be replaced with actual signature
        "X-ONDC-Signature-Key": "placeholder_key_id"  # Will be replaced with actual key ID
    })
    
    # Gateway endpoint
    gateway_url = "https://preprod.gateway.ondc.org/search"
    
    print("=== Sending Search Request to ONDC Gateway ===\n")
    print(f"Gateway URL: {gateway_url}")
    print(f"Transaction ID: {transaction_id}")
    print(f"Subscriber ID: {OrganizationConfig.SUBSCRIBER_ID}")
    print(f"Domain: {OrganizationConfig.DOMAIN}")
    print(f"Type: {OrganizationConfig.TYPE}")
    
    print("\nRequest Headers:")
    for key, value in headers.items():
        if key == "Authorization":
            truncated_token = value[:50] + "..." if len(value) > 50 else value
            print(f"  {key}: {truncated_token}")
        else:
            print(f"  {key}: {value}")
    
    print("\nRequest Payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        print(f"\nSending request to {gateway_url}...")
        
        response = requests.post(
            gateway_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Search request sent successfully!")
            response_data = response.json()
            print("\nResponse Body:")
            print(json.dumps(response_data, indent=2))
        else:
            print(f"❌ Search request failed with status {response.status_code}")
            print(f"Response Body: {response.text}")
        
        return response, transaction_id
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making search request: {e}")
        return None, transaction_id

def save_search_response(response, transaction_id):
    """Save the search response to a file"""
    if response:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"search_response_{transaction_id}_{timestamp}.json"
        
        response_data = {
            "transaction_id": transaction_id,
            "timestamp": timestamp,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(response_data, f, indent=2)
            print(f"\n📁 Search response saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving response: {e}")

def main():
    """Main function to send search request"""
    
    print("=== ONDC Gateway Search Request ===\n")
    
    # Check configuration
    print("Checking organization configuration...")
    if not OrganizationConfig.ED25519_PRIVATE_KEY:
        print("⚠️  Warning: ED25519_PRIVATE_KEY not set in environment")
    if not OrganizationConfig.KEY_ID:
        print("⚠️  Warning: KEY_ID not set in environment")
    
    print(f"✅ Subscriber ID: {OrganizationConfig.SUBSCRIBER_ID}")
    print(f"✅ BAP URI: {OrganizationConfig.BAP_URI}")
    print(f"✅ Domain: {OrganizationConfig.DOMAIN}")
    print(f"✅ Type: {OrganizationConfig.TYPE}")
    
    # Send search request
    response, transaction_id = send_search_request()
    
    # Save response
    save_search_response(response, transaction_id)
    
    print("\n=== Search Request Complete ===")

if __name__ == "__main__":
    main() 