# 🔧 Fix Public Lookup - No v1/bap Prefix

## ✅ **Changes Made**

### **1. Removed `/v1/bap` Prefix from API Routes**
- ✅ **Updated**: `app/api/v1/ondc_bap.py` - Removed prefix
- ✅ **Local Testing**: Endpoints now work without `/v1/bap`

### **2. New Endpoint URLs (No v1/bap)**

| Old URL | New URL |
|---------|---------|
| `/v1/bap/onboarding/lookup/{subscriber_id}` | `/onboarding/lookup/{subscriber_id}` |
| `/v1/bap/onboarding/subscriber-info` | `/onboarding/subscriber-info` |
| `/v1/bap/onboarding/checklist` | `/onboarding/checklist` |
| `/v1/bap/on_subscribe` | `/on_subscribe` |
| `/v1/bap/search` | `/search` |
| `/v1/bap/init` | `/init` |
| `/v1/bap/confirm` | `/confirm` |

## 🚀 **Quick Fix for Public Endpoints**

### **Option 1: Simple Apache Config (Recommended)**

```bash
# SSH into your server
ssh root@neo-server.rozana.in

# Backup current config
sudo cp /etc/apache2/sites-available/ondc-bap.conf /etc/apache2/sites-available/ondc-bap.conf.backup

# Replace with simple config
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
    
    # Proxy FastAPI Application - Simple approach
    ProxyPreserveHost On
    
    # Proxy everything to FastAPI except static files
    ProxyPass /ondc-site-verification.html !
    ProxyPass / http://localhost:8000/
    ProxyPassReverse / http://localhost:8000/
    
    # ONDC Site Verification (static file)
    Alias /ondc-site-verification.html /var/www/html/ondc-site-verification.html
    
    # Logs
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
EOF

# Restart Apache
sudo systemctl restart apache2
```

### **Option 2: Use Deployment Script**

```bash
# Upload new config and deploy
./deployment/upload_files.sh
ssh root@neo-server.rozana.in "cd /opt/ondc-bap && sudo cp deployment/apache_config_simple.conf /etc/apache2/sites-available/ondc-bap.conf && sudo systemctl restart apache2"
```

## 🧪 **Testing After Fix**

### **1. Test Public Lookup (No v1/bap)**
```bash
curl -X GET "https://neo-server.rozana.in/onboarding/lookup/neo-server.rozana.in"
```

### **2. Test Other Endpoints**
```bash
# Subscriber info
curl -X GET "https://neo-server.rozana.in/onboarding/subscriber-info"

# Onboarding checklist
curl -X GET "https://neo-server.rozana.in/onboarding/checklist"

# ONDC callback
curl -X POST "https://neo-server.rozana.in/on_subscribe" \
  -H "Content-Type: application/json" \
  -d '{"test": "public_test"}'
```

### **3. Test Health Endpoints**
```bash
curl -X GET "https://neo-server.rozana.in/healthz"
curl -X GET "https://neo-server.rozana.in/livez"
curl -X GET "https://neo-server.rozana.in/readyz"
```

## 📋 **Expected Results**

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

## 🎯 **Benefits of This Approach**

1. **✅ Simpler URLs**: No `/v1/bap` prefix needed
2. **✅ Easier Configuration**: Single proxy rule for all endpoints
3. **✅ Better UX**: Cleaner, shorter URLs
4. **✅ ONDC Compliance**: Still maintains all required functionality

## 📞 **Next Steps**

1. **Apply Apache Config**: Use the simple config above
2. **Test Public Endpoints**: Verify all endpoints work
3. **Update ONDC Registration**: Use new URLs in registration
4. **Complete Onboarding**: Proceed with ONDC registration

**Your ONDC endpoints will now be accessible without the `/v1/bap` prefix!** 🚀 