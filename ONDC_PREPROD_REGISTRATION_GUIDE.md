# 🚀 ONDC Pre-Production Registration Guide
## Subscriber: neo-server.rozana.in

### 📋 **Prerequisites Checklist**

#### ✅ **1. Domain Name**
- **Subscriber ID**: `neo-server.rozana.in`
- **Subscriber URL**: `https://neo-server.rozana.in`
- **Status**: ✅ Valid FQDN/DNS

#### ✅ **2. SSL Certificate**
- **Domain**: `neo-server.rozana.in`
- **Status**: ⚠️ **REQUIRED** - Ensure HTTPS is enabled
- **Note**: ONDC will perform OCSP validation

#### ⏳ **3. Whitelisting (CRITICAL)**
- **Portal**: https://portal.ondc.org
- **Steps**:
  1. Sign up on Network Participant Portal
  2. Complete profile 100%
  3. Raise whitelist request for `neo-server.rozana.in`
  4. Wait 6-48 hours for approval
- **Status**: ⏳ **PENDING** - Must complete before registration

#### ✅ **4. System Configuration**
- **Callback URL**: `https://neo-server.rozana.in/v1/bap/on_subscribe`
- **Site Verification**: `https://neo-server.rozana.in/ondc-site-verification.html`
- **Status**: ✅ Ready

---

### 🔑 **Generated Keys (✅ COMPLETED)**

#### Ed25519 Signing Keys
- **Public Key**: `QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=`
- **Private Key**: Stored securely in `secrets/ondc_credentials.json`

#### X25519 Encryption Keys
- **Public Key**: `MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=`
- **Private Key**: Stored securely in `secrets/ondc_credentials.json`

#### Request ID & Signature
- **Request ID**: `0102552d-98dc-49de-b6f1-e378bbe2c65d`
- **Signed Request ID**: Generated in `ondc-site-verification.html`

---

### 🌐 **Site Verification File**

#### ✅ **Generated File**: `ondc-site-verification.html`
```html
<!-- Contents of ondc-site-verification.html -->
<html>
    <head>
        <meta name='ondc-site-verification' content='SIGNED_REQUEST_ID' />
    </head>
    <body>
        ONDC Site Verification Page
        <br>
        Subscriber ID: neo-server.rozana.in
        <br>
        Generated: 2025-08-21T06:09:17.219752
    </body>
</html>
```

#### 📍 **Hosting Location**
- **URL**: `https://neo-server.rozana.in/ondc-site-verification.html`
- **Status**: ⚠️ **REQUIRED** - Must be accessible at domain root

---

### 📤 **Pre-Production Subscribe Payload**

#### **Registry URL**
```
https://preprod.registry.ondc.org/ondc/subscribe
```

#### **Payload Details**
```json
{
  "subscriber_id": "neo-server.rozana.in",
  "subscriber_url": "https://neo-server.rozana.in",
  "callback_url": "/v1/bap",
  "signing_public_key": "QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=",
  "encryption_public_key": "MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=",
  "unique_key_id": "key_1755737751",
  "request_id": "0102552d-98dc-49de-b6f1-e378bbe2c65d",
  "timestamp": "2025-08-21T06:28:57.788012+00:00",
  "valid_from": "2025-08-21T06:28:57.788019+00:00",
  "valid_until": "2025-12-31T23:59:59.999Z",
  "network_participant": [
    {
      "subscriber_url": "https://neo-server.rozana.in",
      "domain": "ONDC:RET10",
      "type": "buyerApp",
      "msn": false,
      "city_code": ["std:080", "std:011"],
      "country": "IND"
    }
  ]
}
```

---

### 🚀 **Registration Steps**

#### **Step 1: Whitelist Request (MANDATORY)**
```bash
# Visit: https://portal.ondc.org
# 1. Sign up and complete profile 100%
# 2. Submit whitelist request for: neo-server.rozana.in
# 3. Wait for approval (6-48 hours)
```

#### **Step 2: Host Site Verification**
```bash
# Ensure this file is accessible at:
# https://neo-server.rozana.in/ondc-site-verification.html
```

#### **Step 3: Submit Registration**
```bash
curl -X POST "https://preprod.registry.ondc.org/ondc/subscribe" \
  -H "Content-Type: application/json" \
  -d @preprod_subscribe_payload.json
```

#### **Step 4: Handle ONDC Challenge**
- ONDC will call: `https://neo-server.rozana.in/v1/bap/on_subscribe`
- Your endpoint will decrypt the challenge and respond
- Expected response format:
```json
{
  "answer": "decrypted_challenge_string"
}
```

#### **Step 5: Verify Registration**
```bash
# Check in pre-prod registry lookup
curl -X POST "https://preprod.registry.ondc.org/v2.0/lookup" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "IND",
    "domain": "ONDC:RET10"
  }'
```

---

### 🔍 **Expected Responses**

#### **Success Response**
```json
{
    "message": {
        "ack": {
            "status": "ACK"
        }
    },
    "error": {
        "type": null,
        "code": null,
        "path": null,
        "message": null
    }
}
```

#### **Common Error Responses**

**1. Subscriber ID not whitelisted**
```json
{
    "message": {"ack": {"status": "NACK"}},
    "error": {
        "type": "POLICY-ERROR",
        "code": "132",
        "message": "Subscriber Id is not whitelisted"
    }
}
```

**2. Domain verification failed**
```json
{
    "message": {"ack": {"status": "NACK"}},
    "error": {
        "type": "POLICY-ERROR",
        "code": "132",
        "message": "Domain verification is failed"
    }
}
```

**3. OCSP failed**
```json
{
    "message": {"ack": {"status": "NACK"}},
    "error": {
        "type": "POLICY-ERROR",
        "code": "132",
        "message": "OCSP failed"
    }
}
```

---

### 🛠️ **Testing Your Setup**

#### **1. Test Site Verification**
```bash
curl https://neo-server.rozana.in/ondc-site-verification.html
```

#### **2. Test Callback Endpoint**
```bash
curl -X POST https://neo-server.rozana.in/v1/bap/on_subscribe \
  -H "Content-Type: application/json" \
  -d '{"challenge": "test_challenge_123"}'
```

#### **3. Test Challenge Decryption**
```bash
curl -X POST https://neo-server.rozana.in/v1/bap/onboarding/test-challenge
```

---

### 📞 **Support Information**

#### **ONDC Support**
- **Email**: techsupport@ondc.org
- **Portal**: https://portal.ondc.org

#### **Required Information for Support**
```
Name: [Your Name]
Contact Number: [Your Phone]
Subscriber ID: neo-server.rozana.in
Error occurred: [Error Code]
Error Description: [Error Message]
Issue at step: [Step Number]
Issue/Clarification: [Description]
```

---

### ⚠️ **Important Notes**

1. **Whitelisting is MANDATORY** - Cannot proceed without approval
2. **HTTPS is REQUIRED** - SSL certificate must be valid
3. **Site verification file** must be at domain root
4. **Challenge decryption** must work correctly
5. **Rate limits**: 10 RPM for `/subscribe`
6. **Wait time**: 6-48 hours for whitelist approval

---

### 🎯 **Next Steps**

1. **IMMEDIATE**: Submit whitelist request at https://portal.ondc.org
2. **IMMEDIATE**: Ensure HTTPS is enabled on your domain
3. **IMMEDIATE**: Host `ondc-site-verification.html` at domain root
4. **AFTER WHITELIST**: Submit registration payload
5. **AFTER REGISTRATION**: Test with ONDC sandbox
6. **FINAL**: Move to production registration

---

**Status**: Ready for pre-production registration once whitelisted! 🚀 