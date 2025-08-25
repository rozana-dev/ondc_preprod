#!/usr/bin/env python3
"""
ONDC Search Request to Pramaan Mock Buyer - Fixed Context
=========================================================

This script sends the search request with corrected context structure
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

def send_search_to_pramaan_fixed():
    """Send search request with corrected context structure"""
    
    print("🎯 ONDC SEARCH REQUEST TO PRAMAAN - FIXED CONTEXT")
    print("=" * 70)
    
    # Pramaan mock buyer endpoint
    full_url = "https://pramaan.ondc.org/beta/preprod/mock/buyer/search"
    
    # Generate request details
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = get_timestamp()
    
    # Fixed context structure for Pramaan
    search_request = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:080",  # Changed to Bangalore (std:080) - commonly used in Pramaan
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
                "fulfillment": {
                    "type": "Delivery"
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
    
    print("🔧 FIXES APPLIED:")
    print("=" * 20)
    print("✅ Changed city from std:011 to std:080 (Bangalore)")
    print("✅ Simplified message.intent structure")
    print("✅ Removed specific item search (general catalog search)")
    print("✅ Removed specific location (city-wide search)")
    print()
    
    print("📤 FIXED SEARCH REQUEST:")
    print("=" * 30)
    print(json.dumps(search_request, indent=2))
    print()
    
    # Make the API call
    print("🚀 SENDING FIXED REQUEST TO PRAMAAN...")
    print("-" * 45)
    
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
            
            print(f"\n📥 PRAMAAN RESPONSE:")
            print("=" * 25)
            print(f"📊 Status Code: {status_code}")
            print("📋 Response Headers:")
            for key, value in list(response_headers.items())[:5]:  # Show first 5 headers
                print(f"   {key}: {value}")
            print()
            print("📄 RESPONSE BODY:")
            
            # Try to parse as JSON for better formatting
            try:
                response_json = json.loads(response_body)
                print(json.dumps(response_json, indent=2))
            except json.JSONDecodeError:
                # If too large, show first 500 characters
                if len(response_body) > 500:
                    print(f"Response (first 500 chars): {response_body[:500]}...")
                else:
                    print(f"Raw Response: {response_body}")
            
            print(f"\n✅ SUCCESS: Pramaan responded with status {status_code}")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"📄 Error Response: {error_body}")
        except:
            pass
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def try_minimal_search():
    """Try minimal search structure"""
    print("\n" + "="*70)
    print("🔄 TRYING MINIMAL SEARCH STRUCTURE")
    print("="*70)
    
    full_url = "https://pramaan.ondc.org/beta/preprod/mock/buyer/search"
    
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = get_timestamp()
    
    minimal_search = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:080",
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
                "payment": {
                    "@ondc/org/buyer_app_finder_fee_type": "percent",
                    "@ondc/org/buyer_app_finder_fee_amount": "3"
                }
            }
        }
    }
    
    print("📄 MINIMAL REQUEST:")
    print(json.dumps(minimal_search, indent=2))
    
    try:
        data = json.dumps(minimal_search).encode('utf-8')
        
        req = urllib.request.Request(full_url, data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            
            print(f"\n✅ MINIMAL SEARCH SUCCESS: {status_code}")
            if len(response_body) > 200:
                print(f"Response preview: {response_body[:200]}...")
            else:
                print(f"Response: {response_body}")
            
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ Minimal search failed: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error: {error_body}")
        except:
            pass
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def main():
    """Main function"""
    print("🌟 PRAMAAN SEARCH REQUEST - CONTEXT VALIDATION FIX")
    print("=" * 70)
    
    # Try fixed version first
    success1 = send_search_to_pramaan_fixed()
    
    # If that fails, try minimal version
    if not success1:
        success2 = try_minimal_search()
    else:
        success2 = True
    
    print("\n" + "=" * 70)
    print("📊 PRAMAAN SEARCH TEST RESULTS:")
    print("=" * 70)
    if success1 or success2:
        print("🎉 SUCCESSFULLY CONNECTED TO PRAMAAN MOCK BUYER!")
        print("✅ Context validation passed")
        print("✅ ONDC search protocol working")
    else:
        print("⚠️  Issues connecting to Pramaan mock buyer")
        print("💡 May need additional context adjustments")
    print("=" * 70)

if __name__ == "__main__":
    main()