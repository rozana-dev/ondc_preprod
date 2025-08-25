# 📋 ONDC Pre-Production Postman Collection Setup Guide

## 🚀 Quick Start

### 1. Import Collection & Environment

**Import the Collection:**
1. Open Postman
2. Click "Import" button
3. Select `ONDC_BAP_PreProd_Complete_Collection.json`
4. Click "Import"

**Import the Environment:**
1. Click "Import" button again
2. Select `ONDC_PreProd_Environment.json`
3. Click "Import"
4. Select "ONDC PreProd Environment" from environment dropdown

### 2. Collection Overview

The collection includes **6 main folders** with **40+ endpoints**:

#### 🏥 Health Checks (4 endpoints)
- Kubernetes-style health checks (`/healthz`, `/livez`, `/readyz`)
- Local development health check

#### 🔔 ONDC Subscription & Verification (4 endpoints)
- Challenge/response testing
- Status updates
- Callback URL verification
- HTML verification page

#### 🛒 ONDC Core Actions (8 endpoints)
- Complete transaction flow: `search → select → init → confirm → status → track → cancel → rating → support`
- Updated with proper ONDC 1.1.0 schema
- UUID v4 transaction IDs [[memory:6953533]]

#### 🆔 eKYC Services (7 endpoints)
- Search providers
- Select provider
- Initiate verification
- Verify OTP/biometrics
- Check status
- Track transactions
- List all transactions

#### 🚀 ONDC Onboarding & Registry (10 endpoints)
- Onboarding checklist
- Key generation
- Subscribe payload creation
- Registry registration
- Subscriber lookup
- Status management

#### 🌐 Registry Direct Testing (6 endpoints)
- Direct registry API calls
- PreProd and Staging environments
- Health checks and lookups

#### 🔐 Pramaan eKYC Testing (3 endpoints)
- Direct Pramaan integration
- eKYC service testing

---

## 🔧 Configuration

### Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `base_url` | `https://neo-server.rozana.in` | Production BAP URL |
| `local_url` | `http://localhost:8000` | Local development URL |
| `subscriber_id` | `neo-server.rozana.in` | Your ONDC subscriber ID |
| `domain` | `ONDC:RET10` | Current ONDC domain |
| `preprod_registry` | `https://preprod.registry.ondc.org` | PreProd registry |
| `staging_registry` | `https://staging.registry.ondc.org` | Staging registry |
| `pramaan_url` | `https://pramaan.ondc.org` | Pramaan eKYC service |

### Auto-Generated Variables

The collection automatically generates:
- **Transaction ID**: UUID v4 format [[memory:6953533]]
- **Message ID**: UUID v4 format using `{{$guid}}`
- **Timestamps**: ISO format using `{{$isoTimestamp}}`

---

## 🧪 Testing Workflows

### 1. Health Check Workflow
```
1. Health Check (K8s) → Verify service is running
2. Liveness Probe → Check container health
3. Readiness Probe → Verify ready to serve traffic
4. Local BAP Health → Test local development
```

### 2. Onboarding Workflow
```
1. Get Onboarding Checklist → Review requirements
2. Generate ONDC Keys → Create crypto keys
3. Get Subscriber Info → Verify configuration
4. Get Subscribe Payload → Generate registration
5. Register with Registry → Submit to ONDC
6. Lookup Subscriber → Verify registration
```

### 3. eKYC Workflow
```
1. eKYC Search Providers → Find available services
2. eKYC Select Provider → Choose Pramaan
3. eKYC Initiate → Start verification process
4. eKYC Verify OTP → Complete with OTP
5. eKYC Check Status → Verify completion
```

### 4. ONDC Transaction Flow
```
1. Search → Find products
2. Select → Choose items
3. Init → Add billing/delivery
4. Confirm → Place order
5. Status → Check order status
6. Track → Monitor delivery
7. Rating → Provide feedback
```

---

## 📊 Pre-Production Testing Checklist

### ✅ Prerequisites
- [ ] ONDC keys generated and configured
- [ ] Subscriber ID whitelisted at https://portal.ondc.org
- [ ] HTTPS enabled on `neo-server.rozana.in`
- [ ] `ondc-site-verification.html` hosted at domain root
- [ ] Callback endpoint `/v1/bap/on_subscribe` accessible

### 🔍 Test Sequence

#### Phase 1: Health & Connectivity
```
1. Run all Health Checks → Ensure services are up
2. Test Subscription Callback → Verify ONDC can reach you
3. Test Verification Page → Check HTML page loads
```

#### Phase 2: Registry Registration
```
1. Get Subscribe Payload (PreProd) → Generate payload
2. PreProd Registry Subscribe → Register with registry
3. PreProd Registry Lookup → Verify registration
4. Test Challenge Decryption → Verify crypto works
```

#### Phase 3: Core ONDC Actions
```
1. Search → Test discovery
2. Select → Test item selection
3. Init → Test order initialization
4. Confirm → Test order confirmation
5. Status → Test status inquiry
```

#### Phase 4: eKYC Integration
```
1. eKYC Search → Test provider discovery
2. eKYC Initiate → Test verification start
3. eKYC Verify → Test OTP verification
4. eKYC Status → Test status check
```

---

## 🔄 Environment Switching

### For Local Testing:
1. Change `base_url` to `{{local_url}}`
2. Ensure local server running on port 8000
3. Run health checks first

### For Different Registries:
- **Staging**: Use endpoints in "Registry Direct Testing" folder
- **PreProd**: Use `{{preprod_registry}}` variable
- **Production**: Use production registry URLs

---

## 🐛 Troubleshooting

### Common Issues:

#### 1. 404 Not Found
- **Cause**: Endpoint not available
- **Fix**: Check if service is running, verify URL path

#### 2. 500 Internal Server Error
- **Cause**: Server-side error
- **Fix**: Check server logs, ensure database/dependencies running

#### 3. Challenge Decryption Failed
- **Cause**: Crypto keys mismatch
- **Fix**: Regenerate keys, update environment variables

#### 4. Registry Subscription Failed
- **Cause**: Not whitelisted or invalid payload
- **Fix**: Complete whitelisting process, verify payload format

#### 5. Transaction ID Issues
- **Cause**: Non-UUID format or inconsistent usage
- **Fix**: Use UUID v4 format, maintain consistency [[memory:6953533]]

### Debug Steps:
1. Enable Postman Console (View → Show Postman Console)
2. Check request/response details
3. Verify environment variables are set
4. Test endpoints individually before running flows

---

## 📝 Response Format Notes

- **Health Endpoints**: Return `200 OK` with status message
- **ONDC Actions**: Return `202 Accepted` for async processing
- **Subscription Callback**: Returns `200 OK` with ACK
- **Registry Calls**: Various response codes depending on operation
- **eKYC**: Returns structured response with transaction details

---

## 🔗 Useful Links

- **ONDC Portal**: https://portal.ondc.org
- **PreProd Registry**: https://preprod.registry.ondc.org
- **Staging Registry**: https://staging.registry.ondc.org
- **Pramaan Service**: https://pramaan.ondc.org
- **Your BAP URL**: https://neo-server.rozana.in
- **Verification Page**: https://neo-server.rozana.in/v1/bap/verification

---

## 📞 Support

If you encounter issues:

1. Check server logs for detailed error messages
2. Verify all environment variables are correctly set
3. Ensure prerequisites are completed
4. Test endpoints individually before running complete flows
5. Review ONDC documentation for schema updates

**Happy Testing! 🚀**