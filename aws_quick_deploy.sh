#!/bin/bash

# AWS Quick Deploy Script for ONDC BAP
# Run this on your EC2 instance

set -e

echo "🚀 Starting AWS Quick Deploy..."

# Configuration
S3_BUCKET="your-bucket-name"
S3_PATH="ondc-bap"
DEPLOY_PATH="/opt/ondc-bap"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Step 1: Download from S3
print_status "Downloading BAP from S3..."
sudo aws s3 cp s3://${S3_BUCKET}/${S3_PATH}/ ${DEPLOY_PATH}/ --recursive

# Step 2: Set permissions
print_status "Setting permissions..."
sudo chown -R www-data:www-data ${DEPLOY_PATH}
sudo chmod -R 755 ${DEPLOY_PATH}

# Step 3: Install dependencies
print_status "Installing Python dependencies..."
cd ${DEPLOY_PATH}
sudo -u www-data python3 -m pip install -r requirements.txt

# Step 4: Copy verification file
print_status "Copying verification file..."
if [ -f "${DEPLOY_PATH}/ondc-site-verification.html" ]; then
    sudo cp ${DEPLOY_PATH}/ondc-site-verification.html /var/www/html/
    sudo chown www-data:www-data /var/www/html/ondc-site-verification.html
fi

# Step 5: Restart services
print_status "Restarting services..."
sudo systemctl restart ondc-bap
sudo systemctl restart apache2

# Step 6: Check status
print_status "Checking service status..."
sleep 3

if systemctl is-active --quiet ondc-bap; then
    print_status "✅ ONDC BAP service is running!"
else
    print_warning "❌ ONDC BAP service failed to start"
    sudo journalctl -u ondc-bap -n 10
fi

# Step 7: Test endpoints
print_status "Testing endpoints..."
echo "Testing health endpoint..."
if curl -s -f "https://neo-server.rozana.in/healthz" > /dev/null; then
    print_status "✅ Health endpoint: OK"
else
    print_warning "❌ Health endpoint: Failed"
fi

echo "Testing on_subscribe endpoint..."
if curl -s -f "https://neo-server.rozana.in/on_subscribe" > /dev/null; then
    print_status "✅ on_subscribe endpoint: OK"
else
    print_warning "❌ on_subscribe endpoint: Failed"
fi

print_status "Deployment completed!"
print_status "ONDC BAP is now accessible at:"
echo "  - Health: https://neo-server.rozana.in/healthz"
echo "  - Callback: https://neo-server.rozana.in/on_subscribe"
echo "  - Site Verification: https://neo-server.rozana.in/ondc-site-verification.html" 