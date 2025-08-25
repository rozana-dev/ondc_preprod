#!/usr/bin/env python3
"""
ONDC Search Request to Pramaan Mock Buyer
=========================================

This script sends the search request to the correct Pramaan ONDC mock buyer endpoint
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

def send_search_to_pramaan():
    """Send search request to Pramaan mock buyer endpoint"""
    
    print("🎯 ONDC SEARCH REQUEST TO PRAMAAN MOCK BUYER")
    print("=" * 70)
    
    # Pramaan mock buyer endpoint
    pramaan_buyer_url = "https://pramaan.ondc.org/beta/preprod/mock/buyer"
    search_endpoint = "/search"
    full_url = f"{pramaan_buyer_url}{search_endpoint}"
    
    print("📋 PRAMAAN ENDPOINT DETAILS:")
    print("=" * 35)
    print(f"🌐 Pramaan Base: {pramaan_buyer_url}")
    print(f"🔗 Search Endpoint: {search_endpoint}")
    print(f"🎯 Full URL: {full_url}")
    print(f"🔧 Method: POST")
    print(f"📋 Environment: beta/preprod")
    print()
    
    # Generate request details
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = get_timestamp()
    
    # Create the ONDC-compliant search request for Pramaan
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
    
    print("🔑 REQUEST IDENTIFIERS:")
    print("=" * 25)
    print(f"📊 Transaction ID: {transaction_id}")
    print(f"📧 Message ID: {message_id}")
    print(f"📅 Timestamp: {timestamp}")
    print()
    
    print("📤 SEARCH REQUEST TO PRAMAAN:")
    print("=" * 35)
    print("📄 REQUEST PAYLOAD:")
    print(json.dumps(search_request, indent=2))
    print()
    
    # Make the API call to Pramaan
    print("🚀 SENDING REQUEST TO PRAMAAN...")
    print("-" * 40)
    
    try:
        data = json.dumps(search_request).encode('utf-8')
        
        req = urllib.request.Request(full_url, data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'ONDC-BAP/1.0')
        
        print(f"📡 Making request to: {full_url}")
        
        with urllib.request.urlopen(req, timeout=30) as response:
            status_code = response.getcode()
            response_headers = dict(response.headers)
            response_body = response.read().decode('utf-8')
            
            print("\n📥 PRAMAAN SEARCH RESPONSE:")
            print("=" * 35)
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
            print("✅ SUCCESS: Search request to Pramaan completed!")
            
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"📄 Error Response: {error_body}")
        except:
            pass
        return False
    except urllib.error.URLError as e:
        print(f"\n❌ URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False
    
    finally:
        print("\n" + "=" * 70)
        print("🎯 PRAMAAN SEARCH REQUEST SUMMARY:")
        print("=" * 70)
        print(f"📍 Target URL: {full_url}")
        print(f"🏪 Store Integration: Pramaan Mock Buyer")
        print(f"🌐 Environment: beta/preprod")
        print(f"📋 Domain: ONDC:RET10")
        print(f"🔑 Transaction ID: {transaction_id}")
        print(f"💰 Buyer App Finder Fee: 3%")
        print(f"📄 BAP Terms: Included")
        print(f"📅 Timestamp Format: ONDC Compliant")
        print("=" * 70)

def generate_curl_command():
    """Generate curl command for Pramaan search"""
    
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = get_timestamp()
    
    payload = {
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
    
    print("\n🔧 CURL COMMAND FOR PRAMAAN SEARCH:")
    print("=" * 45)
    curl_cmd = f'''curl -X POST \\
  "https://pramaan.ondc.org/beta/preprod/mock/buyer/search" \\
  -H "Content-Type: application/json" \\
  -H "User-Agent: ONDC-BAP/1.0" \\
  -d '{json.dumps(payload, separators=(',', ':'))}'
'''
    print(curl_cmd)

def main():
    """Main function"""
    print("🌟 ONDC SEARCH REQUEST TO PRAMAAN MOCK BUYER")
    print("=" * 70)
    print("🎯 Sending search request to official Pramaan ONDC mock buyer endpoint")
    print("🌐 Environment: beta/preprod")
    print("🏪 Target: pramaan.ondc.org/beta/preprod/mock/buyer")
    print()
    
    success = send_search_to_pramaan()
    
    # Generate curl command for reference
    generate_curl_command()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 PRAMAAN SEARCH REQUEST COMPLETED SUCCESSFULLY!")
        print("✅ Your BAP successfully communicated with Pramaan mock buyer")
    else:
        print("⚠️  Pramaan search request encountered issues")
        print("💡 Check network connectivity and endpoint availability")
    print("=" * 70)

if __name__ == "__main__":
    main()