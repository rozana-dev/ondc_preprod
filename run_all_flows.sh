#!/bin/bash

# 🚀 Run All Pramaan ONDC Flows
# Master script to execute all flow scripts

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 Pramaan ONDC Flow Test Suite${NC}"
echo "=================================="
echo ""

# Make all scripts executable
echo -e "${YELLOW}📋 Making scripts executable...${NC}"
chmod +x flow_*.sh
chmod +x test_*.sh
chmod +x comprehensive_api_test.sh 2>/dev/null || true
echo "✅ Scripts are now executable"
echo ""

# Display available flows
echo -e "${BLUE}📋 Available ONDC Flows:${NC}"
echo ""
echo -e "${GREEN}Core Order Flows:${NC}"
echo "  1A. Order to Fulfillment (Prepaid) - ./flow_1a_prepaid.sh"
echo "  1B. Order to Fulfillment (COD) - ./flow_1b_cod.sh"
echo ""
echo -e "${GREEN}Cancellation Flows:${NC}"
echo "  2.  Buyer Side Cancellation - ./flow_2_buyer_cancel.sh"
echo "  3A. Merchant Partial Cancellation - ./flow_3a_merchant_partial_cancel.sh"
echo "  3B. Merchant Full Cancellation (RTO) - ./flow_3b_merchant_rto.sh"
echo ""
echo -e "${GREEN}Return Flows:${NC}"
echo "  4A. Buyer Return (Full Order) - ./flow_4a_buyer_return_full.sh"
echo "  4B. Buyer Return (Partial Order) - ./flow_4b_buyer_return_partial.sh"
echo ""
echo -e "${GREEN}Error & Special Flows:${NC}"
echo "  5.  Out of Stock Error - ./flow_5_out_of_stock.sh"
echo "  7.  Non-Cancellable Error - ./flow_7_non_cancellable.sh"
echo ""
echo -e "${GREEN}Issue Management:${NC}"
echo "  6.  Issue & Grievance Management - ./flow_6_igm.sh"
echo ""
echo -e "${GREEN}Search & Info Flows:${NC}"
echo "  8A. Full Catalog Search - ./flow_8a_full_catalog.sh"
echo "  8B. Incremental Search (Same) - ./flow_8b_incremental_same.sh"
echo "  8C. Incremental Search (Different) - ./flow_8c_incremental_diff.sh"
echo "  9.  Catalog Rejection - ./flow_9_catalog_rejection.sh"
echo "  10. Info Request - ./flow_10_info.sh"
echo ""
echo -e "${GREEN}Comprehensive Tests:${NC}"
echo "  •   All API Test - ./comprehensive_api_test.sh"
echo "  •   eKYC Transaction Flow - ./test_pramaan_transaction_flow.sh"
echo ""

# Interactive menu
echo -e "${YELLOW}🎯 What would you like to do?${NC}"
echo ""
echo "1. Run comprehensive API test (all 25 endpoints)"
echo "2. Run eKYC transaction flow"
echo "3. Run Flow 1A (Order to Fulfillment - Prepaid)"
echo "4. Run Flow 2 (Buyer Cancellation)"
echo "5. Run Flow 6 (Issue Management)"
echo "6. Run all basic flows (1A, 2, 6)"
echo "7. Show individual flow commands"
echo "8. Exit"
echo ""

read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        echo -e "${BLUE}🚀 Running Comprehensive API Test...${NC}"
        if [ -f "./comprehensive_api_test.sh" ]; then
            ./comprehensive_api_test.sh
        else
            echo -e "${RED}❌ comprehensive_api_test.sh not found${NC}"
        fi
        ;;
    2)
        echo -e "${BLUE}🚀 Running eKYC Transaction Flow...${NC}"
        if [ -f "./test_pramaan_transaction_flow.sh" ]; then
            ./test_pramaan_transaction_flow.sh
        else
            echo -e "${RED}❌ test_pramaan_transaction_flow.sh not found${NC}"
        fi
        ;;
    3)
        echo -e "${BLUE}🚀 Running Flow 1A (Prepaid Order)...${NC}"
        if [ -f "./flow_1a_prepaid.sh" ]; then
            ./flow_1a_prepaid.sh
        else
            echo -e "${RED}❌ flow_1a_prepaid.sh not found${NC}"
        fi
        ;;
    4)
        echo -e "${BLUE}🚀 Running Flow 2 (Buyer Cancellation)...${NC}"
        if [ -f "./flow_2_buyer_cancel.sh" ]; then
            ./flow_2_buyer_cancel.sh
        else
            echo -e "${RED}❌ flow_2_buyer_cancel.sh not found${NC}"
        fi
        ;;
    5)
        echo -e "${BLUE}🚀 Running Flow 6 (Issue Management)...${NC}"
        if [ -f "./flow_6_igm.sh" ]; then
            ./flow_6_igm.sh
        else
            echo -e "${RED}❌ flow_6_igm.sh not found${NC}"
        fi
        ;;
    6)
        echo -e "${BLUE}🚀 Running All Basic Flows...${NC}"
        echo ""
        
        echo -e "${YELLOW}Running Flow 1A (Prepaid Order)...${NC}"
        if [ -f "./flow_1a_prepaid.sh" ]; then
            ./flow_1a_prepaid.sh
            echo ""
            read -p "Press Enter to continue with Flow 2..."
        fi
        
        echo -e "${YELLOW}Running Flow 2 (Buyer Cancellation)...${NC}"
        if [ -f "./flow_2_buyer_cancel.sh" ]; then
            ./flow_2_buyer_cancel.sh
            echo ""
            read -p "Press Enter to continue with Flow 6..."
        fi
        
        echo -e "${YELLOW}Running Flow 6 (Issue Management)...${NC}"
        if [ -f "./flow_6_igm.sh" ]; then
            ./flow_6_igm.sh
        fi
        
        echo -e "${GREEN}🎉 All basic flows completed!${NC}"
        ;;
    7)
        echo -e "${BLUE}📋 Individual Flow Commands:${NC}"
        echo ""
        echo -e "${GREEN}Copy and paste any of these commands:${NC}"
        echo ""
        echo "./comprehensive_api_test.sh                    # Test all 25 APIs"
        echo "./test_pramaan_transaction_flow.sh             # eKYC flow"
        echo "./flow_1a_prepaid.sh                           # Prepaid order"
        echo "./flow_2_buyer_cancel.sh                       # Buyer cancellation"
        echo "./flow_6_igm.sh                                # Issue management"
        echo ""
        ;;
    8)
        echo -e "${GREEN}👋 Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Flow execution completed!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "  1. Check your callback endpoints for responses"
echo "  2. Monitor transaction IDs in Pramaan dashboard"
echo "  3. Download logs from Pramaan for analysis"
echo "  4. Test additional flows as needed"
echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo "  • Flow Scripts: pramaan_flow_scripts.md"
echo "  • Transaction Guide: pramaan_transaction_guide.md"
echo "  • API Test Results: Check terminal output above"
echo ""
echo -e "${CYAN}🚀 Your ONDC BAP is ready for production!${NC}"