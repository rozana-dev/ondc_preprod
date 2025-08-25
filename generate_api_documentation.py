#!/usr/bin/env python3
"""
ONDC BAP API Documentation Generator
===================================

This script generates comprehensive API documentation with:
- Complete API URLs 
- Request JSON examples
- Response JSON examples  
- HTTP methods and descriptions

Author: ONDC BAP Team
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import uuid
from datetime import datetime, timezone
import time
import sys

class ONDCAPIDocumentationGenerator:
    def __init__(self, base_url="https://neo-server.rozana.in"):
        self.base_url = base_url
        self.transaction_id = str(uuid.uuid4())
        self.ekyc_transaction_id = str(uuid.uuid4())
        self.documentation = []
        
        # Pramaan configuration
        self.pramaan_config = {
            "store_name": "pramaan_provider_1",
            "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller", 
            "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller",
            "domain": "ONDC:RET10",
            "environment": "preprod"
        }
    
    def get_timestamp(self):
        """Generate ONDC-compliant timestamp format: YYYY-MM-DDTHH:mm:ss.sssZ"""
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    def generate_message_id(self):
        """Generate unique message ID"""
        return str(uuid.uuid4())
    
    def create_context(self, action: str, bpp_id: str = None, bpp_uri: str = None) -> dict:
        """Create ONDC context object"""
        context = {
            "domain": self.pramaan_config["domain"],
            "action": action,
            "transaction_id": self.transaction_id,
            "message_id": self.generate_message_id(),
            "timestamp": self.get_timestamp()
        }
        
        if bpp_id:
            context["bpp_id"] = bpp_id
        if bpp_uri:
            context["bpp_uri"] = bpp_uri
            
        return context
    
    def make_api_call(self, endpoint: str, method: str = "POST", payload: dict = None):
        """Make API call and capture response"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                req = urllib.request.Request(url, method="GET")
            else:
                if payload:
                    data = json.dumps(payload).encode('utf-8')
                    req = urllib.request.Request(url, data=data, method="POST")
                    req.add_header('Content-Type', 'application/json')
                else:
                    req = urllib.request.Request(url, method="POST")
            
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                response_body = response.read().decode('utf-8')
                
                try:
                    response_json = json.loads(response_body)
                except json.JSONDecodeError:
                    response_json = {"raw_response": response_body}
                
                return {
                    "status_code": status_code,
                    "response": response_json,
                    "success": True
                }
                
        except urllib.error.HTTPError as e:
            return {
                "status_code": e.code,
                "response": {"error": f"HTTP {e.code}: {e.reason}"},
                "success": False
            }
        except Exception as e:
            return {
                "status_code": None,
                "response": {"error": str(e)},
                "success": False
            }
    
    def document_api(self, endpoint: str, method: str, payload: dict = None, description: str = "API endpoint", category: str = "General"):
        """Document an API endpoint with request/response examples"""
        print(f"📋 Documenting: {method} {endpoint}")
        
        # Make API call to get real response
        result = self.make_api_call(endpoint, method, payload)
        
        # Create documentation entry
        doc_entry = {
            "category": category,
            "endpoint": endpoint,
            "method": method,
            "description": description,
            "url": f"{self.base_url}{endpoint}",
            "request": {
                "method": method,
                "headers": {
                    "Content-Type": "application/json" if method != "GET" else "Not required"
                },
                "body": payload if payload else "No body required"
            },
            "response": {
                "status_code": result["status_code"],
                "body": result["response"]
            },
            "success": result["success"]
        }
        
        self.documentation.append(doc_entry)
        return result
    
    def generate_all_api_docs(self):
        """Generate documentation for all APIs"""
        print("🎯 ONDC BAP API Documentation Generator")
        print("=" * 60)
        print(f"📅 Generated: {self.get_timestamp()}")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🔑 Transaction ID: {self.transaction_id}")
        print()
        
        # 1. HEALTH CHECK APIs
        print("🏥 HEALTH CHECK APIs")
        print("-" * 30)
        self.document_api("/health", "GET", description="Main application health check", category="Health")
        self.document_api("/ekyc/health", "GET", description="eKYC service health check", category="Health")
        print()
        
        # 2. ONDC CORE ORDER FLOW APIs  
        print("📦 ONDC CORE ORDER FLOW APIs")
        print("-" * 35)
        
        # Search (with BAP ID/URI, no BPP info since we're searching for providers)
        search_context = self.create_context("search")
        # Remove BPP info from search context (we're searching for BPPs, not targeting specific one)
        search_context.pop("bpp_id", None)
        search_context.pop("bpp_uri", None)
        
        search_payload = {
            "context": search_context,
            "message": {
                "intent": {
                    "item": {
                        "descriptor": {
                            "name": "Test Product from Pramaan Store"
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
                        "@ondc/org/buyer_app_finder_fee_type": "percent",
                        "@ondc/org/buyer_app_finder_fee_amount": "3"
                    },
                    "tags": [
                        {
                            "code": "bap_terms",
                            "list": [
                                {
                                    "code": "static_terms",
                                    "value": ""
                                },
                                {
                                    "code": "static_terms_new",
                                    "value": "https://neo-server.rozana.in/static-terms/bap/1.0/tc.pdf"
                                },
                                {
                                    "code": "effective_date",
                                    "value": "2023-10-01T00:00:00.000Z"
                                }
                            ]
                        }
                    ]
                }
            }
        }
        self.document_api("/search", "POST", search_payload, "Search for products/services", "ONDC Core")
        
        # Select
        bpp_id = self.pramaan_config["bpp_id"]
        bpp_uri = self.pramaan_config["bpp_uri"]
        
        select_payload = {
            "context": self.create_context("select", bpp_id, bpp_uri),
            "message": {
                "order": {
                    "provider": {
                        "id": self.pramaan_config["store_name"]
                    },
                    "items": [{
                        "id": "item_001",
                        "quantity": {
                            "count": 2
                        }
                    }],
                    "billing": {
                        "address": {
                            "name": "Test User",
                            "building": "123 Test Building",
                            "city": "New Delhi",
                            "state": "Delhi",
                            "country": "IND",
                            "area_code": "110037"
                        },
                        "phone": "9876543210"
                    }
                }
            }
        }
        self.document_api("/select", "POST", select_payload, "Select items from catalog", "ONDC Core")
        
        # Init
        init_payload = {
            "context": self.create_context("init", bpp_id, bpp_uri),
            "message": {
                "order": {
                    "provider": {
                        "id": "provider_1"
                    },
                    "items": [{
                        "id": "item_001",
                        "quantity": {
                            "count": 2
                        }
                    }],
                    "billing": {
                        "address": {
                            "name": "Test User",
                            "city": "New Delhi",
                            "state": "Delhi"
                        },
                        "phone": "9876543210"
                    },
                    "payment": {
                        "type": "PRE-PAID"
                    }
                }
            }
        }
        self.document_api("/init", "POST", init_payload, "Initialize order", "ONDC Core")
        
        # Confirm
        order_id = f"order_{self.transaction_id.replace('-', '_')}"
        confirm_payload = {
            "context": self.create_context("confirm", bpp_id, bpp_uri),
            "message": {
                "order": {
                    "id": order_id,
                    "provider": {
                        "id": "provider_1"
                    },
                    "items": [{
                        "id": "item_001",
                        "quantity": {
                            "count": 2
                        }
                    }],
                    "payment": {
                        "type": "PRE-PAID",
                        "status": "PAID"
                    }
                }
            }
        }
        self.document_api("/confirm", "POST", confirm_payload, "Confirm order", "ONDC Core")
        
        # Status
        status_payload = {
            "context": self.create_context("status", bpp_id, bpp_uri),
            "message": {
                "order_id": order_id
            }
        }
        self.document_api("/status", "POST", status_payload, "Get order status", "ONDC Core")
        
        # Track
        track_payload = {
            "context": self.create_context("track", bpp_id, bpp_uri),
            "message": {
                "order_id": order_id
            }
        }
        self.document_api("/track", "POST", track_payload, "Track order", "ONDC Core")
        
        # Cancel
        cancel_payload = {
            "context": self.create_context("cancel", bpp_id, bpp_uri),
            "message": {
                "order_id": order_id,
                "cancellation_reason_id": "001",
                "descriptor": {
                    "short_desc": "Test cancellation"
                }
            }
        }
        self.document_api("/cancel", "POST", cancel_payload, "Cancel order", "ONDC Core")
        
        # Update
        update_payload = {
            "context": self.create_context("update", bpp_id, bpp_uri),
            "message": {
                "update_target": "order",
                "order": {
                    "id": order_id,
                    "status": "UPDATED"
                }
            }
        }
        self.document_api("/update", "POST", update_payload, "Update order", "ONDC Core")
        print()
        
        # 3. eKYC SERVICES APIs
        print("🔐 eKYC SERVICES APIs")
        print("-" * 25)
        
        # eKYC Search
        ekyc_search_payload = {
            "context": {
                "domain": "ONDC:RET10",
                "action": "search",
                "transaction_id": self.ekyc_transaction_id,
                "message_id": self.generate_message_id(),
                "timestamp": self.get_timestamp()
            },
            "message": {
                "intent": {
                    "provider": {
                        "category_id": "ekyc"
                    }
                }
            }
        }
        self.document_api("/ekyc/search", "POST", ekyc_search_payload, "Search for eKYC providers", "eKYC")
        
        # eKYC Select
        ekyc_select_payload = {
            "context": {
                "domain": "ONDC:RET10",
                "action": "select",
                "transaction_id": self.ekyc_transaction_id,
                "message_id": self.generate_message_id(),
                "timestamp": self.get_timestamp()
            },
            "message": {
                "order": {
                    "provider": {
                        "id": "pramaan.ondc.org"
                    },
                    "items": [{
                        "id": "aadhaar_verification"
                    }]
                }
            }
        }
        self.document_api("/ekyc/select", "POST", ekyc_select_payload, "Select eKYC service", "eKYC")
        
        # eKYC Initiate
        ekyc_initiate_payload = {
            "context": {
                "domain": "ONDC:RET10",
                "action": "initiate",
                "transaction_id": self.ekyc_transaction_id,
                "message_id": self.generate_message_id(),
                "timestamp": self.get_timestamp()
            },
            "message": {
                "order": {
                    "provider": {
                        "id": "pramaan.ondc.org"
                    },
                    "items": [{
                        "id": "aadhaar_verification"
                    }]
                }
            }
        }
        self.document_api("/ekyc/initiate", "POST", ekyc_initiate_payload, "Initiate eKYC process", "eKYC")
        
        # eKYC Verify
        ekyc_verify_payload = {
            "context": {
                "domain": "ONDC:RET10",
                "action": "verify",
                "transaction_id": self.ekyc_transaction_id,
                "message_id": self.generate_message_id(),
                "timestamp": self.get_timestamp()
            },
            "message": {
                "documents": [{
                    "document_type": "AADHAAR",
                    "document_number": "1234-5678-9012",
                    "name": "Test User"
                }]
            }
        }
        self.document_api("/ekyc/verify", "POST", ekyc_verify_payload, "Verify documents", "eKYC")
        
        # eKYC Status
        ekyc_status_payload = {
            "context": {
                "domain": "ONDC:RET10",
                "action": "status",
                "transaction_id": self.ekyc_transaction_id,
                "message_id": self.generate_message_id(),
                "timestamp": self.get_timestamp()
            },
            "message": {
                "verification_id": f"verify_{int(time.time())}"
            }
        }
        self.document_api("/ekyc/status", "POST", ekyc_status_payload, "Check verification status", "eKYC")
        print()
        
        # 4. REGISTRY & ONBOARDING APIs
        print("📋 REGISTRY & ONBOARDING APIs")
        print("-" * 35)
        
        # On Subscribe
        on_subscribe_payload = {
            "context": self.create_context("on_subscribe"),
            "message": {
                "ack": {
                    "status": "ACK"
                }
            }
        }
        self.document_api("/on_subscribe", "POST", on_subscribe_payload, "Registry subscription callback", "Registry")
        
        # VLookup
        self.document_api("/vlookup", "GET", description="Participant lookup", category="Registry")
        print()
        
        # 5. ADDITIONAL ENDPOINTS
        print("🔧 ADDITIONAL ENDPOINTS")
        print("-" * 25)
        
        # Rating
        rating_payload = {
            "context": self.create_context("rating"),
            "message": {
                "rating_category": "Order",
                "id": order_id,
                "value": "4"
            }
        }
        self.document_api("/rating", "POST", rating_payload, "Rate order/service", "Additional")
        
        # Support
        support_payload = {
            "context": self.create_context("support"),
            "message": {
                "support": {
                    "order_id": order_id,
                    "phone": "1800-XXX-XXXX",
                    "email": "support@neo-server.rozana.in"
                }
            }
        }
        self.document_api("/support", "POST", support_payload, "Customer support", "Additional")
        print()
    
    def generate_markdown_documentation(self):
        """Generate comprehensive markdown documentation"""
        markdown_content = f"""# ONDC BAP API Documentation

## Overview
Complete API documentation for ONDC BAP (Buyer App Platform) with request/response examples.

- **Base URL**: `{self.base_url}`
- **Generated**: {self.get_timestamp()}
- **Transaction ID**: `{self.transaction_id}`

## API Categories

"""
        
        # Group by category
        categories = {}
        for doc in self.documentation:
            category = doc['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(doc)
        
        # Generate documentation for each category
        for category_name, apis in categories.items():
            markdown_content += f"\n## {category_name} APIs\n\n"
            
            for api in apis:
                status_icon = "✅" if api['success'] else "❌"
                
                markdown_content += f"### {status_icon} {api['method']} {api['endpoint']}\n\n"
                markdown_content += f"**Description**: {api['description']}\n\n"
                markdown_content += f"**URL**: `{api['url']}`\n\n"
                markdown_content += f"**Method**: {api['method']}\n\n"
                
                if api['request']['body'] != "No body required":
                    markdown_content += "**Request Headers**:\n"
                    markdown_content += "```json\n"
                    markdown_content += json.dumps(api['request']['headers'], indent=2)
                    markdown_content += "\n```\n\n"
                    
                    markdown_content += "**Request Body**:\n"
                    markdown_content += "```json\n"
                    markdown_content += json.dumps(api['request']['body'], indent=2)
                    markdown_content += "\n```\n\n"
                
                markdown_content += "**Response**:\n"
                markdown_content += "```json\n"
                markdown_content += json.dumps({
                    "status_code": api['response']['status_code'],
                    "body": api['response']['body']
                }, indent=2)
                markdown_content += "\n```\n\n"
                markdown_content += "---\n\n"
        
        # Add summary
        total_apis = len(self.documentation)
        successful_apis = len([doc for doc in self.documentation if doc['success']])
        success_rate = (successful_apis / total_apis * 100) if total_apis > 0 else 0
        
        markdown_content += f"""## Summary

- **Total APIs**: {total_apis}
- **Successful**: {successful_apis}
- **Failed**: {total_apis - successful_apis}
- **Success Rate**: {success_rate:.1f}%

### API Status by Category

"""
        
        for category_name, apis in categories.items():
            successful = len([api for api in apis if api['success']])
            total = len(apis)
            markdown_content += f"- **{category_name}**: {successful}/{total} ({successful/total*100:.1f}%)\n"
        
        return markdown_content
    
    def save_documentation(self):
        """Save documentation to files"""
        timestamp = int(time.time())
        
        # Save JSON documentation
        json_filename = f"ondc_api_documentation_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump({
                "metadata": {
                    "base_url": self.base_url,
                    "generated_at": self.get_timestamp(),
                    "transaction_id": self.transaction_id,
                    "total_apis": len(self.documentation)
                },
                "apis": self.documentation
            }, f, indent=2)
        
        # Save Markdown documentation  
        markdown_filename = f"ondc_api_documentation_{timestamp}.md"
        markdown_content = self.generate_markdown_documentation()
        with open(markdown_filename, 'w') as f:
            f.write(markdown_content)
        
        print("💾 DOCUMENTATION SAVED:")
        print(f"   📄 JSON: {json_filename}")
        print(f"   📝 Markdown: {markdown_filename}")
        
        return json_filename, markdown_filename

def main():
    """Generate complete API documentation"""
    print("🎯 ONDC BAP API Documentation Generator Starting...")
    print("=" * 60)
    
    generator = ONDCAPIDocumentationGenerator()
    
    # Generate documentation for all APIs
    generator.generate_all_api_docs()
    
    # Save documentation files
    json_file, markdown_file = generator.save_documentation()
    
    # Print summary
    total_apis = len(generator.documentation)
    successful_apis = len([doc for doc in generator.documentation if doc['success']])
    success_rate = (successful_apis / total_apis * 100) if total_apis > 0 else 0
    
    print("\n" + "=" * 60)
    print("📊 DOCUMENTATION GENERATION COMPLETE")
    print("=" * 60)
    print(f"📋 Total APIs Documented: {total_apis}")
    print(f"✅ Working APIs: {successful_apis}")
    print(f"❌ Failed APIs: {total_apis - successful_apis}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    print()
    print("📂 Generated Files:")
    print(f"   • {json_file} (JSON format)")  
    print(f"   • {markdown_file} (Markdown format)")
    print()
    print("🎉 Documentation ready for use!")

if __name__ == "__main__":
    main()