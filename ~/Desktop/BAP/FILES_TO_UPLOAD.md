# BAP Application - Files to Upload to Server

## 📁 **Complete File List for Server Deployment**

### **1. Application Code (app/)**
```
app/
├── __init__.py
├── main.py
├── api/
│   ├── __init__.py
│   ├── health.py
│   ├── routes.py
│   └── v1/
│       ├── __init__.py
│       ├── ekyc.py
│       └── ondc_bap.py
└── core/
    ├── __init__.py
    ├── config.py
    ├── ondc_crypto.py
    ├── ondc_registry.py
    └── org_config.py
```

### **2. Configuration Files**
```
requirements.txt
Dockerfile
ondc-site-verification.html
```

### **3. Secrets (Critical for ONDC)**
```
secrets/
└── ondc_credentials.json
```

### **4. Deployment Scripts**
```
deployment/
├── apache_config.conf
├── apache_config_lookup.conf
├── apache_config_no_prefix.conf
├── apache_config_simple.conf
├── deploy.sh
├── quick_deploy.sh
├── systemd_service.service
└── upload_files.sh
```

## 🚀 **Upload Commands**

### **Option 1: Using rsync (Recommended)**
```bash
# Upload all files to server
rsync -avz --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
    app/ \
    ubuntu@neo-server.rozana.in:/var/www/bap/app/

# Upload configuration files
rsync -avz \
    requirements.txt \
    Dockerfile \
    ondc-site-verification.html \
    ubuntu@neo-server.rozana.in:/var/www/bap/

# Upload secrets
rsync -avz secrets/ ubuntu@neo-server.rozana.in:/var/www/bap/secrets/

# Upload deployment scripts
rsync -avz deployment/ ubuntu@neo-server.rozana.in:/var/www/bap/deployment/
```

### **Option 2: Using scp**
```bash
# Create directory structure
ssh ubuntu@neo-server.rozana.in "sudo mkdir -p /var/www/bap && sudo chown ubuntu:ubuntu /var/www/bap"

# Upload application
scp -r app/ ubuntu@neo-server.rozana.in:/var/www/bap/

# Upload config files
scp requirements.txt Dockerfile ondc-site-verification.html ubuntu@neo-server.rozana.in:/var/www/bap/

# Upload secrets
scp -r secrets/ ubuntu@neo-server.rozana.in:/var/www/bap/

# Upload deployment
scp -r deployment/ ubuntu@neo-server.rozana.in:/var/www/bap/
```

## 📋 **Server Setup Commands**

### **1. Install Dependencies**
```bash
ssh ubuntu@neo-server.rozana.in "cd /var/www/bap && python3 -m pip install --user -r requirements.txt"
```

### **2. Create Systemd Service**
```bash
# Copy service file
scp deployment/systemd_service.service ubuntu@neo-server.rozana.in:/tmp/ondc-bap.service

# Install service
ssh ubuntu@neo-server.rozana.in "sudo mv /tmp/ondc-bap.service /etc/systemd/system/ && sudo systemctl daemon-reload"
```

### **3. Configure Apache**
```bash
# Copy Apache config
scp deployment/apache_config.conf ubuntu@neo-server.rozana.in:/tmp/bap.conf

# Install config
ssh ubuntu@neo-server.rozana.in "sudo mv /tmp/bap.conf /etc/apache2/sites-available/ && sudo a2ensite bap && sudo systemctl reload apache2"
```

### **4. Start Service**
```bash
ssh ubuntu@neo-server.rozana.in "sudo systemctl enable ondc-bap && sudo systemctl start ondc-bap"
```

## 🔍 **Verification Commands**

### **Test Endpoints After Deployment**
```bash
# Health check
curl https://neo-server.rozana.in/health

# eKYC search
curl -X POST https://neo-server.rozana.in/ekyc/search \
  -H "Content-Type: application/json" \
  -d '{"context":{"action":"search"},"message":{}}'

# Site verification
curl https://neo-server.rozana.in/ondc-site-verification.html

# ONDC lookup
curl https://neo-server.rozana.in/lookup
```

## ⚠️ **Important Notes**

1. **Secrets**: The `secrets/ondc_credentials.json` file contains your ONDC cryptographic keys - keep it secure
2. **Permissions**: Make sure the server user has proper permissions to read the files
3. **Python Version**: Ensure Python 3.8+ is installed on the server
4. **Dependencies**: All required packages are listed in `requirements.txt`
5. **Port**: The BAP application runs on port 8000, Apache proxies to it

## 🎯 **Quick Deploy Script**

Use the existing deployment script:
```bash
cd ~/Desktop/BAP
bash deployment/quick_deploy.sh
```

This will upload all files and configure the server automatically. 