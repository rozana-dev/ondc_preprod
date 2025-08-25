#!/usr/bin/env python3
"""
Example API call using organization configuration
"""

import sys
import os
import requests
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.org_config import OrganizationConfig

def make_subscribe_api_call():
    """Example of making a subscribe API call using organization config"""
    
    # Get configuration data
    headers = OrganizationConfig.get_auth_headers()
    subscriber_info = OrganizationConfig.get_subscriber_info()
    company_info = OrganizationConfig.get_company_info()
    
    # Construct the payload
    payload = {
        "subscriber_id": subscriber_info["subscriber_id"],
        "domain": subscriber_info["domain"],
        "type": subscriber_info["type"],
        "callback_url": subscriber_info["bap_uri"],
        "key_id": subscriber_info["key_id"],
        "company_info": {
            "legal_entity_name": company_info["legal_entity_name"],
            "business_address": company_info["business_address"],
            "gst_number": company_info["gst_number"],
            "pan_number": company_info["pan_number"],
            "date_of_incorporation": company_info["date_of_incorporation"]
        },
        "contact_info": {
            "email_id": company_info["email_id"],
            "mobile_number": company_info["mobile_number"],
            "country": company_info["country"],
            "city_code": company_info["city_code"]
        },
        "authorized_signatory": {
            "name": company_info["authorized_signatory_name"],
            "address": company_info["authorized_signatory_address"]
        }
    }
    
    print("Making API call with payload:")
    print(json.dumps(payload, indent=2))
    
    # Example API endpoint (replace with actual ONDC endpoint)
    api_url = "https://api.ondc.org/subscribe"
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None

def make_lookup_api_call():
    """Example of making a lookup API call"""
    
    headers = OrganizationConfig.get_auth_headers()
    subscriber_info = OrganizationConfig.get_subscriber_info()
    
    # Example lookup payload
    lookup_payload = {
        "subscriber_id": subscriber_info["subscriber_id"],
        "domain": subscriber_info["domain"],
        "type": subscriber_info["type"]
    }
    
    print("Making lookup API call with payload:")
    print(json.dumps(lookup_payload, indent=2))
    
    # Example lookup endpoint
    api_url = "https://api.ondc.org/lookup"
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=lookup_payload,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None

if __name__ == "__main__":
    print("=== Example API Calls Using Organization Config ===\n")
    
    # Check if required environment variables are set
    if not OrganizationConfig.ED25519_PRIVATE_KEY:
        print("Warning: ED25519_PRIVATE_KEY not set in environment")
    if not OrganizationConfig.KEY_ID:
        print("Warning: KEY_ID not set in environment")
    
    print("1. Subscribe API Call Example:")
    make_subscribe_api_call()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Lookup API Call Example:")
    make_lookup_api_call() 