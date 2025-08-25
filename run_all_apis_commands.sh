#!/bin/bash

# 🎯 Run All ONDC APIs - Terminal Commands
# Complete guide for testing all your ONDC BAP endpoints

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

BASE_URL="https://neo-server.rozana.in"

echo -e "${CYAN}🎯 All ONDC API Terminal Commands${NC}"
echo "=================================="
echo "Base URL: $BASE_URL"
echo ""

echo -e "${YELLOW}📋 QUICK START - Run All APIs:${NC}"
echo ""
echo -e "${GREEN}1. Comprehensive Test (All 25+ endpoints):${NC}"
echo "   ./comprehensive_api_test.sh"
echo ""
echo -e "${GREEN}2. Complete ONDC Flow:${NC}"
echo "   ./complete_pramaan_flow_with_search.sh"
echo ""
echo -e "${GREEN}3. Interactive Menu:${NC}"
echo "   ./run_all_flows.sh"
echo ""

echo -e "${BLUE}🔧 Individual API Commands:${NC}"
echo ""

echo -e "${YELLOW}Core ONDC Endpoints:${NC}"
echo ""

# Health Check
echo -e "${PURPLE}Health Check:${NC}"
echo 'curl -X GET '$BASE_URL'/health'
echo ""

# ONDC Flow
echo -e "${PURPLE}ONDC Order Flow:${NC}"
echo 'curl -X POST '$BASE_URL'/search -H "Content-Type: application/json" -d '"'"'{"context":{"domain":"ONDC:RET10","action":"search"}}'"'"''
echo 'curl -X POST '$BASE_URL'/select -H "Content-Type: application/json" -d '"'"'{"context":{"domain":"ONDC:RET10","action":"select"}}'"'"''
echo 'curl -X POST '$BASE_URL'/init -H "Content-Type: application/json" -d '"'"'{"context":{"domain":"ONDC:RET10","action":"init"}}'"'"''
echo 'curl -X POST '$BASE_URL'/confirm -H "Content-Type: application/json" -d '"'"'{"context":{"domain":"ONDC:RET10","action":"confirm"}}'"'"''
echo 'curl -X POST '$BASE_URL'/status -H "Content-Type: application/json" -d '"'"'{"context":{"domain":"ONDC:RET10","action":"status"}}'"'"''
echo 'curl -X POST '$BASE_URL'/track -H "Content-Type: application/json" -d '"'"'{"context":{"domain":"ONDC:RET10","action":"track"}}'"'"''
echo ""

echo -e "${YELLOW}eKYC Endpoints:${NC}"
echo ""
echo 'curl -X GET '$BASE_URL'/ekyc/health'
echo 'curl -X POST '$BASE_URL'/ekyc/search -H "Content-Type: application/json" -d '"'"'{"context":{"action":"search"}}'"'"''
echo 'curl -X POST '$BASE_URL'/ekyc/select -H "Content-Type: application/json" -d '"'"'{"context":{"action":"select"}}'"'"''
echo 'curl -X POST '$BASE_URL'/ekyc/verify -H "Content-Type: application/json" -d '"'"'{"context":{"action":"verify"}}'"'"''
echo 'curl -X POST '$BASE_URL'/ekyc/initiate -H "Content-Type: application/json" -d '"'"'{"context":{"action":"initiate"}}'"'"''
echo 'curl -X POST '$BASE_URL'/ekyc/status -H "Content-Type: application/json" -d '"'"'{"context":{"action":"status"}}'"'"''
echo ""

echo -e "${YELLOW}Registry & Onboarding:${NC}"
echo ""
echo 'curl -X POST '$BASE_URL'/on_subscribe -H "Content-Type: application/json" -d '"'"'{"context":{"action":"on_subscribe"}}'"'"''
echo 'curl -X GET '$BASE_URL'/vlookup'
echo ""

echo -e "${YELLOW}Additional Endpoints:${NC}"
echo ""
echo 'curl -X POST '$BASE_URL'/cancel -H "Content-Type: application/json" -d '"'"'{"context":{"action":"cancel"}}'"'"''
echo 'curl -X POST '$BASE_URL'/rating -H "Content-Type: application/json" -d '"'"'{"context":{"action":"rating"}}'"'"''
echo 'curl -X POST '$BASE_URL'/support -H "Content-Type: application/json" -d '"'"'{"context":{"action":"support"}}'"'"''
echo ""

echo -e "${CYAN}🎯 Recommended Usage:${NC}"
echo ""
echo -e "${GREEN}For Quick Testing:${NC}"
echo "   ./comprehensive_api_test.sh"
echo ""
echo -e "${GREEN}For Complete Flow:${NC}"
echo "   ./complete_pramaan_flow_with_search.sh"
echo ""
echo -e "${GREEN}For Interactive Menu:${NC}"
echo "   ./run_all_flows.sh"
echo ""

echo -e "${BLUE}📋 All Available Test Scripts:${NC}"
ls -la *.sh | grep -E "(test|comprehensive|complete|run)" | awk '{print "   " $9}'
echo ""

echo -e "${PURPLE}🎯 Choose your preferred method and run!${NC}"