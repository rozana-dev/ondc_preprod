# 🔍 ONDC Schema Error Debug Guide

## 📊 **Test Results Summary**

| Test | Payload Variation | Result | Notes |
|------|------------------|--------|-------|
| 1 | Full payload with valid_from/valid_until | ❌ Schema Error | Complete payload |
| 2 | Domain: `nic2004:52110` | ❌ Schema Error | Different domain format |
| 3 | City: `city_code` array | ❌ Schema Error | Array format |
| 4 | Minimal payload (no city) | ❌ Schema Error | Removed optional fields |
| 5 | Timestamp: `2025-08-21T07:12:59Z` | ❌ Schema Error | No milliseconds |

## 🎯 **Possible Root Causes**

### **1. 🔑 Key Format Issues**
- **Signing Public Key**: Ed25519 format might be incorrect
- **Encryption Public Key**: X25519 ASN.1 DER format might be wrong
- **Unique Key ID**: Format might not match ONDC expectations

### **2. 📅 Timestamp Issues**
- **Format**: ONDC might expect different timestamp format
- **Timezone**: UTC vs local timezone
- **Validity**: Timestamp might be too old/new

### **3. 🌐 Domain/Network Issues**
- **Domain Format**: `ONDC:RET10` vs `nic2004:52110`
- **Network Participant**: Required fields missing
- **Callback URL**: Format might be incorrect

### **4. 🔍 ONDC-Specific Requirements**
- **Schema Version**: Might need specific schema version
- **Required Fields**: Missing mandatory fields
- **Field Validation**: Specific validation rules

## 🚀 **Next Steps**

### **1. Contact ONDC Support**
```bash
Email: techsupport@ondc.org
Subject: Schema Error 151 - neo-server.rozana.in
Body:
- Subscriber ID: neo-server.rozana.in
- Error Code: 151
- Error Type: CONTEXT-ERROR
- Error Message: Please provide valid schema. ERROR : JSON-SCHEMA-ERROR
- Request: Please provide exact schema requirements
```

### **2. Check ONDC Documentation**
- **SwaggerHub**: https://app.swaggerhub.com/apis-docs/ONDC/ONDC-Registry-Onboarding/2.0.5
- **Schema Examples**: Look for exact payload examples
- **Field Requirements**: Verify each field format

### **3. Alternative Testing**
- **Staging Environment**: Test with staging first
- **Different Subscriber**: Test with a known working payload
- **Schema Validation**: Use JSON schema validator

## 📋 **Current Payload (Latest Test)**

```json
{
  "subscriber_id": "neo-server.rozana.in",
  "subscriber_url": "https://neo-server.rozana.in",
  "callback_url": "/v1/bap",
  "signing_public_key": "QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=",
  "encryption_public_key": "MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=",
  "unique_key_id": "key_1755737751",
  "request_id": "0102552d-98dc-49de-b6f1-e378bbe2c65d",
  "timestamp": "2025-08-21T07:12:59Z",
  "network_participant": [
    {
      "subscriber_url": "https://neo-server.rozana.in",
      "domain": "ONDC:RET10",
      "type": "buyerApp",
      "msn": false,
      "country": "IND"
    }
  ]
}
```

## 🔧 **Recommendations**

1. **Contact ONDC Support** for exact schema requirements
2. **Deploy Application** to make callback endpoint accessible
3. **Test with Staging** environment first
4. **Verify Site Verification** is accessible
5. **Check ONDC Portal** for any additional requirements

**The schema error persists despite whitelist approval, indicating a specific field format issue that requires ONDC support guidance.** 