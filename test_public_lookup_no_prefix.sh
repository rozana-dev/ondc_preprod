#!/bin/bash

echo "🔍 Testing Public ONDC Endpoints (No v1/bap Prefix)"
echo "=================================================="

# Test 1: Public lookup endpoint
echo "📡 Test 1: Public lookup endpoint"
curl -s -X GET "https://neo-server.rozana.in/onboarding/lookup/neo-server.rozana.in" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 2: Public subscriber info
echo "📡 Test 2: Public subscriber info"
curl -s -X GET "https://neo-server.rozana.in/onboarding/subscriber-info" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 3: Public onboarding checklist
echo "📡 Test 3: Public onboarding checklist"
curl -s -X GET "https://neo-server.rozana.in/onboarding/checklist" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 4: Public test challenge
echo "📡 Test 4: Public test challenge"
curl -s -X POST "https://neo-server.rozana.in/onboarding/test-challenge" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"test": "public_lookup_test"}' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 5: ONDC callback endpoint
echo "📡 Test 5: ONDC callback endpoint"
curl -s -X POST "https://neo-server.rozana.in/on_subscribe" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"test": "public_lookup_test"}' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 6: Health endpoints
echo "📡 Test 6: Health endpoints"
curl -s -X GET "https://neo-server.rozana.in/healthz" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

echo "✅ Public endpoint testing completed!"
echo ""
echo "🎯 Expected Results:"
echo "- All endpoints should return 200 OK"
echo "- No more 404 errors"
echo "- Clean URLs without /v1/bap prefix" 