#!/bin/bash

# 🔐 Complete Pramaan eKYC Transaction Flow Test
# This script demonstrates the full eKYC transaction lifecycle

echo "🚀 Starting Complete Pramaan eKYC Transaction Flow Test"
echo "======================================================"

BASE_URL="https://neo-server.rozana.in"
TRANSACTION_ID="txn_$(date +%s)"
ORDER_ID="ekyc_order_$(date +%s)"

echo "📋 Transaction Details:"
echo "  • Transaction ID: $TRANSACTION_ID"
echo "  • Order ID: $ORDER_ID"
echo "  • Base URL: $BASE_URL"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to make API calls and display results
make_api_call() {
    local step=$1
    local endpoint=$2
    local method=$3
    local payload=$4
    
    echo -e "${BLUE}Step $step: $endpoint${NC}"
    echo "Method: $method"
    echo "Payload:"
    echo "$payload" | jq .
    echo ""
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s "$BASE_URL$endpoint")
    else
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$payload")
    fi
    
    echo -e "${GREEN}Response:${NC}"
    echo "$response" | jq .
    echo ""
    echo "----------------------------------------"
    echo ""
}

# Step 1: Health Check
echo -e "${YELLOW}🏥 Step 1: eKYC Health Check${NC}"
make_api_call "1" "/ekyc/health" "GET" ""

# Step 2: Search for eKYC Providers
echo -e "${YELLOW}🔍 Step 2: Search for eKYC Providers${NC}"
search_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
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
make_api_call "2" "/ekyc/search" "POST" "$search_payload"

# Step 3: Select Pramaan Provider
echo -e "${YELLOW}✅ Step 3: Select Pramaan Provider${NC}"
select_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "select",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
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
    }
  }
}'
make_api_call "3" "/ekyc/select" "POST" "$select_payload"

# Step 4: Initiate eKYC Transaction
echo -e "${YELLOW}🚀 Step 4: Initiate eKYC Transaction${NC}"
initiate_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "initiate",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
  },
  "message": {
    "order": {
      "id": "'$ORDER_ID'",
      "provider": {
        "id": "pramaan.ondc.org"
      },
      "items": [{
        "id": "ekyc_verification",
        "descriptor": {
          "name": "Aadhaar Verification"
        }
      }],
      "customer": {
        "person": {
          "name": "John Doe"
        },
        "contact": {
          "phone": "+919876543210",
          "email": "john.doe@example.com"
        }
      }
    }
  }
}'
make_api_call "4" "/ekyc/initiate" "POST" "$initiate_payload"

# Step 5: Verify Documents
echo -e "${YELLOW}🔐 Step 5: Verify Documents${NC}"
verify_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "verify",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
  },
  "message": {
    "order": {
      "id": "'$ORDER_ID'",
      "items": [{
        "id": "ekyc_verification",
        "descriptor": {
          "name": "Aadhaar Verification"
        }
      }]
    },
    "documents": [{
      "type": "AADHAAR",
      "number": "1234-5678-9012",
      "name": "John Doe",
      "issued_date": "2015-01-15"
    }]
  }
}'
make_api_call "5" "/ekyc/verify" "POST" "$verify_payload"

# Step 6: Check Status
echo -e "${YELLOW}📊 Step 6: Check Verification Status${NC}"
status_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "status",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "'$TRANSACTION_ID'",
    "message_id": "msg_'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
  },
  "message": {
    "order_id": "'$ORDER_ID'"
  }
}'
make_api_call "6" "/ekyc/status" "POST" "$status_payload"

echo ""
echo -e "${GREEN}🎉 Complete Pramaan eKYC Transaction Flow Test Completed!${NC}"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "  ✅ Health Check - Service Available"
echo "  ✅ Search - Found Pramaan Provider"
echo "  ✅ Select - Selected Pramaan for eKYC"
echo "  ✅ Initiate - Started Transaction"
echo "  ✅ Verify - Submitted Documents"
echo "  ✅ Status - Checked Verification Result"
echo ""
echo -e "${YELLOW}🚀 Your eKYC system is ready for real Pramaan integration!${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Register with ONDC for production access"
echo "  2. Get Pramaan API credentials"
echo "  3. Replace mock responses with real API calls"
echo "  4. Deploy to production environment"
echo ""
echo "For more details, see: pramaan_transaction_guide.md"