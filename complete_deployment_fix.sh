#!/bin/bash

# Complete ONDC BAP Deployment Fix
# This script handles the complete deployment process

set -e  # Exit on any error

echo "🚀 Starting complete ONDC BAP deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
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

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run with sudo privileges"
    exit 1
fi

# Step 1: Create directory structure
print_status "Creating directory structure..."
mkdir -p /var/www/bap/app/api/v1
mkdir -p /var/www/bap/app/core
mkdir -p /var/www/bap/app/api
mkdir -p /var/www/bap/secrets
mkdir -p /var/www/bap/scripts

# Step 2: Set permissions
print_status "Setting proper permissions..."
chown -R www-data:www-data /var/www/bap
chmod -R 755 /var/www/bap
chmod 700 /var/www/bap/secrets

# Step 3: Copy application files
print_status "Copying application files..."

# Copy main application files
cp /var/www/one_ondc/app/main.py /var/www/bap/app/main.py
cp /var/www/one_ondc/app/__init__.py /var/www/bap/app/__init__.py

# Copy API files
cp /var/www/one_ondc/app/api/__init__.py /var/www/bap/app/api/__init__.py
cp /var/www/one_ondc/app/api/v1/__init__.py /var/www/bap/app/api/v1/__init__.py
cp /var/www/one_ondc/app/api/v1/ondc_bap.py /var/www/bap/app/api/v1/ondc_bap.py
cp /var/www/one_ondc/app/api/v1/ekyc.py /var/www/bap/app/api/v1/ekyc.py

# Copy core modules
cp /var/www/one_ondc/app/core/__init__.py /var/www/bap/app/core/__init__.py
cp /var/www/one_ondc/app/core/config.py /var/www/bap/app/core/config.py
cp /var/www/one_ondc/app/core/ondc_crypto.py /var/www/bap/app/core/ondc_crypto.py
cp /var/www/one_ondc/app/core/ondc_registry.py /var/www/bap/app/core/ondc_registry.py
cp /var/www/one_ondc/app/core/org_config.py /var/www/bap/app/core/org_config.py

# Copy other necessary files
cp /var/www/one_ondc/requirements.txt /var/www/bap/requirements.txt
cp /var/www/one_ondc/ondc-site-verification.html /var/www/bap/ondc-site-verification.html

# Copy scripts
cp /var/www/one_ondc/scripts/generate_ondc_keys.py /var/www/bap/scripts/generate_ondc_keys.py
cp /var/www/one_ondc/scripts/create_subscribe_payload.py /var/www/bap/scripts/create_subscribe_payload.py

# Step 4: Copy secrets if they exist
if [ -f "/var/www/one_ondc/secrets/ondc_credentials.json" ]; then
    print_status "Copying ONDC credentials..."
    cp /var/www/one_ondc/secrets/ondc_credentials.json /var/www/bap/secrets/ondc_credentials.json
    chmod 600 /var/www/bap/secrets/ondc_credentials.json
    chown www-data:www-data /var/www/bap/secrets/ondc_credentials.json
else
    print_warning "ONDC credentials not found. You may need to generate them."
fi

# Step 5: Install Python dependencies
print_status "Installing Python dependencies..."
cd /var/www/bap
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install -r requirements.txt
else
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Step 6: Verify deployment structure
print_status "Verifying deployment structure..."
echo "📁 Directory structure:"
tree /var/www/bap -I "venv" || ls -la /var/www/bap/

echo "📄 Key files:"
ls -la /var/www/bap/app/api/v1/ondc_bap.py
ls -la /var/www/bap/app/core/ondc_crypto.py

# Step 7: Restart the service
print_status "Restarting ONDC BAP service..."
systemctl restart ondc-bap

# Step 8: Check service status
print_status "Checking service status..."
sleep 3
systemctl status ondc-bap --no-pager

# Step 9: Test the endpoint
print_status "Testing the endpoint..."
sleep 2
if curl -s http://localhost:8000/v1/bap/on_subscribe/test > /dev/null; then
    print_status "✅ Endpoint is responding correctly"
else
    print_warning "⚠️  Endpoint test failed. Check logs with: journalctl -u ondc-bap -f"
fi

# Step 10: Show next steps
echo ""
print_status "🎉 Deployment completed successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Test the callback endpoint: curl https://neo-server.rozana.in/v1/bap/on_subscribe/test"
echo "   2. Check logs: journalctl -u ondc-bap -f"
echo "   3. Verify ONDC registration: curl https://neo-server.rozana.in/v1/bap/onboarding/checklist"
echo "   4. Generate keys if needed: cd /var/www/bap && python scripts/generate_ondc_keys.py"
echo ""
echo "🔍 Useful commands:"
echo "   - View logs: journalctl -u ondc-bap -f"
echo "   - Check service: systemctl status ondc-bap"
echo "   - Restart service: systemctl restart ondc-bap"
echo "   - Test endpoint: curl http://localhost:8000/v1/bap/on_subscribe/test" 