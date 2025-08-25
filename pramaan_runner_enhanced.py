#!/usr/bin/env python3
"""
Enhanced Pramaan API Testing Framework
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

class EnhancedPramaanAPITester:
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
    
    def save_response(self, test_name: str, request_data: dict, response, endpoint: str):
        """Save request and response data"""
        try:
            timestamp = int(time.time())
            filename = f'pramaan_{test_name.lower().replace(" ", "_")}_{timestamp}.json'
            
            response_data = {
                'test_name': test_name,
                'endpoint': endpoint,
                'request': request_data,
                'response_status': response.status_code,
                'response_headers': dict(response.headers),
                'response_text': response.text,
                'timestamp': datetime.now().isoformat()
            }
            
            # Try to parse JSON response
            try:
                response_data['response_json'] = response.json() if response.text else None
            except:
                response_data['response_json'] = None
            
            with open(filename, 'w') as f:
                json.dump(response_data, f, indent=2)
            
            print(f"   📄 Response saved to: {filename}")
            
        except Exception as e:
            print(f"   ⚠️  Could not save response: {e}")
    
    def test_endpoint(self, endpoint: str, method: str = "GET", payload: dict = None, test_name: str = None):
        """Generic endpoint tester"""
        if not test_name:
            test_name = f"{method} {endpoint}"
        
        print(f"\n🔍 Testing {test_name}")
        print("=" * 50)
        print(f"Endpoint: {self.base_url}{endpoint}")
        print(f"Method: {method}")
        
        headers = {
            'Content-Type': 'application/json',
            'X-Request-ID': str(uuid.uuid4())
        }
        
        # Add authorization if payload exists
        if payload:
            payload_str = json.dumps(payload, separators=(',', ':'))
            auth_header = self.generate_authorization_header(payload_str)
            headers['Authorization'] = auth_header
        
        try:
            if method.upper() == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(f"{self.base_url}{endpoint}", json=payload, headers=headers, timeout=30)
            else:
                print(f"❌ Unsupported method: {method}")
                return False
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:500]}{'...' if len(response.text) > 500 else ''}")
            
            # Save response
            self.save_response(test_name, payload or {}, response, endpoint)
            
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return False
    
    def test_health_check(self):
        """Test Pramaan health endpoint"""
        return self.test_endpoint("/health", "GET", test_name="Health Check")
    
    def test_ekyc_search_variants(self):
        """Test eKYC search with different endpoint variants"""
        print("\n🔍 Testing eKYC Search (Multiple Variants)")
        print("=" * 50)
        
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
        
        endpoints = [
            "/ekyc/search",
            "/api/ekyc/search",
            "/v1/ekyc/search",
            "/search",
            "/kyc/search"
        ]
        
        results = []
        for endpoint in endpoints:
            success = self.test_endpoint(endpoint, "POST", payload, f"eKYC Search - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_ekyc_initiate_variants(self):
        """Test eKYC initiate with different endpoint variants"""
        print("\n🆔 Testing eKYC Initiate (Multiple Variants)")
        print("=" * 50)
        
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
        
        endpoints = [
            "/ekyc/initiate",
            "/api/ekyc/initiate",
            "/v1/ekyc/initiate",
            "/initiate",
            "/kyc/initiate"
        ]
        
        results = []
        for endpoint in endpoints:
            success = self.test_endpoint(endpoint, "POST", payload, f"eKYC Initiate - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_ekyc_verify_variants(self):
        """Test eKYC verify with different endpoint variants"""
        print("\n✅ Testing eKYC Verify (Multiple Variants)")
        print("=" * 50)
        
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
                    "otp": "123456",
                    "auth_code": "mock_auth_code"
                }
            }
        }
        
        endpoints = [
            "/ekyc/verify",
            "/api/ekyc/verify",
            "/v1/ekyc/verify",
            "/verify",
            "/kyc/verify"
        ]
        
        results = []
        for endpoint in endpoints:
            success = self.test_endpoint(endpoint, "POST", payload, f"eKYC Verify - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_ekyc_status_variants(self):
        """Test eKYC status with different endpoint variants"""
        print("\n📊 Testing eKYC Status (Multiple Variants)")
        print("=" * 50)
        
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
        
        endpoints = [
            "/ekyc/status",
            "/api/ekyc/status",
            "/v1/ekyc/status",
            "/status",
            "/kyc/status"
        ]
        
        results = []
        for endpoint in endpoints:
            success = self.test_endpoint(endpoint, "POST", payload, f"eKYC Status - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_ekyc_select_variants(self):
        """Test eKYC select with different endpoint variants"""
        print("\n🎯 Testing eKYC Select (Multiple Variants)")
        print("=" * 50)
        
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
                        "id": "pramaan.ondc.org"
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
        
        endpoints = [
            "/ekyc/select",
            "/api/ekyc/select",
            "/v1/ekyc/select",
            "/select",
            "/kyc/select"
        ]
        
        results = []
        for endpoint in endpoints:
            success = self.test_endpoint(endpoint, "POST", payload, f"eKYC Select - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_api_discovery(self):
        """Test API discovery endpoints"""
        print("\n🔍 Testing API Discovery")
        print("=" * 50)
        
        discovery_endpoints = [
            "/",
            "/api",
            "/v1",
            "/docs",
            "/swagger",
            "/openapi",
            "/api-docs",
            "/health",
            "/status"
        ]
        
        results = []
        for endpoint in discovery_endpoints:
            success = self.test_endpoint(endpoint, "GET", test_name=f"Discovery - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def run_all_tests(self):
        """Run all enhanced Pramaan API tests"""
        print("🚀 Enhanced Pramaan API Testing Suite")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"Subscriber ID: {self.subscriber_id}")
        print()
        
        tests = [
            ("Health Check", self.test_health_check),
            ("API Discovery", self.test_api_discovery),
            ("eKYC Search (Multi-variant)", self.test_ekyc_search_variants),
            ("eKYC Select (Multi-variant)", self.test_ekyc_select_variants),
            ("eKYC Initiate (Multi-variant)", self.test_ekyc_initiate_variants),
            ("eKYC Verify (Multi-variant)", self.test_ekyc_verify_variants),
            ("eKYC Status (Multi-variant)", self.test_ekyc_status_variants)
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
            
            time.sleep(1)  # Delay between tests
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 ENHANCED TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All Pramaan API tests passed!")
        elif passed > 0:
            print("⚠️  Some tests passed. Check the responses for working endpoints.")
        else:
            print("❌ All tests failed. Pramaan APIs may not be available or endpoints have changed.")
        
        return results

def main():
    """Main function"""
    try:
        tester = EnhancedPramaanAPITester()
        tester.run_all_tests()
    except Exception as e:
        print(f"❌ Failed to initialize tester: {e}")
        print("Make sure all key files are present:")
        print("  - ed25519_private_key.txt")
        print("  - x25519_public_key.txt")
        print("  - ondc_request_id.txt")

if __name__ == "__main__":
    main() 