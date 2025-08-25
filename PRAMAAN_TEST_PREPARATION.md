# 🚀 Pramaan Test Cases - Complete Preparation Guide

## 🎯 **Overview**
Pramaan will test your ONDC BAP endpoints to ensure compliance with ONDC API Schema v2.0. This guide ensures you're fully prepared.

## ✅ **Current Status**
- **Endpoint Coverage:** 95% (20/21 endpoints working)
- **Schema Compliance:** Ready for v2.0
- **Infrastructure:** Production-ready

## 📋 **Required ONDC BAP Endpoints**

### **✅ Core Action Endpoints (Working)**
```bash
POST /search      # Product/service discovery
POST /select      # Item selection
POST /init        # Order initialization  
POST /confirm     # Order confirmation
POST /status      # Order status check
POST /track       # Order tracking
POST /cancel      # Order cancellation
POST /rating      # Order rating
POST /support     # Customer support
```

### **⚠️ Missing Endpoint**
```bash
POST /update      # Order updates (needs deployment)
```

### **✅ Callback Endpoints (Working)**
```bash
GET  /on_subscribe      # Subscription callback
GET  /on_subscribe/test # Test callback
```

### **✅ Infrastructure Endpoints (Working)**
```bash
GET /health       # Health check
GET /healthz      # Kubernetes health
GET /livez        # Liveness probe  
GET /readyz       # Readiness probe
GET /lookup       # Participant lookup
GET /ondc-site-verification.html  # Domain verification
```

### **✅ eKYC Endpoints (Working)**
```bash
GET  /ekyc/health   # eKYC service health
POST /ekyc/search   # eKYC provider search
POST /ekyc/verify   # Document verification
```

## 🔧 **ONDC API Schema v2.0 Compliance**

### **Standard Request Format:**
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "country": "IND", 
    "city": "std:011",
    "action": "search",
    "core_version": "1.2.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "bpp_id": "seller.example.com",
    "bpp_uri": "https://seller.example.com",
    "transaction_id": "unique-txn-id",
    "message_id": "unique-msg-id", 
    "timestamp": "2025-01-15T10:30:00.000Z",
    "ttl": "PT30S"
  },
  "message": {
    // Action-specific payload
  }
}
```

### **Standard Response Format:**
```json
{
  "context": {
    // Same as request context with updated action
    "action": "on_search"
  },
  "message": {
    "ack": {
      "status": "ACK" | "NACK"
    },
    // Response-specific payload
  }
}
```

## 🔐 **Authentication & Security**

### **Required Headers:**
```bash
Content-Type: application/json
Authorization: Signature keyId="subscriber_id|key_id|algorithm",
               algorithm="ed25519",
               headers="(created) (expires) digest",
               signature="base64_signature"
X-Timestamp: 2025-01-15T10:30:00.000Z
```

### **Signature Verification:**
- **Algorithm:** Ed25519
- **Headers:** (created), (expires), digest
- **Key Format:** Base64 encoded public key

## 🧪 **Test Your Endpoints**

### **Run Pramaan Readiness Check:**
```bash
./pramaan_endpoints_check.sh
```

### **Test Individual Endpoints:**
```bash
# Test search endpoint
curl -X POST https://neo-server.rozana.in/search \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "action": "search",
      "bap_id": "neo-server.rozana.in"
    },
    "message": {
      "intent": {
        "item": {
          "descriptor": {
            "name": "Test Product"
          }
        }
      }
    }
  }'
```

### **Test eKYC Flow:**
```bash
# Test eKYC search
curl -X POST https://neo-server.rozana.in/ekyc/search \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10", 
      "action": "search"
    },
    "message": {}
  }'
```

## 🚀 **Deployment Steps**

### **1. Deploy Missing Update Endpoint:**
```bash
# Copy updated routes.py to server
scp app/api/routes.py user@server:/var/www/bap/BAP/app/api/routes.py

# Restart service
sudo systemctl restart ondc-bap
```

### **2. Verify All Endpoints:**
```bash
./pramaan_endpoints_check.sh
```

## 📊 **Pramaan Test Scenarios**

### **Flow 1: Complete Order Journey**
1. **Search** → Find products
2. **Select** → Choose items  
3. **Init** → Initialize order
4. **Confirm** → Confirm order
5. **Status** → Check order status
6. **Track** → Track fulfillment
7. **Rating** → Rate experience

### **Flow 2: Order Modifications**
1. **Update** → Modify order
2. **Cancel** → Cancel order
3. **Support** → Get support

### **Flow 3: eKYC Integration**
1. **eKYC Search** → Find KYC providers
2. **eKYC Verify** → Verify documents

## 🔍 **Monitoring & Debugging**

### **Log Monitoring:**
```bash
# Monitor application logs
tail -f /var/log/ondc-bap/app.log

# Monitor Apache logs  
tail -f /var/log/apache2/access.log
tail -f /var/log/apache2/error.log
```

### **Common Issues:**
- **404 Errors:** Check Apache proxy configuration
- **500 Errors:** Check application logs
- **Schema Errors:** Validate JSON structure
- **Signature Errors:** Check key configuration

## ✅ **Pre-Test Checklist**

- [ ] All 21 endpoints responding with HTTP 200
- [ ] Responses follow ONDC Schema v2.0 format
- [ ] Context object properly structured
- [ ] Message object contains required fields
- [ ] Timestamps in ISO 8601 format
- [ ] Transaction IDs are unique
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Domain verification active
- [ ] SSL certificate valid

## 🎯 **Pramaan Test Execution**

### **What Pramaan Will Test:**
1. **Endpoint Availability** - All required endpoints accessible
2. **Schema Compliance** - Responses match ONDC v2.0 schema
3. **Data Validation** - Required fields present and valid
4. **Error Handling** - Proper error responses
5. **Performance** - Response times within limits
6. **Security** - Signature verification (if enabled)

### **Expected Response Times:**
- **Health endpoints:** < 100ms
- **Action endpoints:** < 2000ms
- **Complex operations:** < 5000ms

## 🚨 **Final Steps Before Pramaan Testing**

1. **Deploy update endpoint**
2. **Run final endpoint check**
3. **Monitor logs in real-time**
4. **Have debugging tools ready**
5. **Ensure 100% uptime during test window**

## 🌐 **Your BAP Details for Pramaan**

```
BAP URL: https://neo-server.rozana.in
Subscriber ID: neo-server.rozana.in
Domain: ONDC:RET10 (Retail)
Environment: Pre-production ready
```

## 🎉 **Success Metrics**

- **Endpoint Availability:** 100% (21/21)
- **Schema Compliance:** 100%
- **Response Time:** < 2s average
- **Error Rate:** < 1%
- **Uptime:** 99.9%+

Your ONDC BAP is **95% ready** for Pramaan test cases! Deploy the update endpoint to achieve 100% readiness. 🚀