#!/bin/bash

# Fix eKYC Endpoints for ONDC BAP
# This script adds the missing /ekyc route to Apache and tests eKYC functionality

echo "🔧 Fixing eKYC Endpoints for ONDC BAP"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: Add eKYC route to Apache configuration
echo "📝 Adding eKYC route to Apache configuration..."

# Check if we're running as root
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run with sudo privileges"
    exit 1
fi

# Backup current configuration
print_status "Backing up current Apache configuration..."
cp /etc/apache2/sites-available/ondc-bap.conf /etc/apache2/sites-available/ondc-bap.conf.backup.$(date +%Y%m%d_%H%M%S)

# Add eKYC route to Apache config
print_status "Adding /ekyc route to Apache configuration..."
echo "" >> /etc/apache2/sites-available/ondc-bap.conf
echo "    # eKYC endpoints" >> /etc/apache2/sites-available/ondc-bap.conf
echo "    ProxyPass /ekyc http://localhost:8000/ekyc" >> /etc/apache2/sites-available/ondc-bap.conf
echo "    ProxyPassReverse /ekyc http://localhost:8000/ekyc" >> /etc/apache2/sites-available/ondc-bap.conf

# Step 2: Test Apache configuration
print_status "Testing Apache configuration..."
apache2ctl configtest

if [ $? -eq 0 ]; then
    print_status "Apache configuration test passed"
    
    # Step 3: Reload Apache
    print_status "Reloading Apache..."
    systemctl reload apache2
    
    # Step 4: Wait a moment for Apache to reload
    sleep 3
    
    # Step 5: Test eKYC endpoints
    echo ""
    print_status "Testing eKYC endpoints..."
    
    # Test eKYC health endpoint
    echo "Testing eKYC health endpoint..."
    response=$(curl -s https://neo-server.rozana.in/ekyc/health)
    if [[ $response == *"404 Not Found"* ]]; then
        print_error "eKYC health endpoint failed"
        echo "Response: $response"
    else
        print_status "eKYC health endpoint working"
        echo "Response: $response"
    fi
    
    # Test eKYC search endpoint
    echo ""
    echo "Testing eKYC search endpoint..."
    search_payload='{
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:011",
            "action": "search",
            "core_version": "1.2.0",
            "bap_id": "neo-server.rozana.in",
            "bap_uri": "https://neo-server.rozana.in",
            "transaction_id": "test-transaction-123",
            "message_id": "test-message-123",
            "timestamp": "2025-08-22T10:00:00Z",
            "ttl": "PT30S"
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
    
    response=$(curl -s -X POST https://neo-server.rozana.in/ekyc/search \
        -H "Content-Type: application/json" \
        -d "$search_payload")
    
    if [[ $response == *"404 Not Found"* ]]; then
        print_error "eKYC search endpoint failed"
        echo "Response: $response"
    else
        print_status "eKYC search endpoint working"
        echo "Response: $(echo "$response" | head -c 200)..."
    fi
    
    # Test eKYC verify endpoint
    echo ""
    echo "Testing eKYC verify endpoint..."
    verify_payload='{
        "context": {
            "domain": "ONDC:RET10",
            "country": "IND",
            "city": "std:011",
            "action": "verify",
            "core_version": "1.2.0",
            "bap_id": "neo-server.rozana.in",
            "bap_uri": "https://neo-server.rozana.in",
            "transaction_id": "test-transaction-456",
            "message_id": "test-message-456",
            "timestamp": "2025-08-22T10:00:00Z",
            "ttl": "PT30S"
        },
        "message": {
            "order": {
                "provider": {
                    "id": "pramaan.ondc.org"
                },
                "items": [
                    {
                        "id": "ekyc_verification",
                        "name": "eKYC Verification"
                    }
                ]
            }
        }
    }'
    
    response=$(curl -s -X POST https://neo-server.rozana.in/ekyc/verify \
        -H "Content-Type: application/json" \
        -d "$verify_payload")
    
    if [[ $response == *"404 Not Found"* ]]; then
        print_error "eKYC verify endpoint failed"
        echo "Response: $response"
    else
        print_status "eKYC verify endpoint working"
        echo "Response: $(echo "$response" | head -c 200)..."
    fi
    
    # Step 6: Show summary
    echo ""
    print_status "eKYC endpoints fix completed!"
    echo ""
    echo "📝 eKYC Endpoints Available:"
    echo "   - GET  https://neo-server.rozana.in/ekyc/health"
    echo "   - POST https://neo-server.rozana.in/ekyc/search"
    echo "   - POST https://neo-server.rozana.in/ekyc/select"
    echo "   - POST https://neo-server.rozana.in/ekyc/initiate"
    echo "   - POST https://neo-server.rozana.in/ekyc/verify"
    echo "   - POST https://neo-server.rozana.in/ekyc/status"
    echo ""
    echo "🔍 Test Commands:"
    echo "   curl https://neo-server.rozana.in/ekyc/health"
    echo "   curl -X POST https://neo-server.rozana.in/ekyc/search -H 'Content-Type: application/json' -d '{\"test\": \"data\"}'"
    
else
    print_error "Apache configuration test failed"
    echo "Please check the Apache configuration manually"
    exit 1
fi 