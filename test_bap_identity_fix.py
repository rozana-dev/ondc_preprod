#!/usr/bin/env python3
"""
Test Search with Correct BAP Identity
=====================================

Test using our actual BAP identity while sending to Pramaan endpoint
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

def test_correct_bap_identity():
    """Test with correct BAP identity"""
    url = "https://pramaan.ondc.org/beta/preprod/mock/buyer/search"
    
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = get_timestamp()
    
    # Use our actual BAP identity, not Pramaan's
    search_request = {
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:080",
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": "neo-server.rozana.in",  # Our actual BAP ID
            "bap_uri": "https://neo-server.rozana.in",  # Our actual BAP URI
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
    
    print("🎯 TESTING WITH CORRECT BAP IDENTITY")
    print("=" * 50)
    print(f"📍 Endpoint: {url}")
    print(f"🆔 BAP ID: neo-server.rozana.in (our actual identity)")
    print(f"🔗 BAP URI: https://neo-server.rozana.in (our actual URI)")
    print()
    print("📤 Request:")
    print(json.dumps(search_request, indent=2))
    
    try:
        data = json.dumps(search_request).encode('utf-8')
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            
            print(f"\n📥 SUCCESS: {status_code} ✅")
            if len(response_body) > 300:
                print(f"Response: {response_body[:300]}...")
            else:
                print(f"Response: {response_body}")
            
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

def test_alternative_approach():
    """Test alternative endpoint approach"""
    print("\n" + "="*50)
    print("🔄 TRYING ALTERNATIVE: GATEWAY APPROACH")
    print("="*50)
    
    # Try using ONDC staging gateway instead
    gateway_url = "https://staging.gateway.protean.in/search"
    
    transaction_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())
    timestamp = get_timestamp()
    
    search_request = {
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
    
    print(f"📍 Gateway URL: {gateway_url}")
    print("📤 Request:")
    print(json.dumps(search_request, indent=2))
    
    try:
        data = json.dumps(search_request).encode('utf-8')
        req = urllib.request.Request(gateway_url, data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            
            print(f"\n📥 GATEWAY SUCCESS: {status_code} ✅")
            if len(response_body) > 300:
                print(f"Response: {response_body[:300]}...")
            else:
                print(f"Response: {response_body}")
            
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n📥 Gateway Response: {e.code} ❌")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error: {error_body}")
        except:
            print("No error details available")
        return False
    except Exception as e:
        print(f"\n❌ Gateway Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🌟 TESTING CORRECT BAP IDENTITY APPROACH")
    print("=" * 70)
    
    # Test 1: Correct BAP identity with Pramaan endpoint
    success1 = test_correct_bap_identity()
    
    # Test 2: Alternative gateway approach
    success2 = test_alternative_approach()
    
    print("\n" + "=" * 70)
    print("📊 RESULTS SUMMARY:")
    print("=" * 70)
    
    if success1:
        print("✅ SUCCESS: Pramaan endpoint works with correct BAP identity!")
    elif success2:
        print("✅ SUCCESS: ONDC Gateway approach works!")
    else:
        print("⚠️  Both approaches failed. May need:")
        print("   • BAP registration with ONDC")
        print("   • Authentication tokens")
        print("   • Different endpoint structure")
        print("   • Network participant onboarding")
    
    print("=" * 70)

if __name__ == "__main__":
    main()