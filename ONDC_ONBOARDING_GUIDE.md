# ONDC Onboarding Guide for neo-server.rozana.in

## Subscriber Information
- **Subscriber ID**: `neo-server.rozana.in`
- **Subscriber URL**: `https://neo-server.rozana.in/`
- **Domain**: `nic2004:52110`
- **Type**: BAP (Buyer App Platform)
- **Callback URL**: `https://neo-server.rozana.in/v1/bap/on_subscribe`

## Current Implementation Status

### ✅ Completed Features
1. **Callback Endpoint**: `/v1/bap/on_subscribe` - Handles ONDC subscription challenges and updates
2. **All ONDC Actions**: Search, Select, Init, Confirm, Status, Track, Cancel, Rating, Support
3. **Error Handling**: Proper HTTP status codes and error responses
4. **Logging**: Comprehensive logging for debugging and monitoring
5. **Verification Page**: `/v1/bap/verification` - Public verification page
6. **Health Checks**: `/health` endpoint for monitoring

### ⚠️ Required for Production
1. **Authentication**: Implement ONDC authentication mechanism
2. **Encryption**: Implement message encryption/decryption
3. **Signing**: Implement message signing/verification
4. **HTTPS**: Ensure HTTPS is enabled in production
5. **Key Management**: Implement proper key generation and storage

## Onboarding Process

### Step 1: Registry Registration

#### Option A: Manual Registration
1. Visit the ONDC Registry: https://registry.ondc.org
2. Use the registration payload from `/v1/bap/onboarding/registration-payload`
3. Submit the registration form with your details

#### Option B: API Registration
```bash
curl -X POST https://neo-server.rozana.in/v1/bap/onboarding/register
```

### Step 2: Verification
1. ONDC will send a challenge to your callback URL
2. Your endpoint at `/v1/bap/on_subscribe` will handle the challenge
3. Verify the challenge response is working:
   ```bash
   curl -X POST https://neo-server.rozana.in/v1/bap/on_subscribe \
     -H "Content-Type: application/json" \
     -d '{"challenge": "test_challenge_123"}'
   ```

### Step 3: Testing
1. Test all endpoints are accessible:
   ```bash
   # Health check
   curl https://neo-server.rozana.in/health
   
   # Verification page
   curl https://neo-server.rozana.in/v1/bap/verification
   
   # Subscriber info
   curl https://neo-server.rozana.in/v1/bap/onboarding/subscriber-info
   ```

### Step 4: Production Approval
1. Complete sandbox testing with ONDC
2. Submit for production approval
3. Implement security requirements
4. Go live on ONDC network

## API Endpoints

### Core ONDC Endpoints
- `POST /v1/bap/on_subscribe` - Subscription callback
- `POST /v1/bap/search` - Search for products/services
- `POST /v1/bap/select` - Select items
- `POST /v1/bap/init` - Initialize order
- `POST /v1/bap/confirm` - Confirm order
- `POST /v1/bap/status` - Check order status
- `POST /v1/bap/track` - Track order
- `POST /v1/bap/cancel` - Cancel order
- `POST /v1/bap/rating` - Rate order
- `POST /v1/bap/support` - Support request

### Onboarding Endpoints
- `GET /v1/bap/onboarding/checklist` - Get onboarding requirements
- `GET /v1/bap/onboarding/registration-payload` - Generate registration data
- `POST /v1/bap/onboarding/register` - Register with registry
- `GET /v1/bap/onboarding/lookup/{subscriber_id}` - Lookup subscriber
- `PATCH /v1/bap/onboarding/status/{status}` - Update status
- `GET /v1/bap/onboarding/subscriber-info` - Get subscriber details

### Utility Endpoints
- `GET /health` - Health check
- `GET /v1/bap/verification` - Verification page
- `GET /v1/bap/on_subscribe/test` - Test callback endpoint

## Configuration

### Environment Variables
```bash
# ONDC Configuration
ONDC_SUBSCRIBER_ID=neo-server.rozana.in
ONDC_SUBSCRIBER_URL=https://neo-server.rozana.in
ONDC_DOMAIN=nic2004:52110
ONDC_TYPE=BAP
ONDC_CALLBACK_URL=https://neo-server.rozana.in/v1/bap/on_subscribe

# Registry URLs
ONDC_REGISTRY_URL=https://registry.ondc.org
ONDC_GATEWAY_URL=https://gateway.ondc.org

# Security
ONDC_PRIVATE_KEY_PATH=keys/private_key.pem
ONDC_PUBLIC_KEY_PATH=keys/public_key.pem
```

## Security Requirements

### 1. Authentication
- Implement ONDC authentication mechanism
- Validate incoming requests
- Handle authentication tokens

### 2. Encryption
- Encrypt sensitive data in transit
- Implement message encryption/decryption
- Use proper encryption algorithms

### 3. Signing
- Sign outgoing messages
- Verify incoming message signatures
- Implement proper key management

### 4. HTTPS
- Enable HTTPS in production
- Use valid SSL certificates
- Redirect HTTP to HTTPS

## Monitoring and Logging

### Log Levels
- `INFO`: Normal operations
- `WARNING`: Potential issues
- `ERROR`: Errors that need attention
- `DEBUG`: Detailed debugging information

### Key Metrics
- Callback response times
- Error rates
- Authentication failures
- Message processing times

## Troubleshooting

### Common Issues
1. **Callback not accessible**: Ensure HTTPS and public accessibility
2. **Challenge verification fails**: Check challenge response logic
3. **Authentication errors**: Verify key management
4. **Message parsing errors**: Validate JSON structure

### Debug Commands
```bash
# Test callback endpoint
curl -X POST https://neo-server.rozana.in/v1/bap/on_subscribe \
  -H "Content-Type: application/json" \
  -d '{"test": "debug"}'

# Check logs
docker logs <container_name>

# Health check
curl https://neo-server.rozana.in/health
```

## Support

For ONDC onboarding support:
1. Check the verification page: https://neo-server.rozana.in/v1/bap/verification
2. Review the onboarding checklist: `/v1/bap/onboarding/checklist`
3. Contact ONDC support team
4. Check ONDC documentation: https://github.com/ONDC-Official/developer-docs

## Next Steps

1. **Immediate**: Register with ONDC registry
2. **Short-term**: Implement security requirements
3. **Medium-term**: Complete sandbox testing
4. **Long-term**: Go live on ONDC network

---

**Last Updated**: December 2024
**Status**: Ready for Registry Registration 