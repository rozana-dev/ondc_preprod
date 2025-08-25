# 🔐 eKYC Endpoints Guide for ONDC BAP

## 🎯 **Overview**

The eKYC (Electronic Know Your Customer) endpoints provide digital identity verification services for ONDC BAP. These endpoints follow the ONDC eKYC specification and enable secure customer verification.

---

## 🔧 **Current Issue**

The eKYC endpoints are **not working** because the Apache configuration is missing the `/ekyc` route. The FastAPI application has the eKYC router configured with prefix `/ekyc`, but Apache is not proxying this path.

---

## 🚀 **Fix Commands for Server**

Run these commands on your server as root to fix the eKYC endpoints:

```bash
# Step 1: Backup current configuration
cp /etc/apache2/sites-available/ondc-bap.conf /etc/apache2/sites-available/ondc-bap.conf.backup.$(date +%Y%m%d_%H%M%S)

# Step 2: Add eKYC route to Apache config
echo "" >> /etc/apache2/sites-available/ondc-bap.conf
echo "    # eKYC endpoints" >> /etc/apache2/sites-available/ondc-bap.conf
echo "    ProxyPass /ekyc http://localhost:8000/ekyc" >> /etc/apache2/sites-available/ondc-bap.conf
echo "    ProxyPassReverse /ekyc http://localhost:8000/ekyc" >> /etc/apache2/sites-available/ondc-bap.conf

# Step 3: Test the configuration
apache2ctl configtest

# Step 4: Reload Apache
systemctl reload apache2

# Step 5: Test eKYC endpoints
curl https://neo-server.rozana.in/ekyc/health
```

---

## 📋 **Available eKYC Endpoints**

### 1. **Health Check**
```bash
GET https://neo-server.rozana.in/ekyc/health
```
**Purpose:** Check if eKYC service is operational
**Response:** Service status and health information

### 2. **Search eKYC Providers**
```bash
POST https://neo-server.rozana.in/ekyc/search
```
**Purpose:** Search for available eKYC providers
**Payload:** ONDC search request with eKYC intent
**Response:** List of available eKYC providers

### 3. **Select eKYC Provider**
```bash
POST https://neo-server.rozana.in/ekyc/select
```
**Purpose:** Select a specific eKYC provider
**Payload:** Provider selection with order details
**Response:** Provider confirmation and order details

### 4. **Initiate eKYC Process**
```bash
POST https://neo-server.rozana.in/ekyc/initiate
```
**Purpose:** Start the eKYC verification process
**Payload:** Initiation request with fulfillment details
**Response:** Process initiation confirmation

### 5. **Verify eKYC Documents**
```bash
POST https://neo-server.rozana.in/ekyc/verify
```
**Purpose:** Submit documents for eKYC verification
**Payload:** Document verification request
**Response:** Verification status and results

### 6. **Check eKYC Status**
```bash
POST https://neo-server.rozana.in/ekyc/status
```
**Purpose:** Check the status of eKYC verification
**Payload:** Status inquiry with order ID
**Response:** Current verification status

---

## 🧪 **Test Scripts**

### **Quick Test Commands:**
```bash
# Test health endpoint
curl https://neo-server.rozana.in/ekyc/health

# Test search endpoint
curl -X POST https://neo-server.rozana.in/ekyc/search \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Test verify endpoint
curl -X POST https://neo-server.rozana.in/ekyc/verify \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### **Comprehensive Test Script:**
```bash
# Run the comprehensive test script
./test_ekyc_endpoints.sh
```

---

## 📝 **Sample Payloads**

### **Search Request:**
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
        "transaction_id": "test-transaction-123",
        "message_id": "test-message-123",
        "timestamp": "2025-08-22T10:00:00Z",
        "ttl": "PT30S"
    },
    "message": {
        "intent": {
            "item": {
                "descriptor": {
                    "name": "eKYC Verification"
                }
            }
        }
    }
}
```

### **Verify Request:**
```json
{
    "context": {
        "domain": "ONDC:RET10",
        "country": "IND",
        "city": "std:011",
        "action": "verify",
        "core_version": "1.2.0",
        "bap_id": "neo-server.rozana.in",
        "bap_uri": "https://neo-server.rozana.in",
        "transaction_id": "test-transaction-101",
        "message_id": "test-message-101",
        "timestamp": "2025-08-22T10:00:00Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "provider": {
                "id": "pramaan.ondc.org"
            },
            "items": [
                {
                    "id": "ekyc_verification",
                    "name": "eKYC Verification"
                }
            ],
            "fulfillment": {
                "type": "ONDC:ekyc",
                "verification": {
                    "document_type": "AADHAAR",
                    "document_number": "123456789012"
                }
            }
        }
    }
}
```

---

## 🔍 **Mock eKYC Providers**

The system includes mock eKYC providers for testing:

1. **Pramaan eKYC** (`pramaan.ondc.org`)
   - Official ONDC eKYC service
   - Rating: 4.8
   - Documents: AADHAAR, PAN, DRIVING_LICENSE, PASSPORT

2. **UIDAI eKYC** (`uidai.ondc.org`)
   - Aadhaar-based eKYC service
   - Rating: 4.9
   - Documents: AADHAAR

3. **NSDL eKYC** (`nsdl.ondc.org`)
   - PAN-based eKYC service
   - Rating: 4.7
   - Documents: PAN, AADHAAR

---

## 🚀 **Deployment Steps**

### **1. Fix Apache Configuration:**
```bash
# Run the fix script on the server
sudo bash /var/www/one_ondc/fix_ekyc_endpoints.sh
```

### **2. Test the Endpoints:**
```bash
# Test all eKYC endpoints
./test_ekyc_endpoints.sh
```

### **3. Verify Integration:**
```bash
# Check if eKYC is working with ONDC BAP
curl https://neo-server.rozana.in/ekyc/health
```

---

## 📊 **Expected Results**

After fixing the Apache configuration:

- ✅ **eKYC health endpoint**: Returns service status
- ✅ **eKYC search endpoint**: Returns list of providers
- ✅ **eKYC select endpoint**: Confirms provider selection
- ✅ **eKYC initiate endpoint**: Starts verification process
- ✅ **eKYC verify endpoint**: Processes document verification
- ✅ **eKYC status endpoint**: Returns verification status

---

## 🎯 **ONDC Integration**

The eKYC endpoints are designed to integrate with:
- **ONDC Registry**: For provider discovery
- **ONDC Gateway**: For message routing
- **ONDC BAP**: For customer verification workflows

---

## 📞 **Support**

If you encounter issues:
1. Check Apache logs: `tail -f /var/log/apache2/ondc-bap-error.log`
2. Check FastAPI logs: `journalctl -u ondc-bap -f`
3. Verify Apache configuration: `apache2ctl configtest`
4. Test endpoints manually with curl commands 