#!/usr/bin/env python3
"""
Send First Buyer Call (Search) to ONDC Gateway with Correct Authentication
"""

import sys
import os
import requests
import json
import uuid
import time
import base64
from datetime import datetime, timezone
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.org_config import OrganizationConfig

def crypto_sign_ed25519_sk_to_seed(sk):
    """Convert Ed25519 private key to seed"""
    return sk[:32]

class ONDCSearchClient:
    def __init__(self):
        self.subscriber_id = OrganizationConfig.SUBSCRIBER_ID
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
            
            # Import nacl for signing
            from nacl.signing import SigningKey
            self.signing_key = SigningKey(seed)
            
            # Store keys
            self.signing_public_key = creds['signing_keys']['public_key']
            self.encryption_public_key = creds['encryption_keys']['public_key']
            self.request_id = creds['request_id']
            
            print("✅ Keys loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading keys: {e}")
            self.signing_key = None
    
    def generate_signature(self, payload: str) -> str:
        """Generate Ed25519 signature for payload"""
        if not self.signing_key:
            return "placeholder_signature"
        
        signature = self.signing_key.sign(payload.encode('utf-8'))
        return base64.b64encode(signature.signature).decode('utf-8')
    
    def generate_authorization_header(self, payload: str) -> str:
        """Generate authorization header with signature"""
        signature = self.generate_signature(payload)
        timestamp = str(int(time.time()))
        
        auth_string = f'Signature keyId="{self.subscriber_id}",algorithm="ed25519",headers="(created) (expires) digest",signature="{signature}",created="{timestamp}",expires="{int(time.time()) + 300}"'
        return auth_string
    
    def create_search_payload(self):
        """Create a search payload for ONDC gateway"""
        
        # Generate unique transaction ID
        transaction_id = str(uuid.uuid4())
        message_id = str(uuid.uuid4())
        
        # Create search payload
        payload = {
            "context": {
                "domain": OrganizationConfig.DOMAIN,
                "country": "IND",
                "city": "std:011",
                "action": "search",
                "core_version": "1.2.0",
                "bap_id": self.subscriber_id,
                "bap_uri": OrganizationConfig.BAP_URI,
                "transaction_id": transaction_id,
                "message_id": message_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ttl": "PT30S"
            },
            "message": {
                "intent": {
                    "fulfillment": {
                        "start": {
                            "location": {
                                "gps": "28.6139,77.2090"  # Delhi coordinates
                            }
                        },
                        "end": {
                            "location": {
                                "gps": "28.6139,77.2090"  # Delhi coordinates
                            }
                        }
                    },
                    "payment": {
                        "@ondc/org/buyer_app_finder_fee_type": "percent",
                        "@ondc/org/buyer_app_finder_fee_amount": "3"
                    },
                    "category": {
                        "id": "ONDC:RET10"
                    },
                    "item": {
                        "descriptor": {
                            "name": "Groceries"
                        }
                    }
                }
            }
        }
        
        return payload, transaction_id, message_id
    
    def send_search_request(self):
        """Send search request to ONDC gateway with proper authentication"""
        
        # Create payload
        payload, transaction_id, message_id = self.create_search_payload()
        
        # Convert payload to string for signing
        payload_str = json.dumps(payload, separators=(',', ':'))
        
        # Generate authorization header
        auth_header = self.generate_authorization_header(payload_str)
        
        # Create headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth_header
        }
        
        # Gateway endpoint
        gateway_url = "https://preprod.gateway.ondc.org/search"
        
        print("=== Sending Search Request to ONDC Gateway ===\n")
        print(f"Gateway URL: {gateway_url}")
        print(f"Transaction ID: {transaction_id}")
        print(f"Message ID: {message_id}")
        print(f"Subscriber ID: {self.subscriber_id}")
        print(f"Domain: {OrganizationConfig.DOMAIN}")
        print(f"Type: {OrganizationConfig.TYPE}")
        
        print("\nRequest Headers:")
        for key, value in headers.items():
            if key == "Authorization":
                truncated_auth = value[:100] + "..." if len(value) > 100 else value
                print(f"  {key}: {truncated_auth}")
            else:
                print(f"  {key}: {value}")
        
        print("\nRequest Payload:")
        print(json.dumps(payload, indent=2))
        
        try:
            print(f"\nSending request to {gateway_url}...")
            
            response = requests.post(
                gateway_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"\nResponse Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ Search request sent successfully!")
                try:
                    response_data = response.json()
                    print("\nResponse Body:")
                    print(json.dumps(response_data, indent=2))
                except json.JSONDecodeError:
                    print(f"\nResponse Body (raw): {response.text}")
            elif response.status_code == 202:
                print("✅ Search request accepted (202 Accepted)")
                print(f"Response Body: {response.text}")
            else:
                print(f"❌ Search request failed with status {response.status_code}")
                print(f"Response Body: {response.text}")
            
            return response, transaction_id
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error making search request: {e}")
            return None, transaction_id
    
    def save_search_response(self, response, transaction_id):
        """Save the search response to a file"""
        if response:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_response_{transaction_id}_{timestamp}.json"
            
            response_data = {
                "transaction_id": transaction_id,
                "timestamp": timestamp,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response.text
            }
            
            try:
                with open(filename, 'w') as f:
                    json.dump(response_data, f, indent=2)
                print(f"\n📁 Search response saved to: {filename}")
            except Exception as e:
                print(f"❌ Error saving response: {e}")

def main():
    """Main function to send search request"""
    
    print("=== ONDC Gateway Search Request (Corrected) ===\n")
    
    # Check configuration
    print("Checking organization configuration...")
    print(f"✅ Subscriber ID: {OrganizationConfig.SUBSCRIBER_ID}")
    print(f"✅ BAP URI: {OrganizationConfig.BAP_URI}")
    print(f"✅ Domain: {OrganizationConfig.DOMAIN}")
    print(f"✅ Type: {OrganizationConfig.TYPE}")
    
    # Create search client
    client = ONDCSearchClient()
    
    # Send search request
    response, transaction_id = client.send_search_request()
    
    # Save response
    client.save_search_response(response, transaction_id)
    
    print("\n=== Search Request Complete ===")

if __name__ == "__main__":
    main() 