"""
ONDC Registry Integration Module
Handles subscriber registration and onboarding with ONDC registry
"""

import json
import logging
import httpx
from datetime import datetime
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class ONDCRegistryClient:
    """Client for interacting with ONDC Registry"""
    
    def __init__(self):
        self.registry_url = settings.ONDC_REGISTRY_URL
        self.subscriber_id = settings.ONDC_SUBSCRIBER_ID
        self.subscriber_url = settings.ONDC_SUBSCRIBER_URL
        self.domain = settings.ONDC_DOMAIN
        self.callback_url = settings.ONDC_CALLBACK_URL
    
    async def register_subscriber(self) -> Dict[str, Any]:
        """
        Register subscriber with ONDC registry
        """
        registration_data = {
            "subscriber_id": self.subscriber_id,
            "subscriber_url": self.subscriber_url,
            "domain": self.domain,
            "type": settings.ONDC_TYPE,
            "callback_url": self.callback_url,
            "encryption_public_key": self._get_public_key(),
            "signing_public_key": self._get_public_key(),
            "valid_from": datetime.utcnow().isoformat(),
            "valid_until": "2025-12-31T23:59:59Z",
            "status": "SUBSCRIBED"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.registry_url}/subscriber",
                    json=registration_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    logger.info(f"Successfully registered subscriber: {self.subscriber_id}")
                    return response.json()
                else:
                    logger.error(f"Failed to register subscriber: {response.status_code} - {response.text}")
                    return {"error": f"Registration failed: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error registering subscriber: {str(e)}")
            return {"error": f"Registration error: {str(e)}"}
    
    async def lookup_subscriber(self, subscriber_id: str) -> Dict[str, Any]:
        """
        Lookup subscriber in ONDC registry
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.registry_url}/subscriber/{subscriber_id}"
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to lookup subscriber: {response.status_code}")
                    return {"error": f"Lookup failed: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error looking up subscriber: {str(e)}")
            return {"error": f"Lookup error: {str(e)}"}
    
    async def update_subscriber_status(self, status: str) -> Dict[str, Any]:
        """
        Update subscriber status in registry
        """
        update_data = {
            "subscriber_id": self.subscriber_id,
            "status": status,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.registry_url}/subscriber/{self.subscriber_id}",
                    json=update_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    logger.info(f"Successfully updated subscriber status: {status}")
                    return response.json()
                else:
                    logger.error(f"Failed to update status: {response.status_code}")
                    return {"error": f"Update failed: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error updating subscriber status: {str(e)}")
            return {"error": f"Update error: {str(e)}"}
    
    def _get_public_key(self) -> str:
        """
        Get public key for encryption/signing
        TODO: Implement actual key management
        """
        # Placeholder - implement actual key management
        return "placeholder_public_key"
    
    def generate_registration_payload(self) -> Dict[str, Any]:
        """
        Generate the registration payload for manual submission
        """
        return {
            "subscriber_id": self.subscriber_id,
            "subscriber_url": self.subscriber_url,
            "domain": self.domain,
            "type": settings.ONDC_TYPE,
            "callback_url": self.callback_url,
            "encryption_public_key": self._get_public_key(),
            "signing_public_key": self._get_public_key(),
            "valid_from": datetime.utcnow().isoformat(),
            "valid_until": "2025-12-31T23:59:59Z",
            "status": "SUBSCRIBED"
        }


class ONDCOnboardingHelper:
    """Helper class for ONDC onboarding process"""
    
    def __init__(self):
        self.registry_client = ONDCRegistryClient()
    
    def get_onboarding_checklist(self) -> Dict[str, Any]:
        """
        Get onboarding checklist for manual verification
        """
        return {
            "subscriber_details": {
                "subscriber_id": settings.ONDC_SUBSCRIBER_ID,
                "subscriber_url": settings.ONDC_SUBSCRIBER_URL,
                "domain": settings.ONDC_DOMAIN,
                "type": settings.ONDC_TYPE,
                "callback_url": settings.ONDC_CALLBACK_URL
            },
            "technical_requirements": {
                "callback_endpoint": "✅ Implemented at /v1/bap/on_subscribe",
                "challenge_response": "✅ Handles subscription challenges",
                "status_updates": "✅ Handles status updates",
                "error_handling": "✅ Proper error responses",
                "logging": "✅ Comprehensive logging"
            },
            "security_requirements": {
                "https_enabled": "✅ HTTPS required for production",
                "authentication": "⚠️ Implement ONDC authentication",
                "encryption": "⚠️ Implement message encryption",
                "signing": "⚠️ Implement message signing"
            },
            "ondc_actions": {
                "search": "✅ Endpoint implemented",
                "select": "✅ Endpoint implemented", 
                "init": "✅ Endpoint implemented",
                "confirm": "✅ Endpoint implemented",
                "status": "✅ Endpoint implemented",
                "track": "✅ Endpoint implemented",
                "cancel": "✅ Endpoint implemented",
                "rating": "✅ Endpoint implemented",
                "support": "✅ Endpoint implemented"
            },
            "next_steps": [
                "1. Register with ONDC registry using the generated payload",
                "2. Implement proper authentication and encryption",
                "3. Test with ONDC sandbox environment",
                "4. Submit for production approval",
                "5. Go live on ONDC network"
            ]
        }
    
    def generate_registration_json(self) -> str:
        """
        Generate JSON payload for manual registry registration
        """
        payload = self.registry_client.generate_registration_payload()
        return json.dumps(payload, indent=2)


# Global instances
registry_client = ONDCRegistryClient()
onboarding_helper = ONDCOnboardingHelper() 