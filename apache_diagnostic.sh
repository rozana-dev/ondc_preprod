#!/bin/bash

echo "=== APACHE CONFIGURATION DIAGNOSTIC ==="
echo "This script will help you find the correct Apache configuration file"
echo ""

echo "1. Checking Apache sites-available directory..."
echo "Files in /etc/apache2/sites-available/:"
ls -la /etc/apache2/sites-available/

echo ""
echo "2. Checking Apache sites-enabled directory..."
echo "Files in /etc/apache2/sites-enabled/:"
ls -la /etc/apache2/sites-enabled/

echo ""
echo "3. Checking which configuration is active..."
echo "Active Apache configuration:"
sudo apache2ctl -S

echo ""
echo "4. Searching for your domain in configuration files..."
echo "Files containing 'neo-server.rozana.in':"
sudo grep -r "neo-server.rozana.in" /etc/apache2/sites-available/ 2>/dev/null || echo "No files found with neo-server.rozana.in"

echo ""
echo "5. Checking Apache modules..."
echo "Enabled Apache modules:"
sudo apache2ctl -M | grep -E "(proxy|ssl)"

echo ""
echo "6. Checking if FastAPI is running..."
echo "FastAPI service status:"
sudo systemctl status ondc-bap --no-pager -l

echo ""
echo "7. Checking if port 8000 is accessible..."
echo "Port 8000 status:"
sudo netstat -tlnp | grep 8000 || echo "Port 8000 not found"

echo ""
echo "8. Testing local FastAPI endpoints..."
echo "Testing local /onboarding/subscriber-info:"
curl -s http://localhost:8000/onboarding/subscriber-info | head -c 100

echo ""
echo "=== DIAGNOSTIC COMPLETE ==="
echo ""
echo "Based on the results above, you should:"
echo "1. Identify the correct configuration file name"
echo "2. Use that filename in the fix commands"
echo "3. Ensure Apache modules are enabled"
echo "4. Verify FastAPI is running on port 8000" 