#!/bin/bash

# Test eKYC Endpoints Locally
# This script tests the eKYC endpoints that are now at root level

echo "🧪 Testing eKYC Endpoints Locally"
echo "================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local method=$1
    local url=$2
    local payload=$3
    local description=$4
    
    echo -e "${YELLOW}Testing:${NC} $description"
    echo -e "URL: $url"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s "$url")
    else
        response=$(curl -s -X POST "$url" -H "Content-Type: application/json" -d "$payload")
    fi
    
    if [[ $response == *"404 Not Found"* ]] || [[ $response == *"detail"*"Not Found"* ]]; then
        echo -e "${RED}❌ FAILED${NC}"
    else
        echo -e "${GREEN}✅ WORKING${NC}"
        if command -v jq &> /dev/null && echo "$response" | jq . &> /dev/null; then
            echo "$response" | jq .
        else
            echo "$response"
        fi
    fi
    echo ""
}

# Test local endpoints
BASE_URL="http://localhost:8000"

# Test eKYC health endpoint
test_endpoint "GET" "$BASE_URL/ekyc/health" "" "eKYC Health Check"

# Test eKYC search endpoint
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
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
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

test_endpoint "POST" "$BASE_URL/ekyc/search" "$search_payload" "eKYC Search"

# Test eKYC select endpoint
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
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
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

test_endpoint "POST" "$BASE_URL/ekyc/select" "$select_payload" "eKYC Select"

# Test eKYC verify endpoint
verify_payload='{
    "context": {
        "domain": "ONDC:RET10",
        "country": "IND",
        "city": "std:011",
        "action": "verify",
        "core_version": "1.2.0",
        "bap_id": "neo-server.rozana.in",
        "bap_uri": "https://neo-server.rozana.in",
        "transaction_id": "test-transaction-789",
        "message_id": "test-message-789",
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "provider": {
                "id": "pramaan.ondc.org"
            },
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

test_endpoint "POST" "$BASE_URL/ekyc/verify" "$verify_payload" "eKYC Verify"

echo "🎉 Local eKYC testing completed!"
echo ""
echo "📝 If all tests are working, you can deploy this to the server."
echo "   The eKYC endpoints are now at the same root level as other working endpoints."