#!/usr/bin/env python3
"""
Complete ONDC API Testing Framework
Test ALL ONDC APIs including Pramaan, Registry, Local BAP, and more
"""

import requests
import json
import time
import uuid
import base64
from datetime import datetime, timezone
from nacl.signing import SigningKey

def crypto_sign_ed25519_sk_to_seed(sk):
    """Convert Ed25519 private key to seed"""
    return sk[:32]

class CompleteONDCTester:
    def __init__(self):
        # ONDC Registry URLs
        self.preprod_registry = "https://preprod.registry.ondc.org"
        self.staging_registry = "https://staging.registry.ondc.org"
        self.prod_registry = "https://registry.ondc.org"
        
        # Pramaan URLs
        self.pramaan_url = "https://pramaan.ondc.org"
        
        # Local BAP URLs
        self.local_bap = "http://localhost:8000"
        self.public_bap = "https://neo-server.rozana.in"
        
        # Subscriber details
        self.subscriber_id = "neo-server.rozana.in"
        
        # Load keys
        self.load_keys()
        
    def load_keys(self):
        """Load cryptographic keys"""
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
    
    def generate_authorization_header(self, payload: str) -> str:
        """Generate authorization header with signature"""
        signature = self.generate_signature(payload)
        timestamp = str(int(time.time()))
        
        auth_string = f'Signature keyId="{self.subscriber_id}",algorithm="ed25519",headers="(created) (expires) digest",signature="{signature}",created="{timestamp}",expires="{int(time.time()) + 300}"'
        return auth_string
    
    def save_response(self, test_name: str, url: str, request_data: dict, response, method: str = "GET"):
        """Save request and response data"""
        try:
            timestamp = int(time.time())
            filename = f'ondc_test_{test_name.lower().replace(" ", "_")}_{timestamp}.json'
            
            response_data = {
                'test_name': test_name,
                'url': url,
                'method': method,
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
    
    def test_endpoint(self, url: str, method: str = "GET", payload: dict = None, test_name: str = None, auth_required: bool = False):
        """Generic endpoint tester"""
        if not test_name:
            test_name = f"{method} {url}"
        
        print(f"\n🔍 Testing {test_name}")
        print("=" * 50)
        print(f"URL: {url}")
        print(f"Method: {method}")
        
        headers = {
            'Content-Type': 'application/json',
            'X-Request-ID': str(uuid.uuid4())
        }
        
        # Add authorization if required
        if auth_required and payload:
            payload_str = json.dumps(payload, separators=(',', ':'))
            auth_header = self.generate_authorization_header(payload_str)
            headers['Authorization'] = auth_header
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=payload, headers=headers, timeout=30)
            else:
                print(f"❌ Unsupported method: {method}")
                return False
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:500]}{'...' if len(response.text) > 500 else ''}")
            
            # Save response
            self.save_response(test_name, url, payload or {}, response, method)
            
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return False
    
    # ===== PRAMAAN API TESTS =====
    
    def test_pramaan_health(self):
        """Test Pramaan health endpoint"""
        return self.test_endpoint(f"{self.pramaan_url}/health", "GET", test_name="Pramaan Health Check")
    
    def test_pramaan_discovery(self):
        """Test Pramaan API discovery"""
        discovery_endpoints = [
            "/",
            "/api",
            "/v1",
            "/docs",
            "/swagger",
            "/openapi",
            "/api-docs"
        ]
        
        results = []
        for endpoint in discovery_endpoints:
            success = self.test_endpoint(f"{self.pramaan_url}{endpoint}", "GET", test_name=f"Pramaan Discovery - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_pramaan_ekyc_endpoints(self):
        """Test Pramaan eKYC endpoints with multiple variants"""
        print("\n🆔 Testing Pramaan eKYC Endpoints")
        print("=" * 50)
        
        # Test payload
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
                    }
                }
            }
        }
        
        # Test multiple endpoint variants
        endpoints = [
            "/ekyc/search",
            "/api/ekyc/search", 
            "/v1/ekyc/search",
            "/search",
            "/kyc/search",
            "/ekyc/initiate",
            "/api/ekyc/initiate",
            "/v1/ekyc/initiate",
            "/initiate",
            "/kyc/initiate"
        ]
        
        results = []
        for endpoint in endpoints:
            success = self.test_endpoint(f"{self.pramaan_url}{endpoint}", "POST", payload, f"Pramaan eKYC - {endpoint}", auth_required=True)
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    # ===== ONDC REGISTRY TESTS =====
    
    def test_registry_health(self):
        """Test ONDC Registry health endpoints"""
        print("\n🏥 Testing ONDC Registry Health")
        print("=" * 50)
        
        registry_urls = [
            (f"{self.preprod_registry}/health", "Pre-Production Registry"),
            (f"{self.staging_registry}/health", "Staging Registry"),
            (f"{self.prod_registry}/health", "Production Registry")
        ]
        
        results = []
        for url, name in registry_urls:
            success = self.test_endpoint(url, "GET", test_name=f"Registry Health - {name}")
            results.append((name, success))
        
        return any(success for _, success in results)
    
    def test_registry_discovery(self):
        """Test ONDC Registry discovery endpoints"""
        print("\n🔍 Testing ONDC Registry Discovery")
        print("=" * 50)
        
        discovery_endpoints = [
            "/",
            "/api",
            "/v1",
            "/docs",
            "/swagger",
            "/openapi"
        ]
        
        results = []
        for endpoint in discovery_endpoints:
            # Test preprod
            success = self.test_endpoint(f"{self.preprod_registry}{endpoint}", "GET", test_name=f"Preprod Registry Discovery - {endpoint}")
            results.append((f"preprod{endpoint}", success))
            
            # Test staging
            success = self.test_endpoint(f"{self.staging_registry}{endpoint}", "GET", test_name=f"Staging Registry Discovery - {endpoint}")
            results.append((f"staging{endpoint}", success))
        
        return any(success for _, success in results)
    
    def test_registry_subscribe(self):
        """Test ONDC Registry subscribe endpoint"""
        print("\n📝 Testing ONDC Registry Subscribe")
        print("=" * 50)
        
        # Create subscribe payload
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        valid_from = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        valid_until = datetime.now(timezone.utc).replace(year=datetime.now().year + 1).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        payload = {
            "context": {
                "operation": {
                    "ops_no": 1
                }
            },
            "message": {
                "request_id": str(uuid.uuid4()),
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
        
        # Test both environments
        results = []
        
        # Preprod
        success = self.test_endpoint(f"{self.preprod_registry}/ondc/subscribe", "POST", payload, "Registry Subscribe - Preprod", auth_required=True)
        results.append(("Preprod", success))
        
        # Staging
        success = self.test_endpoint(f"{self.staging_registry}/ondc/subscribe", "POST", payload, "Registry Subscribe - Staging", auth_required=True)
        results.append(("Staging", success))
        
        return any(success for _, success in results)
    
    def test_registry_lookup(self):
        """Test ONDC Registry lookup endpoints"""
        print("\n🔍 Testing ONDC Registry Lookup")
        print("=" * 50)
        
        # Test lookup endpoints
        lookup_urls = [
            (f"{self.preprod_registry}/ondc/lookup", "Preprod Lookup"),
            (f"{self.staging_registry}/ondc/lookup", "Staging Lookup"),
            (f"{self.prod_registry}/ondc/lookup", "Production Lookup")
        ]
        
        # Test payload
        payload = {
            "subscriber_id": self.subscriber_id
        }
        
        results = []
        for url, name in lookup_urls:
            success = self.test_endpoint(url, "POST", payload, f"Registry Lookup - {name}", auth_required=True)
            results.append((name, success))
        
        return any(success for _, success in results)
    
    # ===== LOCAL BAP TESTS =====
    
    def test_local_bap_health(self):
        """Test local BAP health endpoint"""
        return self.test_endpoint(f"{self.local_bap}/health", "GET", test_name="Local BAP Health Check")
    
    def test_local_bap_endpoints(self):
        """Test local BAP endpoints"""
        print("\n🏠 Testing Local BAP Endpoints")
        print("=" * 50)
        
        local_endpoints = [
            "/",
            "/health",
            "/api/health",
            "/v1/health",
            "/docs",
            "/openapi.json"
        ]
        
        results = []
        for endpoint in local_endpoints:
            success = self.test_endpoint(f"{self.local_bap}{endpoint}", "GET", test_name=f"Local BAP - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_public_bap_health(self):
        """Test public BAP health endpoint"""
        return self.test_endpoint(f"{self.public_bap}/health", "GET", test_name="Public BAP Health Check")
    
    def test_public_bap_endpoints(self):
        """Test public BAP endpoints"""
        print("\n🌐 Testing Public BAP Endpoints")
        print("=" * 50)
        
        public_endpoints = [
            "/",
            "/health",
            "/api/health",
            "/v1/health",
            "/docs",
            "/openapi.json"
        ]
        
        results = []
        for endpoint in public_endpoints:
            success = self.test_endpoint(f"{self.public_bap}{endpoint}", "GET", test_name=f"Public BAP - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_ondc_site_verification(self):
        """Test ONDC site verification file"""
        print("\n✅ Testing ONDC Site Verification")
        print("=" * 50)
        
        verification_urls = [
            f"{self.public_bap}/ondc-site-verification.html",
            f"{self.public_bap}/.well-known/ondc-site-verification.html",
            f"{self.public_bap}/ondc/ondc-site-verification.html"
        ]
        
        results = []
        for url in verification_urls:
            success = self.test_endpoint(url, "GET", test_name=f"Site Verification - {url}")
            results.append((url, success))
        
        return any(success for _, success in results)
    
    # ===== PRAMAAN API TESTS =====
    
    def test_pramaan_health(self):
        """Test Pramaan health endpoint"""
        return self.test_endpoint(f"{self.pramaan_url}/health", "GET", test_name="Pramaan Health Check")
    
    def test_pramaan_discovery(self):
        """Test Pramaan API discovery"""
        discovery_endpoints = [
            "/",
            "/api",
            "/v1",
            "/docs",
            "/swagger",
            "/openapi",
            "/api-docs"
        ]
        
        results = []
        for endpoint in discovery_endpoints:
            success = self.test_endpoint(f"{self.pramaan_url}{endpoint}", "GET", test_name=f"Pramaan Discovery - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_pramaan_ekyc_endpoints(self):
        """Test Pramaan eKYC endpoints with multiple variants"""
        print("\n🆔 Testing Pramaan eKYC Endpoints")
        print("=" * 50)
        
        # Test payload
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
                    }
                }
            }
        }
        
        # Test multiple endpoint variants
        endpoints = [
            "/ekyc/search",
            "/api/ekyc/search", 
            "/v1/ekyc/search",
            "/search",
            "/kyc/search",
            "/ekyc/initiate",
            "/api/ekyc/initiate",
            "/v1/ekyc/initiate",
            "/initiate",
            "/kyc/initiate"
        ]
        
        results = []
        for endpoint in endpoints:
            success = self.test_endpoint(f"{self.pramaan_url}{endpoint}", "POST", payload, f"Pramaan eKYC - {endpoint}", auth_required=True)
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    # ===== ONDC REGISTRY TESTS =====
    
    def test_registry_health(self):
        """Test ONDC Registry health endpoints"""
        print("\n🏥 Testing ONDC Registry Health")
        print("=" * 50)
        
        registry_urls = [
            (f"{self.preprod_registry}/health", "Pre-Production Registry"),
            (f"{self.staging_registry}/health", "Staging Registry"),
            (f"{self.prod_registry}/health", "Production Registry")
        ]
        
        results = []
        for url, name in registry_urls:
            success = self.test_endpoint(url, "GET", test_name=f"Registry Health - {name}")
            results.append((name, success))
        
        return any(success for _, success in results)
    
    def test_registry_discovery(self):
        """Test ONDC Registry discovery endpoints"""
        print("\n🔍 Testing ONDC Registry Discovery")
        print("=" * 50)
        
        discovery_endpoints = [
            "/",
            "/api",
            "/v1",
            "/docs",
            "/swagger",
            "/openapi"
        ]
        
        results = []
        for endpoint in discovery_endpoints:
            # Test preprod
            success = self.test_endpoint(f"{self.preprod_registry}{endpoint}", "GET", test_name=f"Preprod Registry Discovery - {endpoint}")
            results.append((f"preprod{endpoint}", success))
            
            # Test staging
            success = self.test_endpoint(f"{self.staging_registry}{endpoint}", "GET", test_name=f"Staging Registry Discovery - {endpoint}")
            results.append((f"staging{endpoint}", success))
        
        return any(success for _, success in results)
    
    def test_registry_subscribe(self):
        """Test ONDC Registry subscribe endpoint"""
        print("\n📝 Testing ONDC Registry Subscribe")
        print("=" * 50)
        
        # Create subscribe payload
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        valid_from = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        valid_until = datetime.now(timezone.utc).replace(year=datetime.now().year + 1).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        payload = {
            "context": {
                "operation": {
                    "ops_no": 1
                }
            },
            "message": {
                "request_id": str(uuid.uuid4()),
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
        
        # Test both environments
        results = []
        
        # Preprod
        success = self.test_endpoint(f"{self.preprod_registry}/ondc/subscribe", "POST", payload, "Registry Subscribe - Preprod", auth_required=True)
        results.append(("Preprod", success))
        
        # Staging
        success = self.test_endpoint(f"{self.staging_registry}/ondc/subscribe", "POST", payload, "Registry Subscribe - Staging", auth_required=True)
        results.append(("Staging", success))
        
        return any(success for _, success in results)
    
    def test_registry_lookup(self):
        """Test ONDC Registry lookup endpoints"""
        print("\n🔍 Testing ONDC Registry Lookup")
        print("=" * 50)
        
        # Test lookup endpoints
        lookup_urls = [
            (f"{self.preprod_registry}/ondc/lookup", "Preprod Lookup"),
            (f"{self.staging_registry}/ondc/lookup", "Staging Lookup"),
            (f"{self.prod_registry}/ondc/lookup", "Production Lookup")
        ]
        
        # Test payload
        payload = {
            "subscriber_id": self.subscriber_id
        }
        
        results = []
        for url, name in lookup_urls:
            success = self.test_endpoint(url, "POST", payload, f"Registry Lookup - {name}", auth_required=True)
            results.append((name, success))
        
        return any(success for _, success in results)
    
    # ===== LOCAL BAP TESTS =====
    
    def test_local_bap_health(self):
        """Test local BAP health endpoint"""
        return self.test_endpoint(f"{self.local_bap}/health", "GET", test_name="Local BAP Health Check")
    
    def test_local_bap_endpoints(self):
        """Test local BAP endpoints"""
        print("\n🏠 Testing Local BAP Endpoints")
        print("=" * 50)
        
        local_endpoints = [
            "/",
            "/health",
            "/api/health",
            "/v1/health",
            "/docs",
            "/openapi.json"
        ]
        
        results = []
        for endpoint in local_endpoints:
            success = self.test_endpoint(f"{self.local_bap}{endpoint}", "GET", test_name=f"Local BAP - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_public_bap_health(self):
        """Test public BAP health endpoint"""
        return self.test_endpoint(f"{self.public_bap}/health", "GET", test_name="Public BAP Health Check")
    
    def test_public_bap_endpoints(self):
        """Test public BAP endpoints"""
        print("\n🌐 Testing Public BAP Endpoints")
        print("=" * 50)
        
        public_endpoints = [
            "/",
            "/health",
            "/api/health",
            "/v1/health",
            "/docs",
            "/openapi.json"
        ]
        
        results = []
        for endpoint in public_endpoints:
            success = self.test_endpoint(f"{self.public_bap}{endpoint}", "GET", test_name=f"Public BAP - {endpoint}")
            results.append((endpoint, success))
        
        return any(success for _, success in results)
    
    def test_ondc_site_verification(self):
        """Test ONDC site verification file"""
        print("\n✅ Testing ONDC Site Verification")
        print("=" * 50)
        
        verification_urls = [
            f"{self.public_bap}/ondc-site-verification.html",
            f"{self.public_bap}/.well-known/ondc-site-verification.html",
            f"{self.public_bap}/ondc/ondc-site-verification.html"
        ]
        
        results = []
        for url in verification_urls:
            success = self.test_endpoint(url, "GET", test_name=f"Site Verification - {url}")
            results.append((url, success))
        
        return any(success for _, success in results)
    
    # ===== COMPREHENSIVE TEST RUNNER =====
    
    def run_complete_test_suite(self):
        """Run complete ONDC API test suite"""
        print("🚀 Complete ONDC API Testing Suite")
        print("=" * 70)
        print(f"Subscriber ID: {self.subscriber_id}")
        print(f"Test Time: {datetime.now().isoformat()}")
        print()
        
        # Define all test categories
        test_categories = [
            ("Pramaan Health", self.test_pramaan_health),
            ("Pramaan Discovery", self.test_pramaan_discovery),
            ("Pramaan eKYC", self.test_pramaan_ekyc_endpoints),
            ("Registry Health", self.test_registry_health),
            ("Registry Discovery", self.test_registry_discovery),
            ("Registry Subscribe", self.test_registry_subscribe),
            ("Registry Lookup", self.test_registry_lookup),
            ("Local BAP Health", self.test_local_bap_health),
            ("Local BAP Endpoints", self.test_local_bap_endpoints),
            ("Public BAP Health", self.test_public_bap_health),
            ("Public BAP Endpoints", self.test_public_bap_endpoints),
            ("Site Verification", self.test_ondc_site_verification)
        ]
        
        results = []
        for test_name, test_func in test_categories:
            print(f"\n🧪 Running: {test_name}")
            try:
                success = test_func()
                results.append((test_name, success))
                print(f"   {'✅ PASSED' if success else '❌ FAILED'}")
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                results.append((test_name, False))
            
            time.sleep(1)  # Delay between tests
        
        # Generate comprehensive summary
        self.generate_test_summary(results)
        
        return results
    
    def generate_test_summary(self, results):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 70)
        print("📊 COMPLETE ONDC API TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        # Group results by category
        categories = {
            "Pramaan": [],
            "Registry": [],
            "Local BAP": [],
            "Public BAP": [],
            "Verification": []
        }
        
        for test_name, success in results:
            if "Pramaan" in test_name:
                categories["Pramaan"].append((test_name, success))
            elif "Registry" in test_name:
                categories["Registry"].append((test_name, success))
            elif "Local BAP" in test_name:
                categories["Local BAP"].append((test_name, success))
            elif "Public BAP" in test_name:
                categories["Public BAP"].append((test_name, success))
            elif "Verification" in test_name:
                categories["Verification"].append((test_name, success))
        
        # Print category summaries
        for category, tests in categories.items():
            if tests:
                category_passed = sum(1 for _, success in tests if success)
                category_total = len(tests)
                print(f"\n{category} ({category_passed}/{category_total}):")
                for test_name, success in tests:
                    status = "✅ PASSED" if success else "❌ FAILED"
                    print(f"  {test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All ONDC API tests passed!")
        elif passed > total * 0.7:
            print("✅ Most tests passed. Check failed tests for details.")
        else:
            print("⚠️  Many tests failed. Review the results above.")
        
        # Save summary to file
        timestamp = int(time.time())
        summary_file = f'ondc_complete_test_summary_{timestamp}.json'
        
        with open(summary_file, 'w') as f:
            json.dump({
                'test_time': datetime.now().isoformat(),
                'subscriber_id': self.subscriber_id,
                'total_tests': total,
                'passed_tests': passed,
                'success_rate': passed/total*100,
                'results': results,
                'categories': {k: [(name, success) for name, success in v] for k, v in categories.items()}
            }, f, indent=2)
        
        print(f"\n📄 Complete summary saved to: {summary_file}")

def main():
    """Main function"""
    try:
        tester = CompleteONDCTester()
        tester.run_complete_test_suite()
    except Exception as e:
        print(f"❌ Failed to initialize tester: {e}")
        print("Make sure all key files are present:")
        print("  - secrets/ondc_credentials.json")

if __name__ == "__main__":
    main() 