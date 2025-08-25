#!/bin/bash

# ONDC BAP Quick Deployment Script
# Run this script on the Ubuntu server as root

set -e

echo "🚀 Starting ONDC BAP Deployment..."

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

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script as root (use sudo)"
    exit 1
fi

# Step 1: Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Step 2: Install required packages
print_status "Installing required packages..."
apt install -y apache2 libapache2-mod-proxy-html

# Step 3: Enable Apache modules
print_status "Enabling Apache modules..."
a2enmod proxy
a2enmod proxy_http
a2enmod ssl
a2enmod rewrite

# Step 4: Create application directory
print_status "Creating application directory..."
mkdir -p /opt/ondc-bap
chown www-data:www-data /opt/ondc-bap

# Step 5: Check if application files exist
if [ ! -f "/opt/ondc-bap/requirements.txt" ]; then
    print_error "Application files not found in /opt/ondc-bap/"
    print_error "Please upload the application files first using:"
    print_error "rsync -avz /path/to/ondc-bap/ root@neo-server.rozana.in:/opt/ondc-bap/"
    exit 1
fi

# Step 6: Setup Python environment
print_status "Setting up Python virtual environment..."
cd /opt/ondc-bap

# Check Python version
python3 --version
print_status "Python is already installed"

# Create virtual environment
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install --upgrade pip
sudo -u www-data .venv/bin/pip install -r requirements.txt

# Step 7: Create Apache configuration
print_status "Creating Apache configuration..."
tee /etc/apache2/sites-available/ondc-bap.conf > /dev/null << 'EOF'
<VirtualHost *:80>
    ServerName neo-server.rozana.in
    Redirect permanent / https://neo-server.rozana.in/
</VirtualHost>

<VirtualHost *:443>
    ServerName neo-server.rozana.in
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/neo-server.rozana.in/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/neo-server.rozana.in/privkey.pem
    
    # Proxy FastAPI Application
    ProxyPreserveHost On
    
    # Health endpoints
    ProxyPass /healthz http://localhost:8000/healthz
    ProxyPassReverse /healthz http://localhost:8000/healthz
    
    ProxyPass /livez http://localhost:8000/livez
    ProxyPassReverse /livez http://localhost:8000/livez
    
    ProxyPass /readyz http://localhost:8000/readyz
    ProxyPassReverse /readyz http://localhost:8000/readyz
    
    # ONDC endpoints
    ProxyPass /lookup http://localhost:8000/lookup
    ProxyPassReverse /lookup http://localhost:8000/lookup
    
    ProxyPass /vlookup http://localhost:8000/vlookup
    ProxyPassReverse /vlookup http://localhost:8000/vlookup
    
    ProxyPass /on_subscribe http://localhost:8000/on_subscribe
    ProxyPassReverse /on_subscribe http://localhost:8000/on_subscribe
    
    ProxyPass /onboarding http://localhost:8000/onboarding
    ProxyPassReverse /onboarding http://localhost:8000/onboarding
    
    # ONDC Site Verification
    Alias /ondc-site-verification.html /var/www/html/ondc-site-verification.html
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
EOF

# Step 8: Enable Apache site
print_status "Enabling Apache site..."
a2ensite ondc-bap.conf

# Step 9: Create systemd service
print_status "Creating systemd service..."
tee /etc/systemd/system/ondc-bap.service > /dev/null << 'EOF'
[Unit]
Description=ONDC BAP FastAPI Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/ondc-bap
Environment=PATH=/opt/ondc-bap/.venv/bin
ExecStart=/opt/ondc-bap/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Step 10: Copy ONDC files
print_status "Copying ONDC files..."
if [ -f "/opt/ondc-bap/ondc-site-verification.html" ]; then
    cp /opt/ondc-bap/ondc-site-verification.html /var/www/html/
    chown www-data:www-data /var/www/html/ondc-site-verification.html
else
    print_warning "ondc-site-verification.html not found, skipping..."
fi

# Step 11: Start services
print_status "Starting services..."
systemctl daemon-reload
systemctl enable ondc-bap.service
systemctl start ondc-bap.service
systemctl restart apache2

# Step 12: Wait for service to start
print_status "Waiting for service to start..."
sleep 5

# Step 13: Check service status
print_status "Checking service status..."
if systemctl is-active --quiet ondc-bap.service; then
    print_status "ONDC BAP service is running successfully!"
else
    print_error "ONDC BAP service failed to start. Check logs with:"
    print_error "journalctl -u ondc-bap.service -n 50"
    exit 1
fi

# Step 14: Test endpoints
print_status "Testing endpoints..."
echo "Testing health endpoint..."
if curl -s -f "https://neo-server.rozana.in/healthz" > /dev/null; then
    print_status "Health endpoint: ✅ OK"
else
    print_warning "Health endpoint: ❌ Failed"
fi

echo "Testing lookup endpoint..."
if curl -s -f "https://neo-server.rozana.in/lookup" > /dev/null; then
    print_status "Lookup endpoint: ✅ OK"
else
    print_warning "Lookup endpoint: ❌ Failed"
fi

echo "Testing site verification..."
if curl -s -f "https://neo-server.rozana.in/ondc-site-verification.html" > /dev/null; then
    print_status "Site verification: ✅ OK"
else
    print_warning "Site verification: ❌ Failed"
fi

# Step 15: Final status
print_status "Deployment completed!"
print_status "Service status: $(systemctl is-active ondc-bap.service)"
print_status "Apache status: $(systemctl is-active apache2)"

echo ""
print_status "ONDC BAP is now accessible at:"
echo "  - Health: https://neo-server.rozana.in/healthz"
echo "  - Lookup: https://neo-server.rozana.in/lookup"
echo "  - vlookup: https://neo-server.rozana.in/vlookup"
echo "  - Callback: https://neo-server.rozana.in/on_subscribe"
echo "  - Site Verification: https://neo-server.rozana.in/ondc-site-verification.html"

echo ""
print_status "Useful commands:"
echo "  - Check service: systemctl status ondc-bap.service"
echo "  - View logs: journalctl -u ondc-bap.service -f"
echo "  - Restart service: systemctl restart ondc-bap.service"
echo "  - Check Apache logs: tail -f /var/log/apache2/ondc-bap-error.log" 