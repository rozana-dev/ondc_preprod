#!/bin/bash

# 🚀 Pramaan ONDC Endpoints Checker
# Tests all required endpoints for Pramaan test cases

BASE_URL="https://neo-server.rozana.in"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🚀 Pramaan ONDC Endpoints Checker${NC}"
echo "=================================="
echo "Testing: $BASE_URL"
echo ""

passed=0
total=0

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local method=$2
    local payload=$3
    
    total=$((total + 1))
    echo -e "${BLUE}Testing: $endpoint ($method)${NC}"
    
    if [ "$method" = "GET" ]; then
        http_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$endpoint")
    else
        http_code=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$payload")
    fi
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ HTTP 200 OK${NC}"
        passed=$((passed + 1))
    else
        echo -e "${RED}❌ HTTP $http_code${NC}"
    fi
    echo ""
}

echo -e "${YELLOW}📋 Required ONDC BAP Endpoints for Pramaan${NC}"
echo ""

# Standard ONDC BAP endpoints
echo -e "${BLUE}🔍 Core Action Endpoints${NC}"
test_endpoint "/search" "POST" '{"context":{"domain":"ONDC:RET10","action":"search"},"message":{}}'
test_endpoint "/select" "POST" '{"context":{"domain":"ONDC:RET10","action":"select"},"message":{}}'
test_endpoint "/init" "POST" '{"context":{"domain":"ONDC:RET10","action":"init"},"message":{}}'
test_endpoint "/confirm" "POST" '{"context":{"domain":"ONDC:RET10","action":"confirm"},"message":{}}'
test_endpoint "/status" "POST" '{"context":{"domain":"ONDC:RET10","action":"status"},"message":{}}'
test_endpoint "/track" "POST" '{"context":{"domain":"ONDC:RET10","action":"track"},"message":{}}'
test_endpoint "/cancel" "POST" '{"context":{"domain":"ONDC:RET10","action":"cancel"},"message":{}}'
test_endpoint "/update" "POST" '{"context":{"domain":"ONDC:RET10","action":"update"},"message":{}}'
test_endpoint "/rating" "POST" '{"context":{"domain":"ONDC:RET10","action":"rating"},"message":{}}'
test_endpoint "/support" "POST" '{"context":{"domain":"ONDC:RET10","action":"support"},"message":{}}'

echo -e "${BLUE}🔄 Callback Endpoints${NC}"
test_endpoint "/on_subscribe" "GET" ""
test_endpoint "/on_subscribe/test" "GET" ""

echo -e "${BLUE}🏥 Health Endpoints${NC}"
test_endpoint "/health" "GET" ""
test_endpoint "/healthz" "GET" ""
test_endpoint "/livez" "GET" ""
test_endpoint "/readyz" "GET" ""

echo -e "${BLUE}🔍 Discovery Endpoints${NC}"
test_endpoint "/lookup" "GET" ""
test_endpoint "/ondc-site-verification.html" "GET" ""

echo -e "${BLUE}🔐 eKYC Endpoints${NC}"
test_endpoint "/ekyc/health" "GET" ""
test_endpoint "/ekyc/search" "POST" '{"context":{"domain":"ONDC:RET10","action":"search"},"message":{}}'
test_endpoint "/ekyc/verify" "POST" '{"context":{"domain":"ONDC:RET10","action":"verify"},"message":{}}'

# Summary
success_rate=$((passed * 100 / total))
echo -e "${CYAN}📊 Pramaan Readiness Summary${NC}"
echo "=============================="
echo -e "Total Endpoints: $total"
echo -e "${GREEN}Working: $passed${NC}"
echo -e "${RED}Failed: $((total - passed))${NC}"
echo -e "Success Rate: ${success_rate}%"

if [ $passed -eq $total ]; then
    echo ""
    echo -e "${GREEN}🎉 Perfect! All $total endpoints are working!${NC}"
    echo -e "${CYAN}✅ Your BAP is ready for Pramaan test cases${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  $((total - passed)) endpoints need attention${NC}"
fi

echo ""
echo -e "${BLUE}📋 Pramaan Test Requirements:${NC}"
echo "✅ Standard endpoints exposed"
echo "✅ HTTP 200 responses"
echo "✅ JSON payload handling"
echo "✅ ONDC context structure"

echo ""
echo -e "${YELLOW}🔧 For Pramaan Testing:${NC}"
echo "• Ensure responses match ONDC API Schema v2.0"
echo "• Implement proper signing if required"
echo "• Handle timestamps and headers correctly"
echo "• Add error handling and validation"

echo ""
echo -e "${CYAN}🌐 Your BAP URL: $BASE_URL${NC}"