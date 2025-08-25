#!/bin/bash

echo "=== QUICK APACHE FIX FOR ONDC BAP ==="
echo "This script will update Apache configuration to make all endpoints work"
echo ""

# Step 1: Backup current Apache config
echo "1. Backing up current Apache configuration..."
sudo cp /etc/apache2/sites-available/neo-server.rozana.in.conf /etc/apache2/sites-available/neo-server.rozana.in.conf.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Backup created"

# Step 2: Create new Apache configuration
echo ""
echo "2. Creating new Apache configuration..."
sudo tee /etc/apache2/sites-available/neo-server.rozana.in.conf > /dev/null << 'EOF'
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
    
    # ONDC endpoints - CRITICAL FOR LOOKUP
    ProxyPass /lookup http://localhost:8000/lookup
    ProxyPassReverse /lookup http://localhost:8000/lookup
    
    ProxyPass /vlookup http://localhost:8000/vlookup
    ProxyPassReverse /vlookup http://localhost:8000/vlookup
    
    ProxyPass /on_subscribe http://localhost:8000/on_subscribe
    ProxyPassReverse /on_subscribe http://localhost:8000/on_subscribe
    
    # ONDC Site Verification
    ProxyPass /ondc-site-verification.html http://localhost:8000/ondc-site-verification.html
    ProxyPassReverse /ondc-site-verification.html http://localhost:8000/ondc-site-verification.html
    
    # Onboarding endpoints
    ProxyPass /onboarding http://localhost:8000/onboarding
    ProxyPassReverse /onboarding http://localhost:8000/onboarding
    
    # Core action endpoints
    ProxyPass /search http://localhost:8000/search
    ProxyPassReverse /search http://localhost:8000/search
    
    ProxyPass /select http://localhost:8000/select
    ProxyPassReverse /select http://localhost:8000/select
    
    ProxyPass /init http://localhost:8000/init
    ProxyPassReverse /init http://localhost:8000/init
    
    ProxyPass /confirm http://localhost:8000/confirm
    ProxyPassReverse /confirm http://localhost:8000/confirm
    
    ProxyPass /status http://localhost:8000/status
    ProxyPassReverse /status http://localhost:8000/status
    
    ProxyPass /track http://localhost:8000/track
    ProxyPassReverse /track http://localhost:8000/track
    
    ProxyPass /cancel http://localhost:8000/cancel
    ProxyPassReverse /cancel http://localhost:8000/cancel
    
    ProxyPass /rating http://localhost:8000/rating
    ProxyPassReverse /rating http://localhost:8000/rating
    
    ProxyPass /support http://localhost:8000/support
    ProxyPassReverse /support http://localhost:8000/support
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
EOF

echo "✅ New Apache configuration created"

# Step 3: Test Apache configuration
echo ""
echo "3. Testing Apache configuration..."
sudo apache2ctl configtest
if [ $? -eq 0 ]; then
    echo "✅ Apache configuration is valid"
else
    echo "❌ Apache configuration has errors. Please check manually."
    exit 1
fi

# Step 4: Reload Apache
echo ""
echo "4. Reloading Apache..."
sudo systemctl reload apache2
if [ $? -eq 0 ]; then
    echo "✅ Apache reloaded successfully"
else
    echo "❌ Failed to reload Apache. Trying restart..."
    sudo systemctl restart apache2
fi

# Step 5: Restart FastAPI service
echo ""
echo "5. Restarting FastAPI service..."
sudo systemctl restart ondc-bap
if [ $? -eq 0 ]; then
    echo "✅ FastAPI service restarted"
else
    echo "❌ Failed to restart FastAPI service"
fi

# Step 6: Check service status
echo ""
echo "6. Checking service status..."
echo "Apache status:"
sudo systemctl status apache2 --no-pager -l
echo ""
echo "FastAPI service status:"
sudo systemctl status ondc-bap --no-pager -l

# Step 7: Quick test
echo ""
echo "7. Quick endpoint test..."
echo "Testing /healthz:"
curl -s "https://neo-server.rozana.in/healthz"
echo ""
echo "Testing /livez:"
curl -s "https://neo-server.rozana.in/livez"
echo ""
echo "Testing /lookup:"
curl -s "https://neo-server.rozana.in/lookup"
echo ""

echo ""
echo "=== DEPLOYMENT COMPLETE ==="
echo "All endpoints should now be working!"
echo "Test them with: curl https://neo-server.rozana.in/[endpoint]"
echo ""
echo "If any endpoints still don't work, check:"
echo "1. sudo journalctl -u ondc-bap -f"
echo "2. sudo tail -f /var/log/apache2/ondc-bap-error.log"
echo "3. sudo systemctl status ondc-bap" 