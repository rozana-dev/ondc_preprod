#!/usr/bin/env python3
"""
Test Search Request with BAP ID and BAP URI
===========================================

This script demonstrates the updated search request that includes:
- BAP ID (Buyer App Platform ID)
- BAP URI (Buyer App Platform URI)
- Complete ONDC context information
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import uuid
from datetime import datetime, timezone

def get_timestamp():
    """Generate ISO timestamp"""
    return datetime.now(timezone.utc).isoformat()

def generate_message_id():
    """Generate unique message ID"""
    return str(uuid.uuid4())

def test_search_with_bap():
    """Test search endpoint with complete BAP information"""
    
    base_url = "https://neo-server.rozana.in"
    transaction_id = str(uuid.uuid4())
    
    print("🎯 TESTING SEARCH REQUEST WITH BAP ID/URI")
    print("=" * 50)
    print(f"🌐 Base URL: {base_url}")
    print(f"🔑 Transaction ID: {transaction_id}")
    print()
    
    # Complete search payload with BAP information
    search_payload = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND", 
            "city": "std:011",
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": "neo-server.rozana.in",        # ✅ BAP ID included
            "bap_uri": "https://neo-server.rozana.in", # ✅ BAP URI included
            "transaction_id": transaction_id,
            "message_id": generate_message_id(),
            "timestamp": get_timestamp(),
            "ttl": "PT30S"
            # Note: No bpp_id/bpp_uri in search (we're searching FOR BPPs)
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
                    "type": "PRE-PAID"
                }
            }
        }
    }
    
    print("📋 REQUEST PAYLOAD:")
    print("=" * 30)
    print("✅ Complete context with BAP information:")
    print(f"   • Domain: {search_payload['context']['domain']}")
    print(f"   • Country: {search_payload['context']['country']}")
    print(f"   • City: {search_payload['context']['city']}")
    print(f"   • Action: {search_payload['context']['action']}")
    print(f"   • Core Version: {search_payload['context']['core_version']}")
    print(f"   • 🎯 BAP ID: {search_payload['context']['bap_id']}")
    print(f"   • 🎯 BAP URI: {search_payload['context']['bap_uri']}")
    print(f"   • Transaction ID: {search_payload['context']['transaction_id']}")
    print(f"   • Message ID: {search_payload['context']['message_id']}")
    print(f"   • TTL: {search_payload['context']['ttl']}")
    print()
    
    print("📄 FULL JSON REQUEST:")
    print(json.dumps(search_payload, indent=2))
    print()
    
    # Make the API call
    print("🚀 MAKING API CALL...")
    print("-" * 25)
    
    try:
        url = f"{base_url}/search"
        data = json.dumps(search_payload).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            
            print(f"✅ SUCCESS!")
            print(f"   Status Code: {status_code}")
            print(f"   Response: {response_body}")
            
            return True
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main function"""
    print("🎯 ONDC SEARCH REQUEST WITH BAP ID/URI TEST")
    print("=" * 60)
    print("Testing the updated search request that includes:")
    print("✅ BAP ID (Buyer App Platform ID)")
    print("✅ BAP URI (Buyer App Platform URI)")  
    print("✅ Complete ONDC context information")
    print("✅ No BPP info (since we're searching FOR BPPs)")
    print()
    
    success = test_search_with_bap()
    
    print()
    print("=" * 60)
    if success:
        print("🎉 SEARCH REQUEST WITH BAP ID/URI SUCCESSFUL!")
        print("✅ Your ONDC search now includes complete BAP identification")
    else:
        print("⚠️  Search request failed - check endpoint availability")
    print("=" * 60)

if __name__ == "__main__":
    main()