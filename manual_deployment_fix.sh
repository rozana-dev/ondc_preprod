#!/bin/bash

# Manual ONDC BAP Deployment Fix
# Run this script on the server to fix the directory structure issue

echo "🔧 Manual ONDC BAP deployment fix..."

# Create the missing directory structure
echo "📁 Creating missing directories..."
sudo mkdir -p /var/www/bap/app/api/v1
sudo mkdir -p /var/www/bap/app/core
sudo mkdir -p /var/www/bap/app/api
sudo mkdir -p /var/www/bap/secrets

# Set proper ownership and permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data /var/www/bap
sudo chmod -R 755 /var/www/bap

# Now copy the file (this should work now)
echo "📋 Copying ondc_bap.py..."
sudo cp /var/www/one_ondc/app/api/v1/ondc_bap.py /var/www/bap/app/api/v1/ondc_bap.py

# Verify the copy worked
echo "✅ Verifying file copy..."
ls -la /var/www/bap/app/api/v1/ondc_bap.py

# Restart the service
echo "🔄 Restarting service..."
sudo systemctl restart ondc-bap

echo "🎉 Fix completed! The file should now be properly deployed." 