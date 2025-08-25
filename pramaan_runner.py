#!/usr/bin/env python3
"""
Pramaan API Testing Framework
Test ONDC Pramaan APIs with proper authentication and signing
"""

import requests
import json
import time
import uuid
import base64
from datetime import datetime, timezone
from nacl.signing import SigningKey
from nacl.public import PrivateKey, PublicKey
from nacl.utils import random
from nacl.secret import SecretBox
import hashlib
import hmac

def crypto_sign_ed25519_sk_to_seed(sk):
    """Convert Ed25519 private key to seed"""
    return sk[:32]

class PramaanAPITester:
    def __init__(self):
        self.base_url = "https://pramaan.ondc.org"
        self.subscriber_id = "neo-server.rozana.in"
        self.load_keys()
        
    def load_keys(self):
        """Load cryptographic keys"""
        try:
            # Load Ed25519 signing key
            with open('ed25519_private_key.txt', 'r') as f:
                private_key_b64 = f.read().strip()
            private_key_bytes = base64.b64decode(private_key_b64)
            seed = crypto_sign_ed25519_sk_to_seed(private_key_bytes)
            self.signing_key = SigningKey(seed)
            
            # Load X25519 public key (as string, not object)
            with open('x25519_public_key.txt', 'r') as f:
                self.encryption_public_key = f.read().strip()
            
            # Load request ID
            with open('ondc_request_id.txt', 'r') as f:
                self.request_id = f.read().strip()
                
            print("✅ Keys loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading keys: {e}")
            raise
    
    def generate_signature(self, payload: str) -> str:
        """Generate Ed25519 signature for payload"""
        signature = self.signing_key.sign(payload.encode('utf-8'))
        return base64.b64encode(signature.signature).decode('utf-8')
    
    def generate_authorization_header(self, payload: str) -> str:
        """Generate authorization header with signature"""
        signature = self.generate_signature(payload)
        timestamp = str(int(time.time()))
        
        auth_string = f'Signature keyId="{self.subscriber_id}",algorithm="ed25519",headers="(created) (expires) digest",signature="{signature}",created="{timestamp}",expires="{int(time.time()) + 300}"'
        return auth_string
    
    def test_health_check(self):
        """Test Pramaan health endpoint"""
        print("\n🏥 Testing Pramaan Health Check")
        print("=" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_ekyc_initiate(self):
        """Test eKYC initiation"""
        print("\n🆔 Testing eKYC Initiate")
        print("=" * 40)
        
        payload = {
            "context": {
                "domain": "ONDC:RET10",
                "country": "IND",
                "city": "std:011",
                "action": "initiate",
                "core_version": "1.2.0",
                "bap_id": self.subscriber_id,
                "bap_uri": f"https://{self.subscriber_id}",
                "transaction_id": str(uuid.uuid4()),
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ttl": "PT30S"
            },
            "message": {
                "transaction_id": str(uuid.uuid4()),
                "init": {
                    "requester": {
                        "type": "CONSUMER",
                        "id": "consumer@example.com"
                    },
                    "purpose": {
                        "code": "KYC",
                        "text": "Know Your Customer verification"
                    },
                    "auth": {
                        "type": "OTP",
                        "purpose": "KYC"
                    }
                }
            }
        }
        
        payload_str = json.dumps(payload, separators=(',', ':'))
        auth_header = self.generate_authorization_header(payload_str)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth_header,
            'X-Request-ID': str(uuid.uuid4())
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/initiate",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2) if response.text else response.text}")
            
            # Save response
            timestamp = int(time.time())
            with open(f'pramaan_ekyc_initiate_response_{timestamp}.json', 'w') as f:
                json.dump({
                    'request': payload,
                    'response': response.json() if response.text else response.text,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"❌ eKYC initiate failed: {e}")
            return False
    
    def test_ekyc_verify(self, transaction_id: str = None):
        """Test eKYC verification"""
        print("\n✅ Testing eKYC Verify")
        print("=" * 40)
        
        if not transaction_id:
            transaction_id = str(uuid.uuid4())
        
        payload = {
            "context": {
                "domain": "ONDC:RET10",
                "country": "IND",
                "city": "std:011",
                "action": "verify",
                "core_version": "1.2.0",
                "bap_id": self.subscriber_id,
                "bap_uri": f"https://{self.subscriber_id}",
                "transaction_id": transaction_id,
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ttl": "PT30S"
            },
            "message": {
                "transaction_id": transaction_id,
                "verify": {
                    "otp": "123456",  # Mock OTP
                    "auth_code": "mock_auth_code"
                }
            }
        }
        
        payload_str = json.dumps(payload, separators=(',', ':'))
        auth_header = self.generate_authorization_header(payload_str)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth_header,
            'X-Request-ID': str(uuid.uuid4())
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/verify",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2) if response.text else response.text}")
            
            # Save response
            timestamp = int(time.time())
            with open(f'pramaan_ekyc_verify_response_{timestamp}.json', 'w') as f:
                json.dump({
                    'request': payload,
                    'response': response.json() if response.text else response.text,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"❌ eKYC verify failed: {e}")
            return False
    
    def test_ekyc_status(self, transaction_id: str = None):
        """Test eKYC status check"""
        print("\n📊 Testing eKYC Status")
        print("=" * 40)
        
        if not transaction_id:
            transaction_id = str(uuid.uuid4())
        
        payload = {
            "context": {
                "domain": "ONDC:RET10",
                "country": "IND",
                "city": "std:011",
                "action": "status",
                "core_version": "1.2.0",
                "bap_id": self.subscriber_id,
                "bap_uri": f"https://{self.subscriber_id}",
                "transaction_id": transaction_id,
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ttl": "PT30S"
            },
            "message": {
                "transaction_id": transaction_id
            }
        }
        
        payload_str = json.dumps(payload, separators=(',', ':'))
        auth_header = self.generate_authorization_header(payload_str)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth_header,
            'X-Request-ID': str(uuid.uuid4())
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/status",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2) if response.text else response.text}")
            
            # Save response
            timestamp = int(time.time())
            with open(f'pramaan_ekyc_status_response_{timestamp}.json', 'w') as f:
                json.dump({
                    'request': payload,
                    'response': response.json() if response.text else response.text,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"❌ eKYC status failed: {e}")
            return False
    
    def test_ekyc_search(self):
        """Test eKYC search"""
        print("\n🔍 Testing eKYC Search")
        print("=" * 40)
        
        payload = {
            "context": {
                "domain": "ONDC:RET10",
                "country": "IND",
                "city": "std:011",
                "action": "search",
                "core_version": "1.2.0",
                "bap_id": self.subscriber_id,
                "bap_uri": f"https://{self.subscriber_id}",
                "transaction_id": str(uuid.uuid4()),
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ttl": "PT30S"
            },
            "message": {
                "intent": {
                    "fulfillment": {
                        "type": "KYC",
                        "provider": {
                            "id": "pramaan.ondc.org"
                        }
                    },
                    "payment": {
                        "type": "ON-ORDER"
                    }
                }
            }
        }
        
        payload_str = json.dumps(payload, separators=(',', ':'))
        auth_header = self.generate_authorization_header(payload_str)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth_header,
            'X-Request-ID': str(uuid.uuid4())
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/search",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2) if response.text else response.text}")
            
            # Save response
            timestamp = int(time.time())
            with open(f'pramaan_ekyc_search_response_{timestamp}.json', 'w') as f:
                json.dump({
                    'request': payload,
                    'response': response.json() if response.text else response.text,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"❌ eKYC search failed: {e}")
            return False
    
    def test_ekyc_select(self, provider_id: str = "pramaan.ondc.org"):
        """Test eKYC provider selection"""
        print("\n🎯 Testing eKYC Select")
        print("=" * 40)
        
        payload = {
            "context": {
                "domain": "ONDC:RET10",
                "country": "IND",
                "city": "std:011",
                "action": "select",
                "core_version": "1.2.0",
                "bap_id": self.subscriber_id,
                "bap_uri": f"https://{self.subscriber_id}",
                "transaction_id": str(uuid.uuid4()),
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ttl": "PT30S"
            },
            "message": {
                "order": {
                    "provider": {
                        "id": provider_id
                    },
                    "items": [
                        {
                            "id": "kyc-service",
                            "descriptor": {
                                "name": "KYC Verification Service"
                            },
                            "price": {
                                "currency": "INR",
                                "value": "0"
                            }
                        }
                    ]
                }
            }
        }
        
        payload_str = json.dumps(payload, separators=(',', ':'))
        auth_header = self.generate_authorization_header(payload_str)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': auth_header,
            'X-Request-ID': str(uuid.uuid4())
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/select",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2) if response.text else response.text}")
            
            # Save response
            timestamp = int(time.time())
            with open(f'pramaan_ekyc_select_response_{timestamp}.json', 'w') as f:
                json.dump({
                    'request': payload,
                    'response': response.json() if response.text else response.text,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"❌ eKYC select failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all Pramaan API tests"""
        print("🚀 Pramaan API Testing Suite")
        print("=" * 50)
        print(f"Base URL: {self.base_url}")
        print(f"Subscriber ID: {self.subscriber_id}")
        print()
        
        tests = [
            ("Health Check", self.test_health_check),
            ("eKYC Search", self.test_ekyc_search),
            ("eKYC Select", self.test_ekyc_select),
            ("eKYC Initiate", self.test_ekyc_initiate),
            ("eKYC Verify", self.test_ekyc_verify),
            ("eKYC Status", self.test_ekyc_status)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🧪 Running: {test_name}")
            try:
                success = test_func()
                results.append((test_name, success))
                print(f"   {'✅ PASSED' if success else '❌ FAILED'}")
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                results.append((test_name, False))
            
            time.sleep(2)  # Delay between tests
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All Pramaan API tests passed!")
        else:
            print("⚠️  Some tests failed. Check the responses above.")
        
        return results

def main():
    """Main function"""
    try:
        tester = PramaanAPITester()
        tester.run_all_tests()
    except Exception as e:
        print(f"❌ Failed to initialize tester: {e}")
        print("Make sure all key files are present:")
        print("  - ed25519_private_key.txt")
        print("  - x25519_private_key.txt")
        print("  - x25519_public_key.txt")
        print("  - ondc_request_id.txt")

if __name__ == "__main__":
    main() 