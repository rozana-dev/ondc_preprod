# Ubuntu Server Deployment Guide for ONDC BAP Application

## 🎯 **Overview**
This guide will help you deploy the ONDC BAP (Buyer App) application on your Ubuntu server.

## 📋 **Prerequisites**
- Ubuntu 20.04 LTS or higher
- Python 3.8 or higher
- Apache2 web server
- SSH access to the server
- Domain name pointing to your server

## 🚀 **Step-by-Step Deployment**

### **Step 1: Upload BAP Folder to Server**

#### **Option A: Using SCP (if you have the folder locally)**
```bash
# Create directory on server
ssh ubuntu@your-server.com "sudo mkdir -p /var/www/bap && sudo chown ubuntu:ubuntu /var/www/bap"

# Upload BAP folder
scp -r BAP/* ubuntu@your-server.com:/var/www/bap/
```

#### **Option B: Using rsync (recommended)**
```bash
# Upload all files
rsync -avz --exclude='__pycache__' --exclude='*.pyc' BAP/app/ ubuntu@your-server.com:/var/www/bap/app/
rsync -avz BAP/requirements.txt BAP/Dockerfile BAP/ondc-site-verification.html ubuntu@your-server.com:/var/www/bap/
rsync -avz BAP/secrets/ ubuntu@your-server.com:/var/www/bap/secrets/
rsync -avz BAP/deployment/ ubuntu@your-server.com:/var/www/bap/deployment/
```

### **Step 2: SSH to Your Server**
```bash
ssh ubuntu@your-server.com
```

### **Step 3: Navigate to BAP Directory**
```bash
cd /var/www/bap
```

### **Step 4: Install System Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Apache and required modules
sudo apt install apache2 libapache2-mod-proxy libapache2-mod-proxy-http -y

# Enable required Apache modules
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2enmod rewrite
```

### **Step 5: Install Python Dependencies**
```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### **Step 6: Configure Systemd Service**

#### **Create the service file:**
```bash
sudo tee /etc/systemd/system/ondc-bap.service > /dev/null << 'EOF'
[Unit]
Description=ONDC BAP Application
After=network.target

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/bap
Environment=PATH=/var/www/bap/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

#### **Enable and start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ondc-bap
sudo systemctl start ondc-bap
```

### **Step 7: Configure Apache**

#### **Create Apache configuration:**
```bash
sudo tee /etc/apache2/sites-available/bap.conf > /dev/null << 'EOF'
<VirtualHost *:80>
    ServerName your-domain.com
    ServerAlias www.your-domain.com
    
    # Redirect HTTP to HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</VirtualHost>

<VirtualHost *:443>
    ServerName your-domain.com
    ServerAlias www.your-domain.com
    
    # SSL Configuration (update with your SSL certificate paths)
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/your-domain.com.crt
    SSLCertificateKeyFile /etc/ssl/private/your-domain.com.key
    
    # BAP Application Proxy
    ProxyPreserveHost On
    ProxyPass / http://localhost:8000/
    ProxyPassReverse / http://localhost:8000/
    
    # Health endpoint
    ProxyPass /health http://localhost:8000/health
    ProxyPassReverse /health http://localhost:8000/health
    
    # ONDC endpoints
    ProxyPass /on_subscribe http://localhost:8000/on_subscribe
    ProxyPassReverse /on_subscribe http://localhost:8000/on_subscribe
    
    ProxyPass /lookup http://localhost:8000/lookup
    ProxyPassReverse /lookup http://localhost:8000/lookup
    
    ProxyPass /vlookup http://localhost:8000/vlookup
    ProxyPassReverse /vlookup http://localhost:8000/vlookup
    
    # eKYC endpoints
    ProxyPass /ekyc http://localhost:8000/ekyc
    ProxyPassReverse /ekyc http://localhost:8000/ekyc
    
    # Site verification file
    Alias /ondc-site-verification.html /var/www/bap/ondc-site-verification.html
    <Files "ondc-site-verification.html">
        Require all granted
    </Files>
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/bap_error.log
    CustomLog ${APACHE_LOG_DIR}/bap_access.log combined
</VirtualHost>
EOF
```

#### **Enable the site and restart Apache:**
```bash
sudo a2ensite bap
sudo systemctl reload apache2
```

### **Step 8: Set Proper Permissions**
```bash
# Set ownership
sudo chown -R ubuntu:ubuntu /var/www/bap

# Set permissions
sudo chmod -R 755 /var/www/bap
sudo chmod 600 /var/www/bap/secrets/*

# Make sure Apache can read the files
sudo chmod 644 /var/www/bap/ondc-site-verification.html
```

### **Step 9: Configure SSL Certificate (if not already done)**

#### **Using Let's Encrypt (recommended):**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-apache -y

# Get SSL certificate
sudo certbot --apache -d your-domain.com -d www.your-domain.com
```

#### **Or manually configure SSL:**
Update the Apache configuration with your SSL certificate paths.

### **Step 10: Test the Deployment**

#### **Check service status:**
```bash
sudo systemctl status ondc-bap
```

#### **Test endpoints:**
```bash
# Health check
curl https://your-domain.com/health

# eKYC search
curl -X POST https://your-domain.com/ekyc/search \
  -H "Content-Type: application/json" \
  -d '{"context":{"action":"search"},"message":{}}'

# Site verification
curl https://your-domain.com/ondc-site-verification.html

# ONDC lookup
curl https://your-domain.com/lookup
```

## 🔧 **Troubleshooting**

### **Check Service Logs:**
```bash
# Check BAP service logs
sudo journalctl -u ondc-bap -f

# Check Apache logs
sudo tail -f /var/log/apache2/bap_error.log
sudo tail -f /var/log/apache2/bap_access.log
```

### **Common Issues:**

#### **1. Service won't start:**
```bash
# Check if port 8000 is available
sudo netstat -tlnp | grep :8000

# Check Python dependencies
cd /var/www/bap
python3 -c "import fastapi; print('FastAPI OK')"
```

#### **2. Apache proxy not working:**
```bash
# Check Apache configuration
sudo apache2ctl configtest

# Check if proxy modules are enabled
sudo apache2ctl -M | grep proxy
```

#### **3. Permission issues:**
```bash
# Fix permissions
sudo chown -R ubuntu:ubuntu /var/www/bap
sudo chmod -R 755 /var/www/bap
```

## 📋 **Configuration Files to Update**

### **1. Update Domain Name**
Replace `your-domain.com` with your actual domain in:
- Apache configuration (`/etc/apache2/sites-available/bap.conf`)
- SSL certificate paths

### **2. Update ONDC Configuration**
Edit `/var/www/bap/app/core/org_config.py`:
```python
SUBSCRIBER_ID = "your-domain.com"  # Update with your domain
BAP_URI = "https://your-domain.com/callback"  # Update with your domain
```

### **3. Update SSL Certificate Paths**
Update the Apache configuration with your SSL certificate paths:
```apache
SSLCertificateFile /path/to/your/certificate.crt
SSLCertificateKeyFile /path/to/your/private.key
```

## 🎯 **Final Verification**

After deployment, you should be able to access:

- **Health Check**: `https://your-domain.com/health`
- **eKYC Services**: `https://your-domain.com/ekyc/*`
- **ONDC Callbacks**: `https://your-domain.com/on_subscribe`
- **Lookup Endpoints**: `https://your-domain.com/lookup`
- **Site Verification**: `https://your-domain.com/ondc-site-verification.html`

## 📞 **Support**

If you encounter issues:
1. Check the service logs: `sudo journalctl -u ondc-bap -f`
2. Check Apache logs: `sudo tail -f /var/log/apache2/bap_error.log`
3. Verify all dependencies are installed: `pip list`
4. Test the application locally: `python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000`

---

**Note**: Replace `your-domain.com` with your actual domain name throughout this guide. 