"""
eKYC Service Implementation for ONDC
Implements all eKYC operations: search, select, initiate, verify, status
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import json
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ekyc", tags=["eKYC"])

# In-memory storage for eKYC transactions (replace with database in production)
ekyc_transactions = {}

class EKYCContext(BaseModel):
    domain: str = "ONDC:RET10"
    country: str = "IND"
    city: str = "std:011"
    action: str
    core_version: str = "1.2.0"
    bap_id: str = "neo-server.rozana.in"
    bap_uri: str = "https://neo-server.rozana.in"
    transaction_id: str
    message_id: str
    timestamp: str
    ttl: str = "PT30S"

class EKYCRequester(BaseModel):
    type: str = "CONSUMER"
    id: str

class EKYCProvider(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class EKYCInitiateRequest(BaseModel):
    context: EKYCContext
    message: Dict[str, Any]

class EKYCVerifyRequest(BaseModel):
    context: EKYCContext
    message: Dict[str, Any]

class EKYCStatusRequest(BaseModel):
    context: EKYCContext
    message: Dict[str, Any]

class EKYCSearchRequest(BaseModel):
    context: EKYCContext
    message: Dict[str, Any]

class EKYCSelectRequest(BaseModel):
    context: EKYCContext
    message: Dict[str, Any]

def generate_transaction_id() -> str:
    """Generate unique transaction ID"""
    return str(uuid.uuid4())

def generate_message_id() -> str:
    """Generate unique message ID"""
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

@router.post("/search", status_code=status.HTTP_200_OK)
async def ekyc_search(request: EKYCSearchRequest):
    """
    Search for eKYC providers
    """
    try:
        logger.info(f"eKYC Search request received: {request.context.transaction_id}")
        
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
        
        response = {
            "context": {
                "domain": request.context.domain,
                "country": request.context.country,
                "city": request.context.city,
                "action": "search",
                "core_version": request.context.core_version,
                "bap_id": request.context.bap_id,
                "bap_uri": request.context.bap_uri,
                "transaction_id": request.context.transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": request.context.ttl
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

@router.post("/select", status_code=status.HTTP_200_OK)
async def ekyc_select(request: EKYCSelectRequest):
    """
    Select eKYC provider
    """
    try:
        logger.info(f"eKYC Select request received: {request.context.transaction_id}")
        
        provider_id = request.message.get("order", {}).get("provider", {}).get("id")
        if not provider_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provider ID is required"
            )
        
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
        
        response = {
            "context": {
                "domain": request.context.domain,
                "country": request.context.country,
                "city": request.context.city,
                "action": "select",
                "core_version": request.context.core_version,
                "bap_id": request.context.bap_id,
                "bap_uri": request.context.bap_uri,
                "transaction_id": request.context.transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": request.context.ttl
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
                    ],
                    "fulfillment": {
                        "type": "eKYC",
                        "provider": provider_details
                    }
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

@router.post("/initiate", status_code=status.HTTP_200_OK)
async def ekyc_initiate(request: EKYCInitiateRequest):
    """
    Initiate eKYC process
    """
    try:
        logger.info(f"eKYC Initiate request received: {request.context.transaction_id}")
        
        # Generate eKYC transaction
        ekyc_transaction_id = generate_transaction_id()
        
        # Store transaction details
        ekyc_transactions[ekyc_transaction_id] = {
            "status": "INITIATED",
            "created_at": get_current_timestamp(),
            "requester": request.message.get("init", {}).get("requester", {}),
            "purpose": request.message.get("init", {}).get("purpose", {}),
            "auth_type": request.message.get("init", {}).get("auth", {}).get("type", "OTP"),
            "provider_id": request.message.get("init", {}).get("provider", {}).get("id"),
            "documents": request.message.get("init", {}).get("documents", [])
        }
        
        # Mock OTP generation
        otp = "123456"  # In production, generate real OTP
        
        response = {
            "context": {
                "domain": request.context.domain,
                "country": request.context.country,
                "city": request.context.city,
                "action": "initiate",
                "core_version": request.context.core_version,
                "bap_id": request.context.bap_id,
                "bap_uri": request.context.bap_uri,
                "transaction_id": request.context.transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": request.context.ttl
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "order": {
                    "id": ekyc_transaction_id,
                    "status": "INITIATED",
                    "provider": {
                        "id": ekyc_transactions[ekyc_transaction_id]["provider_id"],
                        "name": "eKYC Provider"
                    },
                    "fulfillment": {
                        "type": "eKYC",
                        "status": "INITIATED",
                        "auth": {
                            "type": ekyc_transactions[ekyc_transaction_id]["auth_type"],
                            "otp": otp if ekyc_transactions[ekyc_transaction_id]["auth_type"] == "OTP" else None
                        }
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

@router.post("/verify", status_code=status.HTTP_200_OK)
async def ekyc_verify(request: EKYCVerifyRequest):
    """
    Verify eKYC process
    """
    try:
        logger.info(f"eKYC Verify request received: {request.context.transaction_id}")
        
        transaction_id = request.message.get("transaction_id")
        if not transaction_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction ID is required"
            )
        
        if transaction_id not in ekyc_transactions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Mock verification process
        verification_data = request.message.get("verification", {})
        auth_type = ekyc_transactions[transaction_id]["auth_type"]
        
        # Simulate verification
        is_verified = False
        if auth_type == "OTP":
            otp = verification_data.get("otp")
            is_verified = otp == "123456"  # Mock OTP validation
        elif auth_type == "BIO":
            biometric_data = verification_data.get("biometric")
            is_verified = bool(biometric_data)  # Mock biometric validation
        
        # Update transaction status
        if is_verified:
            ekyc_transactions[transaction_id]["status"] = "VERIFIED"
            ekyc_transactions[transaction_id]["verified_at"] = get_current_timestamp()
            ekyc_transactions[transaction_id]["verification_data"] = verification_data
        else:
            ekyc_transactions[transaction_id]["status"] = "FAILED"
            ekyc_transactions[transaction_id]["failed_at"] = get_current_timestamp()
        
        response = {
            "context": {
                "domain": request.context.domain,
                "country": request.context.country,
                "city": request.context.city,
                "action": "verify",
                "core_version": request.context.core_version,
                "bap_id": request.context.bap_id,
                "bap_uri": request.context.bap_uri,
                "transaction_id": request.context.transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": request.context.ttl
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "order": {
                    "id": transaction_id,
                    "status": ekyc_transactions[transaction_id]["status"],
                    "fulfillment": {
                        "type": "eKYC",
                        "status": ekyc_transactions[transaction_id]["status"],
                        "verification_result": {
                            "verified": is_verified,
                            "confidence_score": 0.95 if is_verified else 0.0,
                            "verification_method": auth_type
                        }
                    }
                }
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

@router.post("/status", status_code=status.HTTP_200_OK)
async def ekyc_status(request: EKYCStatusRequest):
    """
    Check eKYC status
    """
    try:
        logger.info(f"eKYC Status request received: {request.context.transaction_id}")
        
        transaction_id = request.message.get("transaction_id")
        if not transaction_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction ID is required"
            )
        
        if transaction_id not in ekyc_transactions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        transaction = ekyc_transactions[transaction_id]
        
        response = {
            "context": {
                "domain": request.context.domain,
                "country": request.context.country,
                "city": request.context.city,
                "action": "status",
                "core_version": request.context.core_version,
                "bap_id": request.context.bap_id,
                "bap_uri": request.context.bap_uri,
                "transaction_id": request.context.transaction_id,
                "message_id": generate_message_id(),
                "timestamp": get_current_timestamp(),
                "ttl": request.context.ttl
            },
            "message": {
                "ack": {
                    "status": "ACK"
                },
                "order": {
                    "id": transaction_id,
                    "status": transaction["status"],
                    "created_at": transaction["created_at"],
                    "provider": {
                        "id": transaction.get("provider_id", "unknown"),
                        "name": "eKYC Provider"
                    },
                    "fulfillment": {
                        "type": "eKYC",
                        "status": transaction["status"],
                        "tracking": {
                            "url": f"https://neo-server.rozana.in/ekyc/track/{transaction_id}",
                            "status": transaction["status"]
                        }
                    }
                }
            }
        }
        
        # Add additional fields based on status
        if transaction["status"] == "VERIFIED":
            response["message"]["order"]["fulfillment"]["verification_data"] = {
                "verified_at": transaction.get("verified_at"),
                "verification_method": transaction.get("auth_type"),
                "confidence_score": 0.95
            }
        elif transaction["status"] == "FAILED":
            response["message"]["order"]["fulfillment"]["error"] = {
                "code": "VERIFICATION_FAILED",
                "message": "eKYC verification failed"
            }
        
        logger.info(f"eKYC Status response sent: {response['context']['message_id']}")
        return response
        
    except Exception as e:
        logger.error(f"eKYC Status error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"eKYC Status failed: {str(e)}"
        )

@router.get("/track/{transaction_id}", status_code=status.HTTP_200_OK)
async def ekyc_track(transaction_id: str):
    """
    Track eKYC transaction (web interface)
    """
    try:
        if transaction_id not in ekyc_transactions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        transaction = ekyc_transactions[transaction_id]
        
        # Return HTML tracking page
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>eKYC Transaction Tracking</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .status {{ padding: 10px; border-radius: 5px; margin: 10px 0; }}
                .initiated {{ background-color: #fff3cd; color: #856404; }}
                .verified {{ background-color: #d4edda; color: #155724; }}
                .failed {{ background-color: #f8d7da; color: #721c24; }}
                .details {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>eKYC Transaction Tracking</h1>
            <div class="details">
                <h2>Transaction ID: {transaction_id}</h2>
                <div class="status {transaction['status'].lower()}">
                    <strong>Status: {transaction['status']}</strong>
                </div>
                <p><strong>Created:</strong> {transaction['created_at']}</p>
                <p><strong>Provider:</strong> {transaction.get('provider_id', 'Unknown')}</p>
                <p><strong>Auth Type:</strong> {transaction.get('auth_type', 'Unknown')}</p>
                <p><strong>Purpose:</strong> {transaction.get('purpose', {}).get('text', 'KYC Verification')}</p>
            </div>
        </body>
        </html>
        """
        
        return {"html": html_content}
        
    except Exception as e:
        logger.error(f"eKYC Track error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"eKYC Track failed: {str(e)}"
        )

@router.get("/transactions", status_code=status.HTTP_200_OK)
async def list_ekyc_transactions():
    """
    List all eKYC transactions (admin endpoint)
    """
    try:
        return {
            "transactions": ekyc_transactions,
            "total_count": len(ekyc_transactions)
        }
    except Exception as e:
        logger.error(f"List eKYC transactions error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list transactions: {str(e)}"
        ) 