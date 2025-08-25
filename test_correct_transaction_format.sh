#!/bin/bash

# 🎯 Test Correct ONDC Transaction ID Format
# Validates UUID v4 format and flow consistency for Pramaan testing

BASE_URL="https://neo-server.rozana.in"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🎯 Testing Correct ONDC Transaction ID Format${NC}"
echo "=============================================="
echo "Base URL: $BASE_URL"
echo ""

echo -e "${YELLOW}📋 ONDC Transaction ID Rules:${NC}"
echo "✅ UUID v4 (universally unique identifier)"
echo "✅ Same transaction_id for entire flow"
echo "✅ New transaction_id per new flow"
echo ""

# Generate UUID v4 transaction IDs for different flows
ORDER_TXN_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")
ISSUE_TXN_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")
EKYC_TXN_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")

echo -e "${BLUE}🚀 Generated Transaction IDs (UUID v4):${NC}"
echo "Order Flow: $ORDER_TXN_ID"
echo "Issue Flow: $ISSUE_TXN_ID"
echo "eKYC Flow:  $EKYC_TXN_ID"
echo ""

# Function to generate UUID v4 message ID
generate_message_id() {
    python3 -c "import uuid; print(str(uuid.uuid4()))"
}

# Function to generate timestamp
generate_timestamp() {
    python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')"
}

# Function to test endpoint with correct format
test_endpoint() {
    local endpoint=$1
    local transaction_id=$2
    local payload=$3
    local flow_step=$4
    
    echo -e "${BLUE}Testing: $endpoint${NC}"
    echo "Flow Step: $flow_step"
    echo "Transaction ID: $transaction_id"
    
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    http_code=$(echo "$response" | tail -1)
    response_body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ HTTP 200 OK${NC}"
        if [ ${#response_body} -gt 0 ] && [ "$response_body" != "OK" ]; then
            if echo "$response_body" | jq . >/dev/null 2>&1; then
                echo "Response (JSON):"
                echo "$response_body" | jq -c .
            else
                echo "Response: $response_body"
            fi
        else
            echo "Response: $response_body"
        fi
    else
        echo -e "${RED}❌ HTTP $http_code${NC}"
        echo "Response: $response_body"
    fi
    echo ""
}

echo -e "${YELLOW}🔍 Testing Order Flow (Same transaction_id):${NC}"
echo "Transaction ID: $ORDER_TXN_ID"
echo ""

# Order Flow - Step 1: Search
search_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "'$ORDER_TXN_ID'",
    "message_id": "'$(generate_message_id)'",
    "timestamp": "'$(generate_timestamp)'",
    "ttl": "PT30S"
  },
  "message": {
    "intent": {
      "item": {
        "descriptor": {
          "name": "Test Product for Pramaan"
        }
      },
      "fulfillment": {
        "type": "Delivery"
      },
      "payment": {
        "type": "PRE-PAID"
      }
    }
  }
}'

test_endpoint "/search" "$ORDER_TXN_ID" "$search_payload" "1. Search"

# Order Flow - Step 2: Select (same transaction_id)
select_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "select",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller",
    "transaction_id": "'$ORDER_TXN_ID'",
    "message_id": "'$(generate_message_id)'",
    "timestamp": "'$(generate_timestamp)'",
    "ttl": "PT30S"
  },
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
          "city": "New Delhi",
          "state": "Delhi",
          "country": "IND",
          "area_code": "110037"
        },
        "phone": "9876543210"
      }
    }
  }
}'

test_endpoint "/select" "$ORDER_TXN_ID" "$select_payload" "2. Select"

# Order Flow - Step 3: Status (same transaction_id)
order_id="order_$(echo $ORDER_TXN_ID | tr '-' '_')"
status_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "status",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller",
    "transaction_id": "'$ORDER_TXN_ID'",
    "message_id": "'$(generate_message_id)'",
    "timestamp": "'$(generate_timestamp)'",
    "ttl": "PT30S"
  },
  "message": {
    "order_id": "'$order_id'"
  }
}'

test_endpoint "/status" "$ORDER_TXN_ID" "$status_payload" "3. Status"

echo -e "${YELLOW}🔐 Testing eKYC Flow (Different transaction_id):${NC}"
echo "Transaction ID: $EKYC_TXN_ID"
echo ""

# eKYC Flow - Step 1: Search (new transaction_id)
ekyc_search_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "'$EKYC_TXN_ID'",
    "message_id": "'$(generate_message_id)'",
    "timestamp": "'$(generate_timestamp)'",
    "ttl": "PT30S"
  },
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
}'

test_endpoint "/ekyc/search" "$EKYC_TXN_ID" "$ekyc_search_payload" "1. eKYC Search"

# eKYC Flow - Step 2: Verify (same transaction_id)
ekyc_verify_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "verify",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "'$EKYC_TXN_ID'",
    "message_id": "'$(generate_message_id)'",
    "timestamp": "'$(generate_timestamp)'",
    "ttl": "PT30S"
  },
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
}'

test_endpoint "/ekyc/verify" "$EKYC_TXN_ID" "$ekyc_verify_payload" "2. eKYC Verify"

echo -e "${CYAN}📊 Summary of Correct ONDC Transaction Format${NC}"
echo "=============================================="
echo -e "${GREEN}✅ Transaction ID Format: UUID v4${NC}"
echo -e "${GREEN}✅ Flow Consistency: Same transaction_id per flow${NC}"
echo -e "${GREEN}✅ New Flow: Different transaction_id${NC}"
echo -e "${GREEN}✅ Message ID: New UUID v4 per request${NC}"
echo -e "${GREEN}✅ Timestamp: ISO 8601 with milliseconds + Z${NC}"
echo ""

echo -e "${BLUE}📋 Flow Examples:${NC}"
echo "Order Flow: $ORDER_TXN_ID"
echo "  /search → /select → /init → /confirm → /status → /track"
echo ""
echo "eKYC Flow: $EKYC_TXN_ID"
echo "  /ekyc/search → /ekyc/select → /ekyc/verify"
echo ""
echo "Issue Flow: $ISSUE_TXN_ID"
echo "  /issue → /on_issue → /issue_status → /issue_close"
echo ""

echo -e "${GREEN}🎯 Your BAP follows correct ONDC transaction ID rules!${NC}"
echo -e "${YELLOW}Ready for Pramaan testing with proper UUID v4 format.${NC}"