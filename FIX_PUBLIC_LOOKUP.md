# 🔧 Fix Public Lookup Endpoint Issue

## 🚨 **Current Problem**

The public lookup endpoint is returning **404 Not Found**:
```bash
curl -X GET "https://neo-server.rozana.in/v1/bap/onboarding/lookup/neo-server.rozana.in"
# Returns: 404 Not Found
```

## 🔍 **Root Cause Analysis**

### **✅ What's Working:**
- ✅ **Health Endpoints**: `https://neo-server.rozana.in/healthz` ✅
- ✅ **Site Verification**: `https://neo-server.rozana.in/ondc-site-verification.html` ✅
- ✅ **Local API**: `http://localhost:8000/v1/bap/onboarding/lookup/neo-server.rozana.in` ✅

### **❌ What's Broken:**
- ❌ **Public v1/bap Endpoints**: All `/v1/bap/*` paths return 404
- ❌ **Apache Reverse Proxy**: Not configured for `/v1/bap` path

## 🛠️ **Solution: Fix Apache Configuration**

### **Step 1: Current Apache Config Issue**

The current Apache configuration is missing the `/v1/bap` proxy rule. Here's what needs to be added:

```apache
# Missing in current config:
ProxyPass /v1/bap http://localhost:8000/v1/bap
ProxyPassReverse /v1/bap http://localhost:8000/v1/bap
```

### **Step 2: Correct Apache Configuration**

```apache
<VirtualHost *:443>
    ServerName neo-server.rozana.in
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/neo-server.rozana.in/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/neo-server.rozana.in/privkey.pem
    
    # Proxy FastAPI Application - FIXED
    ProxyPreserveHost On
    
    # Health endpoints (working)
    ProxyPass /healthz http://localhost:8000/healthz
    ProxyPassReverse /healthz http://localhost:8000/healthz
    
    ProxyPass /livez http://localhost:8000/livez
    ProxyPassReverse /livez http://localhost:8000/livez
    
    ProxyPass /readyz http://localhost:8000/readyz
    ProxyPassReverse /readyz http://localhost:8000/readyz
    
    # ONDC BAP endpoints - ADD THIS
    ProxyPass /v1/bap http://localhost:8000/v1/bap
    ProxyPassReverse /v1/bap http://localhost:8000/v1/bap
    
    # ONDC Site Verification
    Alias /ondc-site-verification.html /var/www/html/ondc-site-verification.html
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
```

## 🚀 **Quick Fix Commands**

### **Option 1: SSH into Server and Fix**

```bash
# SSH into your server
ssh root@neo-server.rozana.in

# Edit Apache config
sudo nano /etc/apache2/sites-available/ondc-bap.conf

# Add these lines:
ProxyPass /v1/bap http://localhost:8000/v1/bap
ProxyPassReverse /v1/bap http://localhost:8000/v1/bap

# Restart Apache
sudo systemctl restart apache2

# Test the fix
curl -X GET "https://neo-server.rozana.in/v1/bap/onboarding/lookup/neo-server.rozana.in"
```

### **Option 2: Use Deployment Scripts**

```bash
# Upload and deploy using our scripts
./deployment/upload_files.sh
ssh root@neo-server.rozana.in "cd /opt/ondc-bap && sudo ./deployment/deploy.sh"
```

## 🧪 **Testing After Fix**

### **1. Test Public Lookup**
```bash
curl -X GET "https://neo-server.rozana.in/v1/bap/onboarding/lookup/neo-server.rozana.in"
```

### **2. Test Other v1/bap Endpoints**
```bash
# Subscriber info
curl -X GET "https://neo-server.rozana.in/v1/bap/onboarding/subscriber-info"

# Onboarding checklist
curl -X GET "https://neo-server.rozana.in/v1/bap/onboarding/checklist"

# Test challenge
curl -X POST "https://neo-server.rozana.in/v1/bap/onboarding/test-challenge"
```

### **3. Test ONDC Callback**
```bash
curl -X POST "https://neo-server.rozana.in/on_subscribe" \
  -H "Content-Type: application/json" \
  -d '{"test": "public_lookup_test"}'
```

## 📋 **Expected Results After Fix**

### **✅ Public Lookup Should Return:**
```json
{
  "subscriber_id": "neo-server.rozana.in",
  "subscriber_url": "https://neo-server.rozana.in",
  "callback_url": "/on_subscribe",
  "signing_public_key": "QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=",
  "encryption_public_key": "MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=",
  "unique_key_id": "key_1755737751",
  "status": "active"
}
```

## 🎯 **Next Steps**

1. **Fix Apache Configuration** (above)
2. **Test Public Lookup** 
3. **Verify All v1/bap Endpoints**
4. **Complete ONDC Registration**

**The issue is simply a missing Apache proxy configuration for the `/v1/bap` path!** 🔧 