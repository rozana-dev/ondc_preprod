#!/usr/bin/env python3
"""
ONDC Search API - Request and Response Display
==============================================

This script shows the exact request and response for the ONDC search API
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import uuid
from datetime import datetime, timezone

def get_timestamp():
    """Generate ONDC-compliant timestamp format: YYYY-MM-DDTHH:mm:ss.sssZ"""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def generate_message_id():
    """Generate unique message ID"""
    return str(uuid.uuid4())

def show_search_request_response():
    """Show complete search request and response"""
    
    print("🎯 ONDC SEARCH API - REQUEST AND RESPONSE")
    print("=" * 70)
    
    # Create the ONDC-compliant search request
    transaction_id = str(uuid.uuid4())
    
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
            "message_id": generate_message_id(),
            "timestamp": get_timestamp(),
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
    
    # Display the request
    print("📤 SEARCH REQUEST:")
    print("=" * 50)
    print("🌐 URL: https://neo-server.rozana.in/search")
    print("🔧 Method: POST")
    print("📋 Headers:")
    print("   Content-Type: application/json")
    print()
    print("📄 REQUEST BODY (JSON):")
    print(json.dumps(search_request, indent=2))
    print()
    
    # Make the API call to get the actual response
    print("🚀 MAKING API CALL...")
    print("-" * 30)
    
    try:
        url = "https://neo-server.rozana.in/search"
        data = json.dumps(search_request).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            response_headers = dict(response.headers)
            response_body = response.read().decode('utf-8')
            
            print("📥 SEARCH RESPONSE:")
            print("=" * 50)
            print(f"📊 Status Code: {status_code}")
            print("📋 Response Headers:")
            for key, value in response_headers.items():
                print(f"   {key}: {value}")
            print()
            print("📄 RESPONSE BODY:")
            
            # Try to parse as JSON for better formatting
            try:
                response_json = json.loads(response_body)
                print(json.dumps(response_json, indent=2))
            except json.JSONDecodeError:
                print(f"Raw Response: {response_body}")
            
            print()
            print("✅ SUCCESS: Search request completed successfully!")
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"📄 Error Response: {error_body}")
        except:
            pass
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 70)
    print("🎯 KEY ONDC SEARCH REQUEST FEATURES:")
    print("=" * 70)
    print("✅ BAP Identification:")
    print("   • bap_id: neo-server.rozana.in")
    print("   • bap_uri: https://neo-server.rozana.in")
    print()
    print("✅ ONDC Context:")
    print("   • domain: ONDC:RET10")
    print("   • country: IND")
    print("   • city: std:011")
    print("   • core_version: 1.2.0")
    print("   • ttl: PT30S")
    print()
    print("✅ Buyer App Finder Fees:")
    print("   • @ondc/org/buyer_app_finder_fee_type: percent")
    print("   • @ondc/org/buyer_app_finder_fee_amount: 3")
    print()
    print("✅ BAP Terms:")
    print("   • static_terms: (empty)")
    print("   • static_terms_new: URL to terms PDF")
    print("   • effective_date: 2023-10-01T00:00:00.000Z")
    print()
    print("✅ Search Intent:")
    print("   • Item search by name")
    print("   • Location-based (GPS + area_code)")
    print("   • Delivery fulfillment type")
    print("=" * 70)

if __name__ == "__main__":
    show_search_request_response()