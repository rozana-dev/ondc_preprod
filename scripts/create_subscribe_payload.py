#!/usr/bin/env python3
"""
ONDC Subscribe Payload Generator
Creates the proper /subscribe request payload for ONDC registry registration
"""

import json
import os
from datetime import datetime, timezone
from app.core.ondc_crypto import crypto


def create_subscribe_payload(environment: str = "staging", ops_no: int = 1) -> dict:
    """
    Create ONDC subscribe payload
    
    Args:
        environment: staging, pre_prod, or prod
        ops_no: 1 (Buyer App), 2 (Seller App), 4 (Buyer & Seller App)
    """
    
    # Load credentials
    if not crypto.credentials:
        raise ValueError("ONDC credentials not found. Run generate_ondc_keys.py first.")
    
    # Base payload structure
    payload = {
        "subscriber_id": "neo-server.rozana.in",
        "subscriber_url": "https://neo-server.rozana.in",
        "callback_url": "/v1/bap",
        "signing_public_key": crypto.get_signing_public_key(),
        "encryption_public_key": crypto.get_encryption_public_key(),
        "unique_key_id": crypto.get_unique_key_id(),
        "request_id": crypto.get_request_id(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "valid_from": datetime.now(timezone.utc).isoformat(),
        "valid_until": "2025-12-31T23:59:59.999Z"
    }
    
    # Add network participant details based on ops_no
    if ops_no == 1:  # Buyer App Registration
        payload["network_participant"] = [
            {
                "subscriber_url": "https://neo-server.rozana.in",
                "domain": "ONDC:RET10",
                "type": "buyerApp",
                "msn": False,
                "city_code": ["std:080", "std:011"],
                "country": "IND"
            }
        ]
    elif ops_no == 2:  # Seller App Registration
        payload["network_participant"] = [
            {
                "subscriber_url": "https://neo-server.rozana.in", 
                "domain": "ONDC:RET10",
                "type": "sellerApp",
                "msn": False,
                "city_code": ["std:080", "std:011"],
                "country": "IND"
            }
        ]
    elif ops_no == 4:  # Buyer & Seller App Registration
        payload["network_participant"] = [
            {
                "subscriber_url": "https://neo-server.rozana.in",
                "domain": "ONDC:RET10", 
                "type": "buyerApp",
                "msn": False,
                "city_code": ["std:080", "std:011"],
                "country": "IND"
            },
            {
                "subscriber_url": "https://neo-server.rozana.in",
                "domain": "ONDC:RET10",
                "type": "sellerApp", 
                "msn": False,
                "city_code": ["std:080", "std:011"],
                "country": "IND"
            }
        ]
    else:
        raise ValueError("Invalid ops_no. Use 1 (Buyer), 2 (Seller), or 4 (Both)")
    
    return payload


def get_registry_url(environment: str = "staging") -> str:
    """Get the registry URL for the specified environment"""
    urls = {
        "staging": "https://staging.registry.ondc.org/subscribe",
        "pre_prod": "https://preprod.registry.ondc.org/ondc/subscribe", 
        "prod": "https://prod.registry.ondc.org/subscribe"
    }
    return urls.get(environment, urls["staging"])


def main():
    """Generate subscribe payloads for different environments and operations"""
    
    print("🚀 ONDC Subscribe Payload Generator")
    print("=" * 50)
    
    environments = ["staging", "pre_prod", "prod"]
    operations = [
        (1, "Buyer App Registration"),
        (2, "Seller App Registration"), 
        (4, "Buyer & Seller App Registration")
    ]
    
    # Create payloads directory
    os.makedirs("payloads", exist_ok=True)
    
    for env in environments:
        print(f"\n📋 Environment: {env.upper()}")
        print(f"Registry URL: {get_registry_url(env)}")
        
        for ops_no, ops_desc in operations:
            try:
                payload = create_subscribe_payload(env, ops_no)
                
                # Save payload to file
                filename = f"payloads/subscribe_{env}_ops{ops_no}.json"
                with open(filename, 'w') as f:
                    json.dump(payload, f, indent=2)
                
                print(f"  ✅ {ops_desc} (ops_no: {ops_no}) -> {filename}")
                
            except Exception as e:
                print(f"  ❌ Error creating {ops_desc}: {e}")
    
    # Create a summary file with curl commands
    curl_commands = []
    for env in environments:
        registry_url = get_registry_url(env)
        curl_commands.append(f"""
# {env.upper()} Environment
# Buyer App Registration (ops_no: 1)
curl -X POST "{registry_url}" \\
  -H "Content-Type: application/json" \\
  -d @payloads/subscribe_{env}_ops1.json

# Seller App Registration (ops_no: 2)  
curl -X POST "{registry_url}" \\
  -H "Content-Type: application/json" \\
  -d @payloads/subscribe_{env}_ops2.json

# Buyer & Seller App Registration (ops_no: 4)
curl -X POST "{registry_url}" \\
  -H "Content-Type: application/json" \\
  -d @payloads/subscribe_{env}_ops4.json
""")
    
    with open("payloads/curl_commands.sh", 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# ONDC Registry Subscribe Commands\n")
        f.write("# Make sure to:\n")
        f.write("# 1. Host ondc-site-verification.html at your domain root\n")
        f.write("# 2. Ensure your /on_subscribe endpoint is working\n")
        f.write("# 3. Get your subscriber_id whitelisted by ONDC\n\n")
        f.write("\n".join(curl_commands))
    
    print(f"\n📝 Curl commands saved to: payloads/curl_commands.sh")
    
    # Display next steps
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS FOR ONDC REGISTRATION")
    print("=" * 60)
    print("1. 🔑 Generate keys: python scripts/generate_ondc_keys.py")
    print("2. 📄 Host site verification file at: https://neo-server.rozana.in/ondc-site-verification.html")
    print("3. 🌐 Ensure /on_subscribe endpoint is accessible")
    print("4. ✅ Get subscriber_id whitelisted at: https://portal.ondc.org")
    print("5. 📤 Submit /subscribe request using generated payloads")
    print("6. 🔍 Verify registration in registry lookup")
    print("\n📋 Available Payloads:")
    
    for env in environments:
        for ops_no, ops_desc in operations:
            print(f"  • {env.upper()} - {ops_desc}: payloads/subscribe_{env}_ops{ops_no}.json")
    
    print("=" * 60)


if __name__ == "__main__":
    main()