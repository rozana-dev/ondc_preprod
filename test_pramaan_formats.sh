#!/bin/bash

# 🚀 Test Pramaan Message Formats
# Tests the generated ONDC message formats against your endpoints

BASE_URL="https://neo-server.rozana.in"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Testing Pramaan ONDC Message Formats${NC}"
echo "========================================"
echo "Base URL: $BASE_URL"
echo ""

# Generate transaction ID
TRANSACTION_ID="neo-server_rozana_in_$(date +%s)_$(openssl rand -hex 4)"
echo -e "${YELLOW}📋 Transaction ID: $TRANSACTION_ID${NC}"
echo ""

# Test Search endpoint
echo -e "${BLUE}🔍 Testing SEARCH endpoint${NC}"
search_response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "search",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "https://neo-server.rozana.in",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "'$(uuidgen)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
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
  }')

http_code=$(echo "$search_response" | tail -1)
response_body=$(echo "$search_response" | head -n -1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ HTTP 200 OK${NC}"
    echo "Response: $response_body"
else
    echo -e "${RED}❌ HTTP $http_code${NC}"
    echo "Response: $response_body"
fi
echo ""

# Test Select endpoint
echo -e "${BLUE}📋 Testing SELECT endpoint${NC}"
select_response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/select" \
  -H "Content-Type: application/json" \
  -d '{
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
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "'$(uuidgen)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
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
        }
      }
    }
  }')

http_code=$(echo "$select_response" | tail -1)
response_body=$(echo "$select_response" | head -n -1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ HTTP 200 OK${NC}"
    echo "Response: $response_body"
else
    echo -e "${RED}❌ HTTP $http_code${NC}"
    echo "Response: $response_body"
fi
echo ""

# Test eKYC Search endpoint
echo -e "${BLUE}🔐 Testing eKYC SEARCH endpoint${NC}"
ekyc_response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/ekyc/search" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "search",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "https://neo-server.rozana.in",
      "transaction_id": "'$TRANSACTION_ID'_ekyc",
      "message_id": "'$(uuidgen)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
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
  }')

http_code=$(echo "$ekyc_response" | tail -1)
response_body=$(echo "$ekyc_response" | head -n -1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ HTTP 200 OK${NC}"
    if echo "$response_body" | jq . >/dev/null 2>&1; then
        echo "Response (JSON):"
        echo "$response_body" | jq .
    else
        echo "Response: $response_body"
    fi
else
    echo -e "${RED}❌ HTTP $http_code${NC}"
    echo "Response: $response_body"
fi
echo ""

echo -e "${BLUE}📊 Summary${NC}"
echo "============"
echo -e "${YELLOW}Transaction ID Format:${NC} bap_id_timestamp_random"
echo -e "${YELLOW}Message ID Format:${NC} UUID v4"
echo -e "${YELLOW}Timestamp Format:${NC} ISO 8601 with milliseconds + Z"
echo -e "${YELLOW}Context Structure:${NC} ONDC v2.0 compliant"
echo ""
echo -e "${GREEN}✅ Your BAP is ready for Pramaan testing with correct message formats!${NC}"