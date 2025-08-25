#!/bin/bash

echo "=== VERIFYING APACHE CONFIGURATION ==="
echo "This script will check your current Apache configuration and fix the onboarding endpoints"
echo ""

echo "1. Checking current Apache configuration files..."
echo "Files in /etc/apache2/sites-available/:"
ls -la /etc/apache2/sites-available/

echo ""
echo "2. Checking which configuration is active..."
sudo apache2ctl -S

echo ""
echo "3. Finding the configuration file with your domain..."
CONFIG_FILE=$(sudo grep -r "neo-server.rozana.in" /etc/apache2/sites-available/ | head -1 | cut -d: -f1)
if [ -z "$CONFIG_FILE" ]; then
    echo "❌ No configuration file found with neo-server.rozana.in"
    echo "Let's check the default SSL configuration..."
    CONFIG_FILE="/etc/apache2/sites-available/default-ssl.conf"
    if [ ! -f "$CONFIG_FILE" ]; then
        CONFIG_FILE="/etc/apache2/sites-available/000-default.conf"
    fi
else
    echo "✅ Found configuration file: $CONFIG_FILE"
fi

echo ""
echo "4. Checking current proxy rules in $CONFIG_FILE..."
echo "Current ProxyPass rules:"
sudo grep -n "ProxyPass" "$CONFIG_FILE" || echo "No ProxyPass rules found"

echo ""
echo "5. Checking if /onboarding proxy rule exists..."
if sudo grep -q "ProxyPass /onboarding" "$CONFIG_FILE"; then
    echo "✅ /onboarding proxy rule found"
else
    echo "❌ /onboarding proxy rule NOT found"
fi

echo ""
echo "6. Checking if /vlookup proxy rule exists..."
if sudo grep -q "ProxyPass /vlookup" "$CONFIG_FILE"; then
    echo "✅ /vlookup proxy rule found"
else
    echo "❌ /vlookup proxy rule NOT found"
fi

echo ""
echo "7. Adding missing proxy rules..."
echo "Backing up current configuration..."
sudo cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"

echo "Adding missing proxy rules to $CONFIG_FILE..."
sudo tee -a "$CONFIG_FILE" > /dev/null << 'EOF'

    # Onboarding endpoints - ADDED FOR ONDC SUBSCRIBE
    ProxyPass /onboarding http://localhost:8000/onboarding
    ProxyPassReverse /onboarding http://localhost:8000/onboarding
    
    # Lookup endpoints - ADDED FOR ONDC LOOKUP
    ProxyPass /vlookup http://localhost:8000/vlookup
    ProxyPassReverse /vlookup http://localhost:8000/vlookup
EOF

echo ""
echo "8. Testing Apache configuration..."
sudo apache2ctl configtest
if [ $? -eq 0 ]; then
    echo "✅ Apache configuration is valid"
else
    echo "❌ Apache configuration has errors"
    exit 1
fi

echo ""
echo "9. Reloading Apache..."
sudo systemctl reload apache2
if [ $? -eq 0 ]; then
    echo "✅ Apache reloaded successfully"
else
    echo "❌ Failed to reload Apache. Trying restart..."
    sudo systemctl restart apache2
fi

echo ""
echo "10. Testing onboarding endpoints..."
echo "Testing /onboarding/subscriber-info:"
curl -s "https://neo-server.rozana.in/onboarding/subscriber-info" | head -c 200

echo ""
echo "Testing /onboarding/checklist:"
curl -s "https://neo-server.rozana.in/onboarding/checklist" | head -c 200

echo ""
echo "Testing /vlookup:"
curl -s -X POST "https://neo-server.rozana.in/vlookup" -H "Content-Type: application/json" -d '{"test": "data"}' | head -c 200

echo ""
echo "=== VERIFICATION COMPLETE ==="
echo "If the endpoints are still not working, check:"
echo "1. FastAPI service status: sudo systemctl status ondc-bap"
echo "2. Port 8000 accessibility: sudo netstat -tlnp | grep 8000"
echo "3. Local endpoint test: curl http://localhost:8000/onboarding/subscriber-info"
echo "4. Apache error logs: sudo tail -f /var/log/apache2/error.log" 