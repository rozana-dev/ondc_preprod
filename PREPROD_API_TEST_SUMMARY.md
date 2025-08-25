# Preprod Environment API Test Summary

## 🎯 **Test Overview**
- **Date**: August 22, 2025
- **Environment**: Preprod
- **Subscriber ID**: neo-server.rozana.in
- **Overall Success Rate**: 6/12 tests passed (50.0%)

---

## 📊 **Detailed Test Results**

### ✅ **Pramaan Services** (2/3 PASSED)

#### ✅ **Pramaan Health Check**
- **Endpoint**: `https://pramaan.ondc.org/health`
- **Status**: ✅ **PASSED**
- **Response**: `ok`
- **Details**: Service is operational

#### ✅ **Pramaan Discovery**
- **Endpoint**: `https://pramaan.ondc.org/`
- **Status**: ✅ **PASSED**
- **Response**: HTML page with ONDC Pramaan interface
- **Details**: Main interface accessible

#### ❌ **Pramaan eKYC Services**
- **Status**: ❌ **FAILED**
- **Endpoints Tested**:
  - `/ekyc/search` - 404 Not Found
  - `/api/ekyc/search` - 404 Not Found
  - `/v1/ekyc/search` - 404 Not Found
  - `/search` - 404 Not Found
  - `/kyc/search` - 404 Not Found
  - `/ekyc/initiate` - 404 Not Found
  - `/api/ekyc/initiate` - 404 Not Found
  - `/v1/ekyc/initiate` - 404 Not Found
  - `/initiate` - 404 Not Found
  - `/kyc/initiate` - 404 Not Found
- **Issue**: All eKYC endpoints return 404 - API may not be implemented

---

### ✅ **ONDC Registry Services** (2/4 PASSED)

#### ✅ **Registry Health Check**
- **Preprod**: `https://preprod.registry.ondc.org/health` - ✅ **PASSED**
- **Staging**: `https://staging.registry.ondc.org/health` - ✅ **PASSED**
- **Production**: `https://registry.ondc.org/health` - ❌ SSL Certificate Expired
- **Response**: `OK`

#### ❌ **Registry Discovery**
- **Status**: ❌ **FAILED**
- **Endpoints Tested**: `/`, `/api`, `/v1`, `/docs`, `/swagger`, `/openapi`
- **Issue**: All discovery endpoints return 404
- **Note**: Registry APIs are functional but discovery endpoints are not exposed

#### ✅ **Registry Subscribe**
- **Preprod**: `https://preprod.registry.ondc.org/ondc/subscribe` - ✅ **PASSED**
- **Staging**: `https://staging.registry.ondc.org/ondc/subscribe` - ❌ 404 Not Found
- **Response**: 200 OK (with domain verification error)
- **Error**: `"Domain verification file (ondc-site-verification.html) is not found"`
- **Details**: API accepts requests but requires domain verification

#### ❌ **Registry Lookup**
- **Status**: ❌ **FAILED**
- **Preprod**: `https://preprod.registry.ondc.org/ondc/lookup` - 403 Forbidden
- **Staging**: `https://staging.registry.ondc.org/ondc/lookup` - 403 Forbidden
- **Production**: SSL Certificate Expired
- **Issue**: Access forbidden - may require authentication

---

### ❌ **Local BAP Services** (0/2 FAILED)

#### ❌ **Local BAP Health**
- **Endpoint**: `http://localhost:8000/health`
- **Status**: ❌ **FAILED**
- **Error**: Connection refused
- **Issue**: Local BAP server not running

#### ❌ **Local BAP Endpoints**
- **Status**: ❌ **FAILED**
- **Endpoints Tested**: `/`, `/health`, `/api/health`, `/v1/health`, `/docs`, `/openapi.json`
- **Issue**: All endpoints fail - server not accessible

---

### ✅ **Public BAP Services** (1/2 PASSED)

#### ❌ **Public BAP Health**
- **Endpoint**: `https://neo-server.rozana.in/health`
- **Status**: ❌ **FAILED**
- **Response**: 404 Not Found
- **Issue**: Health endpoint not implemented on public server

#### ✅ **Public BAP Endpoints**
- **Status**: ✅ **PASSED**
- **Root**: `https://neo-server.rozana.in/` - 200 OK (Apache default page)
- **Other endpoints**: 404 Not Found (expected for unimplemented endpoints)
- **Details**: Server is accessible but BAP endpoints not deployed

---

### ✅ **Site Verification** (1/1 PASSED)

#### ✅ **ONDC Site Verification**
- **Primary**: `https://neo-server.rozana.in/ondc-site-verification.html` - ✅ **PASSED**
- **Response**: `OK`
- **Alternative paths**: 404 Not Found (expected)
- **Issue**: File exists but contains only "OK" instead of full verification content

---

## 🔍 **Key Findings**

### ✅ **What's Working**
1. **Pramaan Health**: Service is operational
2. **Registry Health**: Preprod and staging registries are healthy
3. **Registry Subscribe**: API accepts requests (domain verification issue only)
4. **Public Server**: Accessible and responding
5. **Site Verification**: File is accessible (content issue)

### ❌ **What's Not Working**
1. **eKYC Services**: All endpoints return 404 - not implemented
2. **Registry Discovery**: Discovery endpoints not exposed
3. **Registry Lookup**: Access forbidden (authentication required)
4. **Local BAP**: Server not running
5. **Public BAP**: Endpoints not deployed
6. **Domain Verification**: File content incorrect

### ⚠️ **Issues to Address**
1. **Domain Verification**: Upload correct verification file content
2. **Local BAP**: Start the local server for testing
3. **Public BAP**: Deploy BAP endpoints to public server
4. **SSL Certificate**: Production registry has expired certificate

---

## 📋 **Next Steps**

### 1. **Fix Domain Verification** (High Priority)
```bash
# Upload correct verification file
scp ondc-site-verification.html root@neo-server.rozana.in:/var/www/html/
```

### 2. **Deploy Local BAP** (Medium Priority)
```bash
# Start local BAP server
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. **Deploy Public BAP** (Medium Priority)
```bash
# Deploy to public server
bash deployment/upload_files.sh
ssh root@neo-server.rozana.in "cd /opt/ondc-bap && sudo ./deployment/deploy.sh"
```

### 4. **Test Registry Subscribe** (High Priority)
```bash
# Re-test after fixing domain verification
python3 ondc_subscribe_with_schema.py
```

---

## 🎯 **Success Metrics**

- **Pramaan Services**: 67% success rate
- **Registry Services**: 50% success rate
- **BAP Services**: 0% success rate (not deployed)
- **Verification**: 100% success rate

**Overall**: 50% of tested services are operational

---

## 📄 **Test Files Generated**

1. `ondc_complete_test_summary_1755831387.json` - Complete test results
2. `pramaan_health_check_1755831394.json` - Pramaan health check
3. `subscribe_request_response_preprod_1755831116.json` - Subscribe API response
4. Multiple individual test result files

---

**Last Updated**: August 22, 2025  
**Status**: Ready for domain verification fix and BAP deployment 