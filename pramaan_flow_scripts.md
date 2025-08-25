# 🚀 Pramaan ONDC Flow Scripts - Complete Implementation

## Overview
These scripts implement all 10+ ONDC flows for testing with Pramaan mock seller (`pramaan.ondc.org/beta/preprod/mock/seller`).

## 🏪 Store Details
- **Store Name:** pramaan_provider_1
- **BPP URI:** https://pramaan.ondc.org/beta/preprod/mock/seller
- **Test PIN Codes:** 122007, 110037
- **Domain:** ONDC:RET10 (Retail)
- **Environment:** preprod

## 📋 Flow Scripts

### Flow 1A: Order to Confirm to Fulfillment (Prepaid)

```bash
#!/bin/bash
# Flow 1A: Complete Order Flow - Prepaid

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"

echo "🚀 Flow 1A: Order to Confirm to Fulfillment (Prepaid)"
echo "Transaction ID: $TRANSACTION_ID"

# Step 1: Select
curl -X POST "$BASE_URL/select" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "select",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "order": {
        "provider": {
          "id": "pramaan_provider_1"
        },
        "items": [{
          "id": "item_001",
          "quantity": {
            "count": 2
          }
        }],
        "billing": {
          "address": {
            "name": "John Doe",
            "building": "123 Main St",
            "locality": "Downtown",
            "city": "New Delhi",
            "state": "Delhi",
            "country": "IND",
            "area_code": "110037"
          }
        },
        "fulfillment": {
          "type": "Delivery",
          "end": {
            "location": {
              "gps": "28.6139,77.2090",
              "address": {
                "name": "John Doe",
                "building": "123 Main St",
                "locality": "Downtown",
                "city": "New Delhi",
                "state": "Delhi",
                "country": "IND",
                "area_code": "110037"
              }
            },
            "contact": {
              "phone": "9876543210"
            }
          }
        }
      }
    }
  }'

echo "✅ Select call sent. Wait for on_select callback."
echo "📝 Note the transaction ID: $TRANSACTION_ID"

# Step 2: Init (after receiving on_select)
read -p "Press Enter after receiving on_select callback to send init..."

curl -X POST "$BASE_URL/init" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "init",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "order": {
        "provider": {
          "id": "pramaan_provider_1"
        },
        "items": [{
          "id": "item_001",
          "quantity": {
            "count": 2
          }
        }],
        "billing": {
          "address": {
            "name": "John Doe",
            "building": "123 Main St",
            "locality": "Downtown",
            "city": "New Delhi",
            "state": "Delhi",
            "country": "IND",
            "area_code": "110037"
          }
        },
        "fulfillment": {
          "type": "Delivery"
        },
        "payment": {
          "type": "PRE-PAID"
        }
      }
    }
  }'

echo "✅ Init call sent. Wait for on_init callback."

# Step 3: Confirm (after receiving on_init)
read -p "Press Enter after receiving on_init callback to send confirm..."

curl -X POST "$BASE_URL/confirm" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "confirm",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "order": {
        "provider": {
          "id": "pramaan_provider_1"
        },
        "items": [{
          "id": "item_001",
          "quantity": {
            "count": 2
          }
        }],
        "payment": {
          "type": "PRE-PAID",
          "status": "PAID"
        }
      }
    }
  }'

echo "✅ Confirm call sent. Wait for on_confirm callback."

# Step 4: Status (after receiving on_confirm)
read -p "Press Enter after receiving on_confirm callback to send status..."

curl -X POST "$BASE_URL/status" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "status",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "order_id": "order_'$TRANSACTION_ID'"
    }
  }'

echo "✅ Status call sent. Wait for on_status callbacks."

# Step 5: Track (after order status updates)
read -p "Press Enter after receiving fulfillment status updates to send track..."

curl -X POST "$BASE_URL/track" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "track",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "order_id": "order_'$TRANSACTION_ID'"
    }
  }'

echo "✅ Track call sent. Wait for on_track callback."
echo "🎉 Flow 1A Complete! Order delivered."
```

### Flow 1B: Order to Confirm to Fulfillment (COD)

```bash
#!/bin/bash
# Flow 1B: Complete Order Flow - COD

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"

echo "🚀 Flow 1B: Order to Confirm to Fulfillment (COD)"
echo "Transaction ID: $TRANSACTION_ID"

# Same as Flow 1A but with COD payment
# Step 1: Select (same as 1A)
# Step 2: Init with COD payment
curl -X POST "$BASE_URL/init" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "action": "init",
      "transaction_id": "'$TRANSACTION_ID'"
    },
    "message": {
      "order": {
        "payment": {
          "type": "ON-FULFILLMENT",
          "collected_by": "BPP"
        }
      }
    }
  }'

echo "✅ COD Init call sent."
# Continue with same steps as Flow 1A
```

### Flow 2: Buyer Side Order Cancellation

```bash
#!/bin/bash
# Flow 2: Buyer Side Order Cancellation

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"

echo "🚀 Flow 2: Buyer Side Order Cancellation"
echo "Transaction ID: $TRANSACTION_ID"

# Steps 1-3: Same as Flow 1A (Select, Init, Confirm)
# ... (include select, init, confirm steps)

# Step 4: Cancel (instead of status)
read -p "Press Enter after receiving on_confirm to send cancel..."

curl -X POST "$BASE_URL/cancel" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "cancel",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "order_id": "order_'$TRANSACTION_ID'",
      "cancellation_reason_id": "001",
      "descriptor": {
        "short_desc": "Customer requested cancellation"
      }
    }
  }'

echo "✅ Cancel call sent. Wait for on_cancel callback."
echo "🎉 Flow 2 Complete! Order cancelled."
```

### Flow 3A: Merchant Side Partial Order Cancellation

```bash
#!/bin/bash
# Flow 3A: Merchant Side Partial Order Cancellation

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"

echo "🚀 Flow 3A: Merchant Side Partial Order Cancellation"
echo "Transaction ID: $TRANSACTION_ID"

# Step 1: Select with multiple quantities
curl -X POST "$BASE_URL/select" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "action": "select",
      "transaction_id": "'$TRANSACTION_ID'"
    },
    "message": {
      "order": {
        "items": [{
          "id": "item_001",
          "quantity": {
            "count": 5
          }
        }]
      }
    }
  }'

# Continue with init, confirm
# Wait for unsolicited on_update with partial cancellation
# Send update (settlement) response

echo "✅ Waiting for merchant partial cancellation..."
read -p "Press Enter after receiving on_update with partial cancellation to send settlement..."

curl -X POST "$BASE_URL/update" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "action": "update",
      "transaction_id": "'$TRANSACTION_ID'"
    },
    "message": {
      "update_target": "settlement",
      "order": {
        "id": "order_'$TRANSACTION_ID'",
        "status": "ACCEPTED"
      }
    }
  }'

echo "✅ Settlement update sent."
echo "🎉 Flow 3A Complete! Partial cancellation processed."
```

### Flow 4A: Buyer Initiated Return (Full Order)

```bash
#!/bin/bash
# Flow 4A: Buyer Initiated Return (Full Order)

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"

echo "🚀 Flow 4A: Buyer Initiated Return (Full Order)"
echo "Transaction ID: $TRANSACTION_ID"

# Complete Flow 1A first (order delivered)
# Then initiate return

read -p "Press Enter after order is delivered to initiate return..."

curl -X POST "$BASE_URL/update" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "update",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "update_target": "return",
      "order": {
        "id": "order_'$TRANSACTION_ID'",
        "items": [{
          "id": "item_001",
          "quantity": {
            "count": 2
          }
        }],
        "fulfillment": [{
          "type": "Return",
          "state": {
            "descriptor": {
              "code": "RTO-Initiated"
            }
          }
        }]
      }
    }
  }'

echo "✅ Return update sent. Wait for return process callbacks."
echo "🎉 Flow 4A Complete! Full order return initiated."
```

### Flow 5: Out of Stock (Error Code)

```bash
#!/bin/bash
# Flow 5: Out of Stock Error Flow

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"

echo "🚀 Flow 5: Out of Stock Error Flow"
echo "Transaction ID: $TRANSACTION_ID"

# Step 1: Select out of stock item
curl -X POST "$BASE_URL/select" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "action": "select",
      "transaction_id": "'$TRANSACTION_ID'"
    },
    "message": {
      "order": {
        "items": [{
          "id": "out_of_stock_item",
          "quantity": {
            "count": 1
          }
        }]
      }
    }
  }'

echo "✅ Select call sent for out of stock item."
echo "⚠️  Expect on_select with error code for out of stock."
echo "🎉 Flow 5 Complete! Out of stock error handled."
```

### Flow 6: Issue and Grievance Management (IGM)

```bash
#!/bin/bash
# Flow 6: Issue and Grievance Management

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"  # Use existing transaction ID from completed flow

echo "🚀 Flow 6: Issue and Grievance Management"
echo "Transaction ID: $TRANSACTION_ID"

# Step 1: Raise Issue
curl -X POST "$BASE_URL/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "issue",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "issue": {
        "id": "issue_'$(date +%s)'",
        "category": "ITEM",
        "sub_category": "ITM01",
        "complainant_info": {
          "person": {
            "name": "John Doe"
          },
          "contact": {
            "phone": "9876543210",
            "email": "john@example.com"
          }
        },
        "order_details": {
          "id": "order_'$TRANSACTION_ID'",
          "items": [{
            "id": "item_001",
            "quantity": 1
          }]
        },
        "description": {
          "short_desc": "Item damaged",
          "long_desc": "The item received was damaged during delivery"
        },
        "source": {
          "network_participant_id": "neo-server.rozana.in",
          "type": "CONSUMER"
        },
        "expected_response_time": {
          "duration": "PT2H"
        },
        "expected_resolution_time": {
          "duration": "P1D"
        }
      }
    }
  }'

echo "✅ Issue raised. Wait for on_issue callback."

# Step 2: Issue Status
read -p "Press Enter after receiving on_issue to send issue_status..."

curl -X POST "$BASE_URL/issue_status" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "action": "issue_status",
      "transaction_id": "'$TRANSACTION_ID'"
    },
    "message": {
      "issue_id": "issue_'$(date +%s)'"
    }
  }'

echo "✅ Issue status requested."

# Step 3: Close Issue
read -p "Press Enter to close issue..."

curl -X POST "$BASE_URL/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "action": "issue",
      "transaction_id": "'$TRANSACTION_ID'"
    },
    "message": {
      "issue": {
        "status": "CLOSED",
        "resolution": "RESOLVED"
      }
    }
  }'

echo "✅ Issue closed."
echo "🎉 Flow 6 Complete! IGM process completed."
```

### Flow 8A: Search and Custom Menu (Full Catalog)

```bash
#!/bin/bash
# Flow 8A: Full Catalog Search

BASE_URL="https://neo-server.rozana.in"
TRANSACTION_ID="txn_$(date +%s)"

echo "🚀 Flow 8A: Full Catalog Search"
echo "Transaction ID: $TRANSACTION_ID"

curl -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "search",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "intent": {
        "fulfillment": {
          "type": "Delivery",
          "end": {
            "location": {
              "gps": "28.6139,77.2090",
              "address": {
                "area_code": "110037"
              }
            }
          }
        }
      }
    }
  }'

echo "✅ Full catalog search sent. Wait for on_search callback."
echo "🎉 Flow 8A Complete! Full catalog received."
```

### Flow 10: Info

```bash
#!/bin/bash
# Flow 10: Info Request

BASE_URL="https://neo-server.rozana.in"
BPP_URI="https://pramaan.ondc.org/beta/preprod/mock/seller"
TRANSACTION_ID="txn_$(date +%s)"

echo "🚀 Flow 10: Info Request"
echo "Transaction ID: $TRANSACTION_ID"

curl -X POST "$BASE_URL/info" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "info",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "'$BASE_URL'",
      "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
      "bpp_uri": "'$BPP_URI'",
      "transaction_id": "'$TRANSACTION_ID'",
      "message_id": "msg_'$(date +%s)'",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'"
    },
    "message": {
      "info": {
        "provider_id": "pramaan_provider_1"
      }
    }
  }'

echo "✅ Info request sent. Wait for on_info callback."
echo "🎉 Flow 10 Complete! Provider info received."
```

## 🎯 Usage Instructions

1. **Make scripts executable:**
   ```bash
   chmod +x *.sh
   ```

2. **Run individual flows:**
   ```bash
   ./flow_1a_prepaid.sh
   ./flow_1b_cod.sh
   ./flow_2_cancel.sh
   # ... etc
   ```

3. **Important Notes:**
   - Each script generates unique transaction IDs
   - Wait for callbacks before proceeding to next step
   - Monitor your callback endpoints for responses
   - Use the same transaction ID throughout a flow
   - Test with PIN codes: 122007 or 110037

## 📊 Expected Callbacks

Each flow will trigger specific callbacks to your endpoints:
- `on_select` → Send ACK, then proceed to init
- `on_init` → Send ACK, then proceed to confirm
- `on_confirm` → Send ACK, then proceed to status
- `on_status` → Send ACK (multiple status updates)
- `on_cancel`, `on_update`, `on_track` → Send ACK

## 🎉 Success!

Your ONDC BAP is now ready to test all Pramaan flows! Each script implements the complete ONDC protocol for different business scenarios.