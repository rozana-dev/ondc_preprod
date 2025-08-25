#!/usr/bin/env python3
"""
Quick validation script to test ONDC PreProd endpoints
Run this to verify your setup before using Postman collection
"""

import requests
import json
import time
from datetime import datetime

class ONDCEndpointValidator:
    def __init__(self):
        self.base_url = "https://neo-server.rozana.in"
        self.local_url = "http://localhost:8000"
        self.subscriber_id = "neo-server.rozana.in"
        self.preprod_registry = "https://preprod.registry.ondc.org"
        self.staging_registry = "https://staging.registry.ondc.org"
        self.pramaan_url = "https://pramaan.ondc.org"
        
        self.results = []
    
    def test_endpoint(self, url, method="GET", data=None, expected_status=None, description=""):
        """Test a single endpoint and record results"""
        try:
            print(f"Testing: {description or url}")
            
            if method.upper() == "GET":
                response = requests.get(url, timeout=30)
            else:
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, json=data, headers=headers, timeout=30)
            
            status = "✅ PASS" if response.status_code < 400 else "❌ FAIL"
            
            result = {
                "url": url,
                "method": method,
                "status_code": response.status_code,
                "status": status,
                "description": description,
                "response_size": len(response.text),
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            
            print(f"  Status: {response.status_code} - {status}")
            
            if response.status_code < 400:
                try:
                    json_resp = response.json()
                    if 'status' in json_resp:
                        print(f"  Response: {json_resp.get('status', 'No status field')}")
                except:
                    if len(response.text) > 100:
                        print(f"  Response: HTML/Text ({len(response.text)} chars)")
                    else:
                        print(f"  Response: {response.text[:100]}")
            
            print()
            return True
            
        except requests.exceptions.Timeout:
            print(f"  ⏰ TIMEOUT after 30 seconds")
            self.results.append({
                "url": url, "method": method, "status": "TIMEOUT", 
                "description": description, "timestamp": datetime.now().isoformat()
            })
            print()
            return False
            
        except requests.exceptions.ConnectionError:
            print(f"  🔌 CONNECTION ERROR")
            self.results.append({
                "url": url, "method": method, "status": "CONNECTION_ERROR",
                "description": description, "timestamp": datetime.now().isoformat()
            })
            print()
            return False
            
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            self.results.append({
                "url": url, "method": method, "status": f"ERROR: {str(e)}",
                "description": description, "timestamp": datetime.now().isoformat()
            })
            print()
            return False
    
    def run_health_checks(self):
        """Test all health check endpoints"""
        print("🏥 TESTING HEALTH CHECKS")
        print("=" * 50)
        
        endpoints = [
            (f"{self.base_url}/healthz", "Production Health Check"),
            (f"{self.base_url}/livez", "Production Liveness"),
            (f"{self.base_url}/readyz", "Production Readiness"),
            (f"{self.local_url}/health", "Local Development Health"),
        ]
        
        for url, desc in endpoints:
            self.test_endpoint(url, "GET", description=desc)
    
    def run_subscription_tests(self):
        """Test subscription and verification endpoints"""
        print("🔔 TESTING SUBSCRIPTION & VERIFICATION")
        print("=" * 50)
        
        # Test callback endpoint with challenge
        challenge_payload = {
            "challenge": f"test_challenge_{int(time.time())}",
            "subscriber_id": self.subscriber_id
        }
        
        endpoints = [
            (f"{self.base_url}/v1/bap/on_subscribe/test", "GET", None, "Test Callback Accessibility"),
            (f"{self.base_url}/v1/bap/verification", "GET", None, "Verification Page"),
            (f"{self.base_url}/v1/bap/on_subscribe", "POST", challenge_payload, "Challenge Test"),
        ]
        
        for url, method, data, desc in endpoints:
            self.test_endpoint(url, method, data, description=desc)
    
    def run_onboarding_tests(self):
        """Test onboarding endpoints"""
        print("🚀 TESTING ONBOARDING ENDPOINTS")
        print("=" * 50)
        
        endpoints = [
            (f"{self.base_url}/v1/bap/onboarding/checklist", "GET", None, "Onboarding Checklist"),
            (f"{self.base_url}/v1/bap/onboarding/subscriber-info", "GET", None, "Subscriber Info"),
            (f"{self.base_url}/v1/bap/onboarding/registration-payload", "GET", None, "Registration Payload"),
            (f"{self.base_url}/v1/bap/onboarding/subscribe-payload/pre_prod/1", "GET", None, "PreProd Subscribe Payload"),
        ]
        
        for url, method, data, desc in endpoints:
            self.test_endpoint(url, method, data, description=desc)
    
    def run_registry_tests(self):
        """Test registry endpoints"""
        print("🌐 TESTING REGISTRY ENDPOINTS") 
        print("=" * 50)
        
        # Simple lookup payload
        lookup_payload = {
            "subscriber_id": self.subscriber_id
        }
        
        endpoints = [
            (f"{self.preprod_registry}/health", "GET", None, "PreProd Registry Health"),
            (f"{self.staging_registry}/health", "GET", None, "Staging Registry Health"),
            (f"{self.preprod_registry}/ondc/lookup", "POST", lookup_payload, "PreProd Lookup"),
            (f"{self.staging_registry}/ondc/lookup", "POST", lookup_payload, "Staging Lookup"),
        ]
        
        for url, method, data, desc in endpoints:
            self.test_endpoint(url, method, data, description=desc)
    
    def run_ekyc_tests(self):
        """Test eKYC endpoints"""
        print("🆔 TESTING eKYC ENDPOINTS")
        print("=" * 50)
        
        # Basic eKYC search payload
        search_payload = {
            "context": {
                "domain": "ONDC:RET10",
                "country": "IND",
                "city": "std:080",
                "action": "search",
                "core_version": "1.2.0",
                "bap_id": self.subscriber_id,
                "bap_uri": self.base_url,
                "transaction_id": f"txn_{int(time.time())}",
                "message_id": f"msg_{int(time.time())}",
                "timestamp": datetime.now().isoformat(),
                "ttl": "PT30S"
            },
            "message": {
                "intent": {
                    "category": {
                        "descriptor": {
                            "name": "eKYC Services"
                        }
                    }
                }
            }
        }
        
        endpoints = [
            (f"{self.base_url}/v1/bap/ekyc/search", "POST", search_payload, "eKYC Search"),
            (f"{self.base_url}/v1/bap/ekyc/transactions", "GET", None, "eKYC Transactions List"),
            (f"{self.pramaan_url}/health", "GET", None, "Pramaan Health Check"),
        ]
        
        for url, method, data, desc in endpoints:
            self.test_endpoint(url, method, data, description=desc)
    
    def generate_report(self):
        """Generate and save test report"""
        print("📊 GENERATING TEST REPORT")
        print("=" * 50)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.get('status') == '✅ PASS'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Group results by status
        print("🔍 DETAILED RESULTS:")
        print("-" * 30)
        
        for result in self.results:
            status_icon = "✅" if result.get('status') == '✅ PASS' else "❌"
            print(f"{status_icon} {result.get('description', result.get('url'))}")
            if result.get('status') not in ['✅ PASS']:
                print(f"   Status: {result.get('status')}")
        
        # Save detailed report
        report_file = f"postman_endpoint_validation_{int(time.time())}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%"
            },
            "results": self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        
        return passed_tests, failed_tests
    
    def run_all_tests(self):
        """Run all validation tests"""
        print("🚀 ONDC PRE-PRODUCTION ENDPOINT VALIDATION")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Subscriber ID: {self.subscriber_id}")
        print(f"Base URL: {self.base_url}")
        print()
        
        self.run_health_checks()
        self.run_subscription_tests()
        self.run_onboarding_tests()
        self.run_registry_tests()
        self.run_ekyc_tests()
        
        passed, failed = self.generate_report()
        
        print("\n" + "=" * 60)
        if failed == 0:
            print("🎉 ALL TESTS PASSED! Your setup is ready for Postman testing.")
        elif passed > failed:
            print("✅ MOSTLY WORKING! Some endpoints may need attention.")
        else:
            print("⚠️  ISSUES DETECTED! Please review failed endpoints.")
        
        print("\n📋 NEXT STEPS:")
        print("1. Import ONDC_BAP_PreProd_Complete_Collection.json to Postman")
        print("2. Import ONDC_PreProd_Environment.json as environment")
        print("3. Follow POSTMAN_SETUP_GUIDE.md for detailed testing")
        print("4. Start with Health Checks folder in Postman")
        
        return passed, failed

def main():
    """Main function"""
    validator = ONDCEndpointValidator()
    validator.run_all_tests()

if __name__ == "__main__":
    main()