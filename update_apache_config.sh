#!/bin/bash

# Update Apache Configuration for ONDC BAP
# This script updates the Apache config to include the missing /v1/bap/ routes

echo "🔧 Updating Apache configuration for ONDC BAP..."

# Backup current configuration
echo "📋 Backing up current configuration..."
sudo cp /etc/apache2/sites-available/ondc-bap.conf /etc/apache2/sites-available/ondc-bap.conf.backup.$(date +%Y%m%d_%H%M%S)

# Update the configuration
echo "📝 Updating Apache configuration..."
sudo tee /etc/apache2/sites-available/ondc-bap.conf > /dev/null << 'EOF'
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
    ProxyPass /health http://localhost:8000/health
    ProxyPassReverse /health http://localhost:8000/health
    
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
    
    # ONDC BAP API routes - NEW ADDITION
    ProxyPass /v1/bap http://localhost:8000/v1/bap
    ProxyPassReverse /v1/bap http://localhost:8000/v1/bap
    
    # ONDC Site Verification
    ProxyPass /ondc-site-verification.html http://localhost:8000/ondc-site-verification.html
    ProxyPassReverse /ondc-site-verification.html http://localhost:8000/ondc-site-verification.html
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
EOF

# Test configuration
echo "🧪 Testing Apache configuration..."
sudo apache2ctl configtest

if [ $? -eq 0 ]; then
    echo "✅ Configuration test passed"
    
    # Reload Apache
    echo "🔄 Reloading Apache..."
    sudo systemctl reload apache2
    
    # Check Apache status
    echo "📊 Apache status:"
    sudo systemctl status apache2 --no-pager
    
    echo "🎉 Apache configuration updated successfully!"
    echo ""
    echo "📝 Testing endpoints:"
    echo "   - Test endpoint: curl https://neo-server.rozana.in/v1/bap/on_subscribe/test"
    echo "   - Verification page: curl https://neo-server.rozana.in/v1/bap/verification"
    echo "   - Onboarding checklist: curl https://neo-server.rozana.in/v1/bap/onboarding/checklist"
    
else
    echo "❌ Configuration test failed. Please check the configuration."
    exit 1
fi 