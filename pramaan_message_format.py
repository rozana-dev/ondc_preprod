#!/usr/bin/env python3

"""
🚀 Pramaan ONDC Message Format Generator
Generates correct transaction IDs and message formats for Pramaan testing
"""

import uuid
import json
from datetime import datetime, timezone
import hashlib
import base64

class PramaanMessageGenerator:
    
    def __init__(self, bap_id="neo-server.rozana.in", bap_uri="https://neo-server.rozana.in"):
        self.bap_id = bap_id
        self.bap_uri = bap_uri
    
    def generate_transaction_id(self) -> str:
        """Generate ONDC compliant transaction ID"""
        # Format: bap_id prefix + timestamp + random
        timestamp = int(datetime.now().timestamp())
        random_part = str(uuid.uuid4())[:8]
        return f"{self.bap_id.replace('.', '_')}_{timestamp}_{random_part}"
    
    def generate_message_id(self) -> str:
        """Generate ONDC compliant message ID"""
        # Format: UUID v4
        return str(uuid.uuid4())
    
    def get_current_timestamp(self) -> str:
        """Generate ONDC compliant timestamp"""
        # ISO 8601 format with milliseconds and Z suffix
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    def create_context(self, action: str, transaction_id: str = None, bpp_id: str = None, bpp_uri: str = None) -> dict:
        """Create ONDC compliant context object"""
        if not transaction_id:
            transaction_id = self.generate_transaction_id()
            
        context = {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:011",
            "action": action,
            "core_version": "1.2.0",
            "bap_id": self.bap_id,
            "bap_uri": self.bap_uri,
            "transaction_id": transaction_id,
            "message_id": self.generate_message_id(),
            "timestamp": self.get_current_timestamp(),
            "ttl": "PT30S"
        }
        
        # Add BPP details if provided (for requests to sellers)
        if bpp_id:
            context["bpp_id"] = bpp_id
        if bpp_uri:
            context["bpp_uri"] = bpp_uri
            
        return context
    
    def create_search_message(self, transaction_id: str = None) -> dict:
        """Create search message for Pramaan testing"""
        return {
            "context": self.create_context("search", transaction_id),
            "message": {
                "intent": {
                    "item": {
                        "descriptor": {
                            "name": "Test Product for Pramaan"
                        }
                    },
                    "fulfillment": {
                        "type": "Delivery",
                        "end": {
                            "location": {
                                "gps": "28.6139,77.2090",
                                "address": {
                                    "area_code": "110037"
                                }
                            }
                        }
                    },
                    "payment": {
                        "type": "PRE-PAID"
                    }
                }
            }
        }
    
    def create_select_message(self, transaction_id: str, bpp_id: str = "pramaan.ondc.org/beta/preprod/mock/seller") -> dict:
        """Create select message for Pramaan testing"""
        return {
            "context": self.create_context("select", transaction_id, bpp_id, f"https://{bpp_id}"),
            "message": {
                "order": {
                    "provider": {
                        "id": "pramaan_provider_1"
                    },
                    "items": [{
                        "id": "item_001",
                        "quantity": {
                            "count": 2
                        }
                    }],
                    "billing": {
                        "address": {
                            "name": "John Doe",
                            "building": "123 Test Building",
                            "locality": "Test Locality",
                            "city": "New Delhi",
                            "state": "Delhi",
                            "country": "IND",
                            "area_code": "110037"
                        },
                        "phone": "9876543210",
                        "email": "test@neo-server.rozana.in"
                    },
                    "fulfillment": {
                        "type": "Delivery",
                        "end": {
                            "location": {
                                "gps": "28.6139,77.2090",
                                "address": {
                                    "name": "John Doe",
                                    "building": "123 Test Building",
                                    "locality": "Test Locality",
                                    "city": "New Delhi",
                                    "state": "Delhi",
                                    "country": "IND",
                                    "area_code": "110037"
                                }
                            },
                            "contact": {
                                "phone": "9876543210"
                            }
                        }
                    }
                }
            }
        }
    
    def create_init_message(self, transaction_id: str, bpp_id: str = "pramaan.ondc.org/beta/preprod/mock/seller") -> dict:
        """Create init message for Pramaan testing"""
        return {
            "context": self.create_context("init", transaction_id, bpp_id, f"https://{bpp_id}"),
            "message": {
                "order": {
                    "provider": {
                        "id": "pramaan_provider_1"
                    },
                    "items": [{
                        "id": "item_001",
                        "quantity": {
                            "count": 2
                        }
                    }],
                    "billing": {
                        "address": {
                            "name": "John Doe",
                            "building": "123 Test Building",
                            "locality": "Test Locality",
                            "city": "New Delhi",
                            "state": "Delhi",
                            "country": "IND",
                            "area_code": "110037"
                        },
                        "phone": "9876543210",
                        "email": "test@neo-server.rozana.in"
                    },
                    "fulfillment": {
                        "type": "Delivery"
                    },
                    "payment": {
                        "type": "PRE-PAID",
                        "collected_by": "BAP"
                    }
                }
            }
        }
    
    def create_confirm_message(self, transaction_id: str, bpp_id: str = "pramaan.ondc.org/beta/preprod/mock/seller") -> dict:
        """Create confirm message for Pramaan testing"""
        order_id = f"order_{transaction_id}"
        return {
            "context": self.create_context("confirm", transaction_id, bpp_id, f"https://{bpp_id}"),
            "message": {
                "order": {
                    "id": order_id,
                    "provider": {
                        "id": "pramaan_provider_1"
                    },
                    "items": [{
                        "id": "item_001",
                        "quantity": {
                            "count": 2
                        }
                    }],
                    "billing": {
                        "address": {
                            "name": "John Doe",
                            "building": "123 Test Building",
                            "locality": "Test Locality",
                            "city": "New Delhi",
                            "state": "Delhi",
                            "country": "IND",
                            "area_code": "110037"
                        },
                        "phone": "9876543210",
                        "email": "test@neo-server.rozana.in"
                    },
                    "fulfillment": {
                        "type": "Delivery"
                    },
                    "payment": {
                        "type": "PRE-PAID",
                        "collected_by": "BAP",
                        "status": "PAID"
                    }
                }
            }
        }
    
    def create_status_message(self, transaction_id: str, order_id: str = None, bpp_id: str = "pramaan.ondc.org/beta/preprod/mock/seller") -> dict:
        """Create status message for Pramaan testing"""
        if not order_id:
            order_id = f"order_{transaction_id}"
            
        return {
            "context": self.create_context("status", transaction_id, bpp_id, f"https://{bpp_id}"),
            "message": {
                "order_id": order_id
            }
        }
    
    def create_ekyc_search_message(self, transaction_id: str = None) -> dict:
        """Create eKYC search message for Pramaan testing"""
        return {
            "context": self.create_context("search", transaction_id),
            "message": {
                "intent": {
                    "item": {
                        "descriptor": {
                            "name": "eKYC Verification Service"
                        }
                    },
                    "provider": {
                        "category_id": "ekyc"
                    }
                }
            }
        }
    
    def create_ekyc_verify_message(self, transaction_id: str, verification_data: dict = None) -> dict:
        """Create eKYC verify message for Pramaan testing"""
        if not verification_data:
            verification_data = {
                "document_type": "AADHAAR",
                "document_number": "1234-5678-9012",
                "name": "John Doe"
            }
            
        return {
            "context": self.create_context("verify", transaction_id),
            "message": {
                "order": {
                    "provider": {
                        "id": "pramaan.ondc.org"
                    },
                    "items": [{
                        "id": "ekyc_verification",
                        "descriptor": {
                            "name": "Aadhaar Verification"
                        }
                    }]
                },
                "documents": [verification_data]
            }
        }

def main():
    """Generate sample messages for Pramaan testing"""
    generator = PramaanMessageGenerator()
    
    print("🚀 Pramaan ONDC Message Format Generator")
    print("=" * 50)
    print()
    
    # Generate a consistent transaction ID for the flow
    transaction_id = generator.generate_transaction_id()
    print(f"📋 Generated Transaction ID: {transaction_id}")
    print()
    
    # Generate all message formats
    messages = {
        "search": generator.create_search_message(transaction_id),
        "select": generator.create_select_message(transaction_id),
        "init": generator.create_init_message(transaction_id),
        "confirm": generator.create_confirm_message(transaction_id),
        "status": generator.create_status_message(transaction_id),
        "ekyc_search": generator.create_ekyc_search_message(),
        "ekyc_verify": generator.create_ekyc_verify_message(transaction_id)
    }
    
    print("📋 ONDC Message Formats for Pramaan Testing:")
    print()
    
    for action, message in messages.items():
        print(f"🔍 {action.upper()} Message:")
        print(json.dumps(message, indent=2))
        print()
        print("-" * 50)
        print()
    
    # Save to files
    with open("pramaan_test_messages.json", "w") as f:
        json.dump(messages, f, indent=2)
    
    print("✅ Messages saved to: pramaan_test_messages.json")
    print()
    
    print("🎯 Key Points for Pramaan Testing:")
    print("• Transaction ID format: bap_id_timestamp_random")
    print("• Message ID: UUID v4")
    print("• Timestamp: ISO 8601 with milliseconds + Z")
    print("• Context: Always includes domain, country, city, action")
    print("• Message: Action-specific payload structure")
    print()
    
    print("🌐 Your BAP Details:")
    print(f"• BAP ID: {generator.bap_id}")
    print(f"• BAP URI: {generator.bap_uri}")
    print(f"• Domain: ONDC:RET10")
    print(f"• Core Version: 1.2.0")

if __name__ == "__main__":
    main()