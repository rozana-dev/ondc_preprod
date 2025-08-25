#!/bin/bash

# 🎯 Send SELECT call to Pramaan Store
# BPP ID: pramaan.ondc.org/beta/preprod/mock/seller
# Domain: RET10 (Retail)
# Environment: preprod

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🎯 Sending SELECT call to Pramaan Store${NC}"
echo "=" * 50
echo "BPP ID: pramaan.ondc.org/beta/preprod/mock/seller"
echo "Domain: ONDC:RET10 (Retail)"
echo "Environment: preprod"
echo ""

# Generate UUID v4 transaction ID and message ID
TRANSACTION_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")
MESSAGE_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")
TIMESTAMP=$(python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')")

# Pramaan store details
BPP_ID="pramaan.ondc.org/beta/preprod/mock/seller"
BPP_URI="https://${BPP_ID}"

# Your BAP details
BAP_ID="neo-server.rozana.in"
BAP_URI="https://neo-server.rozana.in"
BAP_ENDPOINT="${BAP_URI}/select"

echo -e "${BLUE}📋 Transaction Details:${NC}"
echo "Transaction ID: $TRANSACTION_ID"
echo "Message ID: $MESSAGE_ID"
echo "Timestamp: $TIMESTAMP"
echo "BPP URI: $BPP_URI"
echo "BAP Endpoint: $BAP_ENDPOINT"
echo ""

# Create SELECT payload
SELECT_PAYLOAD=$(cat <<EOF
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "select",
    "core_version": "1.2.0",
    "bap_id": "$BAP_ID",
    "bap_uri": "$BAP_URI",
    "bpp_id": "$BPP_ID",
    "bpp_uri": "$BPP_URI",
    "transaction_id": "$TRANSACTION_ID",
    "message_id": "$MESSAGE_ID",
    "timestamp": "$TIMESTAMP",
    "ttl": "PT30S"
  },
  "message": {
    "order": {
      "provider": {
        "id": "pramaan_provider_1",
        "descriptor": {
          "name": "Pramaan Test Store"
        }
      },
      "items": [
        {
          "id": "pramaan_item_001",
          "descriptor": {
            "name": "Test Product for Pramaan"
          },
          "category_id": "Grocery",
          "quantity": {
            "count": 2
          },
          "price": {
            "currency": "INR",
            "value": "100.00"
          }
        }
      ],
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
        "email": "test@neo-server.rozana.in",
        "created_at": "$TIMESTAMP",
        "updated_at": "$TIMESTAMP"
      },
      "fulfillment": {
        "id": "fulfillment_1",
        "type": "Delivery",
        "provider_id": "pramaan_provider_1",
        "tracking": true,
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
            "phone": "9876543210",
            "email": "test@neo-server.rozana.in"
          }
        }
      },
      "quote": {
        "price": {
          "currency": "INR",
          "value": "200.00"
        },
        "breakup": [
          {
            "title": "Test Product for Pramaan",
            "price": {
              "currency": "INR",
              "value": "200.00"
            }
          }
        ]
      },
      "payment": {
        "type": "PRE-PAID",
        "collected_by": "BAP",
        "status": "NOT-PAID"
      }
    }
  }
}
EOF
)

echo -e "${YELLOW}📤 Sending SELECT call...${NC}"
echo ""

# Send the SELECT request
response=$(curl -s -w "\n%{http_code}" -X POST "$BAP_ENDPOINT" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "$SELECT_PAYLOAD")

# Extract HTTP status code and response body
http_code=$(echo "$response" | tail -1)
response_body=$(echo "$response" | sed '$d')

echo -e "${BLUE}📥 Response Status: $http_code${NC}"

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ SELECT call successful!${NC}"
    
    if [ ${#response_body} -gt 0 ] && [ "$response_body" != "OK" ]; then
        echo ""
        echo -e "${BLUE}📋 Response:${NC}"
        if echo "$response_body" | jq . >/dev/null 2>&1; then
            echo "$response_body" | jq .
        else
            echo "$response_body"
        fi
    else
        echo "Response: $response_body"
    fi
else
    echo -e "${RED}❌ SELECT call failed!${NC}"
    echo "Response: $response_body"
fi

echo ""
echo "=" * 50
echo -e "${YELLOW}📋 IMPORTANT - Save this Transaction ID:${NC}"
echo -e "${GREEN}🔑 Transaction ID: $TRANSACTION_ID${NC}"
echo "=" * 50

# Save transaction details to file
FILENAME="pramaan_select_transaction_$(echo $TRANSACTION_ID | tr '-' '_').json"

cat > "$FILENAME" <<EOF
{
  "transaction_id": "$TRANSACTION_ID",
  "message_id": "$MESSAGE_ID",
  "timestamp": "$TIMESTAMP",
  "bpp_id": "$BPP_ID",
  "bpp_uri": "$BPP_URI",
  "domain": "ONDC:RET10",
  "environment": "preprod",
  "action": "select",
  "response_status": $http_code,
  "response_body": $(echo "$response_body" | jq -R .),
  "payload": $SELECT_PAYLOAD
}
EOF

echo -e "${BLUE}💾 Transaction details saved to: $FILENAME${NC}"
echo ""

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}🎯 SUCCESS!${NC}"
    echo -e "${GREEN}Transaction ID: $TRANSACTION_ID${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo "1. ✅ Note down this transaction ID for Pramaan testing"
    echo "2. ✅ Use the same transaction_id for subsequent calls in this flow"
    echo "3. ✅ This matches the domain (RET10) and environment (preprod) requirements"
    echo "4. ✅ BPP ID matches: pramaan.ondc.org/beta/preprod/mock/seller"
    echo ""
    echo -e "${CYAN}🔗 Flow Continuation:${NC}"
    echo "Use transaction_id '$TRANSACTION_ID' for:"
    echo "  - /init call"
    echo "  - /confirm call"  
    echo "  - /status call"
    echo "  - /track call"
else
    echo -e "${RED}❌ Failed to send SELECT call${NC}"
    exit 1
fi