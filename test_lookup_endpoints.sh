#!/bin/bash

echo "🔍 Testing ONDC Lookup Endpoints on neo-server.rozana.in"
echo "=================================================="

# Test 1: Basic lookup endpoint
echo "📋 Test 1: GET /lookup"
curl -s "https://neo-server.rozana.in/lookup" | jq .
echo -e "\n"

# Test 2: vlookup endpoint
echo "📋 Test 2: POST /vlookup"
curl -s -X POST "https://neo-server.rozana.in/vlookup" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_subscriber_id": "test.ondc.org",
    "request_id": "test-request-123",
    "timestamp": "2025-01-21T10:00:00.000Z",
    "signature": "test-signature",
    "search_parameters": {
      "country": "IND",
      "domain": "nic2004:52110",
      "type": "buyerApp",
      "city": "std:080",
      "subscriber_id": "neo-server.rozana.in"
    }
  }' | jq .
echo -e "\n"

# Test 3: Health check (should work)
echo "📋 Test 3: Health check (verification)"
curl -s "https://neo-server.rozana.in/healthz" | jq .
echo -e "\n"

echo "✅ Lookup endpoint testing complete!" 