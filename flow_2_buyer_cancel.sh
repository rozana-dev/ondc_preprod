#!/bin/bash

# 🚀 Flow 2: Buyer Side Order Cancellation
# Complete order flow with buyer-initiated cancellation

set -e

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"
ORDER_ID="order_${TRANSACTION_ID}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Flow 2: Buyer Side Order Cancellation${NC}"
echo "=========================================="
echo "Transaction ID: $TRANSACTION_ID"
echo "Order ID: $ORDER_ID"
echo "BPP URI: $BPP_URI"
echo ""

# Function to make API calls
make_api_call() {
    local step=$1
    local endpoint=$2
    local payload=$3
    
    echo -e "${YELLOW}Step $step: $endpoint${NC}"
    echo "Payload:"
    echo "$payload" | jq .
    echo ""
    
    response=$(curl -s -X POST "$BASE_URL$endpoint" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    echo -e "${GREEN}Response:${NC}"
    echo "$response" | jq .
    echo ""
    echo "----------------------------------------"
    echo ""
}

# Step 1: Select
echo -e "${YELLOW}📋 Step 1: Select Items${NC}"
select_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "select",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "'$BASE_URL'",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "'$BPP_URI'",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
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
          "building": "123 Main St",
          "locality": "Downtown",
          "city": "New Delhi",
          "state": "Delhi",
          "country": "IND",
          "area_code": "110037"
        },
        "phone": "9876543210",
        "email": "john@example.com"
      },
      "fulfillment": {
        "type": "Delivery",
        "end": {
          "location": {
            "gps": "28.6139,77.2090",
            "address": {
              "name": "John Doe",
              "building": "123 Main St",
              "locality": "Downtown",
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
}'

make_api_call "1" "/select" "$select_payload"

echo -e "${RED}⏳ Wait for on_select callback before proceeding...${NC}"
read -p "Press Enter after receiving on_select callback to continue with init..."

# Step 2: Init
echo -e "${YELLOW}🏁 Step 2: Initialize Order${NC}"
init_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "init",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "'$BASE_URL'",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "'$BPP_URI'",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
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
          "building": "123 Main St",
          "locality": "Downtown",
          "city": "New Delhi",
          "state": "Delhi",
          "country": "IND",
          "area_code": "110037"
        },
        "phone": "9876543210",
        "email": "john@example.com"
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
}'

make_api_call "2" "/init" "$init_payload"

echo -e "${RED}⏳ Wait for on_init callback before proceeding...${NC}"
read -p "Press Enter after receiving on_init callback to continue with confirm..."

# Step 3: Confirm
echo -e "${YELLOW}✅ Step 3: Confirm Order${NC}"
confirm_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "confirm",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "'$BASE_URL'",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "'$BPP_URI'",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
  },
  "message": {
    "order": {
      "id": "'$ORDER_ID'",
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
}'

make_api_call "3" "/confirm" "$confirm_payload"

echo -e "${RED}⏳ Wait for on_confirm callback before proceeding...${NC}"
read -p "Press Enter after receiving on_confirm callback to continue with cancellation..."

# Step 4: Cancel (Buyer-initiated)
echo -e "${YELLOW}❌ Step 4: Cancel Order (Buyer-initiated)${NC}"
cancel_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "cancel",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "'$BASE_URL'",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "'$BPP_URI'",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
  },
  "message": {
    "order_id": "'$ORDER_ID'",
    "cancellation_reason_id": "001",
    "descriptor": {
      "short_desc": "Customer requested cancellation",
      "long_desc": "Customer changed mind and wants to cancel the order"
    }
  }
}'

make_api_call "4" "/cancel" "$cancel_payload"

echo -e "${GREEN}🎉 Flow 2 Complete!${NC}"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "  ✅ Select - Items selected successfully"
echo "  ✅ Init - Order initialized"
echo "  ✅ Confirm - Order confirmed"
echo "  ❌ Cancel - Order cancelled by buyer"
echo ""
echo -e "${GREEN}🚫 Expected final status: Order cancelled${NC}"
echo -e "${YELLOW}📝 Transaction ID: $TRANSACTION_ID${NC}"
echo -e "${YELLOW}📦 Order ID: $ORDER_ID${NC}"
echo ""
echo "Wait for on_cancel callback confirming the cancellation."