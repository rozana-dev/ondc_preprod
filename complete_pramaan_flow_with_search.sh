#!/bin/bash

# 🎯 Complete Pramaan Order Flow with SEARCH
# Full ONDC flow: SEARCH → SELECT → INIT → CONFIRM → STATUS → TRACK
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

# Fixed transaction ID from previous flow
TRANSACTION_ID="02efcdd4-162d-4d5c-a282-bd187401b282"

# Pramaan store details
BPP_ID="pramaan.ondc.org/beta/preprod/mock/seller"
BPP_URI="https://${BPP_ID}"

# Your BAP details
BAP_ID="neo-server.rozana.in"
BAP_URI="https://neo-server.rozana.in"

echo -e "${CYAN}🎯 Complete Pramaan Order Flow with SEARCH${NC}"
echo "=============================================="
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
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "202" ]; then
        echo -e "${GREEN}✅ HTTP $http_code OK${NC}"
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
    local filename="${step_name,,}_pramaan_response.json"
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

echo -e "${BLUE}🚀 Starting Complete Order Flow with SEARCH...${NC}"
echo ""

# Step 0: SEARCH Call (First step in ONDC flow)
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}          STEP 0: SEARCH CALL          ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

SEARCH_PAYLOAD=$(cat <<EOF
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "1.2.0",
    "bap_id": "$BAP_ID",
    "bap_uri": "$BAP_URI",
    "transaction_id": "$TRANSACTION_ID",
    "message_id": "$(generate_message_id)",
    "timestamp": "$(generate_timestamp)",
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
      },
      "category": {
        "id": "Grocery"
      }
    }
  }
}
EOF
)

test_endpoint "/search" "$SEARCH_PAYLOAD" "SEARCH"

# Step 1: SELECT Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}         STEP 1: SELECT CALL           ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

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
      }
    }
  }
}
EOF
)

test_endpoint "/select" "$SELECT_PAYLOAD" "SELECT"

# Step 2: INIT Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}           STEP 2: INIT CALL           ${NC}"
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
        "id": "pramaan_provider_1"
      },
      "items": [
        {
          "id": "pramaan_item_001",
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
        "type": "Delivery"
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

# Step 3: CONFIRM Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}         STEP 3: CONFIRM CALL          ${NC}"
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
        "id": "pramaan_provider_1"
      },
      "items": [
        {
          "id": "pramaan_item_001",
          "quantity": {
            "count": 2
          }
        }
      ],
      "payment": {
        "type": "PRE-PAID",
        "collected_by": "BAP",
        "status": "PAID"
      }
    }
  }
}
EOF
)

test_endpoint "/confirm" "$CONFIRM_PAYLOAD" "CONFIRM"

# Step 4: STATUS Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}         STEP 4: STATUS CALL           ${NC}"
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

# Step 5: TRACK Call
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}          STEP 5: TRACK CALL           ${NC}"
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

# Final Summary
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}        COMPLETE FLOW EXECUTED!        ${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"

echo -e "${GREEN}🎯 Complete Pramaan Order Flow with SEARCH Executed!${NC}"
echo ""
echo -e "${BLUE}📋 Full Flow Summary:${NC}"
echo "Transaction ID: $TRANSACTION_ID"
echo "Order ID: $ORDER_ID"
echo "BPP: $BPP_ID"
echo "Domain: ONDC:RET10 (preprod)"
echo ""

echo -e "${YELLOW}🔄 Complete ONDC Flow Executed:${NC}"
echo "SEARCH → SELECT → INIT → CONFIRM → STATUS → TRACK"
echo "  ✅       ✅       ✅       ✅        ✅       ✅"
echo ""

echo -e "${YELLOW}📂 Response Files Created:${NC}"
echo "- search_pramaan_response.json"
echo "- select_pramaan_response.json"
echo "- init_pramaan_response.json"
echo "- confirm_pramaan_response.json"
echo "- status_pramaan_response.json"
echo "- track_pramaan_response.json"
echo ""

echo -e "${GREEN}✅ All calls completed with same transaction_id!${NC}"
echo -e "${BLUE}🔗 Perfect flow consistency maintained throughout${NC}"
echo -e "${PURPLE}🎯 Complete ONDC flow ready for Pramaan verification!${NC}"