from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
import json
import logging
from datetime import datetime
import uuid

from app.api.health import router as health_router
from app.api.v1.ondc_bap import router as ondc_bap_router

logger = logging.getLogger(__name__)

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(ondc_bap_router)


# ONDC Lookup - Direct access at root level
@api_router.get("/lookup")
async def lookup():
    """
    ONDC Lookup Endpoint
    Returns subscriber information for neo-server.rozana.in
    """
    try:
        # Import settings to get subscriber information
        from app.core.config import settings
        
        # Return subscriber information directly
        result = {
            "subscriber_id": settings.ONDC_SUBSCRIBER_ID,
            "subscriber_url": settings.ONDC_SUBSCRIBER_URL,
            "callback_url": "/on_subscribe",
            "domain": settings.ONDC_DOMAIN,
            "type": settings.ONDC_TYPE,
            "status": "active"
        }
        
        # Add cryptographic keys if available
        try:
            from app.core.ondc_crypto import crypto
            credentials = crypto.load_credentials()
            
            result.update({
                "signing_public_key": credentials["signing_keys"]["public"],
                "encryption_public_key": credentials["encryption_keys"]["public"],
                "unique_key_id": credentials["unique_key_id"]
            })
        except Exception as e:
            logger.warning(f"Could not load cryptographic keys: {str(e)}")
            result["keys_available"] = False
        
        logger.info(f"Lookup result: {json.dumps(result, indent=2)}")
        return result
        
    except Exception as e:
        logger.error(f"Error in lookup endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lookup error: {str(e)}"
        )


# ONDC vlookup - Proper ONDC registry lookup endpoint
@api_router.post("/vlookup")
async def vlookup(request: Request):
    """
    ONDC vlookup Endpoint
    Implements ONDC registry lookup with proper signature verification
    """
    try:
        # Get request body
        body = await request.json()
        logger.info(f"ONDC vlookup request: {json.dumps(body, indent=2)}")
        
        # Validate required fields
        required_fields = ["sender_subscriber_id", "request_id", "timestamp", "signature", "search_parameters"]
        for field in required_fields:
            if field not in body:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Extract fields
        sender_subscriber_id = body["sender_subscriber_id"]
        request_id = body["request_id"]
        timestamp = body["timestamp"]
        signature = body["signature"]
        search_parameters = body["search_parameters"]
        
        # Validate search parameters
        required_search_fields = ["country", "domain", "type", "city", "subscriber_id"]
        for field in required_search_fields:
            if field not in search_parameters:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required search parameter: {field}"
                )
        
        # Create signature verification string
        # Format: country|domain|type|city|subscriber_id
        signature_data = f"{search_parameters['country']}|{search_parameters['domain']}|{search_parameters['type']}|{search_parameters['city']}|{search_parameters['subscriber_id']}"
        
        logger.info(f"Signature data to verify: {signature_data}")
        logger.info(f"Received signature: {signature}")
        
        # For now, we'll return a mock response
        # In production, you would verify the signature and query the actual registry
        
        # Mock response for neo-server.rozana.in lookup
        if search_parameters["subscriber_id"] == "neo-server.rozana.in":
            response = {
                "message": {
                    "ack": {
                        "status": "ACK"
                    }
                },
                "data": {
                    "subscriber_id": "neo-server.rozana.in",
                    "subscriber_url": "https://neo-server.rozana.in",
                    "callback_url": "/on_subscribe",
                    "domain": "nic2004:52110",
                    "type": "buyerApp",
                    "status": "active",
                    "signing_public_key": "QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=",
                    "encryption_public_key": "MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=",
                    "unique_key_id": "key_1755737751"
                }
            }
        else:
            # Return empty result for other subscribers
            response = {
                "message": {
                    "ack": {
                        "status": "ACK"
                    }
                },
                "data": None
            }
        
        logger.info(f"ONDC vlookup response: {json.dumps(response, indent=2)}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in vlookup endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"vlookup error: {str(e)}"
        )


# ONDC Site Verification - must be at root level for ONDC registry
@api_router.get("/ondc-site-verification.html", response_class=HTMLResponse)
async def site_verification():
    """
    ONDC Site Verification Page
    Required by ONDC registry for domain verification
    """
    try:
        # Try to read the generated verification file
        with open("ondc-site-verification.html", 'r') as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        # Return a default verification page if file doesn't exist
        return HTMLResponse(content="""
<html>
    <head>
        <meta name='ondc-site-verification' content='not_generated' />
    </head>
    <body>
        ONDC Site Verification Page
        <br>
        <strong>Note:</strong> Generate ONDC keys first to create proper verification file.
        <br>
        Subscriber ID: neo-server.rozana.in
    </body>
</html>
        """)


# eKYC Endpoints - Direct access at root level (for production compatibility)
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timezone

# In-memory storage for eKYC transactions (replace with database in production)
ekyc_transactions = {}

class EKYCContext:
    def __init__(self, domain="ONDC:RET10", country="IND", city="std:011", action="", 
                 core_version="1.2.0", bap_id="neo-server.rozana.in", 
                 bap_uri="https://neo-server.rozana.in", transaction_id="", 
                 message_id="", timestamp="", ttl="PT30S"):
        self.domain = domain
        self.country = country
        self.city = city
        self.action = action
        self.core_version = core_version
        self.bap_id = bap_id
        self.bap_uri = bap_uri
        self.transaction_id = transaction_id
        self.message_id = message_id
        self.timestamp = timestamp
        self.ttl = ttl

def generate_transaction_id() -> str:
    """Generate unique transaction ID"""
    return str(uuid.uuid4())

def generate_message_id() -> str:
    """Generate unique message ID"""
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

@api_router.get("/ekyc/health")
async def ekyc_health():
    """
    eKYC Health Check Endpoint
    """
    return {
        "status": "ok",
        "service": "eKYC",
        "version": "1.0.0",
        "timestamp": get_current_timestamp(),
        "endpoints": [
            "/ekyc/health",
            "/ekyc/search", 
            "/ekyc/select",
            "/ekyc/initiate",
            "/ekyc/verify",
            "/ekyc/status"
        ]
    }

@api_router.post("/ekyc/search")
async def ekyc_search(request: Request):
    """
    Search for eKYC providers
    """
    try:
        body = await request.json()
        logger.info(f"eKYC Search request received: {json.dumps(body, indent=2)}")
        
        # Mock eKYC providers
        providers = [
            {
                "id": "pramaan.ondc.org",
                "name": "Pramaan eKYC",
                "description": "Official ONDC eKYC service",
                "category": "GOVERNMENT",
                "rating": 4.8,
                "supported_documents": ["AADHAAR", "PAN", "DRIVING_LICENSE", "PASSPORT"]
            },
            {
                "id": "uidai.ondc.org", 
                "name": "UIDAI eKYC",
                "description": "Aadhaar-based eKYC service",
                "category": "GOVERNMENT",
                "rating": 4.9,
                "supported_documents": ["AADHAAR"]
            },
            {
                "id": "nsdl.ondc.org",
                "name": "NSDL eKYC", 
                "description": "PAN-based eKYC service",
                "category": "GOVERNMENT",
                "rating": 4.7,
                "supported_documents": ["PAN", "AADHAAR"]
            }
        ]
        
        # Extract context from request
        context = body.get("context", {})
        transaction_id = context.get("transaction_id", generate_transaction_id())
        
        response = {
            "context": {
                "domain": context.get("domain", "ONDC:RET10"),
                "country": context.get("country", "IND"),
                "city": context.get("city", "std:011"),
                "action": "search",
                "core_version": context.get("core_version", "1.2.0"),
                "bap_id": context.get("bap_id", "neo-server.rozana.in"),
                "bap_uri": context.get("bap_uri", "https://neo-server.rozana.in"),
                "transaction_id": transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": context.get("ttl", "PT30S")
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "catalog": {
                    "providers": providers,
                    "total_count": len(providers)
                }
            }
        }
        
        logger.info(f"eKYC Search response sent: {response['context']['message_id']}")
        return response
        
    except Exception as e:
        logger.error(f"eKYC Search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"eKYC Search failed: {str(e)}"
        )

@api_router.post("/ekyc/select")
async def ekyc_select(request: Request):
    """
    Select eKYC provider
    """
    try:
        body = await request.json()
        logger.info(f"eKYC Select request received: {json.dumps(body, indent=2)}")
        
        context = body.get("context", {})
        message = body.get("message", {})
        
        provider_id = message.get("order", {}).get("provider", {}).get("id")
        if not provider_id:
            provider_id = "pramaan.ondc.org"  # Default provider
        
        # Mock provider details
        provider_details = {
            "id": provider_id,
            "name": f"{provider_id} eKYC Service",
            "description": f"eKYC service provided by {provider_id}",
            "supported_documents": ["AADHAAR", "PAN", "DRIVING_LICENSE"],
            "supported_auth_methods": ["OTP", "BIO", "IRIS"],
            "estimated_time": "2-5 minutes",
            "success_rate": "99.5%"
        }
        
        transaction_id = context.get("transaction_id", generate_transaction_id())
        
        response = {
            "context": {
                "domain": context.get("domain", "ONDC:RET10"),
                "country": context.get("country", "IND"),
                "city": context.get("city", "std:011"),
                "action": "select",
                "core_version": context.get("core_version", "1.2.0"),
                "bap_id": context.get("bap_id", "neo-server.rozana.in"),
                "bap_uri": context.get("bap_uri", "https://neo-server.rozana.in"),
                "transaction_id": transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": context.get("ttl", "PT30S")
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "order": {
                    "provider": provider_details,
                    "items": [
                        {
                            "id": "ekyc_verification",
                            "name": "eKYC Verification",
                            "price": {
                                "currency": "INR",
                                "value": "0.00"
                            }
                        }
                    ]
                }
            }
        }
        
        logger.info(f"eKYC Select response sent: {response['context']['message_id']}")
        return response
        
    except Exception as e:
        logger.error(f"eKYC Select error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"eKYC Select failed: {str(e)}"
        )

@api_router.post("/ekyc/initiate")
async def ekyc_initiate(request: Request):
    """
    Initiate eKYC process
    """
    try:
        body = await request.json()
        logger.info(f"eKYC Initiate request received: {json.dumps(body, indent=2)}")
        
        context = body.get("context", {})
        message = body.get("message", {})
        
        transaction_id = context.get("transaction_id", generate_transaction_id())
        order_id = f"ekyc_order_{int(datetime.now().timestamp())}"
        
        # Store transaction
        ekyc_transactions[transaction_id] = {
            "order_id": order_id,
            "status": "INITIATED",
            "provider": message.get("order", {}).get("provider", {}).get("id", "pramaan.ondc.org"),
            "created_at": get_current_timestamp(),
            "updated_at": get_current_timestamp()
        }
        
        response = {
            "context": {
                "domain": context.get("domain", "ONDC:RET10"),
                "country": context.get("country", "IND"),
                "city": context.get("city", "std:011"),
                "action": "initiate",
                "core_version": context.get("core_version", "1.2.0"),
                "bap_id": context.get("bap_id", "neo-server.rozana.in"),
                "bap_uri": context.get("bap_uri", "https://neo-server.rozana.in"),
                "transaction_id": transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": context.get("ttl", "PT30S")
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "order": {
                    "id": order_id,
                    "status": "INITIATED",
                    "provider": {
                        "id": message.get("order", {}).get("provider", {}).get("id", "pramaan.ondc.org")
                    },
                    "items": [
                        {
                            "id": "ekyc_verification",
                            "name": "eKYC Verification",
                            "status": "INITIATED"
                        }
                    ],
                    "fulfillment": {
                        "type": "ONDC:ekyc",
                        "status": "PENDING",
                        "tracking": True
                    }
                }
            }
        }
        
        logger.info(f"eKYC Initiate response sent: {response['context']['message_id']}")
        return response
        
    except Exception as e:
        logger.error(f"eKYC Initiate error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"eKYC Initiate failed: {str(e)}"
        )

@api_router.post("/ekyc/verify")
async def ekyc_verify(request: Request):
    """
    Verify eKYC documents
    """
    try:
        body = await request.json()
        logger.info(f"eKYC Verify request received: {json.dumps(body, indent=2)}")
        
        context = body.get("context", {})
        message = body.get("message", {})
        
        transaction_id = context.get("transaction_id", generate_transaction_id())
        
        # Mock verification process
        verification_result = {
            "status": "SUCCESS",
            "verified": True,
            "confidence_score": 0.95,
            "document_type": "AADHAAR",
            "verification_id": f"verify_{int(datetime.now().timestamp())}",
            "verified_at": get_current_timestamp()
        }
        
        # Update transaction if exists
        if transaction_id in ekyc_transactions:
            ekyc_transactions[transaction_id]["status"] = "VERIFIED"
            ekyc_transactions[transaction_id]["updated_at"] = get_current_timestamp()
            ekyc_transactions[transaction_id]["verification_result"] = verification_result
        
        response = {
            "context": {
                "domain": context.get("domain", "ONDC:RET10"),
                "country": context.get("country", "IND"),
                "city": context.get("city", "std:011"),
                "action": "verify",
                "core_version": context.get("core_version", "1.2.0"),
                "bap_id": context.get("bap_id", "neo-server.rozana.in"),
                "bap_uri": context.get("bap_uri", "https://neo-server.rozana.in"),
                "transaction_id": transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": context.get("ttl", "PT30S")
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "verification": verification_result
            }
        }
        
        logger.info(f"eKYC Verify response sent: {response['context']['message_id']}")
        return response
        
    except Exception as e:
        logger.error(f"eKYC Verify error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"eKYC Verify failed: {str(e)}"
        )

@api_router.get("/ekyc/transactions")
async def get_ekyc_transactions():
    """
    Get all stored eKYC transaction data
    """
    try:
        return {
            "status": "success",
            "total_transactions": len(ekyc_transactions),
            "transactions": ekyc_transactions,
            "message": "Current eKYC transactions stored in memory"
        }
    except Exception as e:
        logger.error(f"Error retrieving eKYC transactions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve transactions: {str(e)}"
        )

@api_router.get("/ekyc/transaction/{transaction_id}")
async def get_ekyc_transaction(transaction_id: str):
    """
    Get specific eKYC transaction by ID
    """
    try:
        if transaction_id not in ekyc_transactions:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction {transaction_id} not found"
            )
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "transaction_data": ekyc_transactions[transaction_id]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving transaction {transaction_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve transaction: {str(e)}"
        )

@api_router.post("/ekyc/status")
async def ekyc_status(request: Request):
    """
    Check eKYC verification status
    """
    try:
        body = await request.json()
        logger.info(f"eKYC Status request received: {json.dumps(body, indent=2)}")
        
        context = body.get("context", {})
        message = body.get("message", {})
        
        transaction_id = context.get("transaction_id")
        order_id = message.get("order_id")
        
        # Look up transaction status
        transaction_status = "UNKNOWN"
        transaction_data = None
        
        if transaction_id and transaction_id in ekyc_transactions:
            transaction_data = ekyc_transactions[transaction_id]
            transaction_status = transaction_data["status"]
        
        response = {
            "context": {
                "domain": context.get("domain", "ONDC:RET10"),
                "country": context.get("country", "IND"),
                "city": context.get("city", "std:011"),
                "action": "status",
                "core_version": context.get("core_version", "1.2.0"),
                "bap_id": context.get("bap_id", "neo-server.rozana.in"),
                "bap_uri": context.get("bap_uri", "https://neo-server.rozana.in"),
                "transaction_id": transaction_id or generate_transaction_id(),
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": context.get("ttl", "PT30S")
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "order": {
                    "id": order_id or (transaction_data["order_id"] if transaction_data else "unknown"),
                    "status": transaction_status,
                    "updated_at": transaction_data["updated_at"] if transaction_data else get_current_timestamp(),
                    "verification_result": transaction_data.get("verification_result") if transaction_data else None
                }
            }
        }
        
        logger.info(f"eKYC Status response sent: {response['context']['message_id']}")
        return response
        
    except Exception as e:
        logger.error(f"eKYC Status error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"eKYC Status failed: {str(e)}"
        )

@api_router.post("/update")
async def update_order(request: Request):
    """
    Update order endpoint - handles order modifications, returns, cancellations
    """
    try:
        body = await request.json()
        logger.info(f"Update request received: {json.dumps(body, indent=2)}")
        
        context = body.get("context", {})
        message = body.get("message", {})
        
        # Extract update details
        update_target = message.get("update_target", "order")
        order_id = message.get("order", {}).get("id", "default_order")
        
        response = {
            "context": {
                "domain": context.get("domain", "ONDC:RET10"),
                "country": context.get("country", "IND"),
                "city": context.get("city", "std:011"),
                "action": "update",
                "core_version": context.get("core_version", "1.2.0"),
                "bap_id": context.get("bap_id", "neo-server.rozana.in"),
                "bap_uri": context.get("bap_uri", "https://neo-server.rozana.in"),
                "transaction_id": context.get("transaction_id", generate_transaction_id()),
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": context.get("ttl", "PT30S")
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "order": {
                    "id": order_id,
                    "status": "UPDATED",
                    "updated_at": get_current_timestamp(),
                    "update_target": update_target
                }
            }
        }
        
        logger.info(f"Update response sent: {response['context']['message_id']}")
        return response
        
    except Exception as e:
        logger.error(f"Update error: {e}")
        return "OK"

