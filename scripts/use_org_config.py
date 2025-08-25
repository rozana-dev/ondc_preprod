#!/usr/bin/env python3
"""
Utility script to demonstrate how to use the organization configuration
for ONDC API calls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.org_config import OrganizationConfig

def main():
    """Demonstrate usage of organization configuration"""
    
    print("=== Organization Configuration Demo ===\n")
    
    # Show authentication headers
    print("1. Authentication Headers:")
    auth_headers = OrganizationConfig.get_auth_headers()
    for key, value in auth_headers.items():
        if key == "Authorization":
            # Truncate token for display
            truncated_token = value[:50] + "..." if len(value) > 50 else value
            print(f"   {key}: {truncated_token}")
        else:
            print(f"   {key}: {value}")
    
    print("\n2. Subscriber Information:")
    subscriber_info = OrganizationConfig.get_subscriber_info()
    for key, value in subscriber_info.items():
        print(f"   {key}: {value}")
    
    print("\n3. Company Information:")
    company_info = OrganizationConfig.get_company_info()
    for key, value in company_info.items():
        print(f"   {key}: {value}")
    
    print("\n4. Example API Call Structure:")
    print("""
    import requests
    from app.core.org_config import OrganizationConfig
    
    # Make API call with organization config
    headers = OrganizationConfig.get_auth_headers()
    subscriber_data = OrganizationConfig.get_subscriber_info()
    
    response = requests.post(
        "https://api.ondc.org/subscribe",
        headers=headers,
        json={
            "subscriber_id": subscriber_data["subscriber_id"],
            "domain": subscriber_data["domain"],
            "type": subscriber_data["type"],
            # ... other required fields
        }
    )
    """)
    
    print("\n5. Environment Variables to Set:")
    print("   export ED25519_PRIVATE_KEY='your_private_key_here'")
    print("   export KEY_ID='your_key_id_here'")
    
    print("\n=== Configuration Ready for Use ===")

if __name__ == "__main__":
    main() 