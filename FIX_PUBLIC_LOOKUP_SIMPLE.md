# 🔧 Fix Public Lookup - Simple Approach

## ✅ **What's Done**

### **1. Created Direct Lookup Endpoint**
- ✅ **Local Endpoint**: `http://localhost:8000/lookup` ✅
- ✅ **Public URL**: `https://neo-server.rozana.in/lookup` (needs Apache config)

### **2. Lookup Endpoint Returns**
```json
{
  "subscriber_id": "neo-server.rozana.in",
  "subscriber_url": "https://neo-server.rozana.in",
  "callback_url": "/on_subscribe",
  "domain": "nic2004:52110",
  "type": "BAP",
  "status": "active",
  "signing_public_key": "QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=",
  "encryption_public_key": "MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=",
  "unique_key_id": "key_1755737751"
}
```

## 🚀 **Quick Fix for Public Endpoint**

### **SSH into your server and run:**

```bash
# SSH into your server
ssh root@neo-server.rozana.in

# Backup current config
sudo cp /etc/apache2/sites-available/ondc-bap.conf /etc/apache2/sites-available/ondc-bap.conf.backup

# Add lookup endpoint to Apache config
sudo tee -a /etc/apache2/sites-available/ondc-bap.conf > /dev/null << 'EOF'

# Add these lines to the VirtualHost section:
ProxyPass /lookup http://localhost:8000/lookup
ProxyPassReverse /lookup http://localhost:8000/lookup
EOF

# Restart Apache
sudo systemctl restart apache2

# Test the fix
curl -X GET "https://neo-server.rozana.in/lookup"
```

### **Alternative: Replace Entire Config**

```bash
# SSH into your server
ssh root@neo-server.rozana.in

# Replace with new config
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
    
    # Specific endpoints
    ProxyPass /lookup http://localhost:8000/lookup
    ProxyPassReverse /lookup http://localhost:8000/lookup
    
    ProxyPass /on_subscribe http://localhost:8000/on_subscribe
    ProxyPassReverse /on_subscribe http://localhost:8000/on_subscribe
    
    # Health endpoints
    ProxyPass /healthz http://localhost:8000/healthz
    ProxyPassReverse /healthz http://localhost:8000/healthz
    
    ProxyPass /livez http://localhost:8000/livez
    ProxyPassReverse /livez http://localhost:8000/livez
    
    ProxyPass /readyz http://localhost:8000/readyz
    ProxyPassReverse /readyz http://localhost:8000/readyz
    
    # ONDC Site Verification
    Alias /ondc-site-verification.html /var/www/html/ondc-site-verification.html
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
EOF

# Restart Apache
sudo systemctl restart apache2
```

## 🧪 **Testing**

### **After applying the fix:**

```bash
# Test public lookup
curl -X GET "https://neo-server.rozana.in/lookup"

# Test ONDC callback
curl -X POST "https://neo-server.rozana.in/on_subscribe" \
  -H "Content-Type: application/json" \
  -d '{"test": "public_test"}'

# Test health endpoints
curl -X GET "https://neo-server.rozana.in/healthz"
```

## 📋 **Expected Result**

```bash
curl -X GET "https://neo-server.rozana.in/lookup"
# Should return: 200 OK with subscriber information
```

## 🎯 **Summary**

- ✅ **Local endpoint works**: `http://localhost:8000/lookup`
- ⏳ **Public endpoint needs Apache config**: Add proxy rules
- ✅ **Simple URL**: `https://neo-server.rozana.in/lookup`

**Just add the Apache proxy rules and your public lookup will work!** 🚀 