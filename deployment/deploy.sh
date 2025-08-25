#!/bin/bash

# ONDC BAP Deployment Script
# Run this on your server (neo-server.rozana.in)

set -e

echo "🚀 Starting ONDC BAP Deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv apache2 libapache2-mod-proxy-html

# Enable Apache modules
echo "🔌 Enabling Apache modules..."
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2enmod rewrite

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/ondc-bap
sudo chown www-data:www-data /opt/ondc-bap

# Copy application files (you'll need to upload your files)
echo "📋 Copying application files..."
# Note: You need to upload your application files to /opt/ondc-bap/
# You can use scp, rsync, or git clone

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
cd /opt/ondc-bap
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
sudo -u www-data .venv/bin/pip install -r requirements.txt

# Copy Apache configuration
echo "⚙️ Configuring Apache..."
sudo cp /opt/ondc-bap/deployment/apache_config.conf /etc/apache2/sites-available/ondc-bap.conf
sudo a2ensite ondc-bap.conf

# Copy systemd service
echo "🔧 Setting up systemd service..."
sudo cp /opt/ondc-bap/deployment/systemd_service.service /etc/systemd/system/ondc-bap.service
sudo systemctl daemon-reload
sudo systemctl enable ondc-bap.service

# Start the service
echo "🚀 Starting ONDC BAP service..."
sudo systemctl start ondc-bap.service

# Restart Apache
echo "🔄 Restarting Apache..."
sudo systemctl restart apache2

# Check status
echo "📊 Checking service status..."
sudo systemctl status ondc-bap.service

echo "✅ Deployment completed!"
echo "🌐 Your ONDC BAP is now accessible at: https://neo-server.rozana.in/v1/bap/"
echo "📡 ONDC callback URL: https://neo-server.rozana.in/v1/bap/on_subscribe" 