#!/usr/bin/env python3

"""
🎯 Send SELECT call to Pramaan Store
BPP ID: pramaan.ondc.org/beta/preprod/mock/seller
Domain: RET10 (Retail)
Environment: preprod
"""

import requests
import json
import uuid
from datetime import datetime, timezone
import sys

def generate_transaction_id():
    """Generate ONDC compliant transaction ID (UUID v4)"""
    return str(uuid.uuid4())

def generate_message_id():
    """Generate unique message ID (UUID v4)"""
    return str(uuid.uuid4())

def get_current_timestamp():
    """Generate ONDC compliant timestamp"""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def send_select_call():
    """Send SELECT call to Pramaan store"""
    
    # Generate transaction ID for this flow
    transaction_id = generate_transaction_id()
    message_id = generate_message_id()
    timestamp = get_current_timestamp()
    
    # Pramaan store details
    bpp_id = "pramaan.ondc.org/beta/preprod/mock/seller"
    bpp_uri = f"https://{bpp_id}"
    
    # Your BAP details
    bap_id = "neo-server.rozana.in"
    bap_uri = "https://neo-server.rozana.in"
    
    # SELECT payload for Pramaan store
    select_payload = {
        "context": {
            "domain": "ONDC:RET10",  # Retail domain
            "country": "IND",
            "city": "std:011",  # Delhi
            "action": "select",
            "core_version": "1.2.0",
            "bap_id": bap_id,
            "bap_uri": bap_uri,
            "bpp_id": bpp_id,
            "bpp_uri": bpp_uri,
            "transaction_id": transaction_id,
            "message_id": message_id,
            "timestamp": timestamp,
            "ttl": "PT30S"
        },
        "message": {
            "order": {
                "provider": {
                    "id": "pramaan_provider_1",
                    "descriptor": {
                        "name": "Pramaan Test Store"
                    }
                },
                "items": [
                    {
                        "id": "pramaan_item_001",
                        "descriptor": {
                            "name": "Test Product for Pramaan"
                        },
                        "category_id": "Grocery",
                        "quantity": {
                            "count": 2
                        },
                        "price": {
                            "currency": "INR",
                            "value": "100.00"
                        }
                    }
                ],
                "billing": {
                    "address": {
                        "name": "John Doe",
                        "building": "123 Test Building",
                        "locality": "Test Locality",
                        "city": "New Delhi",
                        "state": "Delhi",
                        "country": "IND",
                        "area_code": "110037"
                    },
                    "phone": "9876543210",
                    "email": "test@neo-server.rozana.in",
                    "created_at": timestamp,
                    "updated_at": timestamp
                },
                "fulfillment": {
                    "id": "fulfillment_1",
                    "type": "Delivery",
                    "provider_id": "pramaan_provider_1",
                    "tracking": True,
                    "end": {
                        "location": {
                            "gps": "28.6139,77.2090",
                            "address": {
                                "name": "John Doe",
                                "building": "123 Test Building",
                                "locality": "Test Locality",
                                "city": "New Delhi",
                                "state": "Delhi",
                                "country": "IND",
                                "area_code": "110037"
                            }
                        },
                        "contact": {
                            "phone": "9876543210",
                            "email": "test@neo-server.rozana.in"
                        }
                    }
                },
                "quote": {
                    "price": {
                        "currency": "INR",
                        "value": "200.00"
                    },
                    "breakup": [
                        {
                            "title": "Test Product for Pramaan",
                            "price": {
                                "currency": "INR",
                                "value": "200.00"
                            }
                        }
                    ]
                },
                "payment": {
                    "type": "PRE-PAID",
                    "collected_by": "BAP",
                    "status": "NOT-PAID"
                }
            }
        }
    }
    
    print("🎯 Sending SELECT call to Pramaan Store")
    print("=" * 50)
    print(f"BPP ID: {bpp_id}")
    print(f"BPP URI: {bpp_uri}")
    print(f"Domain: ONDC:RET10 (Retail)")
    print(f"Environment: preprod")
    print(f"Transaction ID: {transaction_id}")
    print(f"Message ID: {message_id}")
    print(f"Timestamp: {timestamp}")
    print()
    
    # Your BAP endpoint
    bap_endpoint = f"{bap_uri}/select"
    
    print(f"📤 Sending to: {bap_endpoint}")
    print()
    
    try:
        # Send the SELECT request
        response = requests.post(
            bap_endpoint,
            json=select_payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SELECT call successful!")
            
            try:
                response_json = response.json()
                print("\n📋 Response:")
                print(json.dumps(response_json, indent=2))
            except:
                print(f"\n📋 Response: {response.text}")
                
        else:
            print(f"❌ SELECT call failed!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
    
    print("\n" + "=" * 50)
    print("📋 IMPORTANT - Save this Transaction ID:")
    print(f"🔑 Transaction ID: {transaction_id}")
    print("=" * 50)
    
    # Save transaction details to file
    transaction_details = {
        "transaction_id": transaction_id,
        "message_id": message_id,
        "timestamp": timestamp,
        "bpp_id": bpp_id,
        "bpp_uri": bpp_uri,
        "domain": "ONDC:RET10",
        "environment": "preprod",
        "action": "select",
        "payload": select_payload,
        "response_status": response.status_code if 'response' in locals() else None,
        "response_body": response.text if 'response' in locals() else None
    }
    
    filename = f"pramaan_select_transaction_{transaction_id.replace('-', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(transaction_details, f, indent=2)
    
    print(f"💾 Transaction details saved to: {filename}")
    
    return transaction_id

if __name__ == "__main__":
    print("🚀 Pramaan SELECT Call Generator")
    print("Domain: ONDC:RET10 (Retail)")
    print("Environment: preprod")
    print("BPP: pramaan.ondc.org/beta/preprod/mock/seller")
    print()
    
    transaction_id = send_select_call()
    
    if transaction_id:
        print(f"\n🎯 SUCCESS!")
        print(f"Transaction ID: {transaction_id}")
        print("\n📋 Next Steps:")
        print("1. Note down this transaction ID for Pramaan testing")
        print("2. Use the same transaction_id for subsequent calls in this flow")
        print("3. This matches the domain (RET10) and environment (preprod) requirements")
    else:
        print("\n❌ Failed to send SELECT call")
        sys.exit(1)