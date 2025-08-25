#!/bin/bash

echo "=== COMPLETE ONBOARDING FIX ==="
echo "Fixing all /onboarding/* endpoints"
echo ""

# Step 1: Backup current Apache config
echo "1. Backing up current Apache configuration..."
sudo cp /etc/apache2/sites-available/neo-server.rozana.in.conf /etc/apache2/sites-available/neo-server.rozana.in.conf.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Backup created"

# Step 2: Check current Apache config
echo ""
echo "2. Checking current Apache configuration..."
echo "Current config contains:"
grep -n "ProxyPass" /etc/apache2/sites-available/neo-server.rozana.in.conf || echo "No ProxyPass rules found"

# Step 3: Create complete Apache configuration
echo ""
echo "3. Creating complete Apache configuration with all onboarding endpoints..."

# Create a complete Apache config
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
    
    # Onboarding endpoints - COMPLETE SET
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

echo "✅ Complete Apache configuration created"

# Step 4: Test Apache configuration
echo ""
echo "4. Testing Apache configuration..."
sudo apache2ctl configtest
if [ $? -eq 0 ]; then
    echo "✅ Apache configuration is valid"
else
    echo "❌ Apache configuration has errors. Please check manually."
    exit 1
fi

# Step 5: Reload Apache
echo ""
echo "5. Reloading Apache..."
sudo systemctl reload apache2
if [ $? -eq 0 ]; then
    echo "✅ Apache reloaded successfully"
else
    echo "❌ Failed to reload Apache. Trying restart..."
    sudo systemctl restart apache2
fi

# Step 6: Test all onboarding endpoints
echo ""
echo "6. Testing all onboarding endpoints..."
echo "Testing /onboarding/subscriber-info:"
curl -s "https://neo-server.rozana.in/onboarding/subscriber-info" | jq . 2>/dev/null || curl -s "https://neo-server.rozana.in/onboarding/subscriber-info"

echo ""
echo "Testing /onboarding/checklist:"
curl -s "https://neo-server.rozana.in/onboarding/checklist" | jq . 2>/dev/null || curl -s "https://neo-server.rozana.in/onboarding/checklist"

echo ""
echo "Testing /onboarding/subscribe-payload/pre_prod/1:"
curl -s "https://neo-server.rozana.in/onboarding/subscribe-payload/pre_prod/1" | jq . 2>/dev/null || curl -s "https://neo-server.rozana.in/onboarding/subscribe-payload/pre_prod/1"

echo ""
echo "Testing /onboarding/generate-keys:"
curl -s -X POST "https://neo-server.rozana.in/onboarding/generate-keys" | jq . 2>/dev/null || curl -s -X POST "https://neo-server.rozana.in/onboarding/generate-keys"

echo ""
echo "=== COMPLETE ONBOARDING FIX FINISHED ==="
echo "All /onboarding/* endpoints should now be working!"
echo ""
echo "Test these endpoints:"
echo "✅ https://neo-server.rozana.in/onboarding/subscriber-info"
echo "✅ https://neo-server.rozana.in/onboarding/checklist"
echo "✅ https://neo-server.rozana.in/onboarding/subscribe-payload/pre_prod/1"
echo "✅ https://neo-server.rozana.in/onboarding/generate-keys"
echo "✅ https://neo-server.rozana.in/onboarding/register"
echo "✅ https://neo-server.rozana.in/onboarding/test-challenge" 