#!/bin/bash

# 🚀 Flow 6: Issue and Grievance Management (IGM)
# Complete IGM flow for raising and resolving issues

set -e

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"  # Use existing transaction ID from completed order
ORDER_ID="order_${TRANSACTION_ID}"
ISSUE_ID="issue_$(date +%s)"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Flow 6: Issue and Grievance Management (IGM)${NC}"
echo "=============================================="
echo "Transaction ID: $TRANSACTION_ID"
echo "Order ID: $ORDER_ID"
echo "Issue ID: $ISSUE_ID"
echo "BPP URI: $BPP_URI"
echo ""
echo -e "${RED}⚠️  Note: This flow requires a completed order transaction.${NC}"
echo -e "${RED}    Use the transaction ID from Flow 1A or 1B.${NC}"
echo ""

# Allow user to input existing transaction ID
read -p "Enter existing transaction ID (or press Enter to use new one): " existing_txn_id
if [ ! -z "$existing_txn_id" ]; then
    TRANSACTION_ID="$existing_txn_id"
    ORDER_ID="order_${existing_txn_id}"
    echo "Using existing transaction ID: $TRANSACTION_ID"
fi

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

# Step 1: Raise Issue
echo -e "${YELLOW}🚨 Step 1: Raise Issue${NC}"
issue_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "issue",
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
    "issue": {
      "id": "'$ISSUE_ID'",
      "category": "ITEM",
      "sub_category": "ITM01",
      "complainant_info": {
        "person": {
          "name": "John Doe"
        },
        "contact": {
          "phone": "9876543210",
          "email": "john@example.com"
        }
      },
      "order_details": {
        "id": "'$ORDER_ID'",
        "state": "Completed",
        "items": [{
          "id": "item_001",
          "quantity": 1
        }],
        "fulfillments": [{
          "id": "fulfillment_001",
          "state": "Order-delivered"
        }]
      },
      "description": {
        "short_desc": "Item damaged during delivery",
        "long_desc": "The item received was damaged during delivery. The packaging was torn and the product has visible scratches."
      },
      "source": {
        "network_participant_id": "neo-server.rozana.in",
        "type": "CONSUMER"
      },
      "expected_response_time": {
        "duration": "PT2H"
      },
      "expected_resolution_time": {
        "duration": "P1D"
      },
      "status": "OPEN",
      "issue_type": "ISSUE",
      "issue_actions": {
        "complainant_actions": [{
          "complainant_action": "OPEN",
          "short_desc": "Issue raised",
          "updated_at": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
          "updated_by": {
            "org": {
              "name": "neo-server.rozana.in::ONDC:RET10"
            },
            "contact": {
              "phone": "9876543210",
              "email": "john@example.com"
            },
            "person": {
              "name": "John Doe"
            }
          }
        }]
      },
      "created_at": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    }
  }
}'

make_api_call "1" "/issue" "$issue_payload"

echo -e "${RED}⏳ Wait for on_issue callback before proceeding...${NC}"
read -p "Press Enter after receiving on_issue callback to continue with issue status check..."

# Step 2: Check Issue Status
echo -e "${YELLOW}📊 Step 2: Check Issue Status${NC}"
issue_status_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "issue_status",
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
    "issue_id": "'$ISSUE_ID'"
  }
}'

make_api_call "2" "/issue_status" "$issue_status_payload"

echo -e "${RED}⏳ Wait for issue updates from seller...${NC}"
read -p "Press Enter after receiving issue status updates to proceed with resolution..."

# Step 3: Close Issue (Resolution)
echo -e "${YELLOW}✅ Step 3: Close Issue${NC}"
issue_close_payload='{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "issue",
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
    "issue": {
      "id": "'$ISSUE_ID'",
      "status": "CLOSED",
      "resolution_provider": {
        "respondent_info": {
          "type": "TRANSACTION-COUNTERPARTY-NP",
          "organization": {
            "org": {
              "name": "pramaan.ondc.org/beta/preprod/mock/seller::ONDC:RET10"
            },
            "contact": {
              "phone": "9876543210",
              "email": "support@pramaan.ondc.org"
            },
            "person": {
              "name": "Customer Support"
            }
          }
        }
      },
      "resolution": {
        "short_desc": "Issue resolved - replacement provided",
        "long_desc": "The damaged item has been replaced with a new one. Customer is satisfied with the resolution.",
        "action_triggered": "REPLACE",
        "refund_amount": "0.00"
      },
      "issue_actions": {
        "complainant_actions": [{
          "complainant_action": "CLOSE",
          "short_desc": "Issue resolved satisfactorily",
          "updated_at": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
          "updated_by": {
            "org": {
              "name": "neo-server.rozana.in::ONDC:RET10"
            },
            "contact": {
              "phone": "9876543210",
              "email": "john@example.com"
            },
            "person": {
              "name": "John Doe"
            }
          }
        }]
      },
      "updated_at": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    }
  }
}'

make_api_call "3" "/issue" "$issue_close_payload"

echo -e "${GREEN}🎉 Flow 6 Complete!${NC}"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "  🚨 Issue Raised - Item damage reported"
echo "  📊 Status Checked - Issue status monitored"
echo "  ✅ Issue Closed - Resolution provided (replacement)"
echo ""
echo -e "${GREEN}🔧 Issue Resolution: Replacement provided${NC}"
echo -e "${YELLOW}📝 Transaction ID: $TRANSACTION_ID${NC}"
echo -e "${YELLOW}📦 Order ID: $ORDER_ID${NC}"
echo -e "${YELLOW}🚨 Issue ID: $ISSUE_ID${NC}"
echo ""
echo -e "${BLUE}📋 IGM Flow Types:${NC}"
echo "  • Flow 6: Basic IGM (completed)"
echo "  • Flow 6b: IGM 2.0 with info request"
echo "  • Flow 6c: IGM 2.0 with resolution selection"
echo "  • Flow 6d: IGM 2.0 with multiple resolutions"
echo "  • Flow 6e: IGM 2.0 escalation flow"
echo ""
echo "Issue and Grievance Management completed successfully!"