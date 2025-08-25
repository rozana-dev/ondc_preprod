#!/usr/bin/env python3

"""
🎯 Correct ONDC Transaction ID Format Generator
Following official ONDC rules for Pramaan testing
"""

import uuid
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

class ONDCTransactionManager:
    
    def __init__(self, bap_id="neo-server.rozana.in", bap_uri="https://neo-server.rozana.in"):
        self.bap_id = bap_id
        self.bap_uri = bap_uri
        self.active_transactions = {}
    
    def generate_transaction_id(self) -> str:
        """
        Generate ONDC compliant transaction ID
        Rule: UUID v4 (universally unique identifier)
        """
        return str(uuid.uuid4())
    
    def generate_message_id(self) -> str:
        """
        Generate ONDC compliant message ID
        Rule: UUID v4 for each request/response
        """
        return str(uuid.uuid4())
    
    def get_current_timestamp(self) -> str:
        """Generate ONDC compliant timestamp"""
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    def start_new_flow(self, flow_type: str) -> str:
        """
        Start a new transaction flow
        Rule: New transaction_id per new flow
        """
        transaction_id = self.generate_transaction_id()
        self.active_transactions[transaction_id] = {
            'flow_type': flow_type,
            'started_at': self.get_current_timestamp(),
            'messages': []
        }
        return transaction_id
    
    def create_context(self, action: str, transaction_id: str, bpp_id: str = None, bpp_uri: str = None) -> dict:
        """Create ONDC compliant context object"""
        context = {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:011",
            "action": action,
            "core_version": "1.2.0",
            "bap_id": self.bap_id,
            "bap_uri": self.bap_uri,
            "transaction_id": transaction_id,  # Same transaction_id for entire flow
            "message_id": self.generate_message_id(),  # New message_id for each call
            "timestamp": self.get_current_timestamp(),
            "ttl": "PT30S"
        }
        
        # Add BPP details if provided
        if bpp_id:
            context["bpp_id"] = bpp_id
        if bpp_uri:
            context["bpp_uri"] = bpp_uri
            
        return context
    
    def create_order_flow_messages(self, transaction_id: str) -> Dict[str, Any]:
        """
        Create complete order flow messages
        Rule: All requests in the flow use the SAME transaction_id
        """
        bpp_id = "pramaan.ondc.org/beta/preprod/mock/seller"
        bpp_uri = f"https://{bpp_id}"
        
        messages = {}
        
        # Step 1: Search (same transaction_id)
        messages["search"] = {
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
        
        # Step 2: Select (same transaction_id)
        messages["select"] = {
            "context": self.create_context("select", transaction_id, bpp_id, bpp_uri),
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
        
        # Step 3: Init (same transaction_id)
        messages["init"] = {
            "context": self.create_context("init", transaction_id, bpp_id, bpp_uri),
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
        
        # Step 4: Confirm (same transaction_id)
        order_id = f"order_{transaction_id.replace('-', '_')}"
        messages["confirm"] = {
            "context": self.create_context("confirm", transaction_id, bpp_id, bpp_uri),
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
                    "payment": {
                        "type": "PRE-PAID",
                        "collected_by": "BAP",
                        "status": "PAID"
                    }
                }
            }
        }
        
        # Step 5: Status (same transaction_id)
        messages["status"] = {
            "context": self.create_context("status", transaction_id, bpp_id, bpp_uri),
            "message": {
                "order_id": order_id
            }
        }
        
        # Step 6: Track (same transaction_id)
        messages["track"] = {
            "context": self.create_context("track", transaction_id, bpp_id, bpp_uri),
            "message": {
                "order_id": order_id
            }
        }
        
        return messages
    
    def create_issue_flow_messages(self, transaction_id: str, order_transaction_id: str) -> Dict[str, Any]:
        """
        Create issue flow messages
        Rule: All issue requests share the SAME transaction_id (different from order)
        """
        bpp_id = "pramaan.ondc.org/beta/preprod/mock/seller"
        bpp_uri = f"https://{bpp_id}"
        order_id = f"order_{order_transaction_id.replace('-', '_')}"
        issue_id = f"issue_{transaction_id.replace('-', '_')}"
        
        messages = {}
        
        # Step 1: Issue (same transaction_id for all issue calls)
        messages["issue"] = {
            "context": self.create_context("issue", transaction_id, bpp_id, bpp_uri),
            "message": {
                "issue": {
                    "id": issue_id,
                    "category": "ITEM",
                    "sub_category": "ITM01",
                    "complainant_info": {
                        "person": {
                            "name": "John Doe"
                        },
                        "contact": {
                            "phone": "9876543210",
                            "email": "test@neo-server.rozana.in"
                        }
                    },
                    "order_details": {
                        "id": order_id,
                        "state": "Completed",
                        "items": [{
                            "id": "item_001",
                            "quantity": 1
                        }]
                    },
                    "description": {
                        "short_desc": "Item damaged during delivery",
                        "long_desc": "The item received was damaged during delivery"
                    },
                    "source": {
                        "network_participant_id": self.bap_id,
                        "type": "CONSUMER"
                    },
                    "expected_response_time": {
                        "duration": "PT2H"
                    },
                    "expected_resolution_time": {
                        "duration": "P1D"
                    },
                    "status": "OPEN",
                    "issue_type": "ISSUE",
                    "created_at": self.get_current_timestamp()
                }
            }
        }
        
        # Step 2: Issue Status (same transaction_id)
        messages["issue_status"] = {
            "context": self.create_context("issue_status", transaction_id, bpp_id, bpp_uri),
            "message": {
                "issue_id": issue_id
            }
        }
        
        # Step 3: Issue Close (same transaction_id)
        messages["issue_close"] = {
            "context": self.create_context("issue", transaction_id, bpp_id, bpp_uri),
            "message": {
                "issue": {
                    "id": issue_id,
                    "status": "CLOSED",
                    "resolution": {
                        "short_desc": "Issue resolved - replacement provided",
                        "long_desc": "The damaged item has been replaced",
                        "action_triggered": "REPLACE"
                    },
                    "updated_at": self.get_current_timestamp()
                }
            }
        }
        
        return messages
    
    def create_ekyc_flow_messages(self, transaction_id: str) -> Dict[str, Any]:
        """
        Create eKYC flow messages
        Rule: All eKYC requests share the SAME transaction_id
        """
        messages = {}
        
        # Step 1: eKYC Search (same transaction_id)
        messages["ekyc_search"] = {
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
        
        # Step 2: eKYC Select (same transaction_id)
        messages["ekyc_select"] = {
            "context": self.create_context("select", transaction_id),
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
                }
            }
        }
        
        # Step 3: eKYC Verify (same transaction_id)
        messages["ekyc_verify"] = {
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
                "documents": [{
                    "document_type": "AADHAAR",
                    "document_number": "1234-5678-9012",
                    "name": "John Doe"
                }]
            }
        }
        
        return messages

def main():
    """Generate correct ONDC transaction formats for Pramaan testing"""
    manager = ONDCTransactionManager()
    
    print("🎯 Correct ONDC Transaction ID Format for Pramaan Testing")
    print("=" * 60)
    print()
    
    print("📋 ONDC Transaction ID Rules:")
    print("✅ UUID v4 (universally unique identifier)")
    print("✅ Same transaction_id for entire flow")
    print("✅ New transaction_id per new flow")
    print()
    
    # Generate different flows with correct transaction IDs
    flows = {}
    
    # Flow 1: Complete Order Flow
    order_txn_id = manager.start_new_flow("order")
    flows["order_flow"] = {
        "transaction_id": order_txn_id,
        "flow_type": "Complete Order Journey",
        "messages": manager.create_order_flow_messages(order_txn_id)
    }
    
    # Flow 2: Issue Flow (different transaction_id)
    issue_txn_id = manager.start_new_flow("issue")
    flows["issue_flow"] = {
        "transaction_id": issue_txn_id,
        "flow_type": "Issue & Grievance Management",
        "messages": manager.create_issue_flow_messages(issue_txn_id, order_txn_id)
    }
    
    # Flow 3: eKYC Flow (different transaction_id)
    ekyc_txn_id = manager.start_new_flow("ekyc")
    flows["ekyc_flow"] = {
        "transaction_id": ekyc_txn_id,
        "flow_type": "eKYC Verification",
        "messages": manager.create_ekyc_flow_messages(ekyc_txn_id)
    }
    
    print("🚀 Generated Transaction IDs (UUID v4 format):")
    print()
    for flow_name, flow_data in flows.items():
        print(f"📋 {flow_data['flow_type']}:")
        print(f"   Transaction ID: {flow_data['transaction_id']}")
        print(f"   Format: UUID v4 ✅")
        print()
    
    print("🔍 Flow Consistency Examples:")
    print()
    
    # Show order flow consistency
    print("📦 Order Flow (Same transaction_id for all steps):")
    order_messages = flows["order_flow"]["messages"]
    order_txn = flows["order_flow"]["transaction_id"]
    
    for step, message in order_messages.items():
        msg_id = message["context"]["message_id"]
        print(f"   {step.upper()}: txn={order_txn[:8]}... msg={msg_id[:8]}...")
    print()
    
    # Show issue flow consistency  
    print("🚨 Issue Flow (Same transaction_id for all steps):")
    issue_messages = flows["issue_flow"]["messages"]
    issue_txn = flows["issue_flow"]["transaction_id"]
    
    for step, message in issue_messages.items():
        msg_id = message["context"]["message_id"]
        print(f"   {step.upper()}: txn={issue_txn[:8]}... msg={msg_id[:8]}...")
    print()
    
    # Save all flows
    with open("correct_ondc_transaction_flows.json", "w") as f:
        json.dump(flows, f, indent=2)
    
    print("✅ All flows saved to: correct_ondc_transaction_flows.json")
    print()
    
    print("🎯 Key Rules Summary:")
    print("• Transaction ID: UUID v4 format")
    print("• Flow Consistency: Same transaction_id for entire flow")
    print("• New Flow: Generate new transaction_id")
    print("• Message ID: New UUID v4 for each request/response")
    print("• Timestamp: ISO 8601 with milliseconds + Z")
    print()
    
    print("📋 Example Usage:")
    print(f"Order Flow: {order_txn}")
    print("  /search → /select → /init → /confirm → /status → /track")
    print()
    print(f"Issue Flow: {issue_txn}")
    print("  /issue → /on_issue → /issue_status → /on_issue_status → /issue_close")
    print()
    print(f"eKYC Flow: {ekyc_txn_id}")
    print("  /ekyc/search → /ekyc/select → /ekyc/verify")

if __name__ == "__main__":
    main()