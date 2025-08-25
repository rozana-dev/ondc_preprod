#!/bin/bash

echo "=== COMPLETE APACHE FIX FOR ONBOARDING ENDPOINTS ==="
echo "This script will fix the Apache configuration to handle all /onboarding/* sub-paths"
echo ""

# Find the Apache configuration file
echo "1. Finding Apache configuration file..."
CONFIG_FILE=$(sudo grep -r "neo-server.rozana.in" /etc/apache2/sites-available/ | head -1 | cut -d: -f1)
if [ -z "$CONFIG_FILE" ]; then
    echo "❌ Could not find Apache config file with neo-server.rozana.in"
    echo "Available config files:"
    ls -la /etc/apache2/sites-available/
    exit 1
fi
echo "✅ Found config file: $CONFIG_FILE"

# Backup the current configuration
echo ""
echo "2. Creating backup..."
BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
sudo cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "✅ Backup created: $BACKUP_FILE"

# Create complete Apache configuration
echo ""
echo "3. Creating complete Apache configuration..."
sudo tee "$CONFIG_FILE" > /dev/null << 'EOF'
<VirtualHost *:80>
    ServerName neo-server.rozana.in
    Redirect permanent / https://neo-server.rozana.in/
</VirtualHost>

<VirtualHost *:443>
    ServerName neo-server.rozana.in
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/neo-server.rozana.in/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/neo-server.rozana.in/privkey.pem
    
    ProxyPreserveHost On
    
    # Health endpoints
    ProxyPass /healthz http://localhost:8000/healthz
    ProxyPassReverse /healthz http://localhost:8000/healthz
    ProxyPass /livez http://localhost:8000/livez
    ProxyPassReverse /livez http://localhost:8000/livez
    ProxyPass /readyz http://localhost:8000/readyz
    ProxyPassReverse /readyz http://localhost:8000/readyz
    
    # Onboarding endpoints - COMPLETE SET (handles all sub-paths)
    ProxyPass /onboarding/ http://localhost:8000/onboarding/
    ProxyPassReverse /onboarding/ http://localhost:8000/onboarding/
    ProxyPass /onboarding http://localhost:8000/onboarding
    ProxyPassReverse /onboarding http://localhost:8000/onboarding
    
    # Lookup endpoints
    ProxyPass /vlookup http://localhost:8000/vlookup
    ProxyPassReverse /vlookup http://localhost:8000/vlookup
    ProxyPass /lookup http://localhost:8000/lookup
    ProxyPassReverse /lookup http://localhost:8000/lookup
    
    # ONDC callback
    ProxyPass /on_subscribe http://localhost:8000/on_subscribe
    ProxyPassReverse /on_subscribe http://localhost:8000/on_subscribe
    
    # Site verification
    ProxyPass /ondc-site-verification.html http://localhost:8000/ondc-site-verification.html
    ProxyPassReverse /ondc-site-verification.html http://localhost:8000/ondc-site-verification.html
    
    # Core ONDC actions
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
    
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
EOF

echo "✅ Complete Apache configuration created"

# Test Apache configuration
echo ""
echo "4. Testing Apache configuration..."
sudo apache2ctl configtest
if [ $? -eq 0 ]; then
    echo "✅ Apache configuration is valid"
else
    echo "❌ Apache configuration has errors"
    echo "Restoring backup..."
    sudo cp "$BACKUP_FILE" "$CONFIG_FILE"
    exit 1
fi

# Reload Apache
echo ""
echo "5. Reloading Apache..."
sudo systemctl reload apache2
if [ $? -eq 0 ]; then
    echo "✅ Apache reloaded successfully"
else
    echo "❌ Failed to reload Apache"
    exit 1
fi

# Test endpoints
echo ""
echo "6. Testing endpoints..."
echo "Testing base /onboarding endpoint:"
curl -s "https://neo-server.rozana.in/onboarding" | head -c 100
echo ""

echo "Testing /onboarding/subscriber-info:"
curl -s "https://neo-server.rozana.in/onboarding/subscriber-info" | head -c 100
echo ""

echo "Testing /vlookup:"
curl -s -X POST "https://neo-server.rozana.in/vlookup" -H "Content-Type: application/json" -d '{"test": "data"}' | head -c 100
echo ""

echo ""
echo "=== APACHE FIX COMPLETED ==="
echo "✅ Complete Apache configuration applied"
echo "✅ All /onboarding/* sub-paths should now work"
echo "✅ /vlookup endpoint should now work"
echo ""
echo "Next steps:"
echo "1. Test all onboarding endpoints on https://neo-server.rozana.in"
echo "2. If any endpoints still fail, check the Apache error logs"
echo "3. Proceed with ONDC onboarding once all endpoints are working" 