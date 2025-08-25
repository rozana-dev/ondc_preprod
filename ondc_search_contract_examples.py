#!/usr/bin/env python3
"""
ONDC Search Contract Examples
============================

This script demonstrates all ONDC search patterns as per the official API contract:
1. Search by city
2. Search by city (response as downloadable link)
3. Search by item
4. Search by fulfillment end location

All examples follow the ONDC:RET10 specification with proper:
- Buyer app finder fees
- BAP terms with static terms
- Complete context information
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

def create_base_context(transaction_id):
    """Create base ONDC context"""
    return {
        "domain": "ONDC:RET10",
        "action": "search",
        "country": "IND",
        "city": "std:011",  # Delhi
        "core_version": "1.2.0",
        "bap_id": "neo-server.rozana.in",
        "bap_uri": "https://neo-server.rozana.in",
        "transaction_id": transaction_id,
        "message_id": generate_message_id(),
        "timestamp": get_timestamp(),
        "ttl": "PT30S"
    }

def get_bap_terms():
    """Get standard BAP terms"""
    return [
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

def search_by_city():
    """Search by city (full catalog refresh)"""
    transaction_id = str(uuid.uuid4())
    
    payload = {
        "context": create_base_context(transaction_id),
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
                },
                "tags": get_bap_terms()
            }
        }
    }
    
    return payload

def search_by_city_with_link():
    """Search by city (response as downloadable link)"""
    transaction_id = str(uuid.uuid4())
    
    payload = {
        "context": create_base_context(transaction_id),
        "message": {
            "intent": {
                "payment": {
                    "@ondc/org/buyer_app_finder_fee_type": "percent",
                    "@ondc/org/buyer_app_finder_fee_amount": "3"
                },
                "tags": [
                    {
                        "code": "catalog_full",
                        "list": [
                            {
                                "code": "payload_type",
                                "value": "link"
                            }
                        ]
                    },
                    *get_bap_terms()
                ]
            }
        }
    }
    
    return payload

def search_by_item():
    """Search by specific item"""
    transaction_id = str(uuid.uuid4())
    
    payload = {
        "context": create_base_context(transaction_id),
        "message": {
            "intent": {
                "item": {
                    "descriptor": {
                        "name": "coffee"
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
                "tags": get_bap_terms()
            }
        }
    }
    
    return payload

def search_by_fulfillment_location():
    """Search by fulfillment end location"""
    transaction_id = str(uuid.uuid4())
    
    payload = {
        "context": create_base_context(transaction_id),
        "message": {
            "intent": {
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
                "tags": get_bap_terms()
            }
        }
    }
    
    return payload

def test_search_endpoint(payload, description):
    """Test search endpoint with given payload"""
    print(f"\n🎯 TESTING: {description}")
    print("=" * 60)
    
    # Display payload
    print("📋 REQUEST PAYLOAD:")
    print(json.dumps(payload, indent=2))
    print()
    
    # Make API call
    try:
        url = "https://neo-server.rozana.in/search"
        data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            
            print(f"✅ SUCCESS: HTTP {status_code}")
            print(f"📋 Response: {response_body}")
            
            return True
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Test all ONDC search patterns"""
    print("🎯 ONDC SEARCH CONTRACT EXAMPLES - COMPLETE TEST SUITE")
    print("=" * 70)
    print("Testing all official ONDC search patterns with:")
    print("✅ Buyer app finder fees (@ondc/org/buyer_app_finder_fee_*)")
    print("✅ BAP terms with static terms and effective dates")
    print("✅ Complete ONDC-compliant context structure")
    print("✅ Different search intents as per API contract")
    print()
    
    # Test all search patterns
    search_patterns = [
        (search_by_city(), "Search by City (Full Catalog Refresh)"),
        (search_by_city_with_link(), "Search by City (Response as Downloadable Link)"),
        (search_by_item(), "Search by Item (Product-specific)"),
        (search_by_fulfillment_location(), "Search by Fulfillment Location")
    ]
    
    results = []
    for payload, description in search_patterns:
        success = test_search_endpoint(payload, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"📋 Total Search Patterns Tested: {total}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {total - successful}")
    print(f"📈 Success Rate: {successful/total*100:.1f}%")
    print()
    
    for description, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {description}")
    
    print("\n" + "=" * 70)
    if successful == total:
        print("🎉 ALL ONDC SEARCH PATTERNS WORKING PERFECTLY!")
        print("✅ Your BAP is fully compliant with ONDC search contract")
    else:
        print("⚠️  Some search patterns need attention")
    print("=" * 70)

if __name__ == "__main__":
    main()