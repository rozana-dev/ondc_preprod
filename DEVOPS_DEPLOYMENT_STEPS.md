# 🚀 ONDC BAP Deployment Steps for DevOps Team

## 📋 **Prerequisites**
- Ubuntu server with root/sudo access
- Python 3.8+ already installed ✅
- Apache2 web server
- SSL certificate for `neo-server.rozana.in`

## 📦 **Step 1: Prepare the Application Package**

### **1.1 Create Deployment Package**
```bash
# On your local machine, create a deployment package
cd /Users/anshumankumar/Desktop/one_ondc

# Create deployment archive (exclude development files)
tar -czf ondc-bap-deployment.tar.gz \
  --exclude='.venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.git' \
  --exclude='.DS_Store' \
  --exclude='*.log' \
  .
```

### **1.2 Files to Include in Package**
- ✅ `app/` - Complete application code
- ✅ `requirements.txt` - Python dependencies
- ✅ `deployment/` - Deployment configuration files
- ✅ `secrets/ondc_credentials.json` - ONDC cryptographic keys
- ✅ `ondc-site-verification.html` - ONDC verification file
- ✅ `scripts/` - Utility scripts

## 🖥️ **Step 2: Server Setup (Ubuntu Server)**

### **2.1 SSH into Server**
```bash
ssh root@neo-server.rozana.in
```

### **2.2 Update System**
```bash
sudo apt update && sudo apt upgrade -y
```

### **2.3 Install Required Packages**
```bash
sudo apt install -y apache2 libapache2-mod-proxy-html
```

### **2.4 Enable Apache Modules**
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2enmod rewrite
```

## 📁 **Step 3: Deploy Application**

### **3.1 Create Application Directory**
```bash
sudo mkdir -p /opt/ondc-bap
sudo chown www-data:www-data /opt/ondc-bap
```

### **3.2 Upload Application Files**
```bash
# Upload the deployment package to server
# Method 1: Using scp (from your local machine)
scp ondc-bap-deployment.tar.gz root@neo-server.rozana.in:/tmp/

# Method 2: Using rsync (from your local machine)
rsync -avz --exclude '.venv' --exclude '__pycache__' --exclude '*.pyc' \
  /Users/anshumankumar/Desktop/one_ondc/ root@neo-server.rozana.in:/opt/ondc-bap/
```

### **3.3 Extract and Setup Application**
```bash
# On the server
cd /opt/ondc-bap

# If using tar package:
sudo tar -xzf /tmp/ondc-bap-deployment.tar.gz -C /opt/ondc-bap/
sudo chown -R www-data:www-data /opt/ondc-bap/

# Check Python version (already installed)
python3 --version

# Create virtual environment
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install --upgrade pip

# Install dependencies
sudo -u www-data .venv/bin/pip install -r requirements.txt
```

## ⚙️ **Step 4: Configure Apache**

### **4.1 Create Apache Configuration**
```bash
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
    ProxyPass /healthz http://localhost:8000/healthz
    ProxyPassReverse /healthz http://localhost:8000/healthz
    
    ProxyPass /livez http://localhost:8000/livez
    ProxyPassReverse /livez http://localhost:8000/livez
    
    ProxyPass /readyz http://localhost:8000/readyz
    ProxyPassReverse /readyz http://localhost:8000/readyz
    
    # ONDC endpoints
    ProxyPass /lookup http://localhost:8000/lookup
    ProxyPassReverse /lookup http://localhost:8000/lookup
    
    ProxyPass /vlookup http://localhost:8000/vlookup
    ProxyPassReverse /vlookup http://localhost:8000/vlookup
    
    ProxyPass /on_subscribe http://localhost:8000/on_subscribe
    ProxyPassReverse /on_subscribe http://localhost:8000/on_subscribe
    
    ProxyPass /onboarding http://localhost:8000/onboarding
    ProxyPassReverse /onboarding http://localhost:8000/onboarding
    
    # ONDC Site Verification
    Alias /ondc-site-verification.html /var/www/html/ondc-site-verification.html
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
EOF
```

### **4.2 Enable Site and Restart Apache**
```bash
sudo a2ensite ondc-bap.conf
sudo systemctl restart apache2
```

## 🔧 **Step 5: Setup Systemd Service**

### **5.1 Create Systemd Service File**
```bash
sudo tee /etc/systemd/system/ondc-bap.service > /dev/null << 'EOF'
[Unit]
Description=ONDC BAP FastAPI Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/ondc-bap
Environment=PATH=/opt/ondc-bap/.venv/bin
ExecStart=/opt/ondc-bap/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### **5.2 Enable and Start Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ondc-bap.service
sudo systemctl start ondc-bap.service
```

## 📋 **Step 6: Copy ONDC Files**

### **6.1 Copy Site Verification File**
```bash
sudo cp /opt/ondc-bap/ondc-site-verification.html /var/www/html/
sudo chown www-data:www-data /var/www/html/ondc-site-verification.html
```

## 🧪 **Step 7: Testing**

### **7.1 Check Service Status**
```bash
sudo systemctl status ondc-bap.service
```

### **7.2 Test Health Endpoints**
```bash
curl -X GET "https://neo-server.rozana.in/healthz"
curl -X GET "https://neo-server.rozana.in/livez"
curl -X GET "https://neo-server.rozana.in/readyz"
```

### **7.3 Test ONDC Endpoints**
```bash
# Test lookup endpoint
curl -X GET "https://neo-server.rozana.in/lookup"

# Test vlookup endpoint
curl -X POST "https://neo-server.rozana.in/vlookup" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_subscriber_id": "test-sender.ondc.org",
    "request_id": "27baa06d-f90a-486c-85e5-cc621b787f04",
    "timestamp": "2024-08-21T10:00:00.000Z",
    "signature": "test_signature_here",
    "search_parameters": {
      "country": "IND",
      "domain": "ONDC:RET10",
      "type": "buyerApp",
      "city": "std:080",
      "subscriber_id": "neo-server.rozana.in"
    }
  }'

# Test ONDC callback
curl -X POST "https://neo-server.rozana.in/on_subscribe" \
  -H "Content-Type: application/json" \
  -d '{"test": "deployment_test"}'

# Test site verification
curl -X GET "https://neo-server.rozana.in/ondc-site-verification.html"
```

## 📊 **Step 8: Monitoring**

### **8.1 Check Logs**
```bash
# Application logs
sudo journalctl -u ondc-bap.service -f

# Apache logs
sudo tail -f /var/log/apache2/ondc-bap-error.log
sudo tail -f /var/log/apache2/ondc-bap-access.log
```

### **8.2 Check Service Status**
```bash
sudo systemctl status ondc-bap.service
sudo systemctl status apache2
```

## 🔄 **Step 9: Troubleshooting**

### **9.1 Common Issues**

**Service won't start:**
```bash
# Check logs
sudo journalctl -u ondc-bap.service -n 50

# Check permissions
sudo chown -R www-data:www-data /opt/ondc-bap/
```

**Apache 404 errors:**
```bash
# Check Apache config
sudo apache2ctl configtest

# Check if service is running
sudo systemctl status ondc-bap.service
```

**SSL issues:**
```bash
# Check SSL certificate
sudo certbot certificates

# Renew if needed
sudo certbot renew
```

## ✅ **Step 10: Verification Checklist**

- [ ] Service is running: `sudo systemctl status ondc-bap.service`
- [ ] Apache is running: `sudo systemctl status apache2`
- [ ] Health endpoint works: `curl https://neo-server.rozana.in/healthz`
- [ ] Lookup endpoint works: `curl https://neo-server.rozana.in/lookup`
- [ ] vlookup endpoint works: `curl -X POST https://neo-server.rozana.in/vlookup`
- [ ] ONDC callback works: `curl -X POST https://neo-server.rozana.in/on_subscribe`
- [ ] Site verification accessible: `curl https://neo-server.rozana.in/ondc-site-verification.html`

## 📞 **Support Information**

**Application Details:**
- **Service Name**: ondc-bap
- **Port**: 8000 (internal)
- **User**: www-data
- **Directory**: /opt/ondc-bap
- **Logs**: /var/log/apache2/ondc-bap-*.log

**ONDC Endpoints:**
- **Lookup**: `https://neo-server.rozana.in/lookup`
- **vlookup**: `https://neo-server.rozana.in/vlookup`
- **Callback**: `https://neo-server.rozana.in/on_subscribe`
- **Site Verification**: `https://neo-server.rozana.in/ondc-site-verification.html`

**Deployment completed successfully!** 🚀 