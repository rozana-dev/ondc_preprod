#!/bin/bash

# Test eKYC Endpoints for ONDC BAP
# This script tests all eKYC endpoints with proper payloads

echo "🧪 Testing eKYC Endpoints for ONDC BAP"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to test endpoint
test_endpoint() {
    local method=$1
    local url=$2
    local payload=$3
    local description=$4
    
    echo -n "Testing $description... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s "$url")
    else
        response=$(curl -s -X POST "$url" -H "Content-Type: application/json" -d "$payload")
    fi
    
    if [[ $response == *"404 Not Found"* ]]; then
        echo -e "${RED}❌ FAILED${NC}"
        echo "   URL: $url"
        echo "   Response: $response"
    elif [[ $response == *"error"* ]] || [[ $response == *"Error"* ]]; then
        echo -e "${YELLOW}⚠️  WARNING${NC}"
        echo "   URL: $url"
        echo "   Response: $(echo "$response" | head -c 100)..."
    else
        echo -e "${GREEN}✅ WORKING${NC}"
        echo "   URL: $url"
        echo "   Response: $(echo "$response" | head -c 100)..."
    fi
    echo ""
}

# Test eKYC health endpoint
echo "🔍 Testing eKYC Health Endpoint:"
test_endpoint "GET" "https://neo-server.rozana.in/ekyc/health" "" "eKYC Health Check"

# Test eKYC search endpoint
echo "🔍 Testing eKYC Search Endpoint:"
search_payload='{
    "context": {
        "domain": "ONDC:RET10",
        "country": "IND",
        "city": "std:011",
        "action": "search",
        "core_version": "1.2.0",
        "bap_id": "neo-server.rozana.in",
        "bap_uri": "https://neo-server.rozana.in",
        "transaction_id": "test-transaction-123",
        "message_id": "test-message-123",
        "timestamp": "2025-08-22T10:00:00Z",
        "ttl": "PT30S"
    },
    "message": {
        "intent": {
            "item": {
                "descriptor": {
                    "name": "eKYC Verification"
                }
            }
        }
    }
}'
test_endpoint "POST" "https://neo-server.rozana.in/ekyc/search" "$search_payload" "eKYC Search"

# Test eKYC select endpoint
echo "🔍 Testing eKYC Select Endpoint:"
select_payload='{
    "context": {
        "domain": "ONDC:RET10",
        "country": "IND",
        "city": "std:011",
        "action": "select",
        "core_version": "1.2.0",
        "bap_id": "neo-server.rozana.in",
        "bap_uri": "https://neo-server.rozana.in",
        "transaction_id": "test-transaction-456",
        "message_id": "test-message-456",
        "timestamp": "2025-08-22T10:00:00Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "provider": {
                "id": "pramaan.ondc.org"
            },
            "items": [
                {
                    "id": "ekyc_verification",
                    "name": "eKYC Verification"
                }
            ]
        }
    }
}'
test_endpoint "POST" "https://neo-server.rozana.in/ekyc/select" "$select_payload" "eKYC Select"

# Test eKYC initiate endpoint
echo "🔍 Testing eKYC Initiate Endpoint:"
initiate_payload='{
    "context": {
        "domain": "ONDC:RET10",
        "country": "IND",
        "city": "std:011",
        "action": "initiate",
        "core_version": "1.2.0",
        "bap_id": "neo-server.rozana.in",
        "bap_uri": "https://neo-server.rozana.in",
        "transaction_id": "test-transaction-789",
        "message_id": "test-message-789",
        "timestamp": "2025-08-22T10:00:00Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "provider": {
                "id": "pramaan.ondc.org"
            },
            "items": [
                {
                    "id": "ekyc_verification",
                    "name": "eKYC Verification"
                }
            ],
            "fulfillment": {
                "type": "ONDC:ekyc",
                "start": {
                    "location": {
                        "gps": "12.9716,77.5946"
                    }
                }
            }
        }
    }
}'
test_endpoint "POST" "https://neo-server.rozana.in/ekyc/initiate" "$initiate_payload" "eKYC Initiate"

# Test eKYC verify endpoint
echo "🔍 Testing eKYC Verify Endpoint:"
verify_payload='{
    "context": {
        "domain": "ONDC:RET10",
        "country": "IND",
        "city": "std:011",
        "action": "verify",
        "core_version": "1.2.0",
        "bap_id": "neo-server.rozana.in",
        "bap_uri": "https://neo-server.rozana.in",
        "transaction_id": "test-transaction-101",
        "message_id": "test-message-101",
        "timestamp": "2025-08-22T10:00:00Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "provider": {
                "id": "pramaan.ondc.org"
            },
            "items": [
                {
                    "id": "ekyc_verification",
                    "name": "eKYC Verification"
                }
            ],
            "fulfillment": {
                "type": "ONDC:ekyc",
                "verification": {
                    "document_type": "AADHAAR",
                    "document_number": "123456789012"
                }
            }
        }
    }
}'
test_endpoint "POST" "https://neo-server.rozana.in/ekyc/verify" "$verify_payload" "eKYC Verify"

# Test eKYC status endpoint
echo "🔍 Testing eKYC Status Endpoint:"
status_payload='{
    "context": {
        "domain": "ONDC:RET10",
        "country": "IND",
        "city": "std:011",
        "action": "status",
        "core_version": "1.2.0",
        "bap_id": "neo-server.rozana.in",
        "bap_uri": "https://neo-server.rozana.in",
        "transaction_id": "test-transaction-202",
        "message_id": "test-message-202",
        "timestamp": "2025-08-22T10:00:00Z",
        "ttl": "PT30S"
    },
    "message": {
        "order_id": "test-order-123"
    }
}'
test_endpoint "POST" "https://neo-server.rozana.in/ekyc/status" "$status_payload" "eKYC Status"

echo "🎉 eKYC endpoint testing completed!"
echo ""
echo "📝 Summary:"
echo "   - All eKYC endpoints should be accessible at /ekyc/"
echo "   - Endpoints follow ONDC eKYC specification"
echo "   - Proper error handling and responses"
echo ""
echo "🔍 Available eKYC Endpoints:"
echo "   - GET  /ekyc/health - Health check"
echo "   - POST /ekyc/search - Search eKYC providers"
echo "   - POST /ekyc/select - Select eKYC provider"
echo "   - POST /ekyc/initiate - Initiate eKYC process"
echo "   - POST /ekyc/verify - Verify eKYC documents"
echo "   - POST /ekyc/status - Check eKYC status" 