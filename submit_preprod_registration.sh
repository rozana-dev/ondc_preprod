#!/bin/bash

# ONDC Pre-Production Registration Script
# Subscriber: neo-server.rozana.in

echo "🚀 ONDC Pre-Production Registration"
echo "=================================="
echo "Subscriber ID: neo-server.rozana.in"
echo "Registry URL: https://preprod.registry.ondc.org/ondc/subscribe"
echo ""

# Check if payload file exists
if [ ! -f "preprod_subscribe_payload.json" ]; then
    echo "❌ Error: preprod_subscribe_payload.json not found"
    echo "Run: curl -s http://localhost:8000/v1/bap/onboarding/subscribe-payload/pre_prod/1 | jq '.payload' > preprod_subscribe_payload.json"
    exit 1
fi

echo "✅ Payload file found: preprod_subscribe_payload.json"
echo ""

# Display payload preview
echo "📋 Payload Preview:"
echo "=================="
cat preprod_subscribe_payload.json | jq '.subscriber_id, .signing_public_key, .encryption_public_key, .request_id'
echo ""

# Confirm before submission
echo "⚠️  IMPORTANT PREREQUISITES:"
echo "1. ✅ Whitelist request submitted at https://portal.ondc.org"
echo "2. ✅ HTTPS enabled on neo-server.rozana.in"
echo "3. ✅ ondc-site-verification.html hosted at domain root"
echo "4. ✅ /on_subscribe endpoint accessible"
echo ""

read -p "Have you completed all prerequisites? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Please complete prerequisites before proceeding"
    exit 1
fi

echo ""
echo "🚀 Submitting registration to ONDC Pre-Production Registry..."
echo ""

# Submit registration
response=$(curl -s -w "\n%{http_code}" -X POST "https://preprod.registry.ondc.org/ondc/subscribe" \
  -H "Content-Type: application/json" \
  -d @preprod_subscribe_payload.json)

# Extract HTTP status code
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

echo "📡 Response Status: $http_code"
echo "📄 Response Body:"
echo "$response_body" | jq '.'

echo ""
echo "🔍 Next Steps:"
echo "1. If successful (ACK), ONDC will send a challenge to your callback"
echo "2. Your endpoint will decrypt and respond to the challenge"
echo "3. Check registration status in registry lookup"
echo ""

# Test lookup
echo "🔍 Testing Registry Lookup..."
lookup_response=$(curl -s -X POST "https://preprod.registry.ondc.org/v2.0/lookup" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "IND",
    "domain": "ONDC:RET10"
  }')

echo "Lookup Response:"
echo "$lookup_response" | jq '.' | head -20

echo ""
echo "📞 If you encounter issues, contact ONDC support:"
echo "Email: techsupport@ondc.org"
echo "Portal: https://portal.ondc.org"
echo ""
echo "Include these details:"
echo "- Subscriber ID: neo-server.rozana.in"
echo "- Error Code: [from response above]"
echo "- Error Description: [from response above]" 