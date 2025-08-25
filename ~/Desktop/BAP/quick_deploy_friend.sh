#!/bin/bash

# Quick Deployment Script for ONDC BAP Application
# Run this script on your Ubuntu server after uploading the BAP folder

set -e

echo "🚀 ONDC BAP Quick Deployment Script"
echo "===================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

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
    print_error "This script must be run from the BAP directory (/var/www/bap)"
    print_error "Please navigate to the BAP directory first: cd /var/www/bap"
    exit 1
fi

print_status "Starting BAP deployment..."

# Step 1: Install system dependencies
print_status "Installing system dependencies..."
sudo apt update -y
sudo apt install python3 python3-pip python3-venv apache2 libapache2-mod-proxy libapache2-mod-proxy-http -y

# Step 2: Enable Apache modules
print_status "Enabling Apache modules..."
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2enmod rewrite

# Step 3: Install Python dependencies
print_status "Installing Python dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Step 4: Create systemd service
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/ondc-bap.service > /dev/null << 'EOF'
[Unit]
Description=ONDC BAP Application
After=network.target

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/bap
Environment=PATH=/var/www/bap/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Step 5: Enable and start service
print_status "Starting BAP service..."
sudo systemctl daemon-reload
sudo systemctl enable ondc-bap
sudo systemctl start ondc-bap

# Step 6: Create Apache configuration
print_status "Configuring Apache..."
sudo tee /etc/apache2/sites-available/bap.conf > /dev/null << 'EOF'
<VirtualHost *:80>
    ServerName localhost
    
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
    Alias /ondc-site-verification.html /var/www/bap/ondc-site-verification.html
    <Files "ondc-site-verification.html">
        Require all granted
    </Files>
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/bap_error.log
    CustomLog ${APACHE_LOG_DIR}/bap_access.log combined
</VirtualHost>
EOF

# Step 7: Enable site and restart Apache
print_status "Enabling Apache site..."
sudo a2ensite bap
sudo systemctl reload apache2

# Step 8: Set permissions
print_status "Setting file permissions..."
sudo chown -R ubuntu:ubuntu /var/www/bap
sudo chmod -R 755 /var/www/bap
sudo chmod 600 /var/www/bap/secrets/*
sudo chmod 644 /var/www/bap/ondc-site-verification.html

# Step 9: Check service status
print_status "Checking service status..."
sudo systemctl status ondc-bap --no-pager

# Step 10: Test endpoints
print_status "Testing endpoints..."
echo "Testing health endpoint..."
curl -s http://localhost/health || print_warning "Health endpoint not accessible"

echo "Testing eKYC search endpoint..."
curl -s -X POST http://localhost/ekyc/search -H "Content-Type: application/json" -d '{"test": "data"}' || print_warning "eKYC endpoint not accessible"

echo "Testing site verification file..."
curl -s http://localhost/ondc-site-verification.html | head -5 || print_warning "Site verification file not accessible"

print_status "Deployment completed!"
print_status "BAP Application is now running at: http://localhost"
print_status "eKYC Services available at: http://localhost/ekyc"
print_status "Health check: http://localhost/health"

print_warning "IMPORTANT: Update the domain name in the configuration files:"
echo "1. Edit /etc/apache2/sites-available/bap.conf and replace 'localhost' with your domain"
echo "2. Edit /var/www/bap/app/core/org_config.py and update SUBSCRIBER_ID and BAP_URI"
echo "3. Configure SSL certificates for HTTPS"
echo "4. Restart Apache: sudo systemctl reload apache2"

echo ""
print_status "Quick deployment completed successfully!" 