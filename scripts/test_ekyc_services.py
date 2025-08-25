#!/usr/bin/env python3
"""
Test eKYC Services
Test all eKYC endpoints: search, select, initiate, verify, status
"""

import requests
import json
import uuid
from datetime import datetime, timezone
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.org_config import OrganizationConfig

class EKYCTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.subscriber_id = OrganizationConfig.SUBSCRIBER_ID
        
    def generate_context(self, action: str):
        """Generate ONDC context for eKYC requests"""
        return {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:011",
            "action": action,
            "core_version": "1.2.0",
            "bap_id": self.subscriber_id,
            "bap_uri": f"https://{self.subscriber_id}",
            "transaction_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ttl": "PT30S"
        }
    
    def test_ekyc_search(self):
        """Test eKYC search endpoint"""
        print("\n🔍 Testing eKYC Search")
        print("=" * 50)
        
        payload = {
            "context": self.generate_context("search"),
            "message": {
                "intent": {
                    "fulfillment": {
                        "type": "eKYC"
                    }
                }
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/search",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✅ eKYC Search successful!")
                print(f"Providers found: {data['message']['catalog']['total_count']}")
                for provider in data['message']['catalog']['providers']:
                    print(f"  - {provider['name']} ({provider['id']})")
                return True
            else:
                print(f"❌ eKYC Search failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ eKYC Search error: {e}")
            return False
    
    def test_ekyc_select(self):
        """Test eKYC select endpoint"""
        print("\n🎯 Testing eKYC Select")
        print("=" * 50)
        
        payload = {
            "context": self.generate_context("select"),
            "message": {
                "order": {
                    "provider": {
                        "id": "pramaan.ondc.org",
                        "name": "Pramaan eKYC"
                    }
                }
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/select",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✅ eKYC Select successful!")
                print(f"Provider: {data['message']['order']['provider']['name']}")
                return True
            else:
                print(f"❌ eKYC Select failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ eKYC Select error: {e}")
            return False
    
    def test_ekyc_initiate(self):
        """Test eKYC initiate endpoint"""
        print("\n🆔 Testing eKYC Initiate")
        print("=" * 50)
        
        payload = {
            "context": self.generate_context("initiate"),
            "message": {
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
                    },
                    "provider": {
                        "id": "pramaan.ondc.org"
                    },
                    "documents": [
                        {
                            "type": "AADHAAR",
                            "number": "123456789012"
                        }
                    ]
                }
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/initiate",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✅ eKYC Initiate successful!")
                transaction_id = data['message']['order']['id']
                print(f"Transaction ID: {transaction_id}")
                print(f"Status: {data['message']['order']['status']}")
                if 'otp' in data['message']['order']['fulfillment']['auth']:
                    print(f"OTP: {data['message']['order']['fulfillment']['auth']['otp']}")
                return transaction_id
            else:
                print(f"❌ eKYC Initiate failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ eKYC Initiate error: {e}")
            return None
    
    def test_ekyc_verify(self, transaction_id: str):
        """Test eKYC verify endpoint"""
        print("\n✅ Testing eKYC Verify")
        print("=" * 50)
        
        payload = {
            "context": self.generate_context("verify"),
            "message": {
                "transaction_id": transaction_id,
                "verification": {
                    "otp": "123456"  # Mock OTP
                }
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/verify",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✅ eKYC Verify successful!")
                print(f"Status: {data['message']['order']['status']}")
                if 'verification_result' in data['message']['order']['fulfillment']:
                    result = data['message']['order']['fulfillment']['verification_result']
                    print(f"Verified: {result['verified']}")
                    print(f"Confidence Score: {result['confidence_score']}")
                return True
            else:
                print(f"❌ eKYC Verify failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ eKYC Verify error: {e}")
            return False
    
    def test_ekyc_status(self, transaction_id: str):
        """Test eKYC status endpoint"""
        print("\n📊 Testing eKYC Status")
        print("=" * 50)
        
        payload = {
            "context": self.generate_context("status"),
            "message": {
                "transaction_id": transaction_id
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ekyc/status",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✅ eKYC Status successful!")
                print(f"Transaction Status: {data['message']['order']['status']}")
                print(f"Created: {data['message']['order']['created_at']}")
                if 'tracking' in data['message']['order']['fulfillment']:
                    tracking = data['message']['order']['fulfillment']['tracking']
                    print(f"Tracking URL: {tracking['url']}")
                return True
            else:
                print(f"❌ eKYC Status failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ eKYC Status error: {e}")
            return False
    
    def test_ekyc_tracking(self, transaction_id: str):
        """Test eKYC tracking web interface"""
        print("\n🌐 Testing eKYC Tracking")
        print("=" * 50)
        
        try:
            response = requests.get(
                f"{self.base_url}/ekyc/track/{transaction_id}",
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✅ eKYC Tracking successful!")
                print("HTML tracking page available")
                return True
            else:
                print(f"❌ eKYC Tracking failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ eKYC Tracking error: {e}")
            return False
    
    def test_ekyc_transactions(self):
        """Test eKYC transactions list endpoint"""
        print("\n📋 Testing eKYC Transactions List")
        print("=" * 50)
        
        try:
            response = requests.get(
                f"{self.base_url}/ekyc/transactions",
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("✅ eKYC Transactions list successful!")
                print(f"Total transactions: {data['total_count']}")
                return True
            else:
                print(f"❌ eKYC Transactions list failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ eKYC Transactions list error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all eKYC tests"""
        print("🧪 eKYC Services Test Suite")
        print("=" * 60)
        
        results = []
        
        # Test 1: Search
        results.append(("Search", self.test_ekyc_search()))
        
        # Test 2: Select
        results.append(("Select", self.test_ekyc_select()))
        
        # Test 3: Initiate
        transaction_id = self.test_ekyc_initiate()
        results.append(("Initiate", transaction_id is not None))
        
        if transaction_id:
            # Test 4: Verify
            results.append(("Verify", self.test_ekyc_verify(transaction_id)))
            
            # Test 5: Status
            results.append(("Status", self.test_ekyc_status(transaction_id)))
            
            # Test 6: Tracking
            results.append(("Tracking", self.test_ekyc_tracking(transaction_id)))
        
        # Test 7: Transactions List
        results.append(("Transactions List", self.test_ekyc_transactions()))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 eKYC Services Test Summary")
        print("=" * 60)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All eKYC services are working correctly!")
        else:
            print("⚠️  Some eKYC services need attention.")
        
        return results

def main():
    """Main function"""
    tester = EKYCTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(result for _, result in results)
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 