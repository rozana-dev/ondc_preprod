#!/bin/bash

echo "=== FIXING ONBOARDING ENDPOINTS ==="
echo "Adding Apache proxy rules for /onboarding endpoints"
echo ""

# Step 1: Backup current Apache config
echo "1. Backing up current Apache configuration..."
sudo cp /etc/apache2/sites-available/neo-server.rozana.in.conf /etc/apache2/sites-available/neo-server.rozana.in.conf.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Backup created"

# Step 2: Add onboarding proxy rules to Apache config
echo ""
echo "2. Adding onboarding proxy rules to Apache configuration..."

# Read current config and add onboarding rules
sudo tee -a /etc/apache2/sites-available/neo-server.rozana.in.conf > /dev/null << 'EOF'

    # Onboarding endpoints - ADDED FOR ONDC SUBSCRIBE
    ProxyPass /onboarding http://localhost:8000/onboarding
    ProxyPassReverse /onboarding http://localhost:8000/onboarding
EOF

echo "✅ Onboarding proxy rules added"

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

# Step 5: Test onboarding endpoints
echo ""
echo "5. Testing onboarding endpoints..."
echo "Testing /onboarding/subscriber-info:"
curl -s "https://neo-server.rozana.in/onboarding/subscriber-info" | jq . 2>/dev/null || curl -s "https://neo-server.rozana.in/onboarding/subscriber-info"

echo ""
echo "Testing /onboarding/checklist:"
curl -s "https://neo-server.rozana.in/onboarding/checklist" | jq . 2>/dev/null || curl -s "https://neo-server.rozana.in/onboarding/checklist"

echo ""
echo "Testing /onboarding/subscribe-payload/pre_prod/1:"
curl -s "https://neo-server.rozana.in/onboarding/subscribe-payload/pre_prod/1" | jq . 2>/dev/null || curl -s "https://neo-server.rozana.in/onboarding/subscribe-payload/pre_prod/1"

echo ""
echo "=== ONBOARDING FIX COMPLETE ==="
echo "All /onboarding/* endpoints should now be accessible!"
echo ""
echo "Test these endpoints:"
echo "✅ https://neo-server.rozana.in/onboarding/subscriber-info"
echo "✅ https://neo-server.rozana.in/onboarding/checklist"
echo "✅ https://neo-server.rozana.in/onboarding/subscribe-payload/pre_prod/1"
echo "✅ https://neo-server.rozana.in/onboarding/generate-keys"
echo "✅ https://neo-server.rozana.in/onboarding/register"
echo "✅ https://neo-server.rozana.in/onboarding/test-challenge" 