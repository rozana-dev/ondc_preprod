#!/bin/bash

# BAP Application Upload Script
# Uploads all necessary files to the server

set -e

echo "🚀 BAP Application Upload Script"
echo "================================="

# Configuration
SERVER_HOST="neo-server.rozana.in"
SERVER_USER="ubuntu"
SERVER_PATH="/var/www/bap"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the BAP directory
if [ ! -f "requirements.txt" ] || [ ! -d "app" ]; then
    print_error "This script must be run from the BAP directory"
    exit 1
fi

print_status "Starting file upload to server..."

# Step 1: Create server directory
print_status "Creating server directory..."
ssh ${SERVER_USER}@${SERVER_HOST} "sudo mkdir -p ${SERVER_PATH} && sudo chown ${SERVER_USER}:${SERVER_USER} ${SERVER_PATH}"

# Step 2: Upload application code
print_status "Uploading application code..."
rsync -avz --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
    app/ \
    ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/app/

# Step 3: Upload configuration files
print_status "Uploading configuration files..."
rsync -avz \
    requirements.txt \
    Dockerfile \
    ondc-site-verification.html \
    ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/

# Step 4: Upload secrets
print_status "Uploading secrets..."
rsync -avz secrets/ ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/secrets/

# Step 5: Upload deployment scripts
print_status "Uploading deployment scripts..."
rsync -avz deployment/ ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/deployment/

# Step 6: Set proper permissions
print_status "Setting file permissions..."
ssh ${SERVER_USER}@${SERVER_HOST} "chmod -R 755 ${SERVER_PATH} && chmod 600 ${SERVER_PATH}/secrets/*"

print_status "File upload completed successfully!"
print_status "Next steps:"
echo "1. SSH to server: ssh ${SERVER_USER}@${SERVER_HOST}"
echo "2. Install dependencies: cd ${SERVER_PATH} && python3 -m pip install --user -r requirements.txt"
echo "3. Run deployment script: bash deployment/quick_deploy.sh"
echo "4. Or manually configure systemd and Apache"

echo ""
print_status "Upload script completed!" 