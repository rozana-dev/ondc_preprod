#!/bin/bash

echo "🔍 Testing ONDC Registry Lookup for neo-server.rozana.in"
echo "=================================================="

# Test 1: Pre-prod v2.0 lookup with query parameter
echo "📡 Test 1: Pre-prod v2.0 lookup (GET with query param)"
curl -s -X GET "https://preprod.registry.ondc.org/v2.0/lookup?subscriber_id=neo-server.rozana.in" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 2: Staging v2.0 lookup with query parameter
echo "📡 Test 2: Staging v2.0 lookup (GET with query param)"
curl -s -X GET "https://staging.registry.ondc.org/v2.0/lookup?subscriber_id=neo-server.rozana.in" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 3: Pre-prod original lookup endpoint
echo "📡 Test 3: Pre-prod original lookup endpoint"
curl -s -X GET "https://preprod.registry.ondc.org/ondc/lookup?subscriber_id=neo-server.rozana.in" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 4: Staging original lookup endpoint
echo "📡 Test 4: Staging original lookup endpoint"
curl -s -X GET "https://staging.registry.ondc.org/ondc/lookup?subscriber_id=neo-server.rozana.in" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 5: Pre-prod v2.0 lookup with POST and JSON body
echo "📡 Test 5: Pre-prod v2.0 lookup (POST with JSON body)"
curl -s -X POST "https://preprod.registry.ondc.org/v2.0/lookup" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"subscriber_id": "neo-server.rozana.in"}' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 6: Staging v2.0 lookup with POST and JSON body
echo "📡 Test 6: Staging v2.0 lookup (POST with JSON body)"
curl -s -X POST "https://staging.registry.ondc.org/v2.0/lookup" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"subscriber_id": "neo-server.rozana.in"}' \
  -w "\nHTTP Status: %{http_code}\n\n"

# Test 7: Check if endpoints exist without parameters
echo "📡 Test 7: Check pre-prod v2.0 lookup endpoint (no params)"
curl -s -X GET "https://preprod.registry.ondc.org/v2.0/lookup" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n\n"

echo "✅ Lookup testing completed!" 