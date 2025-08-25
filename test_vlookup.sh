#!/bin/bash

echo "🔍 Testing ONDC vlookup Endpoint"
echo "================================"

# Test 1: Local vlookup endpoint
echo "📡 Test 1: Local vlookup endpoint"
curl -s -X POST "http://localhost:8000/vlookup" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_subscriber_id": "test-sender.ondc.org",
    "request_id": "27baa06d-f90a-486c-85e5-cc621b787f04",
    "timestamp": "2024-08-21T10:00:00.000Z",
    "signature": "test_signature_here",
    "search_parameters": {
      "country": "IND",
      "domain": "ONDC:RET10",
      "type": "buyerApp",
      "city": "std:080",
      "subscriber_id": "neo-server.rozana.in"
    }
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 2: Public vlookup endpoint (after Apache config)
echo "📡 Test 2: Public vlookup endpoint"
curl -s -X POST "https://neo-server.rozana.in/vlookup" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_subscriber_id": "test-sender.ondc.org",
    "request_id": "27baa06d-f90a-486c-85e5-cc621b787f04",
    "timestamp": "2024-08-21T10:00:00.000Z",
    "signature": "test_signature_here",
    "search_parameters": {
      "country": "IND",
      "domain": "ONDC:RET10",
      "type": "buyerApp",
      "city": "std:080",
      "subscriber_id": "neo-server.rozana.in"
    }
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 3: Test with different subscriber
echo "📡 Test 3: Test with different subscriber"
curl -s -X POST "http://localhost:8000/vlookup" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_subscriber_id": "test-sender.ondc.org",
    "request_id": "27baa06d-f90a-486c-85e5-cc621b787f05",
    "timestamp": "2024-08-21T10:00:00.000Z",
    "signature": "test_signature_here",
    "search_parameters": {
      "country": "IND",
      "domain": "ONDC:RET10",
      "type": "sellerApp",
      "city": "std:080",
      "subscriber_id": "other-server.ondc.org"
    }
  }' \
  -w "\nHTTP Status: %{http_code}\n\n"

echo "✅ vlookup testing completed!"
echo ""
echo "🎯 Expected Results:"
echo "- Test 1: Should return 200 OK with neo-server.rozana.in data"
echo "- Test 2: Should return 200 OK (after Apache config)"
echo "- Test 3: Should return 200 OK with null data for unknown subscriber" 