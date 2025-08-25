#!/bin/bash

# BAP Application Deployment Script
# This script deploys the ONDC BAP application to the server

set -e

echo "🚀 BAP Application Deployment Script"
echo "======================================"

# Configuration
SERVER_HOST="neo-server.rozana.in"
SERVER_USER="ubuntu"
SERVER_PATH="/var/www/bap"
SERVICE_NAME="ondc-bap"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the BAP directory
if [ ! -f "requirements.txt" ] || [ ! -d "app" ]; then
    print_error "This script must be run from the BAP directory"
    exit 1
fi

print_status "Starting BAP deployment..."

# Step 1: Create server directory structure
print_status "Creating server directory structure..."
ssh ${SERVER_USER}@${SERVER_HOST} "sudo mkdir -p ${SERVER_PATH} && sudo chown ${SERVER_USER}:${SERVER_USER} ${SERVER_PATH}"

# Step 2: Upload application files
print_status "Uploading application files..."
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

# Step 4: Upload secrets (if they exist)
if [ -d "secrets" ]; then
    print_status "Uploading secrets..."
    rsync -avz secrets/ ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/secrets/
fi

# Step 5: Upload deployment scripts
if [ -d "deployment" ]; then
    print_status "Uploading deployment scripts..."
    rsync -avz deployment/ ${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/deployment/
fi

# Step 6: Install Python dependencies on server
print_status "Installing Python dependencies..."
ssh ${SERVER_USER}@${SERVER_HOST} "cd ${SERVER_PATH} && python3 -m pip install --user -r requirements.txt"

# Step 7: Create systemd service
print_status "Creating systemd service..."
cat > /tmp/ondc-bap.service << EOF
[Unit]
Description=ONDC BAP Application
After=network.target

[Service]
Type=exec
User=${SERVER_USER}
Group=${SERVER_USER}
WorkingDirectory=${SERVER_PATH}
Environment=PATH=${SERVER_PATH}/venv/bin
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

scp /tmp/ondc-bap.service ${SERVER_USER}@${SERVER_HOST}:/tmp/
ssh ${SERVER_USER}@${SERVER_HOST} "sudo mv /tmp/ondc-bap.service /etc/systemd/system/ && sudo systemctl daemon-reload"

# Step 8: Configure Apache reverse proxy
print_status "Configuring Apache reverse proxy..."
cat > /tmp/bap-apache.conf << EOF
<VirtualHost *:80>
    ServerName neo-server.rozana.in
    ServerAlias www.neo-server.rozana.in
    
    # Redirect HTTP to HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</VirtualHost>

<VirtualHost *:443>
    ServerName neo-server.rozana.in
    ServerAlias www.neo-server.rozana.in
    
    # SSL Configuration (assuming SSL is already configured)
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/neo-server.rozana.in.crt
    SSLCertificateKeyFile /etc/ssl/private/neo-server.rozana.in.key
    
    # BAP Application Proxy
    ProxyPreserveHost On
    ProxyPass / http://localhost:8000/
    ProxyPassReverse / http://localhost:8000/
    
    # Health endpoint
    ProxyPass /health http://localhost:8000/health
    ProxyPassReverse /health http://localhost:8000/health
    
    # ONDC endpoints
    ProxyPass /on_subscribe http://localhost:8000/on_subscribe
    ProxyPassReverse /on_subscribe http://localhost:8000/on_subscribe
    
    ProxyPass /lookup http://localhost:8000/lookup
    ProxyPassReverse /lookup http://localhost:8000/lookup
    
    ProxyPass /vlookup http://localhost:8000/vlookup
    ProxyPassReverse /vlookup http://localhost:8000/vlookup
    
    # eKYC endpoints
    ProxyPass /ekyc http://localhost:8000/ekyc
    ProxyPassReverse /ekyc http://localhost:8000/ekyc
    
    # Site verification file
    Alias /ondc-site-verification.html ${SERVER_PATH}/ondc-site-verification.html
    <Files "ondc-site-verification.html">
        Require all granted
    </Files>
    
    # Logs
    ErrorLog \${APACHE_LOG_DIR}/bap_error.log
    CustomLog \${APACHE_LOG_DIR}/bap_access.log combined
</VirtualHost>
EOF

scp /tmp/bap-apache.conf ${SERVER_USER}@${SERVER_HOST}:/tmp/
ssh ${SERVER_USER}@${SERVER_HOST} "sudo mv /tmp/bap-apache.conf /etc/apache2/sites-available/bap.conf && sudo a2ensite bap && sudo systemctl reload apache2"

# Step 9: Start the service
print_status "Starting BAP service..."
ssh ${SERVER_USER}@${SERVER_HOST} "sudo systemctl enable ${SERVICE_NAME} && sudo systemctl start ${SERVICE_NAME}"

# Step 10: Check service status
print_status "Checking service status..."
ssh ${SERVER_USER}@${SERVER_HOST} "sudo systemctl status ${SERVICE_NAME} --no-pager"

# Step 11: Test endpoints
print_status "Testing deployed endpoints..."
echo "Testing health endpoint..."
curl -s https://neo-server.rozana.in/health || print_warning "Health endpoint not accessible"

echo "Testing eKYC search endpoint..."
curl -s -X POST https://neo-server.rozana.in/ekyc/search -H "Content-Type: application/json" -d '{"test": "data"}' || print_warning "eKYC endpoint not accessible"

echo "Testing site verification file..."
curl -s https://neo-server.rozana.in/ondc-site-verification.html | head -5 || print_warning "Site verification file not accessible"

print_status "Deployment completed!"
print_status "BAP Application is now running at: https://neo-server.rozana.in"
print_status "eKYC Services available at: https://neo-server.rozana.in/ekyc"
print_status "Health check: https://neo-server.rozana.in/health"

# Cleanup
rm -f /tmp/ondc-bap.service /tmp/bap-apache.conf

echo ""
print_status "Deployment script completed successfully!" 