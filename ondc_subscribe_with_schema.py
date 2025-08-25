#!/usr/bin/env python3
"""
ONDC Subscribe API with Correct Schema
Generate and send subscribe request using the official ONDC schema
"""

import requests
import json
import time
import uuid
from datetime import datetime, timezone
import base64
from nacl.signing import SigningKey

def crypto_sign_ed25519_sk_to_seed(sk):
    """Convert Ed25519 private key to seed"""
    return sk[:32]

class ONDCSubscribeAPI:
    def __init__(self):
        self.subscriber_id = "neo-server.rozana.in"
        self.preprod_url = "https://preprod.registry.ondc.org/ondc/subscribe"
        self.staging_url = "https://staging.registry.ondc.org/ondc/subscribe"
        self.load_keys()
        
    def load_keys(self):
        """Load cryptographic keys from credentials"""
        try:
            with open('secrets/ondc_credentials.json', 'r') as f:
                creds = json.load(f)
            
            # Load signing key
            private_key_b64 = creds['signing_keys']['private_key']
            private_key_bytes = base64.b64decode(private_key_b64)
            seed = crypto_sign_ed25519_sk_to_seed(private_key_bytes)
            self.signing_key = SigningKey(seed)
            
            # Store keys
            self.signing_public_key = creds['signing_keys']['public_key']
            self.encryption_public_key = creds['encryption_keys']['public_key']
            self.request_id = creds['request_id']
            
            print("✅ Keys loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading keys: {e}")
            raise
    
    def generate_signature(self, payload: str) -> str:
        """Generate Ed25519 signature for payload"""
        signature = self.signing_key.sign(payload.encode('utf-8'))
        return base64.b64encode(signature.signature).decode('utf-8')
    
    def create_subscribe_payload(self, ops_no: int = 1):
        """Create subscribe payload using official schema"""
        
        # Current timestamp in RFC3339 format
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        valid_from = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # Valid for 1 year
        valid_until = datetime.now(timezone.utc).replace(year=datetime.now().year + 1).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        payload = {
            "context": {
                "operation": {
                    "ops_no": ops_no  # 1 = Buyer New entity registration
                }
            },
            "message": {
                "request_id": self.request_id,
                "timestamp": timestamp,
                "entity": {
                    "gst": {
                        "legal_entity_name": "Neo Server Rozana Private Limited",
                        "business_address": "123 Tech Park, Electronic City, Bengaluru, Karnataka 560100",
                        "city_code": ["std:080"],
                        "gst_no": "29AABCN1234N1Z5"
                    },
                    "pan": {
                        "name_as_per_pan": "Neo Server Rozana Private Limited",
                        "pan_no": "AABCN1234N",
                        "date_of_incorporation": "15/06/2020"
                    },
                    "name_of_authorised_signatory": "Authorized Signatory",
                    "address_of_authorised_signatory": "123 Tech Park, Electronic City, Bengaluru, Karnataka 560100",
                    "email_id": "admin@neo-server.rozana.in",
                    "mobile_no": 9876543210,
                    "country": "IND",
                    "subscriber_id": self.subscriber_id,
                    "callback_url": "/on_subscribe",
                    "unique_key_id": f"key_{int(time.time())}",
                    "key_pair": {
                        "signing_public_key": self.signing_public_key,
                        "encryption_public_key": self.encryption_public_key,
                        "valid_from": valid_from,
                        "valid_until": valid_until
                    }
                },
                "network_participant": [
                    {
                        "subscriber_url": "/",
                        "domain": "nic2004:52110",
                        "type": "buyerApp",
                        "msn": False,
                        "city_code": ["std:080"]
                    }
                ]
            }
        }
        
        return payload
    
    def generate_authorization_header(self, payload_str: str) -> str:
        """Generate authorization header with signature"""
        signature = self.generate_signature(payload_str)
        timestamp = str(int(time.time()))
        
        auth_string = f'Signature keyId="{self.subscriber_id}",algorithm="ed25519",headers="(created) (expires) digest",signature="{signature}",created="{timestamp}",expires="{int(time.time()) + 300}"'
        return auth_string
    
    def submit_subscribe_request(self, environment="staging", ops_no=1):
        """Submit subscribe request to ONDC registry"""
        
        url = self.staging_url if environment == "staging" else self.preprod_url
        
        print(f"\n🚀 Submitting ONDC Subscribe Request")
        print("=" * 50)
        print(f"Environment: {environment}")
        print(f"URL: {url}")
        print(f"Operation: {ops_no} (Buyer New entity registration)")
        print(f"Subscriber ID: {self.subscriber_id}")
        
        # Create payload
        payload = self.create_subscribe_payload(ops_no)
        payload_str = json.dumps(payload, separators=(',', ':'))
        
        # Generate authorization header
        auth_header = self.generate_authorization_header(payload_str)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth_header,
            'X-Request-ID': str(uuid.uuid4())
        }
        
        print(f"\n📋 Request Payload:")
        print(json.dumps(payload, indent=2))
        
        try:
            print(f"\n📡 Sending request...")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            print(f"\n📊 Response:")
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Response: {response.text}")
            
            # Save request and response
            timestamp = int(time.time())
            filename = f'subscribe_request_response_{environment}_{timestamp}.json'
            
            with open(filename, 'w') as f:
                json.dump({
                    'environment': environment,
                    'url': url,
                    'request': payload,
                    'request_headers': headers,
                    'response_status': response.status_code,
                    'response_headers': dict(response.headers),
                    'response_text': response.text,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            
            print(f"\n💾 Request and response saved to: {filename}")
            
            # Parse response
            if response.status_code == 200:
                print("✅ Subscribe request successful!")
                try:
                    response_data = response.json()
                    if 'message' in response_data:
                        print(f"Message: {response_data['message']}")
                except:
                    pass
            elif response.status_code == 400:
                print("❌ Bad Request - Check payload format")
            elif response.status_code == 401:
                print("❌ Unauthorized - Check authentication")
            elif response.status_code == 403:
                print("❌ Forbidden - Check permissions")
            else:
                print(f"⚠️  Unexpected response: {response.status_code}")
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return False
    
    def test_preprod_only(self):
        """Test subscribe API on preprod environment only"""
        print("🧪 Testing ONDC Subscribe API on Pre-Production Environment")
        print("=" * 60)
        
        # Test preprod only
        print(f"\n🚀 Testing Pre-Production Environment")
        preprod_success = self.submit_subscribe_request("preprod", ops_no=1)
        
        # Summary
        print(f"\n" + "=" * 60)
        print("📊 SUBSCRIBE API TEST SUMMARY")
        print("=" * 60)
        
        status = "✅ SUCCESS" if preprod_success else "❌ FAILED"
        print(f"Pre-Production: {status}")
        
        if preprod_success:
            print(f"\n🎉 Pre-Production environment accepted the subscribe request!")
        else:
            print(f"\n⚠️  Pre-Production environment failed. Check the saved response files for details.")
        
        return preprod_success

def main():
    """Main function"""
    try:
        api = ONDCSubscribeAPI()
        
        # Test preprod environment only
        success = api.test_preprod_only()
        
        if success:
            print("\n🎉 Pre-Production environment accepted the subscribe request!")
        else:
            print("\n⚠️  Pre-Production environment failed. Check the saved response files for details.")
            
    except Exception as e:
        print(f"❌ Failed to initialize API: {e}")

if __name__ == "__main__":
    main()