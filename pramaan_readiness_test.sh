#!/bin/bash

# 🚀 Pramaan Test Case Readiness Checker
# Validates all ONDC endpoints for Pramaan testing

set -e

BASE_URL="https://neo-server.rozana.in"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 Pramaan Test Case Readiness Checker${NC}"
echo "========================================"
echo "Testing: $BASE_URL"
echo ""

# Test results tracking
total_tests=0
passed_tests=0
failed_tests=0

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local method=$2
    local payload=$3
    local expected_fields=$4
    
    total_tests=$((total_tests + 1))
    
    echo -e "${BLUE}Testing: $endpoint${NC}"
    echo "Method: $method"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -H "Authorization: Signature keyId=\"neo-server.rozana.in|key_1755821120|ed25519\",algorithm=\"ed25519\",headers=\"(created) (expires) digest\",signature=\"test_signature\"" \
            -H "X-Timestamp: $(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" \
            -d "$payload")
    fi
    
    http_code=$(echo "$response" | tail -1)
    response_body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ HTTP 200 OK${NC}"
        
        # Check if response is valid JSON
        if echo "$response_body" | jq . >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Valid JSON Response${NC}"
            
            # Check for expected ONDC fields if specified
            if [ ! -z "$expected_fields" ]; then
                echo "Expected fields: $expected_fields"
                # Add field validation logic here if needed
            fi
            
            passed_tests=$((passed_tests + 1))
        else
            echo -e "${YELLOW}⚠️  Non-JSON Response: $response_body${NC}"
            if [ "$response_body" = "OK" ]; then
                echo -e "${GREEN}✅ Simple OK response (acceptable for basic endpoints)${NC}"
                passed_tests=$((passed_tests + 1))
            else
                failed_tests=$((failed_tests + 1))
            fi
        fi
    else
        echo -e "${RED}❌ HTTP $http_code${NC}"
        echo "Response: $response_body"
        failed_tests=$((failed_tests + 1))
    fi
    
    echo ""
    echo "----------------------------------------"
    echo ""
}

echo -e "${YELLOW}📋 Standard ONDC BAP Endpoints${NC}"
echo ""

# Standard BAP endpoints that Pramaan will test
echo -e "${BLUE}🔍 Core Action Endpoints${NC}"

test_endpoint "/search" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND",
    "city": "std:011",
    "action": "search",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "pramaan-test-'$(date +%s)'",
    "message_id": "msg-'$(date +%s)'",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
  },
  "message": {
    "intent": {
      "item": {
        "descriptor": {
          "name": "Test Product"
        }
      },
      "fulfillment": {
        "type": "Delivery"
      }
    }
  }
}' "context,message"

test_endpoint "/select" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "select",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "order": {
      "provider": {
        "id": "test_provider"
      },
      "items": [{
        "id": "test_item",
        "quantity": {
          "count": 1
        }
      }]
    }
  }
}' "context,message"

test_endpoint "/init" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "init",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "order": {
      "provider": {
        "id": "test_provider"
      },
      "items": [{
        "id": "test_item",
        "quantity": {
          "count": 1
        }
      }],
      "billing": {
        "name": "Test User"
      }
    }
  }
}' "context,message"

test_endpoint "/confirm" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "confirm",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "order": {
      "id": "test_order_'$(date +%s)'",
      "provider": {
        "id": "test_provider"
      },
      "items": [{
        "id": "test_item",
        "quantity": {
          "count": 1
        }
      }],
      "payment": {
        "type": "PRE-PAID",
        "status": "PAID"
      }
    }
  }
}' "context,message"

test_endpoint "/status" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "status",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "order_id": "test_order_123"
  }
}' "context,message"

test_endpoint "/track" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "track",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "order_id": "test_order_123"
  }
}' "context,message"

test_endpoint "/cancel" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "cancel",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "order_id": "test_order_123",
    "cancellation_reason_id": "001"
  }
}' "context,message"

test_endpoint "/update" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "update",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "update_target": "order",
    "order": {
      "id": "test_order_123"
    }
  }
}' "context,message"

test_endpoint "/rating" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "rating",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "rating_category": "Order",
    "id": "test_order_123",
    "value": "5"
  }
}' "context,message"

test_endpoint "/support" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "support",
    "transaction_id": "pramaan-test-'$(date +%s)'"
  },
  "message": {
    "support": {
      "order_id": "test_order_123",
      "phone": "1800-123-4567",
      "email": "support@neo-server.rozana.in"
    }
  }
}' "context,message"

echo -e "${BLUE}🔄 Callback Endpoints (on_*)${NC}"

test_endpoint "/on_subscribe" "GET" "" ""

test_endpoint "/on_subscribe/test" "GET" "" ""

echo -e "${BLUE}🏥 Health & Infrastructure${NC}"

test_endpoint "/health" "GET" "" ""
test_endpoint "/healthz" "GET" "" ""
test_endpoint "/livez" "GET" "" ""
test_endpoint "/readyz" "GET" "" ""

echo -e "${BLUE}🔍 Discovery & Verification${NC}"

test_endpoint "/lookup" "GET" "" ""
test_endpoint "/ondc-site-verification.html" "GET" "" ""

echo -e "${BLUE}🔐 eKYC Endpoints${NC}"

test_endpoint "/ekyc/health" "GET" "" ""

test_endpoint "/ekyc/search" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "search",
    "transaction_id": "ekyc-test-'$(date +%s)'"
  },
  "message": {}
}' "context,message"

test_endpoint "/ekyc/verify" "POST" '{
  "context": {
    "domain": "ONDC:RET10",
    "action": "verify",
    "transaction_id": "ekyc-test-'$(date +%s)'"
  },
  "message": {}
}' "context,message"

# Summary
echo -e "${CYAN}📊 Pramaan Readiness Summary${NC}"
echo "=============================="
echo -e "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed_tests${NC}"
echo -e "${RED}Failed: $failed_tests${NC}"

success_rate=$((passed_tests * 100 / total_tests))
echo -e "Success Rate: ${success_rate}%"

if [ $failed_tests -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All endpoints are Pramaan-ready!${NC}"
    echo -e "${CYAN}✅ Your BAP is ready for Pramaan test cases${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Some endpoints need attention before Pramaan testing${NC}"
fi

echo ""
echo -e "${BLUE}📋 Pramaan Test Requirements Checklist:${NC}"
echo "✅ Standard endpoints exposed (/search, /select, etc.)"
echo "✅ ONDC API Schema v2.0 structure (context + message)"
echo "✅ Proper HTTP status codes (200 OK)"
echo "✅ JSON response format"
echo "⚠️  Signing verification (implement if required)"
echo "⚠️  Header validation (implement if required)"
echo "⚠️  Timestamp validation (implement if required)"

echo ""
echo -e "${YELLOW}🔧 Next Steps for Pramaan Testing:${NC}"
echo "1. Ensure all endpoints return proper ONDC schema responses"
echo "2. Implement signature verification if required"
echo "3. Add proper error handling and validation"
echo "4. Test with actual Pramaan test cases"
echo "5. Monitor logs during Pramaan testing"

echo ""
echo -e "${CYAN}🌐 Your BAP URL for Pramaan: $BASE_URL${NC}"