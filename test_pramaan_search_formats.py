#!/usr/bin/env python3
"""
Test Different Search Formats for Pramaan
==========================================

This script tries different search request formats to find what Pramaan accepts
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

def test_search_format(format_name, search_payload):
    """Test a specific search format"""
    url = "https://pramaan.ondc.org/beta/preprod/mock/buyer/search"
    
    print(f"\n🧪 TESTING: {format_name}")
    print("=" * 50)
    print("📤 Request:")
    print(json.dumps(search_payload, indent=2))
    
    try:
        data = json.dumps(search_payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            
            print(f"\n📥 Response: {status_code} ✅")
            if len(response_body) > 200:
                print(f"Body: {response_body[:200]}...")
            else:
                print(f"Body: {response_body}")
            
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n📥 Response: {e.code} ❌")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error: {error_body}")
        except:
            print("No error details available")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def main():
    """Test different search formats"""
    print("🎯 TESTING DIFFERENT SEARCH FORMATS FOR PRAMAAN")
    print("=" * 70)
    
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = get_timestamp()
    
    # Format 1: Minimal search (just payment)
    format1 = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND", 
            "city": "std:080",
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": "pramaan.ondc.org/beta/preprod/mock/buyer",
            "bap_uri": "https://pramaan.ondc.org/beta/preprod/mock/buyer",
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
    
    # Format 2: Category search
    format2 = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:080", 
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": "pramaan.ondc.org/beta/preprod/mock/buyer",
            "bap_uri": "https://pramaan.ondc.org/beta/preprod/mock/buyer",
            "transaction_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "timestamp": get_timestamp(),
            "ttl": "PT30S"
        },
        "message": {
            "intent": {
                "category": {
                    "id": "Foodgrains"
                },
                "fulfillment": {
                    "type": "Delivery"
                },
                "payment": {
                    "@ondc/org/buyer_app_finder_fee_type": "percent",
                    "@ondc/org/buyer_app_finder_fee_amount": "3"
                }
            }
        }
    }
    
    # Format 3: Location-based search
    format3 = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:080",
            "action": "search", 
            "core_version": "1.2.0",
            "bap_id": "pramaan.ondc.org/beta/preprod/mock/buyer",
            "bap_uri": "https://pramaan.ondc.org/beta/preprod/mock/buyer",
            "transaction_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "timestamp": get_timestamp(),
            "ttl": "PT30S"
        },
        "message": {
            "intent": {
                "fulfillment": {
                    "type": "Delivery",
                    "end": {
                        "location": {
                            "gps": "12.9716,77.5946",
                            "address": {
                                "area_code": "560001"
                            }
                        }
                    }
                },
                "payment": {
                    "@ondc/org/buyer_app_finder_fee_type": "percent",
                    "@ondc/org/buyer_app_finder_fee_amount": "3"
                }
            }
        }
    }
    
    # Format 4: Empty intent (just context)
    format4 = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:080",
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": "pramaan.ondc.org/beta/preprod/mock/buyer",
            "bap_uri": "https://pramaan.ondc.org/beta/preprod/mock/buyer",
            "transaction_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "timestamp": get_timestamp(),
            "ttl": "PT30S"
        },
        "message": {
            "intent": {}
        }
    }
    
    # Format 5: Just fulfillment
    format5 = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:080",
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": "pramaan.ondc.org/beta/preprod/mock/buyer",
            "bap_uri": "https://pramaan.ondc.org/beta/preprod/mock/buyer",
            "transaction_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "timestamp": get_timestamp(),
            "ttl": "PT30S"
        },
        "message": {
            "intent": {
                "fulfillment": {
                    "type": "Delivery"
                }
            }
        }
    }
    
    # Test all formats
    formats = [
        ("Format 1: Minimal (Payment only)", format1),
        ("Format 2: Category search", format2), 
        ("Format 3: Location-based search", format3),
        ("Format 4: Empty intent", format4),
        ("Format 5: Just fulfillment", format5)
    ]
    
    results = []
    for name, payload in formats:
        success = test_search_format(name, payload)
        results.append((name, success))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY:")
    print("=" * 70)
    
    successful = [name for name, success in results if success]
    failed = [name for name, success in results if not success]
    
    print(f"✅ Successful formats: {len(successful)}")
    for name in successful:
        print(f"   • {name}")
    
    print(f"\n❌ Failed formats: {len(failed)}")
    for name in failed:
        print(f"   • {name}")
    
    if successful:
        print(f"\n🎉 FOUND WORKING FORMAT! Use: {successful[0]}")
    else:
        print(f"\n⚠️  No formats worked. May need different approach.")

if __name__ == "__main__":
    main()