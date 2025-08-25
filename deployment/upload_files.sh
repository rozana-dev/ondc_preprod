#!/bin/bash

# Upload ONDC BAP files to server
# Run this from your local machine

SERVER="neo-server.rozana.in"
REMOTE_DIR="/opt/ondc-bap"

echo "📤 Uploading ONDC BAP files to $SERVER..."

# Create remote directory
ssh root@$SERVER "mkdir -p $REMOTE_DIR"

# Upload application files
echo "📁 Uploading application files..."
rsync -avz --exclude '.venv' --exclude '__pycache__' --exclude '*.pyc' \
    ./ $SERVER:$REMOTE_DIR/

# Upload deployment files
echo "⚙️ Uploading deployment configuration..."
rsync -avz deployment/ $SERVER:$REMOTE_DIR/deployment/

# Set permissions
echo "🔐 Setting permissions..."
ssh root@$SERVER "chown -R www-data:www-data $REMOTE_DIR"
ssh root@$SERVER "chmod +x $REMOTE_DIR/deployment/deploy.sh"

echo "✅ Upload completed!"
echo "🚀 Now run the deployment script on the server:"
echo "   ssh root@$SERVER"
echo "   cd $REMOTE_DIR"
echo "   sudo ./deployment/deploy.sh" 