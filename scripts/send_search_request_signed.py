#!/usr/bin/env python3
"""
Send First Buyer Call (Search) to ONDC Gateway with Proper Signing
"""

import sys
import os
import requests
import json
import uuid
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.org_config import OrganizationConfig
from app.core.ondc_crypto import crypto

def create_search_payload():
    """Create a search payload for ONDC gateway"""
    
    # Get organization config
    subscriber_info = OrganizationConfig.get_subscriber_info()
    
    # Generate unique transaction ID
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    
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
            "message_id": message_id,
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
    
    return payload, transaction_id, message_id

def create_signed_headers(payload_str: str, key_id: str = None):
    """Create headers with proper ONDC signing"""
    
    # Get key ID from crypto or config
    if not key_id:
        key_id = crypto.get_unique_key_id() or OrganizationConfig.KEY_ID
    
    # Sign the payload
    signature = crypto.sign_data(payload_str)
    
    if not signature:
        print("⚠️  Warning: Could not create signature, using placeholder")
        signature = "placeholder_signature"
        key_id = "placeholder_key_id"
    
    headers = {
        "Content-Type": "application/json",
        "X-ONDC-Signature": signature,
        "X-ONDC-Signature-Key": key_id
    }
    
    return headers

def send_search_request():
    """Send search request to ONDC gateway with proper signing"""
    
    # Create payload
    payload, transaction_id, message_id = create_search_payload()
    
    # Convert payload to string for signing
    payload_str = json.dumps(payload, separators=(',', ':'))
    
    # Create signed headers
    headers = create_signed_headers(payload_str)
    
    # Gateway endpoint
    gateway_url = "https://preprod.gateway.ondc.org/search"
    
    print("=== Sending Signed Search Request to ONDC Gateway ===\n")
    print(f"Gateway URL: {gateway_url}")
    print(f"Transaction ID: {transaction_id}")
    print(f"Message ID: {message_id}")
    print(f"Subscriber ID: {OrganizationConfig.SUBSCRIBER_ID}")
    print(f"Domain: {OrganizationConfig.DOMAIN}")
    print(f"Type: {OrganizationConfig.TYPE}")
    
    print("\nRequest Headers:")
    for key, value in headers.items():
        if key == "X-ONDC-Signature":
            truncated_sig = value[:50] + "..." if len(value) > 50 else value
            print(f"  {key}: {truncated_sig}")
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
            try:
                response_data = response.json()
                print("\nResponse Body:")
                print(json.dumps(response_data, indent=2))
            except json.JSONDecodeError:
                print(f"\nResponse Body (raw): {response.text}")
        elif response.status_code == 202:
            print("✅ Search request accepted (202 Accepted)")
            print(f"Response Body: {response.text}")
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

def check_crypto_setup():
    """Check if crypto setup is properly configured"""
    print("Checking crypto configuration...")
    
    # Check signing key
    signing_key = crypto.get_signing_public_key()
    if signing_key:
        print(f"✅ Signing public key available: {signing_key[:20]}...")
    else:
        print("❌ Signing public key not available")
    
    # Check unique key ID
    key_id = crypto.get_unique_key_id()
    if key_id:
        print(f"✅ Unique key ID available: {key_id}")
    else:
        print("❌ Unique key ID not available")
    
    # Check request ID
    request_id = crypto.get_request_id()
    if request_id:
        print(f"✅ Request ID available: {request_id}")
    else:
        print("❌ Request ID not available")
    
    return signing_key and key_id

def main():
    """Main function to send signed search request"""
    
    print("=== ONDC Gateway Signed Search Request ===\n")
    
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
    
    # Check crypto setup
    crypto_ready = check_crypto_setup()
    if not crypto_ready:
        print("\n⚠️  Warning: Crypto setup may not be complete")
        print("   The request will be sent with placeholder signatures")
    
    # Send search request
    response, transaction_id = send_search_request()
    
    # Save response
    save_search_response(response, transaction_id)
    
    print("\n=== Signed Search Request Complete ===")

if __name__ == "__main__":
    main() 