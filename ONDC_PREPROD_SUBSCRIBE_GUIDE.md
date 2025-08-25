# 🚀 ONDC Pre-Production Subscribe Request Guide
## Subscriber: neo-server.rozana.in

### 📋 **ONDC Supported Registrations**

| ops_no | Type | Description |
|--------|------|-------------|
| 1 | Buyer App Registration | ✅ **SELECTED** |
| 2 | Seller App Registration | Available |
| 4 | Buyer & Seller App Registration | Available |

**Note**: ops_no 3 & 5 are deprecated as Seller On Record (SOR) feature is obsolete.

---

### 🔑 **Your Generated Credentials**

#### **Step 1 & 2: Key Generation (✅ COMPLETED)**
```json
{
  "subscriber_id": "neo-server.rozana.in",
  "signing_public_key": "QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=",
  "encryption_public_key": "MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=",
  "unique_key_id": "key_1755737751",
  "request_id": "0102552d-98dc-49de-b6f1-e378bbe2c65d"
}
```

---

### 📤 **Pre-Production Subscribe Request**

#### **Registry URL**
```
https://preprod.registry.ondc.org/ondc/subscribe
```

#### **Complete Payload**
```json
{
  "subscriber_id": "neo-server.rozana.in",
  "subscriber_url": "https://neo-server.rozana.in",
  "callback_url": "/v1/bap",
  "signing_public_key": "QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=",
  "encryption_public_key": "MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=",
  "unique_key_id": "key_1755737751",
  "request_id": "0102552d-98dc-49de-b6f1-e378bbe2c65d",
  "timestamp": "2025-08-21T06:46:08.514766+00:00",
  "valid_from": "2025-08-21T06:46:08.514775+00:00",
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

### 🔍 **Field-by-Field Verification**

| Field | Value | Status | Notes |
|-------|-------|--------|-------|
| **subscriber_id** | `neo-server.rozana.in` | ✅ | Your domain |
| **subscriber_url** | `https://neo-server.rozana.in` | ✅ | HTTPS required |
| **callback_url** | `/v1/bap` | ✅ | Relative path to on_subscribe |
| **signing_public_key** | `QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=` | ✅ | Ed25519 public key |
| **encryption_public_key** | `MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=` | ✅ | X25519 ASN.1 DER |
| **unique_key_id** | `key_1755737751` | ✅ | Unique tracking ID |
| **request_id** | `0102552d-98dc-49de-b6f1-e378bbe2c65d` | ✅ | UUID format |
| **timestamp** | `2025-08-21T06:46:08.514766+00:00` | ✅ | RFC3339 format |
| **valid_from** | `2025-08-21T06:46:08.514775+00:00` | ✅ | Current timestamp |
| **valid_until** | `2025-12-31T23:59:59.999Z` | ✅ | Future date |
| **network_participant[0].type** | `buyerApp` | ✅ | ops_no: 1 |
| **network_participant[0].domain** | `ONDC:RET10` | ✅ | Retail domain |
| **network_participant[0].country** | `IND` | ✅ | India |
| **network_participant[0].city_code** | `["std:080", "std:011"]` | ✅ | Bangalore, Delhi |

---

### 🚀 **Submit Registration**

#### **Method 1: Using curl**
```bash
curl -X POST "https://preprod.registry.ondc.org/ondc/subscribe" \
  -H "Content-Type: application/json" \
  -d @preprod_subscribe_payload.json
```

#### **Method 2: Using the script**
```bash
./submit_preprod_registration.sh
```

#### **Method 3: Manual submission**
```bash
curl -X POST "https://preprod.registry.ondc.org/ondc/subscribe" \
  -H "Content-Type: application/json" \
  -d '{
    "subscriber_id": "neo-server.rozana.in",
    "subscriber_url": "https://neo-server.rozana.in",
    "callback_url": "/v1/bap",
    "signing_public_key": "QfhgZ30kF6m6aj6gjpvFl2NsdSaV2AfGDNvs9Sqbdl0=",
    "encryption_public_key": "MCowBQYDK2VuAyEAYyPyJR9s9pzfzVPY0+P/X4mxPKPvS5RnGgFkqSLc+mM=",
    "unique_key_id": "key_1755737751",
    "request_id": "0102552d-98dc-49de-b6f1-e378bbe2c65d",
    "timestamp": "2025-08-21T06:46:08.514766+00:00",
    "valid_from": "2025-08-21T06:46:08.514775+00:00",
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
  }'
```

---

### 🔍 **Expected Response**

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

---

### ⚠️ **Prerequisites Checklist**

Before submitting, ensure:

- ✅ **Whitelist Request**: Submitted at https://portal.ondc.org
- ✅ **HTTPS Enabled**: SSL certificate valid for neo-server.rozana.in
- ✅ **Site Verification**: ondc-site-verification.html hosted at domain root
- ✅ **Callback Endpoint**: /v1/bap/on_subscribe accessible
- ✅ **Challenge Decryption**: Implemented and tested

---

### 🔄 **Registration Flow**

1. **Submit Payload** → ONDC Pre-Prod Registry
2. **ONDC Validates** → Schema, OCSP, Domain verification
3. **ONDC Sends Challenge** → To your callback endpoint
4. **Your System Responds** → Decrypted challenge answer
5. **Registration Complete** → Check in registry lookup

---

### 📞 **Support Information**

If you encounter issues:
- **Email**: techsupport@ondc.org
- **Portal**: https://portal.ondc.org
- **Include**: Subscriber ID, error codes, step details

---

**Status**: Ready for pre-production registration! 🚀 