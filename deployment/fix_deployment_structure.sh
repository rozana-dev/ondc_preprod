#!/bin/bash

# Fix ONDC BAP Deployment Structure
# This script creates the proper directory structure and copies files to the server

echo "🔧 Fixing ONDC BAP deployment structure..."

# Create the proper directory structure
echo "📁 Creating directory structure..."
sudo mkdir -p /var/www/bap/app/api/v1
sudo mkdir -p /var/www/bap/app/core
sudo mkdir -p /var/www/bap/app/api
sudo mkdir -p /var/www/bap/secrets

# Set proper permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data /var/www/bap
sudo chmod -R 755 /var/www/bap

# Copy the updated files
echo "📋 Copying updated files..."

# Copy the main ondc_bap.py file
sudo cp /var/www/one_ondc/app/api/v1/ondc_bap.py /var/www/bap/app/api/v1/ondc_bap.py

# Copy other necessary files
sudo cp /var/www/one_ondc/app/api/v1/ekyc.py /var/www/bap/app/api/v1/ekyc.py
sudo cp /var/www/one_ondc/app/api/v1/__init__.py /var/www/bap/app/api/v1/__init__.py
sudo cp /var/www/one_ondc/app/api/__init__.py /var/www/bap/app/api/__init__.py
sudo cp /var/www/one_ondc/app/__init__.py /var/www/bap/app/__init__.py
sudo cp /var/www/one_ondc/app/main.py /var/www/bap/app/main.py

# Copy core modules
sudo cp /var/www/one_ondc/app/core/config.py /var/www/bap/app/core/config.py
sudo cp /var/www/one_ondc/app/core/ondc_crypto.py /var/www/bap/app/core/ondc_crypto.py
sudo cp /var/www/one_ondc/app/core/ondc_registry.py /var/www/bap/app/core/ondc_registry.py
sudo cp /var/www/one_ondc/app/core/org_config.py /var/www/bap/app/core/org_config.py
sudo cp /var/www/one_ondc/app/core/__init__.py /var/www/bap/app/core/__init__.py

# Copy requirements and other files
sudo cp /var/www/one_ondc/requirements.txt /var/www/bap/requirements.txt
sudo cp /var/www/one_ondc/ondc-site-verification.html /var/www/bap/ondc-site-verification.html

# Copy secrets if they exist
if [ -f "/var/www/one_ondc/secrets/ondc_credentials.json" ]; then
    sudo cp /var/www/one_ondc/secrets/ondc_credentials.json /var/www/bap/secrets/ondc_credentials.json
    sudo chmod 600 /var/www/bap/secrets/ondc_credentials.json
fi

# Verify the structure
echo "✅ Verifying deployment structure..."
ls -la /var/www/bap/app/api/v1/
ls -la /var/www/bap/app/core/

# Restart the service
echo "🔄 Restarting ONDC BAP service..."
sudo systemctl restart ondc-bap

# Check service status
echo "📊 Service status:"
sudo systemctl status ondc-bap --no-pager

echo "🎉 Deployment structure fixed successfully!"
echo "📝 Next steps:"
echo "   1. Test the callback endpoint: curl https://neo-server.rozana.in/v1/bap/on_subscribe/test"
echo "   2. Check logs: sudo journalctl -u ondc-bap -f"
echo "   3. Verify ONDC registration is working" 