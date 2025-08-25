#!/bin/bash

# 🎯 Complete Pramaan Order Flow
# Using transaction_id: 02efcdd4-162d-4d5c-a282-bd187401b282
# BPP: pramaan.ondc.org/beta/preprod/mock/seller

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Fixed transaction ID from SELECT call
TRANSACTION_ID="02efcdd4-162d-4d5c-a282-bd187401b282"

# Pramaan store details
BPP_ID="pramaan.ondc.org/beta/preprod/mock/seller"
BPP_URI="https://${BPP_ID}"

# Your BAP details
BAP_ID="neo-server.rozana.in"
BAP_URI="https://neo-server.rozana.in"

echo -e "${CYAN}🎯 Complete Pramaan Order Flow${NC}"
echo "=========================================="
echo -e "${BLUE}Transaction ID: $TRANSACTION_ID${NC}"
echo -e "${BLUE}BPP: $BPP_ID${NC}"
echo -e "${BLUE}Domain: ONDC:RET10 (preprod)${NC}"
echo ""

# Function to generate UUID v4 message ID
generate_message_id() {
    python3 -c "import uuid; print(str(uuid.uuid4()))"
}

# Function to generate timestamp
generate_timestamp() {
    python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')"
}

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local payload=$2
    local step_name=$3
    
    echo -e "${YELLOW}📤 Step: $step_name${NC}"
    echo "Endpoint: $endpoint"
    echo "Transaction ID: $TRANSACTION_ID"
    
    response=$(curl -s -w "\n%{http_code}" -X POST "$BAP_URI$endpoint" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$payload")
    
    http_code=$(echo "$response" | tail -1)
    response_body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ HTTP 200 OK${NC}"
        if [ ${#response_body} -gt 0 ] && [ "$response_body" != "OK" ]; then
            if echo "$response_body" | jq . >/dev/null 2>&1; then
                echo "Response:"
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
    
    # Save response
    local filename="${step_name,,}_response_$(echo $TRANSACTION_ID | tr '-' '_').json"
    cat > "$filename" <<EOF
{
  "step": "$step_name",
  "endpoint": "$endpoint",
  "transaction_id": "$TRANSACTION_ID",
  "timestamp": "$(generate_timestamp)",
  "http_code": $http_code,
  "response": $(echo "$response_body" | jq -R .),
  "payload": $payload
}
EOF
    echo -e "${PURPLE}💾 Saved: $filename${NC}"
    echo ""
}

echo -e "${BLUE}🚀 Starting Complete Order Flow...${NC}"
echo ""

# Step 1: INIT Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}           STEP 1: INIT CALL           ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

INIT_PAYLOAD=$(cat <<EOF
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "init",
    "core_version": "1.2.0",
    "bap_id": "$BAP_ID",
    "bap_uri": "$BAP_URI",
    "bpp_id": "$BPP_ID",
    "bpp_uri": "$BPP_URI",
    "transaction_id": "$TRANSACTION_ID",
    "message_id": "$(generate_message_id)",
    "timestamp": "$(generate_timestamp)",
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
          "quantity": {
            "count": 2
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
        "email": "test@neo-server.rozana.in"
      },
      "fulfillment": {
        "id": "fulfillment_1",
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
      },
      "payment": {
        "type": "PRE-PAID",
        "collected_by": "BAP"
      }
    }
  }
}
EOF
)

test_endpoint "/init" "$INIT_PAYLOAD" "INIT"

# Step 2: CONFIRM Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}         STEP 2: CONFIRM CALL          ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

ORDER_ID="order_$(echo $TRANSACTION_ID | tr '-' '_')"

CONFIRM_PAYLOAD=$(cat <<EOF
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "confirm",
    "core_version": "1.2.0",
    "bap_id": "$BAP_ID",
    "bap_uri": "$BAP_URI",
    "bpp_id": "$BPP_ID",
    "bpp_uri": "$BPP_URI",
    "transaction_id": "$TRANSACTION_ID",
    "message_id": "$(generate_message_id)",
    "timestamp": "$(generate_timestamp)",
    "ttl": "PT30S"
  },
  "message": {
    "order": {
      "id": "$ORDER_ID",
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
          "quantity": {
            "count": 2
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
        "email": "test@neo-server.rozana.in"
      },
      "fulfillment": {
        "id": "fulfillment_1",
        "type": "Delivery"
      },
      "payment": {
        "type": "PRE-PAID",
        "collected_by": "BAP",
        "status": "PAID"
      },
      "quote": {
        "price": {
          "currency": "INR",
          "value": "200.00"
        }
      }
    }
  }
}
EOF
)

test_endpoint "/confirm" "$CONFIRM_PAYLOAD" "CONFIRM"

# Step 3: STATUS Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}         STEP 3: STATUS CALL           ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

STATUS_PAYLOAD=$(cat <<EOF
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "status",
    "core_version": "1.2.0",
    "bap_id": "$BAP_ID",
    "bap_uri": "$BAP_URI",
    "bpp_id": "$BPP_ID",
    "bpp_uri": "$BPP_URI",
    "transaction_id": "$TRANSACTION_ID",
    "message_id": "$(generate_message_id)",
    "timestamp": "$(generate_timestamp)",
    "ttl": "PT30S"
  },
  "message": {
    "order_id": "$ORDER_ID"
  }
}
EOF
)

test_endpoint "/status" "$STATUS_PAYLOAD" "STATUS"

# Step 4: TRACK Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}          STEP 4: TRACK CALL           ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

TRACK_PAYLOAD=$(cat <<EOF
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "track",
    "core_version": "1.2.0",
    "bap_id": "$BAP_ID",
    "bap_uri": "$BAP_URI",
    "bpp_id": "$BPP_ID",
    "bpp_uri": "$BPP_URI",
    "transaction_id": "$TRANSACTION_ID",
    "message_id": "$(generate_message_id)",
    "timestamp": "$(generate_timestamp)",
    "ttl": "PT30S"
  },
  "message": {
    "order_id": "$ORDER_ID"
  }
}
EOF
)

test_endpoint "/track" "$TRACK_PAYLOAD" "TRACK"

# Step 5: UPDATE Call (Optional)
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}         STEP 5: UPDATE CALL           ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

UPDATE_PAYLOAD=$(cat <<EOF
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "update",
    "core_version": "1.2.0",
    "bap_id": "$BAP_ID",
    "bap_uri": "$BAP_URI",
    "bpp_id": "$BPP_ID",
    "bpp_uri": "$BPP_URI",
    "transaction_id": "$TRANSACTION_ID",
    "message_id": "$(generate_message_id)",
    "timestamp": "$(generate_timestamp)",
    "ttl": "PT30S"
  },
  "message": {
    "update_target": "order",
    "order": {
      "id": "$ORDER_ID",
      "status": "UPDATED"
    }
  }
}
EOF
)

test_endpoint "/update" "$UPDATE_PAYLOAD" "UPDATE"

# Final Summary
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}           FLOW COMPLETED!             ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

echo -e "${GREEN}🎯 Complete Pramaan Order Flow Executed!${NC}"
echo ""
echo -e "${BLUE}📋 Flow Summary:${NC}"
echo "Transaction ID: $TRANSACTION_ID"
echo "Order ID: $ORDER_ID"
echo "BPP: $BPP_ID"
echo "Domain: ONDC:RET10 (preprod)"
echo ""

echo -e "${YELLOW}📂 Response Files Created:${NC}"
echo "- init_response_$(echo $TRANSACTION_ID | tr '-' '_').json"
echo "- confirm_response_$(echo $TRANSACTION_ID | tr '-' '_').json"
echo "- status_response_$(echo $TRANSACTION_ID | tr '-' '_').json"
echo "- track_response_$(echo $TRANSACTION_ID | tr '-' '_').json"
echo "- update_response_$(echo $TRANSACTION_ID | tr '-' '_').json"
echo ""

echo -e "${GREEN}✅ All calls completed with same transaction_id!${NC}"
echo -e "${BLUE}🔗 Flow consistency maintained throughout${NC}"
echo -e "${PURPLE}🎯 Ready for Pramaan verification!${NC}"